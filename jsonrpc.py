# SPDX-License-Identifier: GPL-3.0
import io
import json
import os
import re

import xbmc


class JsonRpcApi(object):

    __ADDON_INFO = None

    def __init__(self):
        """ Initialise the JSON RPC API Implementation. """
        if JsonRpcApi.__ADDON_INFO is None:
            JsonRpcApi.__ADDON_INFO = xbmc.get_add_on_info_from_calling_script()

    def handle(self, json_data):
        """ Handle the JSON RPC Request

        :param obj json_data: The JSON RPC request.

        """
        (namespace, method_name) = json_data["method"].split('.')

        # Find class
        try:
            class_ = getattr(JsonRpcApi, namespace)
        except AttributeError:
            raise NotImplementedError

        # Find method
        instance = class_(JsonRpcApi.__ADDON_INFO)
        try:
            method_ = getattr(instance, method_name)
        except AttributeError:
            raise NotImplementedError

        # Invoke method
        result = method_(**json_data["params"])

        return json.dumps(dict(
            id=0,
            jsonrpc='2.0',
            result=result,
        ))

    class Settings(object):
        """ Allows manipulation of Kodi settings. """
        __SETTINGS = None

        def __init__(self, addon_info):
            """ Initialise the JSON RPC API Settings Namespace.

            :param obj addon_info:   Information about the current Add-on paths.

            """
            self._ADDON_INFO = addon_info

            # Load the guisettings.xml file
            if JsonRpcApi.Settings.__SETTINGS is None:
                settings_xml_file = os.path.join(self._ADDON_INFO.kodi_profile_path, "guisettings.xml")
                if os.path.isfile(settings_xml_file):
                    with io.open(settings_xml_file, encoding='utf-8') as fp:
                        settings_xml = fp.read()
                    results = re.findall(r'id="([^"]+)"[^>]*>([^<]+)<', settings_xml)
                    JsonRpcApi.Settings.__SETTINGS = dict(results)

        # noinspection PyPep8Naming
        def GetSettingValue(self, setting):
            """ Retrieves the value of a setting

            :param str setting:  The name of the settings for which the value is retrieved.

            :return: The value for the given setting.
            :rtype: str
            """
            value = JsonRpcApi.Settings.__SETTINGS.get(setting, '')
            if value == 'true':
                value = True

            return dict(
                value=value
            )
