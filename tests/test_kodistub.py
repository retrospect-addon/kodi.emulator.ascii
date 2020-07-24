import unittest


class TestKeyboardStub(unittest.TestCase):
    def test_single_keyboard(self):
        def get_import():
            import sakee.stub
            s = sakee.stub.KodiStub()
            return s.get_keyboard_stub()

        def get_import_from_package():
            import sakee
            s = sakee.stub.KodiStub()
            return s.get_keyboard_stub()

        def get_import_from():
            from sakee.stub import KodiStub
            s = KodiStub()
            return s.get_keyboard_stub()

        kb1 = get_import()
        kb2 = get_import_from()
        kb3 = get_import_from_package()
        self.assertEqual(kb1, kb2)
        self.assertEqual(kb1, kb3)
        self.assertEqual(kb1._KeyboardStub__id, kb2._KeyboardStub__id)

    def test_keyboard(self):
        import xbmc
        k = xbmc.Keyboard()
        stub = k.get_keyboard_stub()
        stub.clear_input()
        stub.add_input("1234")
        stub.add_input("12345")

        k.doModal()
        self.assertEqual("1234", k.getText())
        k.doModal()
        self.assertEqual("12345", k.getText())
        self.assertEqual(stub._KeyboardStub__queue, [])

    def test_keyboard_environment(self):
        import os
        import xbmc
        os.environ["KODI_STUB_INPUT"] = "123456"

        k = xbmc.Keyboard()
        k.get_keyboard_stub().reset()
        k.doModal()
        self.assertEqual(k.getText(), "123456")
