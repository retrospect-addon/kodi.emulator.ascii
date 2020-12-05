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
