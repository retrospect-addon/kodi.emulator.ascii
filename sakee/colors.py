# SPDX-License-Identifier: GPL-3.0


class Colors:
    def __init__(self):
        pass

    EndColor = '\033[0m'
    Reset = '\033[39m'

    White = '\033[37m'
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


class BackGroundColor:
    def __init__(self):
        pass

    Black = '\033[40m'
    Red = '\033[41m'
    Green = '\033[42m'
    Yellow = '\033[43m'
    Blue = '\033[44m'
    Magenta = '\033[45m'
    Cyan = '\033[46m'
    White = '\033[47m'
    Reset = '\033[49m'


class Styles:
    def __init__(self):
        pass

    Bright = '\033[1m'
    Dim = '\033[2m'
    Normal = '\033[22m'
    Reset = '\033[0m'


if __name__ == '__main__':
    for color in dir(Colors):
        if color.startswith("__"):
            continue
        exec("print(Colors.%s + color + Colors.EndColor)" % (color, ))
        exec("print(Styles.Bright + Colors.%s + color + Colors.EndColor)" % (color, ))

    for color in dir(BackGroundColor):
        if color.startswith("__"):
            continue
        exec("print(BackGroundColor.%s + color + BackGroundColor.Reset)" % (color, ))
