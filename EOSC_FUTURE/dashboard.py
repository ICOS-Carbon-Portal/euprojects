from dash import Dash, dcc, html, Input, Output
from flask import request
from ReadPlugins import EoscValueObject

sd_data_obj = EoscValueObject()


app = Dash(__name__, )

infrastructure_checklist = dcc.Checklist(
    className='input-checklist',
    id='input-checklist',
    options=sd_data_obj.get_providers(),
    # labelStyle={'display': 'block'},
    inputClassName='input-checkbox',
    labelClassName='label-input'
)

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
            if item == 'ICOS':
                my_source = 'https://data.icos-cp.eu/dashboard/?stationId=BIR&valueType=co&height=50'
            elif item == 'INGOS':
                my_source = 'https://www.ingos-infrastructure.eu/'
            elif item == 'NEON':
                my_source = 'assets/static-html/neon.html'
            elif item == 'OCEAN':
                my_source = 'assets/static-html/ocean.html'
            else:
                my_source = '/assets/static-html/folium_map.html'
            frame_div = html.Div(
                className='frame-container',
                children=[
                    html.Iframe(
                        className='infrastructure-frame',
                        src=my_source,
                        title=item,
                    )])
            frame_containers.append(frame_div)
    print(request.remote_addr)
    return frame_containers
    # box = html.Div(className='sth', children=frame_containers)
    # return box


if __name__ == '__main__':
    app.run_server(debug=True)
