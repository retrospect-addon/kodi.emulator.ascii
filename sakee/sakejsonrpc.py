# SPDX-License-Identifier: GPL-3.0

import io
import os
import re

from sakee import addoninfo


class JsonRpcApi(object):
    __ADDON_INFO = None

    def __init__(self):
        """ Initialise the JSON RPC API Implementation. """
        if JsonRpcApi.__ADDON_INFO is None:
            JsonRpcApi.__ADDON_INFO = addoninfo.get_add_on_info_from_calling_script()

    def handle(self, json_data):
        """ Handle the JSON RPC Request

        :param obj json_data: The JSON RPC request.

        :return: The JSON RPC reply.
        :rtype: dict
        """
        (class_name, method_name) = json_data["method"].split('.')

        # Find class
        try:
            class_reference = getattr(JsonRpcApi, class_name)
        except AttributeError:
            raise NotImplementedError

        # Find method
        class_instance = class_reference(JsonRpcApi.__ADDON_INFO)
        try:
            method_reference = getattr(class_instance, method_name)
        except AttributeError:
            raise NotImplementedError

        # Invoke method
        result = method_reference(**json_data["params"])

        return dict(
            id=0,
            jsonrpc='2.0',
            result=result,
        )

    class Addons(object):
        """ List, enable and execute addons. """
        __ADDONS = []

        def __init__(self, addon_info):
            """ Initialise the JSON RPC API Addons Namespace.

            :param obj addon_info:   Information about the current Add-on paths.
            """
            self._ADDON_INFO = addon_info

        # noinspection PyPep8Naming
        def GetAddons(self, type=None, content=None, enabled=None, properties=None, limits=None, installed=True):  # NOSONAR
            """ Gets all available addons. """
            addons = []
            for addon in os.listdir(os.path.join(self._ADDON_INFO.kodi_home_path, 'addons')):
                addon_xml = os.path.join(self._ADDON_INFO.kodi_home_path, 'addons', addon, 'addon.xml')
                if not os.path.exists(addon_xml):
                    continue

                addon_info = addoninfo.read_addon_xml(addon_xml)
                addons.append(dict(
                    type=addon_info.get('type'),
                    addonid=addon_info.get('id')))

            return dict(
                addons=addons,
                limits=dict(
                    start=0,
                    end=len(addons),
                    total=len(addons)
                )
            )

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
        def GetSettingValue(self, setting):  # NOSONAR
            """ Retrieves the value of a setting.

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
