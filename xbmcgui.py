# SPDX-License-Identifier: GPL-3.0
from typing import List, Optional, Union


from sakee.colors import Colors
from sakee.stub import KodiStub

NOTIFICATION_INFO = "info"
NOTIFICATION_WARNING = "warning"
NOTIFICATION_ERROR = "error"

INPUT_ALPHANUM = 0
INPUT_NUMERIC = 1
INPUT_DATE = 2
INPUT_TIME = 3
INPUT_IPADDRESS = 4
INPUT_PASSWORD = 5

PASSWORD_VERIFY = 1
ALPHANUM_HIDE_INPUT = 2


# noinspection PyPep8Naming
class ListItem(KodiStub):

    # noinspection PyUnusedLocal
    def __init__(self, label="", label2="", path="", offscreen=False):
        """ ListItem class. Creates a new ListItem.

        label          : [opt] string or unicode -
        label2         : [opt] string or unicode - label2 text.
        iconImage      : [opt] string - icon filename.
        thumbnailImage : [opt] string - thumbnail filename.
        path           : [opt] string or unicode -

        :param str label:           Label1 text.
        :param str label2:          Label2 text.
        :param str path:            Listitem's path.
        :param bool offscreen:      Is an offscreen item?

        *Note, You can use the above as keywords for arguments and skip certain optional arguments.
           Once you use a keyword, all following arguments require the keyword.

        """

        super(ListItem, self).__init__()

        self.__info = dict()
        self.__art = dict()
        self.__type = None

        self.__label = label
        self.__info["*label1"] = label
        self.__label2 = label2
        self.__info["*label2"] = label2

        self.__path = path
        self.__subtitles = []

        # store properties
        self.__properties = {"path": path}

    def setIconImage(self, icon):  # NOSONAR
        raise DeprecationWarning("No more setIconImage: http://kodi.wiki/view/Jarvis_API_changes")

    def setThumbnailImage(self, thumbnail):  # NOSONAR
        raise DeprecationWarning("No more setThumbnailImage: http://kodi.wiki/view/Jarvis_API_changes")

    # noinspection PyShadowingBuiltins
    def setInfo(self, type, infoLabels):  # NOSONAR
        """ Sets the listitem's infoLabels.

        :param str type:                    Type of
        :param dict[str,str] infoLabels:    Pairs of { label: value }

        ============  ======================================
        Command name  Description
        ============  ======================================
        video         Video information
        music         Music information
        pictures      Pictures informanion
        game          Game information
        ============  ======================================

        See http://kodi.wiki/view/InfoLabels

        """

        self.__type = type
        self.__info.update(infoLabels)
        self.print_line("Updating infolabels with {}".format(infoLabels), verbose=True)

    def setContentLookup(self, enable):
        """ Enable or disable content lookup for item.

        :param bool enable: bool to enable content lookup

        If disabled, HEAD requests to e.g determine mime type will not be sent.

        """
        pass

    def setArt(self, values):  # NOSONAR
        """ Sets the listitem's art

        :param dict[str,str] values:    Pairs of { label: value }.

        ==========  ======================================
        Label       Type
        ==========  ======================================
        thumb       image filename
        poster      image filename
        banner      image filename
        fanart      image filename
        clearart    image filename
        clearlogo   image filename
        landscape   image filename
        icon        image filename
        ==========  ======================================

        """

        self.__art.update(values)
        self.print_line("Updating artwork with {}".format(values), verbose=True)

    def setLabel(self, label):  # NOSONAR
        """ Sets the listitem's label.

        :param str label:   text string.

        """

        self.__label = label
        self.__art["label1"] = label
        self.print_line("Setting label1='{}'".format(label), verbose=True)

    def getLabel(self):
        """ Returns the listitem label.

        :return: label2
        :rtype: str

        """

        return self.__label

    def setLabel2(self, label):  # NOSONAR
        """ Sets the listitem's label.

        :param str label:   text string.

        """

        self.__label2 = label
        self.__art["label2"] = label
        self.print_line("Setting label2='{}'".format(label), verbose=True)

    def getLabel2(self):
        """ Returns the listitem label.

        :return: label2
        :rtype: str

        """

        return self.__label2

    def setSubtitles(self, subtitleFiles):  # NOSONAR
        """ Sets subtitles for this listitem.

        :param list[str] subtitleFiles: list with path to subtitle files

        """

        self.__subtitles = subtitleFiles
        for sub in subtitleFiles:
            self.print_line("Adding subtitles: {}".format(sub), verbose=True)

    def setProperty(self, key, value):  # NOSONAR
        """ Sets a listitem property, similar to an infolabel.

        :param str key:         Property name.
        :param str value:       Value of property.

        NOTE: Key is NOT case sensitive.

        """

        self.__properties[key.lower()] = value
        self.print_line("Adding property: {}: {}".format(key, value), verbose=True)

    def getProperty(self, key):  # NOSONAR
        """ Returns a listitem property as a string, similar to an infolabel.

        :param str key: property name.

        :return:

        NOTE: Key is NOT case sensitive.

        """

        return self.__properties.get(key.lower(), None)

    def getPath(self):  # NOSONAR
        """ Returns the path of this listitem.

        :return: The path of this listitem.
        :rtype: str
        """

        return self.__path or self.getProperty("path") or ""

    def setPath(self, path):  # NOSONAR
        """ Sets the listitem's path.

        :param str path:    Activated when item is clicked.

        """

        self.__path = path
        self.setProperty("path", path)

    def __str__(self):
        if KodiStub.is_verbose:
            value = "%s [%s]\n" % (self.__label, self.__type or "")
            value = "%sInfoLabels\n" % (value,)
            keys = sorted(self.__info.keys())
            for key in keys:
                value = "%s    - %s: %s\n" % (value, key, self.__info[key])
            value = "%sProperties\n" % (value,)
            keys = sorted(self.__properties.keys())
            for key in keys:
                value = "%s    - %s: %s\n" % (value, key, self.__properties[key])

            return value
        else:
            return self.__label

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()


# noinspection PyPep8Naming,PyShadowingBuiltins
class Dialog(KodiStub):
    def __init__(self):
        super(Dialog, self).__init__()

    def ok(self, heading: str, message: str) -> bool:
        """ OK dialog

        The functions permit the call of a dialog of information, a confirmation
        of the user by press from OK required.

        :param heading:      dialog heading.
        :param message:      dialog message.

        :return: Returns True if 'Ok' was pressed, else False.

        Example::

            dialog = xbmcgui.Dialog()
            ok = dialog.ok('Kodi', 'There was an error.')

        """

        KodiStub.print_heading(heading)

        if KodiStub.is_interactive:
            self.read_input("{}. OK?".format(message), color=Colors.Yellow)
        else:
            KodiStub.print_line("{}. OK?".format(message), Colors.Yellow)
        return True

    # noinspection PyUnusedLocal
    def textviewer(self, heading: str, text: str, usemono: bool = False) -> None:
        """ The text viewer dialog can be used to display descriptions,
        help texts or other larger texts.

        :param heading:     Dialog heading.
        :param text:        Dialog text.
        :param usemono:     Use a monospace font.

        """

        text = self.replace_colors(text)
        text = text.replace("\\n", "\n")
        self.print_heading(heading)
        self.print_line(text)
        self.print_line("=" * 120, color=Colors.Yellow)

        if KodiStub.is_interactive:
            self.read_input("OK?", color=Colors.Yellow)
        else:
            KodiStub.print_line("OK?", Colors.Yellow)
        return

    # noinspection PyPep8Naming,PyUnusedLocal
    def multiselect(self, heading: str,
                    options: Union[List[str], List[ListItem]],
                    autoclose: int = 0,
                    preselect: Optional[List[int]] = None,
                    useDetails: bool = False) -> Optional[List[int]]:
        """ Show a multi-select dialog.

        :param heading:          Dialog heading.
        :param options:          Options to choose from.
        :param autoclose:        Milliseconds to autoclose dialog. (default=do not autoclose)
        :param preselect:        Indexes of items to preselect in list (default: do not preselect any item)
        :param useDetails:       Use detailed list instead of a compact list. (default=false)

        :return: Returns the selected items as a list of indices, or None if cancelled.

        """

        self.print_heading(heading)

        selections = []
        for i in range(0, len(options)):
            self.print_line("{} ) {}".format(i, options[i]))
            selections.append(str(i))
        self.print_line("=" * 120, color=Colors.Yellow)
        selections = self.read_input("What items to select (%s)? " % (",".join(selections)),
                                     color=Colors.Yellow).lower()
        if not selections:
            return None
        return list(map(lambda index_value: int(index_value), selections.split(",")))

    # noinspection PyPep8Naming,PyUnusedLocal
    def select(self, heading: str,
               options: Union[List[str], List[ListItem]],
               autoclose: int = 0, preselect: int = -1,
               useDetails: bool = False) -> Optional[int]:
        """ Show a select dialog.

        :param heading:         Dialog heading.
        :param options:         Options to choose from.
        :param autoclose:       Milliseconds to autoclose dialog. (default=do not autoclose)
        :param preselect:       Indexes of items to preselect in list (default: do not preselect any item)
        :param useDetails:      Use detailed list instead of a compact list. (default=false)

        :return: Returns the selected items as a list of indices, or None if cancelled.

        """
        self.print_heading(heading)

        selections = []
        for i in range(0, len(options)):
            self.print_line("{} ) {}".format(i, options[i]))
            selections.append(str(i))
        self.print_line("=" * 120, color=Colors.Yellow)
        selections = self.read_input("What item to select (%s)? " % (",".join(selections)), color=Colors.Yellow).lower()
        if not selections:
            return None
        return list(map(lambda index_value: int(index_value), selections.split(",")))[0]

    # noinspection PyUnusedLocal
    def yesno(self, heading: str, message: str, nolabel: str = "", yeslabel: str = "",
              customlabel: Optional[str] = None, autoclose: int = 0) -> bool:
        """ The Yes / No dialog can be used to inform the user about questions and get the answer.

        :param heading:             Dialog heading.
        :param message:             Message to display.
        :param nolabel:             Label to put on the no button.
        :param yeslabel:            Label to put on the yes button.
        :param customlabel:         Label to put on the custom button.
        :param autoclose:           Milliseconds to autoclose dialog. (default=do not autoclose)

        :return: Returns True if 'Yes' was pressed, else False.

        """

        if not nolabel:
            nolabel = "No"

        if not yeslabel:
            yeslabel = "Yes"

        self.print_heading(heading)
        question = "{} [{}]{} or [{}]{}:".format(message, yeslabel[0], yeslabel[1:], nolabel[0], nolabel[1:])
        if KodiStub.is_interactive:
            answer = self.read_input(question, Colors.Yellow)
            return yeslabel.lower().startswith(answer.lower())
        else:
            KodiStub.print_line(question, Colors.Yellow)
            return True

    # noinspection PyUnusedLocal
    def notification(self, heading: str, message: str, icon: str = NOTIFICATION_INFO,
                     time: int = 5000, sound: bool = True) -> False:
        """ Show a Notification alert.

        :param heading:             Dialog heading.
        :param message:             Message to display.
        :param icon:                Icon to use. (default=xbmcgui.NOTIFICATION_INFO)
        :param time:                Time in milliseconds.
        :param sound:               Play notification sound. (default=True)

        ============================  ============
        Icon                          Description
        ============================  ============
        xbmcgui.NOTIFICATION_INFO     Info icon
        xbmcgui.NOTIFICATION_WARNING  Warning icon
        xbmcgui.NOTIFICATION_ERROR    Error icon
        ============================  ============

        """
        if icon == NOTIFICATION_WARNING:
            color = Colors.Yellow
        elif icon == NOTIFICATION_ERROR:
            color = Colors.Red
        else:
            color = Colors.White

        self.print_heading(heading, align_right=True, color=color)
        self.print_line(message, color=color)
        self.print_line("=" * 120, color)

    # noinspection PyUnusedLocal
    def input(self, heading: str, defaultt: str = "", type: int = INPUT_ALPHANUM,
              option: int = 0, autoclose: int = 0):
        """ Show an input dialog.

        :param heading:             Dialog heading.
        :param defaultt:            Default value
        :param type:                The type of keyboard dialog.
        :param option:              Option for the dialog.
        :param autoclose:           Milliseconds to autoclose dialog. (default=do not autoclose)

        ========================  =========================================
        Type                      Description
        ========================  =========================================
        xbmcgui.INPUT_ALPHANUM    Standard keyboard
        xbmcgui.INPUT_NUMERIC     Format: #
        xbmcgui.INPUT_DATE        Format: DD/MM/YYYY
        xbmcgui.INPUT_TIME        Format: HH:MM
        xbmcgui.INPUT_IPADDRESS   Format: #.#.#.#
        xbmcgui.INPUT_PASSWORD    Return MD5 hash of input, input is masked
        ========================  =========================================

        ===========================  ============================================================================
        Option                       Description
        ===========================  ============================================================================
        xbmcgui.PASSWORD_VERIFY      Verifies an existing (default) md5 hashed password. Use with INPUT_PASSWORD.
        xbmcgui.ALPHANUM_HIDE_INPUT  Masks input. Use with INPUT_ALPHANUM.
        ===========================  ============================================================================

        :return: Returns the entered data as a string. Returns an empty string if dialog was canceled.
        :rtype: str

        """
        if not self.is_interactive:
            keyboard = self.get_keyboard_stub()
            value = keyboard.get_next_input()
            return value if value is not None else defaultt

        KodiStub.print_heading(heading)
        try:
            answer = self.read_input("Please provide keyboard input [{}]?".format(defaultt), color=Colors.Yellow)
            return answer if answer != "" else defaultt
        except EOFError:
            return ""

    # noinspection PyUnusedLocal
    def numeric(self, type: int, heading: str, defaultt: str = "", bHiddenInput: bool = False):
        """ Show an numeric input dialog.

        :param type:                The type of numeric dialog.
        :param heading:             Dialog heading (will be ignored for type 4).
        :param defaultt:            Default value.
        :param bHiddenInput:        Mask input (available for type 0).

        =====  ========================  ========================================================
        Param  Type                      Description
        =====  ========================  ========================================================
        0      ShowAndGetNumber          Default format: #
        1      ShowAndGetDate            Default format: DD/MM/YYYY
        2      ShowAndGetTime            Default format: HH:MM
        3      ShowAndGetIPAddress       Default format: #.#.#.#
        4      ShowAndVerifyNewPassword  Default format: *
        =====  ========================  ========================================================

        :return: Returns the entered data as a string. Returns the default value if dialog was canceled.

        """

        if not self.is_interactive:
            keyboard = self.get_keyboard_stub()
            value = keyboard.get_next_input()
            return value if value is not None else defaultt

        KodiStub.print_heading(heading)
        try:
            answer = self.read_input("Please provide keyboard input [{}]?".format(defaultt), color=Colors.Yellow)
            return answer if answer != "" else defaultt
        except EOFError:
            return ""

    # noinspection PyUnusedLocal
    def browse(self, type: int, heading: str, shares: str, mask: str = "", useThumbs: bool = False,
               treatAsFolder: bool = False, defaultt: str = "",
               enableMultiple: bool = False) -> Union[str, List[str]]:
        """ Browser dialog.

        The function offer the possibility to select a file by the user of the add-on.
        It allows all the options that are possible in Kodi itself and offers all support file types.

        :param type:                The type of browse dialog.
        :param heading:             Dialog heading.
        :param shares:              From sources.xml
        :param mask:                '|' separated file mask. (i.e. '.jpg|.png')
        :param useThumbs:           Auto switch to Thumb view if files exist.
        :param treatAsFolder:       Playlists and archives act as folders.
        :param defaultt:            Default path or file.
        :param enableMultiple:      Multiple file selection is enabled.

        ========================  =========================================
        Type                      Description
        ========================  =========================================
        0                         ShowAndGetDirectory
        1                         ShowAndGetFile
        2                         ShowAndGetImage
        3                         ShowAndGetWriteableDirectory
        ========================  =========================================

        ===========================  ============================================================================
        Shares                       Description
        ===========================  ============================================================================
        "programs"                   list program addons
        "video"                      list video sources
        "music"                      list music sources
        "pictures"                   list picture sources
        "files"                      list file sources (added through filemanager)
        "games"                      list game sources
        "local"                      list local drives
        ""                           list local drives and network shares
        ===========================  ============================================================================

        :return: If enableMultiple is False (default): returns filename and/or path as a string to the location of the highlighted item, if user pressed 'Ok' or
                 a masked item was selected. Returns the default value if dialog was canceled.
                 If enableMultiple is True: returns tuple of marked filenames as a string if user pressed 'Ok' or a masked item was selected. Returns empty
                 tuple if dialog was canceled.
                 If type is 0 or 3 the enableMultiple parameter is ignored.

        """

        if enableMultiple:
            return self.browseMultiple(type, heading, shares, mask, useThumbs, treatAsFolder, defaultt)
        else:
            return self.browseSingle(type, heading, shares, mask, useThumbs, treatAsFolder, defaultt)

    # noinspection PyUnusedLocal
    def browseMultiple(self, type: int, heading: str, shares: str, mask: str = "",
                       useThumbs: bool = False, treatAsFolder: bool = False,
                       defaultt: str = "") -> List[str]:
        """ Browser dialog.

        The function offer the possibility to select a file by the user of the add-on.
        It allows all the options that are possible in Kodi itself and offers all support file types.

        :param type:                The type of browse dialog.
        :param heading:             Dialog heading.
        :param shares:              From sources.xml
        :param mask:                '|' separated file mask. (i.e. '.jpg|.png')
        :param useThumbs:           Auto switch to Thumb view if files exist.
        :param treatAsFolder:       Playlists and archives act as folders.
        :param defaultt:            Default path or file.

        ========================  =========================================
        Type                      Description
        ========================  =========================================
        0                         ShowAndGetDirectory
        1                         ShowAndGetFile
        2                         ShowAndGetImage
        3                         ShowAndGetWriteableDirectory
        ========================  =========================================

        ===========================  ============================================================================
        Shares                       Description
        ===========================  ============================================================================
        "programs"                   list program addons
        "video"                      list video sources
        "music"                      list music sources
        "pictures"                   list picture sources
        "files"                      list file sources (added through filemanager)
        "games"                      list game sources
        "local"                      list local drives
        ""                           list local drives and network shares
        ===========================  ============================================================================

        :return: Returns tuple of marked filenames as a string if user pressed 'Ok' or a masked item was selected.
                 Returns empty tuple if dialog was canceled.

        """

        if not self.is_interactive:
            keyboard = self.get_keyboard_stub()
            value = keyboard.get_next_input()
            return [value] if value is not None else [defaultt]

        KodiStub.print_heading(heading)
        try:
            answer = self.read_input("Please enter the path to a file [{}]?".format(defaultt), color=Colors.Yellow)
            return [answer] if answer != "" else [defaultt]
        except EOFError:
            return []

    # noinspection PyUnusedLocal
    def browseSingle(self, type: int, heading: str, shares: str, mask: str = "",
                     useThumbs: bool = False, treatAsFolder: bool = False,
                     defaultt: str = "") -> str:
        """ Browser dialog.

        The function offer the possibility to select a file by the user of the add-on.
        It allows all the options that are possible in Kodi itself and offers all support file types.

        :param type:                The type of browse dialog.
        :param heading:             Dialog heading.
        :param shares:              From sources.xml
        :param mask:                '|' separated file mask. (i.e. '.jpg|.png')
        :param useThumbs:           Auto switch to Thumb view if files exist.
        :param treatAsFolder:       Playlists and archives act as folders.
        :param defaultt:            Default path or file.

        ========================  =========================================
        Type                      Description
        ========================  =========================================
        0                         ShowAndGetDirectory
        1                         ShowAndGetFile
        2                         ShowAndGetImage
        3                         ShowAndGetWriteableDirectory
        ========================  =========================================

        ===========================  ============================================================================
        Shares                       Description
        ===========================  ============================================================================
        "programs"                   list program addons
        "video"                      list video sources
        "music"                      list music sources
        "pictures"                   list picture sources
        "files"                      list file sources (added through filemanager)
        "games"                      list game sources
        "local"                      list local drives
        ""                           list local drives and network shares
        ===========================  ============================================================================

        :return: Returns filename and/or path as a string to the location of the highlighted item, if user pressed 'Ok' or a masked item was selected.
                 Returns the default value if dialog was canceled.

        """

        if not self.is_interactive:
            keyboard = self.get_keyboard_stub()
            value = keyboard.get_next_input()
            return value if value is not None else defaultt

        KodiStub.print_heading(heading)
        try:
            answer = self.read_input("Please enter the path to a file [{}]?".format(defaultt), color=Colors.Yellow)
            return answer if answer != "" else defaultt
        except EOFError:
            return ""


class DialogProgress(KodiStub):
    def __init__(self):
        """ Kodi's progress dialog class (Duh!) """

        self.__message = None

        super(DialogProgress, self).__init__()

    def create(self, heading: str, message: str = "") -> None:
        """
        Create and show a progress dialog.

        :param heading:   dialog heading.
        :param message:   line f text to show.

        It is preferred to only use line1 as it is actually a multi-line text.
        In this case line2 and line3 must be omitted.

        Use update() to update lines and progressbar.

        """

        self.__message = message
        self.print_heading(heading)
        self.print_line(message)

    def update(self, percent: int, message: str = "") -> None:
        """ Updates the progress dialog.

        :param percent:    Percent complete. (0:100)
        :param message:    Message to show.

        """

        self.print_line(
            "{}{}%{}: {}".format(
                Colors.Yellow, percent, Colors.EndColor, message or self.__message))

    def close(self) -> None:
        """ Close the progress dialog. """
        self.print_line("=" * 120, color=Colors.Yellow)

    def iscanceled(self) -> bool:
        """ Checks progress is canceled. """
        return False


# noinspection PyArgumentList
class DialogProgressBG(KodiStub):
    def __init__(self):
        self.__message = None
        super(DialogProgressBG, self).__init__()

    def create(self, heading: str, message: str = "") -> None:
        """
        Create and show a progress background dialog.

        :param heading:   dialog heading.
        :param message:   line f text to show.

        It is preferred to only use line1 as it is actually a multi-line text.
        In this case line2 and line3 must be omitted.

        Use update() to update lines and progressbar.

        """

        self.__message = message
        self.print_heading(heading, align_right=True)
        self.print_line(message)

    def update(self, percent: int, heading: str = "", message: str = "") -> None:
        """ Updates the progress dialog.

        :param percent:    Percent complete. (0:100)
        :param heading:    Dialog heading.
        :param message:    Message to show.

        """

        if heading:
            self.print_line(
                "{}{}%: {}{} - {}".format(
                    Colors.Yellow, percent, heading, Colors.EndColor, message or self.__message))
        else:
            self.print_line(
                "{}{}%{}: {}".format(
                    Colors.Yellow, percent, Colors.EndColor, message or self.__message))

    def close(self) -> None:
        """ Close the progress dialog. """
        self.print_line("=" * 120, color=Colors.Yellow)

    # noinspection PyPep8Naming
    def isFinished(self) -> bool:
        """ Checks progress is finished. """
        return False
