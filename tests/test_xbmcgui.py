import unittest

import xbmc
import xbmcgui


class XbmcGuiTest(unittest.TestCase):

    def test_dialog_input(self):
        text = "This is a test"
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(text)

        dlg = xbmcgui.Dialog()
        value = dlg.input('Heading')
        self.assertEqual(text, value)

    def test_dialog_input_empty(self):
        text = "This is a default value"
        dlg = xbmcgui.Dialog()
        value = dlg.input('Heading', defaultt=text)
        self.assertEqual(text, value)

    def test_dialog_numeric(self):
        text = "1234"
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(text)

        dlg = xbmcgui.Dialog()
        value = dlg.numeric(0, 'Heading', text)
        self.assertEqual(text, value)

    def test_dialog_numeric_empty(self):
        text = "5555"
        dlg = xbmcgui.Dialog()
        value = dlg.numeric(0, 'Heading', defaultt=text)
        self.assertEqual(text, value)

    def test_dialog_browse_single(self):
        default_filename = '/tmp/default'

        dlg = xbmcgui.Dialog()
        value = dlg.browseSingle(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertEqual(default_filename, value)

        entered_filename = '/tmp/entered'
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(entered_filename)

        dlg = xbmcgui.Dialog()
        value = dlg.browseSingle(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertEqual(entered_filename, value)

    def test_dialog_browse_multiple(self):
        default_filename = '/tmp/default'

        dlg = xbmcgui.Dialog()
        value = dlg.browseMultiple(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertListEqual([default_filename], value)

        entered_filename = '/tmp/entered'
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(entered_filename)

        dlg = xbmcgui.Dialog()
        value = dlg.browseMultiple(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertListEqual([entered_filename], value)

    def test_list_item_path(self):
        path = "https://test/path"
        item = xbmcgui.ListItem(path=path)
        self.assertEqual(path, item.getPath())
        self.assertEqual(path, item.getProperty("path"))
