# SPDX-License-Identifier: GPL-3.0
from sakee.colors import Colors
import io
import os
import re
import xml.etree.ElementTree as ElementTree
from typing import Dict, List, Literal
from typing import Optional

from sakee import addoninfo
from sakee.stub import KodiStub

SettingType = Literal[
    "string",
    "boolean",
    "integer",
    "float",
    "string_list",
    "boolean_list",
    "integer_list",
    "float_list",
]


# noinspection PyPep8Naming,PyShadowingBuiltins
class Settings:
    __profile_settings_path: Optional[str]
    __default_settings_path: str
    __settings: Dict[str, str]
    __setting_types: Dict[str, SettingType]

    def __init__(self, default_settings_path: str, profile_settings_path: Optional[str] = None) -> None:
        self.__default_settings_path = default_settings_path
        self.__profile_settings_path = profile_settings_path
        self.__settings = {}
        self.__setting_types = {}
        self.__read_settings()

    # String settings
    def getString(self, id: str) -> str:
        self.__validate_setting_type(id, "string")
        return self.__settings[id]

    def setString(self, id: str, value: str) -> None:
        self.__validate_setting_type(id, "string")
        if not isinstance(value, str):
            raise TypeError(f"Setting '{id}' requires a string value")
        self.__settings[id] = value

    def getStringList(self, id: str) -> List[str]:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "string_list")
        # values = json.loads(self.__settings[id])
        # return [str(value) for value in values]

    def setStringList(self, id: str, values: List[str]) -> None:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "string_list")
        # if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        #     raise TypeError(f"Setting '{id}' requires a list of strings")
        # self.__settings[id] = json.dumps(values)

    # Boolean settings
    def getBool(self, id: str) -> bool:
        self.__validate_setting_type(id, "boolean")
        return self.__settings[id].strip().lower() == "true"

    def setBool(self, id: str, value: bool) -> None:
        self.__validate_setting_type(id, "boolean")
        if not isinstance(value, bool):
            raise TypeError(f"Setting '{id}' requires a boolean value")
        self.__settings[id] = "true" if value else "false"

    def getBoolList(self, id: str) -> List[bool]:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "boolean_list")
        # values = json.loads(self.__settings[id])
        # return [bool(value) for value in values]

    def setBoolList(self, id: str, values: List[bool]) -> None:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "boolean_list")
        # if not isinstance(values, list) or not all(isinstance(value, bool) for value in values):
        #     raise TypeError(f"Setting '{id}' requires a list of booleans")
        # self.__settings[id] = json.dumps(values)

    # Integer settings
    def getInt(self, id: str) -> int:
        self.__validate_setting_type(id, "integer")
        return int(self.__settings[id])

    def setInt(self, id: str, value: int) -> None:
        self.__validate_setting_type(id, "integer")
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"Setting '{id}' requires an integer value")
        self.__settings[id] = str(value)

    def getIntList(self, id: str) -> List[int]:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "integer_list")
        # values = json.loads(self.__settings[id])
        # return [int(value) for value in values]

    def setIntList(self, id: str, values: List[int]) -> None:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "integer_list")
        # if not isinstance(values, list) or not all(
        #     isinstance(value, int) and not isinstance(value, bool) for value in values
        # ):
        #     raise TypeError(f"Setting '{id}' requires a list of integers")
        # self.__settings[id] = json.dumps(values)

    # Number settings
    def getNumber(self, id: str) -> float:
        self.__validate_setting_type(id, "float")
        return float(self.__settings[id])

    def setNumber(self, id: str, value: float) -> None:
        self.__validate_setting_type(id, "float")
        if not isinstance(value, float):
            raise TypeError(f"Setting '{id}' requires a floating-point value")
        self.__settings[id] = str(value)

    def getNumberList(self, id: str) -> List[float]:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "integer_list")
        # values = json.loads(self.__settings[id])
        # return [float(value) for value in values]

    def setNumberList(self, id: str, values: List[float]) -> None:
        raise NotImplementedError("Not Yet Implemented")

        # self.__validate_setting_type(id, "integer_list")
        # if not isinstance(values, list) or not all(isinstance(value, float) for value in values):
        #     raise TypeError(f"Setting '{id}' requires a list of integer values")
        # self.__settings[id] = json.dumps(values)

    def _raw_settings(self) -> Dict[str, str]:
        return self.__settings

    def __getitem__(self, id: str) -> str:
        """ Returns the actual stored string value for the setting with `id` for TESTING purposes only.

        :param id:  The ID of the setting.

        :return: The string value of the setting.

        """

        return self.__settings.get(id, "")

    def __setitem__(self, id: str, value: str) -> None:
        """ Sets the string value of the setting with `id` to `value` for TESTING purposes only.

        :param id:      The ID of the setting.
        :param value:   The string value for this settings.

        """

        self.__settings[id] = value

    def items(self):
        return self.__settings.items()

    def __iter__(self):
        return self.__settings.__iter__()

    def __len__(self):
        return len(self.__settings)

    def __read_settings(self) -> None:
        if not os.path.isfile(self.__default_settings_path):
            return

        with io.open(self.__default_settings_path, encoding="utf-8") as fp:
            default_root = ElementTree.parse(fp).getroot()

        for element in default_root.iter("setting"):
            setting_id = element.get("id")

            if not setting_id:
                continue

            setting_type = self.__get_setting_type(element)
            default_node = [a for a in element.iterfind("default")]
            if default_node:
                default_value = default_node[0].text or ""
            else:
                default_value = element.get("default", "")

            self.__setting_types[setting_id] = setting_type
            self.__settings[setting_id] = default_value

        if not self.__profile_settings_path or not os.path.isfile(self.__profile_settings_path):
            return

        with io.open(self.__profile_settings_path, encoding="utf-8") as fp:
            profile_root = ElementTree.parse(fp).getroot()

        for element in profile_root.iter("setting"):
            setting_id = element.get("id")

            if not setting_id or setting_id not in self.__setting_types:
                continue

            value = element.get("value")
            if value is None:
                value = element.text or ""

            self.__settings[setting_id] = value

    @staticmethod
    def __get_setting_type(element: ElementTree.Element) -> SettingType:
        setting_type = element.get("type", "text").lower()
        option = element.get("option", "").lower()

        if setting_type == "bool":
            return "boolean"

        if setting_type == "number":
            return "float"

        if setting_type in {"enum", "lvalues_enum"}:
            return "integer"

        if setting_type == "slider":
            return "float" if option == "float" else "integer"

        if setting_type in {"boolean", "integer", "string"}:
            return setting_type

        if setting_type == "number_list":
            return "integer_list"

        if setting_type in {"string_list", "boolean_list", "integer_list"}:
            return setting_type

        return "string"

    def __validate_setting_type(self, id: str, expected_type: SettingType) -> None:
        if id not in self.__settings:
            raise KeyError(f"Unknown setting '{id}'")

        actual_type = self.__setting_types[id]
        if actual_type != expected_type:
            raise TypeError(f"Setting '{id}' is '{actual_type}', not '{expected_type}'")

# noinspection PyPep8Naming,PyShadowingBuiltins
class Addon(KodiStub):
    __version: Optional[str]
    __name: Optional[str]
    __author: Optional[str]
    __icon: Optional[str]
    __summary: Optional[str]
    __news: Optional[str]
    __disclaimer: Optional[str]
    __description: Optional[str]
    __settings: Settings

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

        default_settings_path = os.path.join(self.__add_on_path, "resources", "settings.xml")
        profile_settings_path = os.path.join(self.__add_on_profile_path, "settings.xml")
        self.__settings = Settings(default_settings_path, profile_settings_path)

    def getLocalizedString(self, id: int) -> str:
        """ Returns an addon's localized 'unicode string'.

        :param int id:      Id# for string you want to localize.

        :return: Localized 'unicode string'
        :rtype: str

        """

        return self.__localization.get(id, "Translated {}".format(id))

    def getSettings(self):
        """ Returns a wrapper around the addon’s settings.

        :return: A wrapper around the addon’s settings.

        """

        return self.__settings

    def getSetting(self, id: str) -> Optional[str]:
        """ Returns the value of a setting as a unicode string.

        :param id: ID of the setting that the module needs to access.

        :return: The value of a setting as a unicode string. If the value was not set, None
        is returned.

        """

        return self.getSettings()[id]

    def getSettingBool(self, id: str) -> bool:
        """ Returns the value of a setting as a boolean.

        :param id: ID of the setting that the module needs to access.

        :return: The value of a setting as a boolean.

        """

        self.print_line("Deprecated. Use Settings.getBool() instead.", color=Colors.Red)
        return self.__settings.getBool(id)

    def getSettingInt(self, id: str) -> int:
        """ Returns the value of a setting as an integer.

        :param str id: ID of the setting that the module needs to access.

        :return: The value of a setting as an integer.
        :rtype: int

        """

        self.print_line("Deprecated. Use Settings.getInt() instead.", color=Colors.Red)
        return self.__settings.getInt(id)

    def getSettingNumber(self, id: str) -> float:
        """ Returns the value of a setting as a floating point number.

        :param id: ID of the setting that the module needs to access.

        :return: The value of a setting as a floating point number.

        """

        self.print_line("Deprecated. Use Settings.getNumber() instead.", color=Colors.Red)
        return self.__settings.getNumber(id)

    def getSettingString(self, id: str) -> str:
        """ Returns the value of a setting as a string.

        :param id: ID of the setting that the module needs to access.

        :return: The value of a setting as a string.

        """

        self.print_line("Deprecated. Use Settings.getString() instead.", color=Colors.Red)
        return self.__settings.getString(id)

    def setSetting(self, id: str, value: str) -> None:
        """ Sets a script setting.

        :param id:       ID of the setting that the module needs to access.
        :param value:    Value of the setting.

        """

        self.__settings[id] = value

    def setSettingBool(self, id: str, value: bool) -> bool:
        """ Sets a script setting.

        :param id:       ID of the setting that the module needs to access.
        :param value:    Value of the setting.

        :return: True if the value of the setting was set, false otherwise

        """

        self.print_line("Deprecated. Use Settings.setBool() instead.", color=Colors.Red)
        self.__settings.setBool(id, value)
        return True

    def setSettingInt(self, id: str, value: int) -> bool:
        """ Sets a script setting.

        :param id:       ID of the setting that the module needs to access.
        :param value:    Value of the setting.

        :return: True if the value of the setting was set, false otherwise

        """

        self.print_line("Deprecated. Use Settings.setInt() instead.", color=Colors.Red)
        self.__settings.setInt(id, value)
        return True

    def setSettingNumber(self, id: str, value: float) -> bool:
        """ Sets a script setting.

        :param str id:       ID of the setting that the module needs to access.
        :param float value:  Value of the setting.

        :return: True if the value of the setting was set, false otherwise

        """

        self.print_line("Deprecated. Use Settings.setNumber() instead.", color=Colors.Red)
        self.__settings.setNumber(id, value)
        return True

    def setSettingString(self, id: str, value: str) -> bool:  # NOSONAR
        """ Sets a script setting.

        :param id:     ID of the setting that the module needs to access.
        :param value:  Value of the setting.

        :return: True if the value of the setting was set, false otherwise

        """

        self.print_line("Deprecated. Use Settings.setString() instead.", color=Colors.Red)
        self.__settings.setString(id, value)
        return True

    def openSettings(self) -> None:
        self.print_heading("Add-on settings")
        for setting, value in self.__settings.items():
            self.print_line("{}:{}".format(setting, value), verbose=True)

    def getAddonInfo(self, id: str) -> str:
        """ Returns the value of an addon property as a string.

        :param id:  Id of the property that the module needs to access.

        :return: Returns the value of an addon property as a string.

        Possible options are: author, changelog, description, disclaimer, fanart, icon, id,
                              name, path, profile, stars, summary, type, version
        """
        id = id.lower()
        # missing: starts - type

        if id == "author":
            return self.__author or ""
        elif id == "changelog":
            return self.__news or ""
        elif id == "description":
            return self.__description or ""
        elif id == "disclaimer":
            return self.__disclaimer or ""
        elif id == "fanart":
            return str(self.__fanart)
        elif id == "icon":
            return self.__icon or ""
        elif id == "id":
            return self.__add_on_id or ""
        elif id == "name":
            return self.__name or ""
        elif id == "path":
            return self.__add_on_path or ""
        elif id == "profile":
            return self.__add_on_profile_path
        elif id == "summary":
            return self.__summary or ""
        elif id == "version":
            return self.__version or ""

        raise ValueError("Cannot find info '%s'" % (id,))

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
