# SPDX-License-Identifier: GPL-3.0
import io
import json
import os
import re

import xbmc


class JsonRpcApi(object):
    def __init__(self):
        """ Initialise the JSON RPC API Implementation. """
        self._paths = xbmc.get_add_on_info_from_calling_script()


class Settings(JsonRpcApi):
    """ Allows manipulation of Kodi settings. """
    __SETTINGS = None

    def __init__(self):
        """ Initialise the JSON RPC API Settings Namespace. """
        super(Settings, self).__init__()

        if Settings.__SETTINGS is None:
            settings_xml_file = os.path.join(self._paths.kodi_profile_path, "guisettings.xml")
            if os.path.isfile(settings_xml_file):
                with io.open(settings_xml_file, encoding='utf-8') as fp:
                    settings_xml = fp.read()
                results = re.findall(r'id="([^"]+)"[^>]*>([^<]+)<', settings_xml)
                Settings.__SETTINGS = dict(results)

    def GetSettingValue(self, setting):
        """ Retrieves the value of a setting

        :param str setting:  The name of the settings for which the value is retrieved.

        :return: The value for the given setting.
        :rtype: str
        """
        value = Settings.__SETTINGS.get(setting, '')
        if value == 'true':
            value = True

        return json.dumps(dict(
            id=0,
            jsonrpc='2.0',
            result=dict(
                value=value
            ),
        ))
