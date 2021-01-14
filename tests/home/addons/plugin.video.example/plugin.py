# -*- coding: utf-8 -*-
""" This is a fake addon """

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import tempfile

import xbmc
import xbmcplugin

try:  # Python 3
    from urllib.parse import urlparse, parse_qsl
except ImportError:  # Python 2
    from urlparse import urlparse, parse_qsl

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print('ERROR: Missing URL as first parameter')
        exit(1)

    # Parse routing
    url_parts = urlparse(sys.argv[0])
    route = url_parts.path
    if len(sys.argv) > 2:
        query = dict(parse_qsl(sys.argv[2].lstrip('?')))
    else:
        query = {}
    print('Invoked plugin.video.example with route %s and query %s' % (route, query))

    # Execute add-on functions
    if route == '/touch':
        file = os.path.join(tempfile.gettempdir(), query.get('filename'))
        open(file, 'w').close()
        exit()

    if route == '/play':
        listitem = xbmc.ListItem(label='Something', path=query.get('filename'))
        xbmcplugin.setResolvedUrl(-1, True, listitem)
        exit()

    # Unknown route
    print('Unknown route %s' % route)
    exit(1)
