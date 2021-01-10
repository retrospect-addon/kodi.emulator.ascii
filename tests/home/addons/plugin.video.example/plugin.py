# -*- coding: utf-8 -*-
""" This is a fake addon """

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

try:  # Python 3
    from urllib.parse import parse_qsl, urlparse, urlsplit, parse_qs
except ImportError:  # Python 2
    from urlparse import parse_qsl, urlparse

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print('ERROR: Missing URL as first parameter')
        exit(1)

    # Parse routing
    path = urlsplit(sys.argv[0]).path or '/'
    if len(sys.argv) > 2:
        params = parse_qs(sys.argv[2].lstrip('?'))
    else:
        params = {}

    print('Invoked plugin.video.example with route %s and query %s' % (path, params))
