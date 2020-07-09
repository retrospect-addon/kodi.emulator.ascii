# SPDX-License-Identifier: GPL-3.0
import time
import unittest

import xbmc
import xbmcgui
import xbmcplugin


class TestXbmcPlayer(unittest.TestCase):

    def test_player(self):
        filename = '/tmp/file1.mov'

        player = xbmc.Player()

        # Start playback trough a setResolvedFile
        li = xbmcgui.ListItem(label='Label', path=filename)
        xbmcplugin.setResolvedUrl(-1, True, li)

        # Wait for up to 5 seconds until the Player started playing
        deadline = time.time() + 5
        while deadline > time.time():
            if player.isPlaying():
                break
            time.sleep(0.1)  # Sleep 100ms

        self.assertEqual(player.isPlaying(), True)
        self.assertEqual(player.isPlayingVideo(), True)

        # Check if we have the right file
        self.assertEqual(player.getPlayingFile(), filename)

        # Hit pause, we should be paused now
        player.pause()
        self.assertEqual(player.isPlaying(), False)

        # Seek to 3 seconds
        player.seekTime(3)
        self.assertEqual(player.getTime(), 3)

        # Hit pause again, we should be playing again
        player.pause()
        self.assertEqual(player.isPlaying(), True)

        # Hit stop
        player.stop()
        self.assertEqual(player.isPlaying(), False)
        self.assertEqual(player.isPlayingVideo(), False)
