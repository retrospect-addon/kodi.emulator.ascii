# SPDX-License-Identifier: GPL-3.0


class Colors:
    def __init__(self):
        pass

    EndColor = '\033[0m'
    # Some styles
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'

    White = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Orange = '\033[33m'
    Blue = '\033[34m'
    Purple = '\033[35m'
    Cyan = '\033[36m'
    LightGrey = '\033[37m'
    DarkGrey = '\033[90m'
    LightRed = '\033[91m'
    LightGreen = '\033[92m'
    Yellow = '\033[93m'
    LightBlue = '\033[94m'
    Pink = '\033[95m'
    LightCyan = '\033[96m'


if __name__ == '__main__':
    for color in dir(Colors):
        if color.startswith("__"):
            continue
        exec("print Colors.%s + color + Colors.EndColor" % (color, ))
