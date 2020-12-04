# SPDX-License-Identifier: CC-BY-NC-SA-4.0

import sys

# Make UTF-8 the default encoding in Python 2
if sys.version_info[0] == 2:
    # noinspection PyUnresolvedReferences
    reload(sys)
    # noinspection PyUnresolvedReferences
    sys.setdefaultencoding("utf-8")

__all__ = ["test_kodistub", "test_unicode", "test_xbmc", "test_xbmc_player", "test_xbmcgui", "test_xbmcvfs"]
