from dash import Dash, html, Input, Output
from flask import request
import dashContent

dashContent.init_data()

app = Dash(__name__, )

infrastructure_checklist = dashContent.mainmenu()

app.layout = html.Div([
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
        # html.Div(
        #     className='checklist-container',
        #     children=[infrastructure_checklist]),
        html.Div(className='output', id='my-output')
    ])])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='input-checklist', component_property='value')
)
def update_output_div(input_value):
    frame_containers = list()
    if input_value:
        for item in input_value:
            frame_div = dashContent.fetch_div(item)
            frame_containers.append(frame_div)
    print(request.remote_addr)
    return frame_containers
    # box = html.Div(className='sth', children=frame_containers)
    # return box


if __name__ == '__main__':
    # The application runs in a docker container on ganymede. External
    # users make requests to https://future.ganymede.icos-cp.eu/
    # (port 443) which are then proxy passed to port 8081 on ganymede
    # and then to port 8080 in the application's docker container.
    # The `ssl_context='adhoc'` parameter is used to quickly serve an
    # application over HTTPS without having to mess with certificates.
    app.run(host='0.0.0.0', port=8080, ssl_context='adhoc')
    #app.run_server(debug=True)    # to be removed