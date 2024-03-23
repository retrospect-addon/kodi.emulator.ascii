# SPDX-License-Identifier: GPL-3.0

import os
import re
import sys
import random
from typing import Optional, Any

from sakee.colors import Colors


class KeyboardStub(object):
    def __init__(self):
        self.__id = random.random()
        self.__queue = []
        self.reset()

    def add_input(self, line: str) -> None:
        self.__queue.append(line)

    def clear_input(self) -> None:
        self.__queue = []

    def get_next_input(self) -> Optional[str]:
        if len(self.__queue) == 0:
            return None

        return self.__queue.pop(0)

    def reset(self) -> None:
        self.__queue = []
        line = os.environ.get("KODI_STUB_INPUT", None)
        if line:
            self.__queue.append(line)


class KodiStub(object):
    PY2: bool
    PY3: bool

    __keyboard_stub = None

    is_interactive: bool = os.environ.get("KODI_INTERACTIVE", "1") == "1"
    is_verbose: bool = os.environ.get("KODI_STUB_VERBOSE", "0") == "1"

    def __init__(self):
        self.PY2 = sys.version_info[0] == 2
        self.PY3 = sys.version_info[0] == 3

    def get_keyboard_stub(self) -> KeyboardStub:
        if KodiStub.__keyboard_stub is None:
            KodiStub.__keyboard_stub = KeyboardStub()

        return KodiStub.__keyboard_stub

    def read_input(self, text: str, color: Optional[str] = None) -> str:
        """ Reads user's input from the console

        :param text:    Question for the input

        :return: the read input

        """

        text = "{} ".format(text)

        if color is not None:
            text = "{}{}{}".format(color, text, Colors.EndColor)

        # noinspection PyUnresolvedReferences
        return input(text) if self.PY3 else raw_input(text)

    @staticmethod
    def print_heading(text: str, align_right: bool = False, color: str = Colors.Yellow) -> None:
        """ Aligns text over 120 chars

        :param text:            The Text to show.
        :param align_right:     Align right instead of left?
        :param color:           The color to use.

        :return: The headline text.

        """

        if text == "":
            heading = "=" * 120
        elif not align_right:
            heading = "= {} {}".format(text, "=" * (120 - 3 - len(text)))
        else:
            heading = "{} {} =".format("=" * (120 - 3 - len(text)), text)

        KodiStub.print_line(heading, color=color)

    @staticmethod
    def print_line(line: str, color: Optional[str] = None, verbose: bool = False) -> None:
        """ Prints a full line including colors

        :param line:        The line to print
        :param color:       The color to print (use Color)
        :param verbose:     Is the line verbose data?

        """

        if verbose and not KodiStub.is_verbose:
            return

        if color:
            print(color + line + Colors.EndColor)
        else:
            print(line)

    def log_method(self, code_module: str, name: str, *args: Any, **kwargs: Any) -> None:
        """

        :param code_module:  The module that called this method
        :param name:         The method that was callled
        :param *args:        The arguments that were passed
        :param **kwargs:     The keyword arguments that where passed

        :return: None

        """

        KodiStub.print_line("Call to missing: {0}.{1}".format(code_module, name), color=Colors.Blue, verbose=True)
        if not self.is_verbose:
            return

        if not args and not kwargs:
            print("-> %s.%s()" % (code_module, name,))
        if args and not kwargs:
            print("-> %s.%s(args=%s)" % (code_module, name, args))
        if args and kwargs:
            print("-> %s.%s(args=%s, kwargs=%s)" % (code_module, name, args, kwargs))
        if not args and kwargs:
            print("-> %s.%s(kwargs=%s)" % (code_module, name, kwargs))

    @staticmethod
    def replace_colors(color_tag: str) -> str:
        """ Replace the Kodi color tags with actual tags.

        :param color_tag: The text that contains color tags

        :return: The text with actual ASCII color codes

        """

        def __color_replacer(color_input):
            color_name = color_input.group(1)
            if color_name == "gold":
                return Colors.Yellow
            elif color_name == "dimgray":
                return Colors.DarkGrey
            elif color_name == "aqua":
                return Colors.LightBlue
            elif color_name == "red":
                return Colors.Red
            else:
                return Colors.EndColor

        color_tag = re.sub(r'\[COLOR (\w+)]', __color_replacer, color_tag)
        color_tag = color_tag.replace("[/COLOR]", Colors.EndColor)
        return color_tag

    def __str__(self) -> str:
        return self.__class__.__name__

    def __getattr__(self, name: str):
        """ Logs any missing methods calls

        :param str name:    The name of the attribute
        :return: object

        """

        def method(*args, **kwargs):
            return self.log_method(self.__class__.__name__, name, *args, **kwargs)
        return method
