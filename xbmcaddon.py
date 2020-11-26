# SPDX-License-Identifier: GPL-3.0

import os
import io
import re

from sakee import addoninfo
from sakee.stub import KodiStub


# noinspection PyPep8Naming,PyShadowingBuiltins
class Addon(KodiStub):
    __settings = {}

    def __init__(self, id=None):
        super(Addon, self).__init__()

        self.__add_on_id = id
        # Get some data from the path of the calling file
        paths = addoninfo.get_add_on_info_from_calling_script(id)
        self.__kodi_home_path = paths.kodi_home_path
        self.__add_on_id = paths.add_on_id
        self.__add_on_path = paths.add_on_path
        self.__add_on_profile_path = os.path.join(paths.kodi_profile_path, "addon_data", self.__add_on_id)

        # actual live data
        self.__version = None
        self.__name = None
        self.__author = None
        self.__icon = None
        self.__summary = None
        self.__news = None
        self.__disclaimer = None
        self.__description = None
        self.__load_add_on_xml()
        self.__localization = self.__get_strings()
        self.__settings = self.__get_settings()

    def getSetting(self, id):  # NOSONAR
        """ Returns the value of a setting as a unicode string.

        :param str id:  Id of the setting that the module needs to access.

        :return: The value of a setting as a unicode string.
        :rtype: str

        """
        if id in self.__settings:
            return self.__settings[id]
        else:
            return ''

    def getSettingBool(self, id):
        """ Returns the value of a setting as a boolean.

        :param str id:  Id of the setting that the module needs to access.

        :return: The value of a setting as a boolean.
        :rtype: bool

        """
        return self.getSetting(id).lower() == "true"

    def getSettingInt(self, id):
        """ Returns the value of a setting as an integer.

        :param str id:  Id of the setting that the module needs to access.

        :return: The value of a setting as an integer.
        :rtype: int

        """

        return int(self.getSetting(id) or 0)

    def getSettingNumber(self, id):
        """ Returns the value of a setting as a floating point number.

        :param str id:  Id of the setting that the module needs to access.

        :return: The value of a setting as a floating point number.
        :rtype: float

        """

        return float(self.getSetting(id) or 0.0)

    def getSettingString(self, id):
        """ Returns the value of a setting as a string.

        :param str id:  Id of the setting that the module needs to access.

        :return: The value of a setting as a string.
        :rtype: float

        """

        return str(self.getSetting(id) or "")

    def setSetting(self, id, value):  # NOSONAR
        """ Sets a script setting.

        :param str id:       Id of the setting that the module needs to access.
        :param str value:    Value of the setting.

        """

        self.__settings[id] = value

    def setSettingBool(self, id, value):  # NOSONAR
        """ Sets a script setting.

        :param str id:       Id of the setting that the module needs to access.
        :param bool value:    Value of the setting.

        """

        self.__settings[id] = "true" if value else "false"
        return True

    def setSettingInt(self, id, value):  # NOSONAR
        """ Sets a script setting.

        :param str id:       Id of the setting that the module needs to access.
        :param int value:    Value of the setting.

        """

        self.__settings[id] = str(value)
        return True

    def setSettingNumber(self, id, value):  # NOSONAR
        """ Sets a script setting.

        :param str id:       Id of the setting that the module needs to access.
        :param float value:  Value of the setting.

        """

        self.__settings[id] = str(value)
        return True

    def setSettingString(self, id, value):  # NOSONAR
        """ Sets a script setting.

        :param str id:       Id of the setting that the module needs to access.
        :param str value:  Value of the setting.

        """

        self.__settings[id] = value
        return True

    def getAddonInfo(self, id):  # NOSONAR
        """ Returns the value of an addon property as a string.

        :param str id:  Id of the property that the module needs to access.

        :return: Returns the value of an addon property as a string.
        :rtype: str

        Possible options are: author, changelog, description, disclaimer, fanart, icon, id,
                              name, path, profile, stars, summary, type, version
        """
        id = id.lower()
        # missing: starts - type

        if id == "author":
            return self.__author
        elif id == "changelog":
            return self.__news
        elif id == "description":
            return self.__description
        elif id == "disclaimer":
            return self.__disclaimer
        elif id == "fanart":
            return self.__fanart
        elif id == "icon":
            return self.__icon
        elif id == "id":
            return self.__add_on_id
        elif id == "name":
            return self.__name
        elif id == "path":
            return self.__add_on_path
        elif id == "profile":
            return self.__add_on_profile_path
        elif id == "summary":
            return self.__summary
        elif id == "version":
            return self.__version

        raise ValueError("Cannot find info '%s'" % (id,))

    def getLocalizedString(self, id):  # NOSONAR
        """ Returns an addon's localized 'unicode string'.

        :param int id:      Id# for string you want to localize.

        :return: Localized 'unicode string'
        :rtype: str

        """

        return self.__localization.get(id, "Translated {}".format(id))

    def openSettings(self):  # NOSONAR
        self.print_heading("Add-on settings")
        for setting, value in self.__settings.items():
            self.print_line("{}:{}".format(setting, value), verbose=True)

    def __repr__(self):
        return repr(self.__settings)

    def __get_strings(self):
        english = os.path.join(self.__add_on_path, "resources", "language", "resource.language.en_gb", "strings.po")
        if not os.path.isfile(english):
            return {}

        with io.open(english, "r", encoding='utf-8') as fp:
            english_data = fp.read()

        translations = {}
        if not english_data:
            return translations

        # Take into account that there could be multi-line translations.
        strings = re.findall(
            r'msgctxt "#(\d+)"\W+msgid ((?:"[^\n\r]*"\W{1,2})+)msgstr ((?:"[^\n\r]*"\W{1,2})+)',
            english_data, flags=re.IGNORECASE)

        for string in strings:
            translation = string[1]
            # See if there was a translation present, if so, use it.
            if string[2].strip('\n\r"'):
                translation = string[2]
            parts = translation.split('"')
            msgs = [t for t in parts if t.strip()]
            translation = "".join(msgs)
            translation = translation.replace("[CR]", "\n")
            translations[int(string[0])] = translation

        return translations

    def __filter_lang_xmltag(self, tag, xml_content):
        tag_matches = re.findall(r'<' + tag + r'(?:\s*lang=\"([a-zA-Z-_]+)\")?\s*>(.*?)</' + tag + '>', xml_content, flags=re.DOTALL)
        if tag_matches:
            for match in tag_matches:
                if match[0].startswith('en'):
                    return match[1]
            else:
                return tag_matches[0][1]
        return None

    def __load_add_on_xml(self):
        add_on_xml = os.path.join(self.__add_on_path, "addon.xml")

        with io.open(add_on_xml, encoding='utf-8') as fp:
            xml_content = fp.read()
            self.__version = re.findall(r'<addon.*?version="([^"]*)', xml_content, flags=re.DOTALL)[0]
            self.__add_on_id = re.findall(r'addon.*?id="([^"]+)"', xml_content, flags=re.DOTALL)[0]
            self.__name = re.findall(r'name="([^"]+)"', xml_content)[0]

            self.__description = self.__filter_lang_xmltag('description', xml_content)
            self.__disclaimer = self.__filter_lang_xmltag('disclaimer', xml_content)
            self.__summary = self.__filter_lang_xmltag('summary', xml_content)

            author_matches = re.findall(r'<addon.*?provider-name="([^"]+)', xml_content, flags=re.DOTALL)
            if author_matches:
                self.__author = author_matches[0]

            news_matches = re.findall(r'<news>(.*?)</news>', xml_content, flags=re.DOTALL)
            if news_matches:
                self.__news = news_matches[0]

            fanart_matches = re.findall(r'<fanart>(.*?)</fanart>', xml_content, flags=re.DOTALL)
            if fanart_matches:
                self.__fanart = os.path.join(self.__add_on_path, fanart_matches[0])

            icon_matches = re.findall(r'<icon>(.*?)</icon>', xml_content, flags=re.DOTALL)
            if icon_matches:
                self.__icon = os.path.join(self.__add_on_path, icon_matches[0])

    def __get_settings(self):
        if self.__add_on_id in Addon.__settings:
            settings = Addon.__settings[self.__add_on_id]
            return settings

        # load defaults
        settings = {}
        settings_xml = os.path.join(self.__add_on_path, "resources", "settings.xml")
        if not os.path.isfile(settings_xml):
            Addon.__settings[self.__add_on_id] = settings
            return settings

        with io.open(settings_xml, encoding='utf-8') as fp:
            default_xml = fp.read()

        setting_regex = r'id="([^"]+)"[^>]*default="([^"]*)"'
        results = re.findall(setting_regex, default_xml)
        if not results:
            results = re.findall(r'setting id="(.*?)".*?(?:<default>(.*?)<|<default\s*/>|<data)', default_xml, re.DOTALL)
        settings = {}
        for result in results:
            settings[result[0]] = result[1]

        user_xml = os.path.join(self.__add_on_profile_path, "settings.xml")
        if os.path.isfile(user_xml):
            with io.open(user_xml, encoding="utf-8") as fp:
                user_xml = fp.read()

            setting_regex = r'id="([^"]+)"[^>]*value="([^"]*)"'
            results = re.findall(setting_regex, user_xml)
            if not results:
                results = re.findall(r'id="([^"]+)"[^>]*>([^<]+)<', user_xml)

            for result in results:
                # if result[0] in settings:  -> We need to keep all settings in the settings.xml
                settings[result[0]] = result[1]

        Addon.__settings[self.__add_on_id] = settings
        return settings
