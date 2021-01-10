import json
import os
import time
import unittest

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

    def test_jsonrpc(self):
        # Addons.GetAddons
        cmd = dict(
            jsonrpc='2.0',
            method='Addons.GetAddons',
            params={'installed': True, 'enabled': True, 'type': 'xbmc.python.pluginsource'},
            id=1
        )
        result = json.loads(xbmc.executeJSONRPC(json.dumps(cmd)))
        self.assertEqual(result.get('jsonrpc'), '2.0')
        self.assertIsInstance(result.get('result'), dict)
        self.assertIsInstance(result.get('result').get('addons'), list)
        self.assertEqual(result.get('result').get('addons')[0].get('addonid'), 'plugin.video.example')

    def test_executebuiltin(self):

        def _wait_for_file(filename, timeout=10):
            """Wait until a file appears on the filesystem."""
            deadline = time.time() + timeout
            while time.time() < deadline:
                if os.path.exists(filename):
                    return True
                time.sleep(.1)
            return False

        filename = 'tests/home/userdata/plugin.video.example/executed.txt'
        if os.path.exists(filename):
            os.remove(filename)

        tests = [
            'RunPlugin(plugin://plugin.video.example/path/to/method/?port=1234)'
            'RunPlugin(plugin://plugin.video.example/path/to/method/)'
            'RunPlugin(plugin://plugin.video.example/)'
            'RunPlugin(plugin://plugin.video.example)'
        ]

        for test in tests:
            xbmc.executebuiltin(test)
            success = _wait_for_file(filename)
            self.assertTrue(success)
