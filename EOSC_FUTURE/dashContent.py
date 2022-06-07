#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Deliver content to dashboard
"""

from dash import dcc, html
from ReadPlugins import EoscValueObject

# Plugin data
sd_data_obj = EoscValueObject()

# List of Scientific Dashboard providers
# global var see init_data()
provider_list = []

# Each provider is mapped to an id which is a stringed number, to be used in different widgets.
# global var see init_data()
provider_id_dict = {}


def init_data():
    def iter_to_dict(key_iter: iter, value_iter: object = None) -> dict:
        if value_iter is None:
            value_iter = [str(100 + x) for x in range(len(key_iter))]
        if hasattr(key_iter, '__iter__') and hasattr(value_iter, '__iter__'):
            return dict(zip(key_iter, value_iter))
        else:
            raise TypeError('argument nust be iterable.')

    global provider_list, provider_id_dict
    provider_list = sd_data_obj.get_providers()
    provider_id_dict = iter_to_dict(provider_list)


def fetch_div(provider):
    try:
        sd_data = sd_data_obj.get_provider_plug(provider)
    except Exception as e:
        raise Exception('Check call for {}.'.format(provider), e)

    inner_content = tabs_content(sd_data, provider)
#    my_source = 'https://data.icos-cp.eu/dashboard/?stationId=BIR&valueType=co&height=50'
#
#    if inner_content is None:
#        inner_content = html.Iframe(className='tab-outer-container',
#                                    src=my_source,
#                                    title=provider,
#                                    )

    plugin_div = html.Div(className='tab-outer-container',
                          children=[inner_content])
    return plugin_div


def get_provider_id(provider):
    return provider_id_dict[provider]


def main_menu():
    menu = dcc.Checklist(
        className='input-checklist',
        id='input-checklist',
        options=provider_list,
        inputClassName='input-checkbox',
        labelClassName='label-input'
    )
    return menu


def tab_1_dropdown(sd_data: dict, provider: str):
    provider_id = get_provider_id(provider)
    menu_options = []
    drop = None
    base = ''
    try:
        base = sd_data['SD_URL']['base_url']
        if 'parameters' in sd_data['SD_URL'].keys():
            if sd_data['SD_URL']['parameters'] is not None:
                menu_options = [{'label': key, 'value': f'{base}{value}'} for
                                key, value in sd_data['SD_URL']['parameters'].items()]
    except Exception as e:
        raise Warning(f'Check yaml-file for {provider}. \nThe base_url: {base}' +
                      'parameters: {}'.format(sd_data['SD_URL']['parameters']) +
                      ' (missing backslash \'\\''?) \nException: ', e)

    finally:
        if len(menu_options) > 1:
            link = menu_options[0]['value']
            drop = dcc.Dropdown(options=menu_options,
                                value=link,
                                id=f'{provider_id}-drop')
        elif menu_options == 1:
            link = menu_options[0]['value']
        else:
            link = base

    return drop, link


def tab_1_iframe(sd_data: dict, provider: str, link: str):
    # TODO
    # validate output to sd_data is it
    #  - an image
    #  - html
    #  - ....
    provider_id = get_provider_id(provider)
    try:
        if link[-4:] in {'.png', '.jpg'}:
            output = html.Img(id=f'{provider_id}-frame',
                              className='frame-container',
                              src=link)
        elif link[-4:] in {'html', '.htm'}:
            output = html.Embed(id=f'{provider_id}-frame',
                                className='frame-container',
                                src=link
                                )
        else:
            output = html.Embed(id=f'{provider_id}-frame',
                                className='frame-container',
                                src=link)

    except Exception as e:
        raise Exception(f'Iframe {link} of {provider} generated Exception: ', e)

    return output


def tab_1_content(sd_data: dict, provider: str):
    drop, link = tab_1_dropdown(sd_data, provider)

    if drop is not None:
        try:
            tab = html.Div(className='tab-column',
                           children=[tab_row_123(sd_data, provider),
                                     # 1. Top section, horizontal, height ~ 1/5 of tab
                                     # html.Div(className='tab-1-row',
                                     #          children=[html.H4(provider),
                                     #                    html.P('Some tab content '),
                                     #                    html.Img(className='logo-img',
                                     #                             src=sd_data['SD_logo_url'],
                                     #                             style={'width': 'max(30%, 80px)'})
                                     #                    ]),
                                     # tab1 end
                                     # 2. Middle section, horizontal, height ~ 1/5 of tab
                                     html.Div(className='tab-row',
                                              children=[drop]),  # tab2 end
                                     # 3. Fill up remaining?
                                     html.Div(className='tab-row',
                                              children=[tab_1_iframe(sd_data,
                                                                     provider,
                                                                     link)])
                                     ])  # tabs end
        except Exception as e:
            raise Exception(f'Tab-1 error 1. Check file for {provider}. Exception: ', e)
    else:
        try:
            tab = html.Div(className='tab-column',
                           children=[
                               # 1. Top section, horizontal, height ~ 1/5 of tab
                               tab_row_123(sd_data, provider),
                               # tab1 end
                               # 2. Middle section, horizontal, height ~ 1/5 of tab
                               #  empty...
                               # 3. Fill up remaining?
                               html.Div(className='tab-3-row',
                                        children=None)
                           ])  # tabs end
        except Exception as e:
            raise Exception(f'Tab-1 error 2. Check file for {provider}. Exception: ', e)
    return tab


def tab_1_rows(sd_data, provider):
    return dcc.Tab(id='Tab-1',
                   value='Tab-1',
                   label='Indicator',
                   selected_className='custom-tab--selected',
                   className='the-tab',
                   children=tab_1_content(sd_data, provider))


def tab_2_content(sd_data, provider):
    try:
        tab = html.Div(className='tab-column',
                       children=[tab_row_123(sd_data,
                                             provider)
                                 ])
    except Exception as e:
        raise Exception(f'{provider} tab-2', e)

    return tab


def tab_2_rows(sd_data, provider):
    return dcc.Tab(id='Tab-2',
                   label='Info',
                   selected_className='custom-tab--selected',
                   className='the-tab',
                   children=tab_2_content(sd_data, provider))


def tab_3_content(sd_data, provider):
    try:
        tab = html.Div(className='tab-column',
                       children=[
                           tab_row_123(sd_data,
                                       provider),
                           html.Div(className='tab-row',
                                    children=[
                                        html.P('Some text.....')]
                                    )
                       ])

    except Exception as e:
        raise Exception(f'{provider} tab-3', e)

    return tab


def tab_3_rows(sd_data, provider):
    return dcc.Tab(id='Tab-3',
                   label='About',
                   selected_className='custom-tab--selected',
                   className='the-tab',
                   children=tab_3_content(sd_data, provider))


def tab_row_123(sd_data: dict, provider: str):
    top_row = html.Div(className='tab-row',
                       children=[html.A([html.P(sd_data['SD_provider'])],
                                        href=sd_data['SD_link']),
                                 html.P('Some tab content '),
                                 html.A([
                                     html.Img(
                                         className='logo-img',
                                         src=sd_data['SD_logo_url'])
                                 ], href=sd_data['SD_link'])])
    return top_row


def tabs_content(sd_data: dict, provider: str):
    provider_id = get_provider_id(provider)
    content = dcc.Tabs(id=f'content-{provider_id}',
                       className='tab-menu',
                       parent_className='tab-outer-container',
                       value='Tab-1',
                       children=[
                           tab_1_rows(sd_data, provider),
                           tab_2_rows(sd_data, provider),
                           tab_3_rows(sd_data, provider)
                       ])
    return content