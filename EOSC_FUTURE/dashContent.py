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

    #  temporary we set this to none...
    inner_content = None

    if provider == 'ICOS Carbon Portal':
        inner_content = tabs(sd_data, provider)
        my_source = 'https://data.icos-cp.eu/dashboard/?stationId=BIR&valueType=co&height=50'
    elif provider == 'INGOS':
        my_source = 'https://www.ingos-infrastructure.eu/'
    elif provider == 'NEON':
        my_source = 'assets/static-html/neon.html'
    elif provider == 'OCEAN':
        my_source = 'assets/static-html/ocean.html'
    else:
        my_source = '/assets/static-html/folium_map.html'

    if inner_content is None:
        inner_content = html.Iframe(className='infrastructure-frame',
                              src=my_source,
                              title=provider,
                              )

    plugin_div = html.Div(className='frame-container',
                          children=[inner_content])

    return plugin_div


def get_providerid(provider):
    return provider_id_dict[provider]

def mainmenu():
    menu = dcc.Checklist(
        className='input-checklist',
        id='input-checklist',
        options=provider_list,
        inputClassName='input-checkbox',
        labelClassName='label-input'
    )
    return menu


def tabs(sd_data: dict, provider):
    provider_id = get_providerid(provider)
    tabs_content = dcc.Tabs(className='tab-container',
                            id=provider,
                            value=provider_id,
                            children=[
                                dcc.Tab(id=provider_id + 'Tab-1', label='Indicator',
                                        children=tab_1_content(sd_data, provider)),
                                dcc.Tab(id=provider_id + 'Tab-2', label='About',
                                        children=tab_1_content(sd_data, provider)),
                                dcc.Tab(id=provider_id + 'Tab-3', label='Config',
                                        children=tab_1_content(sd_data, provider)),
                            ])
    return tabs_content

def tab_1_content(sd_data, provider):

    try:
        tab = html.Div(className='tab-1-content',
                       children=[
                           html.P('Some tab content '),
                           html.H4(provider),
                           html.Img(className='logo-img', src=sd_data['SD_logo_url'])
                       ])
    except Exception as e:
        raise Exception(provider + ' -2 \n ' + sd_data['SD_logo_url'], e)

    return tab

def tab_2_content(sd_data, provider):

    try:
        tab = html.Div(className='tab-2-content',
                       children=[
                           html.P('Some tab content '),
                           html.H4(provider),
                           html.Img(className='logo-img', src=sd_data['SD_logo_url'])
                       ])
    except Exception as e:
        raise Exception(provider + ' -2 \n ' + sd_data['SD_logo_url'], e)

    return tab

def tab_3_content(sd_data, provider):

    try:
        tab = html.Div(className='tab-3-content',
                       children=[
                           html.Div(className='tab-3-row-1',
                                    children=[
                                        html.P('Some tab content '),
                                        html.H4(provider),
                                        html.Img(className='logo-img', src=sd_data['SD_logo_url']
                                                 )]
                                    ),
                           html.Div(className='tab-3-row-1',
                                    children=[
                                        html.P('Some text.....')]
                                    )
                       ])

    except Exception as e:
        raise Exception(provider + '  \nProblem: ' + sd_data['SD_logo_url'], e)

    return tab
