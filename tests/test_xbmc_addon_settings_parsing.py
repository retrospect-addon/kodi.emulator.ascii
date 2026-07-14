import os
import unittest

from xbmcaddon import Settings


class TestOldSettingsParsing(unittest.TestCase):
    default_path = os.path.abspath("./tests/data/old_settings_default.xml")
    profile_path = os.path.abspath("./tests/data/old_settings_profile.xml")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"Testing with {cls.default_path} and {cls.profile_path}")

    def _load_default_settings(self) -> Settings:
        settings = Settings(self.default_path)
        return settings

    def _load_profile_settings(self) -> Settings:
        settings = Settings(self.default_path, self.profile_path)
        return settings

    # Untyped string setting
    def test_settings_parsing_untyped_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("No typed text", settings["no_type"])
        self.assertIsInstance(settings["no_type"], str)

    def test_settings_parsing_untyped_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("No typed value", settings["no_type"])
        self.assertIsInstance(settings["no_type"], str)

    # Text setting
    def test_settings_parsing_text_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("Hello World", settings["text"])
        self.assertIsInstance(settings["text"], str)

    def test_settings_parsing_text_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("Kodi", settings["text"])
        self.assertIsInstance(settings["text"], str)

    # Boolean setting
    def test_settings_parsing_bool_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("true", settings["bool"])
        self.assertIsInstance(settings["bool"], str)

    def test_settings_parsing_bool_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("false", settings["bool"])
        self.assertIsInstance(settings["bool"], str)

    def test_new_settings_get_bool(self):
        settings = self._load_default_settings()
        self.assertEqual(True, settings.getBool("bool"))
        self.assertIsInstance(settings.getBool("bool"), bool)

        settings = self._load_profile_settings()
        self.assertEqual(False, settings.getBool("bool"))
        self.assertIsInstance(settings.getBool("bool"), bool)

    # Number setting
    def test_settings_parsing_number_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("3.14", settings["number"])
        self.assertIsInstance(settings["number"], str)

    def test_settings_parsing_number_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("1.618", settings["number"])
        self.assertIsInstance(settings["number"], str)

    # Integer slider setting
    def test_settings_parsing_integer_slider_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("42", settings["slider_int"])
        self.assertIsInstance(settings["slider_int"], str)

    def test_settings_parsing_integer_slider_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("73", settings["slider_int"])
        self.assertIsInstance(settings["slider_int"], str)

    # Float slider setting
    def test_settings_parsing_float_slider_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("2.5", settings["slider_float"])
        self.assertIsInstance(settings["slider_float"], str)

    def test_settings_parsing_float_slider_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("4.5", settings["slider_float"])
        self.assertIsInstance(settings["slider_float"], str)

    # Enum setting
    def test_settings_parsing_enum_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("1", settings["enum"])
        self.assertIsInstance(settings["enum"], str)

    def test_settings_parsing_enum_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("2", settings["enum"])
        self.assertIsInstance(settings["enum"], str)

    # Select setting
    def test_settings_parsing_select_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("2", settings["select"])
        self.assertIsInstance(settings["select"], str)

    def test_settings_parsing_select_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("0", settings["select"])
        self.assertIsInstance(settings["select"], str)

    # Localized enum setting
    def test_settings_parsing_localized_enum_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("0", settings["lvalues_enum"])
        self.assertIsInstance(settings["lvalues_enum"], str)

    def test_settings_parsing_localized_enum_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("1", settings["lvalues_enum"])
        self.assertIsInstance(settings["lvalues_enum"], str)

    # Localized select setting
    def test_settings_parsing_localized_select_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("1", settings["lvalues_select"])
        self.assertIsInstance(settings["lvalues_select"], str)

    def test_settings_parsing_localized_select_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("2", settings["lvalues_select"])
        self.assertIsInstance(settings["lvalues_select"], str)

    # File setting
    def test_settings_parsing_file_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("/tmp/file.txt", settings["setting_file"])
        self.assertIsInstance(settings["setting_file"], str)

    def test_settings_parsing_file_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("/home/user/movie.mkv", settings["setting_file"])
        self.assertIsInstance(settings["setting_file"], str)

    # Folder setting
    def test_settings_parsing_folder_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("/tmp", settings["setting_folder"])
        self.assertIsInstance(settings["setting_folder"], str)

    def test_settings_parsing_folder_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("/home/user/Videos", settings["setting_folder"])
        self.assertIsInstance(settings["setting_folder"], str)

    # Path setting
    def test_settings_parsing_path_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("/storage", settings["path"])
        self.assertIsInstance(settings["path"], str)

    def test_settings_parsing_path_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("special://profile/", settings["path"])
        self.assertIsInstance(settings["path"], str)

    # IP address setting
    def test_settings_parsing_ipaddress_setting_reads_default_value(self):
        settings = self._load_default_settings()

        self.assertEqual("192.168.1.100", settings["ip"])
        self.assertIsInstance(settings["ip"], str)

    def test_settings_parsing_ipaddress_setting_reads_profile_value(self):
        settings = self._load_profile_settings()

        self.assertEqual("10.0.0.5", settings["ip"])
        self.assertIsInstance(settings["ip"], str)

    # Complete settings collections
    def test_settings_parsing_settings_reads_all_default_values(self):
        settings = Settings(self.default_path)

        self.assertEqual(
            {
                "text": "Hello World",
                "bool": "true",
                "number": "3.14",
                "slider_int": "42",
                "slider_float": "2.5",
                "enum": "1",
                "select": "2",
                "lvalues_enum": "0",
                "lvalues_select": "1",
                "path": "/storage",
                "ip": "192.168.1.100",
                "no_type": "No typed text",
                "setting_audio": "/tmp/file.mp3",
                "setting_executable": "/tmp/file.exe",
                "setting_file": "/tmp/file.txt",
                "setting_fileenum": "/tmp/file.txt",
                "setting_folder": "/tmp",
                "setting_image": "/tmp/file.jpg",
                "setting_video": "/tmp/file.mp4",
            },
            settings._raw_settings(),
        )

    def test_settings_parsing_settings_reads_all_profile_overrides(self):
        settings = Settings(self.default_path, self.profile_path)

        self.assertEqual(
            {
                "text": "Kodi",
                "bool": "false",
                "number": "1.618",
                "slider_int": "73",
                "slider_float": "4.5",
                "enum": "2",
                "select": "0",
                "lvalues_enum": "1",
                "lvalues_select": "2",
                "path": "special://profile/",
                "ip": "10.0.0.5",
                "no_type": "No typed value",
                "setting_audio": "/tmp/file.mp3",
                "setting_executable": "/tmp/file.exe",
                "setting_file": "/home/user/movie.mkv",
                "setting_fileenum": "/tmp/file.txt",
                "setting_folder": "/home/user/Videos",
                "setting_image": "/tmp/file.jpg",
                "setting_video": "/tmp/file.mp4",
            },
            settings._raw_settings(),
        )

    def test_settings_parsing_settings_contains_expected_number_of_default_settings(self):
        settings = Settings(self.default_path)

        self.assertEqual(19, len(settings))

    def test_settings_parsing_settings_contains_expected_number_of_settings_with_profile(self):
        settings = Settings(self.default_path, self.profile_path)

        self.assertEqual(19, len(settings))

    # Missing files
    def test_missing_profile_settings_file_keeps_default_settings(self):
        settings = Settings(self.default_path)

        self.assertEqual("Hello World", settings["text"])
        self.assertEqual("true", settings["bool"])
        self.assertEqual("3.14", settings["number"])
        self.assertEqual(19, len(settings))


class TestNewSettingsParsing(TestOldSettingsParsing):
    default_path = os.path.abspath("./tests/data/new_settings_default.xml")
    profile_path = os.path.abspath("./tests/data/new_settings_profile.xml")