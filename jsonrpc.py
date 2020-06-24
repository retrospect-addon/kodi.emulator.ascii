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


class Addons(JsonRpcApi):
    """ List, enable and execute addons. """
    pass


class Application(JsonRpcApi):
    """ Application information and control. """
    pass


class AudioLibrary(JsonRpcApi):
    """ Audio Library information. """
    pass


class Favourites(JsonRpcApi):
    """ Favourites GetFavourites and AddFavourite. """
    pass


class Files(JsonRpcApi):
    """ Shares information & filesystem listings. """
    pass


class GUI(JsonRpcApi):
    """ Window properties and activation. """
    pass


class Input(JsonRpcApi):
    """ Allows limited navigation within Kodi. """
    pass


class JSONRPC(JsonRpcApi):
    """ A variety of standard JSONRPC calls. """
    pass


class PVR(JsonRpcApi):
    """ Live TV control. """
    pass


class Player(JsonRpcApi):
    """ Manages all available players. """
    pass


class Playlist(JsonRpcApi):
    """ Playlist modification. """
    pass


class Profiles(JsonRpcApi):
    """ Support for Profiles operations to Kodi. """
    pass


class Settings(JsonRpcApi):
    """ Allows manipulation of Kodi settings. """
    __SETTINGS = None

    def __init__(self):
        """ Initialise the JSON RPC API Settings Namespace. """
        super(Settings, self).__init__()

        if self.__SETTINGS is None:
            settings_xml_file = os.path.join(self._paths.kodi_profile_path, "guisettings.xml")
            if os.path.isfile(settings_xml_file):
                with io.open(settings_xml_file, encoding='utf-8') as fp:
                    settings_xml = fp.read().decode()
                results = re.findall(r'id="([^"]+)"[^>]*>([^<]+)<', settings_xml)
                self.__SETTINGS = dict(results)

    def GetCategories(self, level, section, properties):
        """ Retrieves all setting categories """
        raise NotImplementedError()

    def GetSections(self, level, section):
        """ Retrieves all setting sections """
        raise NotImplementedError()

    def GetSettingValue(self, setting):
        """ Retrieves the value of a setting

        :param mixed setting: str
        :return: value
        :rtype: string
        """
        value = self.__SETTINGS.get(setting, '')
        if value == 'true':
            value = True

        return json.dumps(dict(
            id=0,
            jsonrpc='2.0',
            result=dict(
                value=value
            ),
        ))

    def GetSettings(self, level, filter):
        """ Retrieves all settings """
        raise NotImplementedError()

    def ResetSettingValue(self, setting):
        """ Resets the value of a setting """
        raise NotImplementedError()

    def SetSettingValue(self, setting, value):
        """ Changes the value of a setting """
        raise NotImplementedError()


class System(JsonRpcApi):
    """ System controls and information. """
    pass


class Textures(JsonRpcApi):
    """ Supplies GetTextures and RemoveTexture. Textures are images. """
    pass


class VideoLibrary(JsonRpcApi):
    """ Video Library information. """
    pass


class XBMC(JsonRpcApi):
    """ Dumping ground for very Kodi specific operations. """
    pass
