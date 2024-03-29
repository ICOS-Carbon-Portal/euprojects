from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
# from flask import request
import dashContent
import os


# We use this in checklist-callback
# to preserve objects
# (Also... it is not possible to just use the list!
# ... bug or a good reason?)
dashboard_dict = {'previous_dashboards': []}

dashContent.init_data()

infrastructure_checklist = dashContent.main_menu()



# Below we set
#     `suppress_callback_exceptions=True`
# in order to suppress exceptions when app.callbacks
# are created to non-existing objects.
app = Dash(__name__,
           suppress_callback_exceptions=True,
           title='ENVRI - State of the Environment')

# Main layout
app.layout = html.Div([dcc.Store(id='local-state', storage_type='local'),
                       html.Div(children=[
                           html.Div(className='header-container', children=[
                               html.Div(className='flex-child-image', children=[
                                   html.Img(className='header-image',
                                            src='https://eoscfuture.eu/wp-content/themes/eosc/assets/img/logos/eosc-future.svg'),
                               ]),
                               html.Div(className='flex-child-headings', children=[
                                   html.H1('Data in action'),
                                   html.H2('State of the Environment')
                               ])]),
                           infrastructure_checklist,
                           html.Div(className='output', id='my-output')
                       ])])

# In order to create callbacks from start we need to
# initialize possible component id's even though the

# objects are not yet created.
# Each id must be unique, and hence the dash content with a
# specific id must only be loaded once per provider.
# Also, the comment on suppress_callback_exceptions at app = ....
provider_id_list = [dashContent.get_provider_id(p) for p in dashContent.provider_list]

for provider in provider_id_list:
    @app.callback(
        Output(component_id=f'{provider}-frame', component_property='src'),
        Input(component_id=f'{provider}-drop', component_property='value'),
        # State(component_id=f'{provider}-frame', component_property='src'),
        prevent_initial_call=True
    )
    def update_frame(frame_link):  # def update_frame(link, src): if we want to cancel?
        return frame_link


@app.callback(
    Output(component_id='local-state', component_property='data'),
    Input(component_id='output', component_property='children'),
    State(component_id='local-state', component_property='data'),
    # State(component_id=f'{provider}-frame', component_property='src'),
    prevent_initial_call=True
)
def update_state(frame_link, present_children):
    if frame_link is None or present_children is None:
        raise PreventUpdate
    else:
        data = present_children or []
    return data


@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='output', component_property='children'),
     Input(component_id='local-state', component_property='modified_timestamp')],
    State(component_id='local-state', component_property='data')
)
def update_children_from_state(present_children, timestamp, data):
    if timestamp is None:
        raise PreventUpdate
    elif present_children:
        return
    else:
        return data.get()  # cookie_for_children


@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='input-checklist', component_property='value'),
     Input(component_id='my-output', component_property='children')]
)
def update_output_div(input_value, children_list):

    # We don't want to run this
    # right after it been executed.
    if input_value is None:
        return
    frame_containers = []
    prev_dash_list = dashboard_dict['previous_dashboards']

    if children_list is None or \
            (isinstance(children_list, list) and
             children_list == []):
        prev_dash_list = []

    if input_value:

        if len(prev_dash_list) > 0:
            # remove old items
            for old_item in list(set(prev_dash_list).difference(input_value)):
                old_index = prev_dash_list.index(old_item)
                prev_dash_list.remove(old_item)
                # Not a complete fix. Just catches some cases.
                if children_list:
                    children_list.pop(old_index)

        for item in input_value:
            # reuse common objects
            if item in prev_dash_list:
                try:
                    keep_index = prev_dash_list.index(item)
                    frame_containers.append(children_list[keep_index])
                except Exception as e:
                    raise Exception(f'Keep_index: {keep_index or None} \n'
                                    f'prev_dash_list: {prev_dash_list}'
                                    f'\nlen(children_list): '
                                    f'{len(children_list)}\n',e)
            else:
                # create new objects
                prev_dash_list.append(item)
                frame_containers.append(dashContent.fetch_div(item))

    dashboard_dict['previous_dashboards'] = prev_dash_list

    # print(request.remote_addr, input_value)
    return frame_containers


if __name__ == '__main__':
    # The application runs in a docker container on ganymede. External
    # users make requests to https://future.ganymede.icos-cp.eu/
    # (port 443) which are then proxy passed to port 8081 on ganymede
    # and then to port 8080 in the application's docker container.
    # The `ssl_context='adhoc'` parameter is used to quickly serve an
    # application over HTTPS without having to mess with certificates.
    #
    externalIP = os.popen('curl -s ifconfig.me').readline()
    if externalIP == "194.47.223.137":
        app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')
    else:
        app.run(debug=True, port=8082, threaded=True)