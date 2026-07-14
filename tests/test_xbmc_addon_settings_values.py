from unittest import skip
from xbmcaddon import Settings
import os
import unittest


class TestSettingsValues(unittest.TestCase):
    default_path = os.path.abspath("./tests/data/old_settings_default.xml")
    profile_path = os.path.abspath("./tests/data/old_settings_profile.xml")

    def setUp(self) -> None:
        self.settings = Settings(TestSettingsValues.default_path)

    def test_get_string_returns_default_value(self) -> None:
        self.assertEqual("Hello World", self.settings.getString("text"))

    def test_get_string_supports_settings_without_explicit_type(self) -> None:
        self.assertEqual("No typed text", self.settings.getString("no_type"))

    def test_set_string_updates_value(self) -> None:
        self.settings.setString("text", "Goodbye World")

        self.assertEqual("Goodbye World", self.settings.getString("text"))
        self.assertEqual("Goodbye World", self.settings["text"])

    def test_set_string_rejects_non_string(self) -> None:
        with self.assertRaisesRegex(TypeError, "requires a string value"):
            self.settings.setString("text", 42)  # type: ignore[arg-type]

    def test_get_bool_returns_default_value(self) -> None:
        self.assertTrue(self.settings.getBool("bool"))

    def test_set_bool_updates_value(self) -> None:
        self.settings.setBool("bool", False)

        self.assertFalse(self.settings.getBool("bool"))
        self.assertEqual("false", self.settings["bool"])

    def test_set_bool_rejects_non_boolean(self) -> None:
        with self.assertRaisesRegex(TypeError, "requires a boolean value"):
            self.settings.setBool("bool", 1)  # type: ignore[arg-type]

    def test_get_int_returns_slider_and_enum_defaults(self) -> None:
        self.assertEqual(42, self.settings.getInt("slider_int"))
        self.assertEqual(1, self.settings.getInt("enum"))
        self.assertEqual(0, self.settings.getInt("lvalues_enum"))

    def test_set_int_updates_value(self) -> None:
        self.settings.setInt("slider_int", 73)

        self.assertEqual(73, self.settings.getInt("slider_int"))
        self.assertEqual("73", self.settings["slider_int"])

    def test_set_int_rejects_boolean_and_non_integer(self) -> None:
        for invalid_value in (True, 4.2, "4"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires an integer value"):
                    self.settings.setInt("slider_int", invalid_value)  # type: ignore[arg-type]

    def test_get_number_returns_float(self) -> None:
        self.assertEqual(3.14, self.settings.getNumber("number"))

    def test_set_number_updates_value(self) -> None:
        self.settings.setNumber("number", 6.28)

        self.assertEqual(6.28, self.settings.getNumber("number"))
        self.assertEqual("6.28", self.settings["number"])

    def test_set_number_rejects_non_float(self) -> None:
        for invalid_value in (1, True, "1.5"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires a floating-point value"):
                    self.settings.setNumber("number", invalid_value)  # type: ignore[arg-type]

    def test_string_fallback_types_are_accessible_as_strings(self) -> None:
        expected = {
            "select": "2",
            "lvalues_select": "1",
            "setting_file": "/tmp/file.txt",
            "setting_audio": "/tmp/file.mp3",
            "setting_video": "/tmp/file.mp4",
            "setting_image": "/tmp/file.jpg",
            "setting_executable": "/tmp/file.exe",
            "setting_folder": "/tmp",
            "path": "/storage",
            "ip": "192.168.1.100",
        }

        for setting_id, value in expected.items():
            with self.subTest(setting_id=setting_id):
                self.assertEqual(value, self.settings.getString(setting_id))

    def test_unknown_setting_raises_key_error(self) -> None:
        with self.assertRaisesRegex(KeyError, "Unknown setting 'missing'"):
            self.settings.getString("missing")

    def test_getter_for_wrong_type_raises_type_error(self) -> None:
        with self.assertRaisesRegex(TypeError, "Setting 'bool' is 'boolean', not 'string'"):
            self.settings.getString("bool")

    def test_len_and_raw_settings(self) -> None:
        self.assertEqual(19, len(self.settings))
        self.assertEqual("Hello World", self.settings._raw_settings()["text"])


@skip
class TestSettingsListValues(unittest.TestCase):
    default_path = os.path.abspath("./tests/data/old_settings_default.xml")
    profile_path = os.path.abspath("./tests/data/old_settings_profile.xml")

    def setUp(self) -> None:
        self.settings = Settings(TestSettingsValues.default_path)

    def test_get_and_set_string_list(self) -> None:
        self.assertEqual(["alpha", "beta"], self.settings.getStringList("strings"))

        self.settings.setStringList("strings", ["gamma", "delta"])

        self.assertEqual(["gamma", "delta"], self.settings.getStringList("strings"))

    def test_set_string_list_rejects_invalid_values(self) -> None:
        for invalid_value in (("alpha",), ["alpha", 2], "alpha"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires a list of strings"):
                    self.settings.setStringList("strings", invalid_value)  # type: ignore[arg-type]

    def test_get_and_set_bool_list(self) -> None:
        self.assertEqual([True, False], self.settings.getBoolList("booleans"))

        self.settings.setBoolList("booleans", [False, True])

        self.assertEqual([False, True], self.settings.getBoolList("booleans"))

    def test_set_bool_list_rejects_invalid_values(self) -> None:
        for invalid_value in ((True,), [True, 1], "true"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires a list of booleans"):
                    self.settings.setBoolList("booleans", invalid_value)  # type: ignore[arg-type]

    def test_get_and_set_int_list(self) -> None:
        self.assertEqual([1, 2], self.settings.getIntList("integers"))

        self.settings.setIntList("integers", [3, 4])

        self.assertEqual([3, 4], self.settings.getIntList("integers"))

    def test_set_int_list_rejects_invalid_values(self) -> None:
        for invalid_value in ((1, 2), [1, True], [1, 2.0], "1,2"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires a list of integers"):
                    self.settings.setIntList("integers", invalid_value)  # type: ignore[arg-type]

    def test_get_and_set_number_list(self) -> None:
        self.assertEqual([1.5, 2.75], self.settings.getNumberList("numbers"))

        self.settings.setNumberList("numbers", [3.25, 4.5])

        self.assertEqual([3.25, 4.5], self.settings.getNumberList("numbers"))

    def test_set_number_list_rejects_invalid_values(self) -> None:
        for invalid_value in ((1.5,), [1.5, 2], "1.5,2.0"):
            with self.subTest(value=invalid_value):
                with self.assertRaisesRegex(TypeError, "requires a list of integer values"):
                    self.settings.setNumberList("numbers", invalid_value)  # type: ignore[arg-type]
