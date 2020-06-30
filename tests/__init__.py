# SPDX-License-Identifier: CC-BY-NC-SA-4.0

import sys

# Make UTF-8 the default encoding in Python 2
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding("utf-8")

__all__ = ["test_unicode"]
