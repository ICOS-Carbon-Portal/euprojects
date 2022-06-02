# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:45:10 2022

    Objective:
    ==========
    Parse yaml-files and validate the content
    with respect to the dashboard of
    the EOSC Future project.

    The EoscValueObject store data parsed
    from the yaml-files and which are retrieved
    using two getters. (Similar to the DTO/Value Object pattern)

    Example:
    ========
    from ReadPlugins import EoscValueObject

    # server side object
    eosc_vo = EoscValueObject()

    # List of data providers in EOSC
    provider_list = eosc_vo.get_providers()

    # Dictionary holds data for each provider
    usr_choice = provider_list[0]
    provider_dict = eosc_vo.get_provider_plug(usr_choice)

"""

import yaml
import os


class EoscValueObject:
    """ The object holds data to EOSC plugins """

    def __init__(self, pluginpath='./yaml-files/'):
        
        # In what follows 'SD' stands for Scientific Dashboard, while
        # Provider is a Research Infrastructure.
        # _SD_providers is a list for an outer menu to the dashboards
        self._SD_providers = []

        # _plug_dict is a dictionary with widget data from the yaml-files.
        # Each provider in the list, is a key to their data
        # Example:
        # _plug_dict ={'ICOS':{config-data from ICOS}, 'MARIS':{config-data from MARIS},...}
        # retrieve the data using .get_provider_plug(sd)  #(with sd from _SD_provider)
        self._plug_dict = {}

        self._PLUGPATH = pluginpath
        self.__main__()

    def __main__(self):
        
        plugins = [x for x in os.listdir(self._PLUGPATH) if x[-5:] == ".yaml"]

        # We loop the files to find proper data
        for plug in plugins:
            if plug != '.ipynb_checkpoints':
                config = self.__validate_plugin__(plug)
                try:
                    self._SD_providers.append(config.pop('SD_provider'))
                except Exception as e:
                    print(plug, '\n', config, '\n', e)
                self._plug_dict[self._SD_providers[-1]] = config

        return

    def __validate_plugin__(self, plugin):
        """
        Read a plugin yaml file from the CONST PLUGPATH and validate the entries.

        Parameters
        ----------
        plugin: STR the name of the plugin.
    
        Raises
        ------
        Exception
            Exceptions are raised if:
            - The yaml parser finds an error
            - Mandatory keys in the configuration are missing.
            - Mandatory keys has no value.
    
        Returns
        -------
        Dictionary.
    
        """
        config = os.path.join(self._PLUGPATH, plugin)

        with open(config,  encoding='utf8') as config:
            
            try:
                # parse the file
                cfg = yaml.load(config, Loader=yaml.FullLoader)
                # validation 1: check for mandatory keys
                mandatory_keys = {'SD_provider', 'authors', 'title',
                                  'description', 'keywords', 'license', 
                                  'funding', 'resourcetype', 'SD_URL'}
                provided_keys = cfg.keys()
                
                if not mandatory_keys.issubset(provided_keys):
                    raise Exception('The file {} is missing the mandatory key(s):'.format(plugin),
                                    mandatory_keys - provided_keys)
                
                # validation 2: values of mandatory keys are 'valid'
                if None in [cfg[x] for x in mandatory_keys]:
                    raise Exception('Some mandatory key(s) are not set ' +
                                    'in the file {}:'.format(plugin),
                                    [x for x in
                                     mandatory_keys if cfg[x] is None])
            except yaml.YAMLError as exc:
                raise Exception('Error in plugin file: {}'.format(plugin), exc)
            except Exception as generalErr:
                raise Exception('The file: {} caused the '.format(plugin) +
                                'excption: ', generalErr)

        return cfg
    
    def get_provider_plug(self, data_provider) -> dict:
        """ Returns dictionary with data for a specific provider """
        if data_provider not in self._SD_providers:
            raise Warning(str('The data provider \'{}\' is not' +
                              'in the  SD-provider list. ' +
                              'Use \'get_providers()\' to get' +
                              'the list.').format(data_provider))
        else:
            return self._plug_dict[data_provider]
        
    def get_providers(self) -> list:
        """ Returns a list of data providers """
        return self._SD_providers
