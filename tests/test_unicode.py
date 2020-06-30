# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0
import unittest

import xbmcgui
import xbmcplugin


class TestUnicode(unittest.TestCase):

    def test_unicode(self):
        for label in ['saké', u'saké', '酒', u'酒']:
            li = xbmcgui.ListItem(label=label, path='plugin://plugin.video.example/' + label)
            xbmcplugin.addDirectoryItem(-1, li.getPath(), li)

        xbmcplugin.endOfDirectory(-1)
