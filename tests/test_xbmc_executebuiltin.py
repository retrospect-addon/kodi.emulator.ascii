import os
import tempfile
import time
import unittest

import xbmc


class XbmcBuiltinTest(unittest.TestCase):

    def test_runplugin(self):

        def _wait_for_file(filename, timeout=3):
            """Wait until a file appears on the filesystem."""
            deadline = time.time() + timeout
            while time.time() < deadline:
                if os.path.exists(filename):
                    return True
                time.sleep(.1)
            return False

        filename = 'sakee_runplugin.txt'
        full_filename = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(full_filename):
            os.remove(full_filename)

        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.example/touch?filename=%s)' % filename)
        self.assertTrue(_wait_for_file(full_filename))

    def test_playmedia(self):

        def _wait_for_playing(player, filename, timeout=3):
            """Wait until a file appears on the filesystem."""
            deadline = time.time() + timeout
            while time.time() < deadline:
                if player.isPlaying() and player.getPlayingFile() == filename:
                    return True
                time.sleep(.1)
            return False

        player = xbmc.Player()

        # Invalid command
        with self.assertRaises(ValueError):
            xbmc.executebuiltin('PlayerControl(error)')

        # Play something from a file
        filename = 'something_file.mp4'
        xbmc.executebuiltin('PlayMedia(%s)' % filename)  # This can take a few ms to start
        self.assertTrue(_wait_for_playing(player, filename))

        xbmc.executebuiltin('PlayerControl(Play)')  # This is instant
        self.assertFalse(player.isPlaying())

        # Play something from a plugin://-uri
        filename = 'something_plugin.mp4'
        xbmc.executebuiltin('PlayMedia(plugin://plugin.video.example/play?filename=%s)' % filename)  # This can take a few ms to start
        self.assertTrue(_wait_for_playing(player, filename))

        xbmc.executebuiltin('PlayerControl(Stop)')  # This is instant
        self.assertFalse(player.isPlaying())
