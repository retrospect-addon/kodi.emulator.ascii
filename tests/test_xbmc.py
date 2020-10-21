import unittest
import os
import xbmc


class XbmcTest(unittest.TestCase):

    def test_keyboard_preset_text(self):
        text = "This is a test"
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(text)
        kb.doModal()
        self.assertTrue(kb.isConfirmed())
        self.assertEqual(text, kb.getText())

    def test_keyboard_empty(self):
        kb = xbmc.Keyboard()
        kb.doModal()
        self.assertTrue(kb.isConfirmed())
        self.assertIsNone(kb.getText())

    def test_keyboard_env_var(self):
        text = "Input set via environment variable"
        os.environ["KODI_STUB_INPUT"] = text
        kb = xbmc.Keyboard()
        kb.get_keyboard_stub().reset()
        kb.doModal()
        self.assertTrue(kb.isConfirmed())
        self.assertEqual(text, kb.getText())
