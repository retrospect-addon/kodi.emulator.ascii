# SPDX-License-Identifier: GPL-3.0

from colors import Colors
from stub import KodiStub

NOTIFICATION_INFO = "info"
NOTIFICATION_WARNING = "warning"
NOTIFICATION_ERROR = "error"


class Dialog(KodiStub):
    def __init__(self):
        super(Dialog, self).__init__()

    def ok(self, heading, message):  # NOSONAR
        """ OK dialog

        The functions permit the call of a dialog of information, a confirmation
        of the user by press from OK required.

        :param str heading:      dialog heading.
        :param str message:      dialog message.

        :return: Returns True if 'Ok' was pressed, else False.
        :rtype: bool

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
    def textviewer(self, heading, text, usemono):
        """ The text viewer dialog can be used to display descriptions, help texts or other larger texts.

        :param str heading:     Dialog heading.
        :param str text:        Dialog text.
        :param bool usemono:    Use a monospace font.

        """

        self.print_heading(heading)
        self.print_line(text)
        self.print_line("=" * 120, color=Colors.Yellow)

    # noinspection PyPep8Naming,PyUnusedLocal
    def multiselect(self, heading, options, autoclose=0, preselect=None, useDetails=False):  # NOSONAR
        """ Show a multi-select dialog.

        :param str heading:                     Dialog heading.
        :param list[string|ListItem] options:   Otions to choose from.
        :param int autoclose:                   Milliseconds to autoclose dialog. (default=do not autoclose)
        :param list[int]|None preselect:        Indexes of items to preselect in list (default: do not preselect any item)
        :param bool useDetails:                 Use detailed list instead of a compact list. (default=false)

        :return: Returns the selected items as a list of indices, or None if cancelled.
        :rtype: list[int]

        """

        self.print_heading(heading)

        selections = []
        for i in range(0, len(options)):
            self.print_line("{} ) {}".format(i, options[i]))
            selections.append(str(i))
        self.print_line("=" * 120, color=Colors.Yellow)
        selections = self.read_input("What items to select (%s)? " % (",".join(selections)), color=Colors.Yellow).lower()
        if not selections:
            return None
        return list(map(lambda index_value: int(index_value), selections.split(",")))

    # noinspection PyPep8Naming,PyUnusedLocal
    def select(self, heading, options, autoclose=0, preselect=None, useDetails=False):  # NOSONAR
        """ Show a select dialog.

        :param str heading:                     Dialog heading.
        :param list[string|ListItem] options:   Otions to choose from.
        :param int autoclose:                   Milliseconds to autoclose dialog. (default=do not autoclose)
        :param int|None preselect:              Indexes of items to preselect in list (default: do not preselect any item)
        :param bool useDetails:                 Use detailed list instead of a compact list. (default=false)

        :return: Returns the selected items as a list of indices, or None if cancelled.
        :rtype: int

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
    def yesno(self, heading, message, nolabel="No", yeslabel="Yes", customlabel=None, autoclose=0):
        """ The Yes / No dialog can be used to inform the user about questions and get the answer.

        :param str heading:             Dialog heading.
        :param str message:             Message to display.
        :param str nolabel:             Label to put on the no button.
        :param str yeslabel:            Label to put on the yes button.
        :param str|None customlabel:    Label to put on the custom button.
        :param autoclose:               Milliseconds to autoclose dialog. (default=do not autoclose)

        :return: Returns True if 'Yes' was pressed, else False.
        :rtype: bool

        """

        self.print_heading(heading)
        question = "{} [{}]{} or [{}]{}:".format(message, yeslabel[0], yeslabel[1:], nolabel[0], nolabel[1:])
        if KodiStub.is_interactive:
            answer = self.read_input(question, Colors.Yellow)
            return yeslabel.lower().startswith(answer.lower())
        else:
            KodiStub.print_line(question, Colors.Yellow)
            return True

    # noinspection PyUnusedLocal
    def notification(self, heading, message, icon=NOTIFICATION_INFO, time=5000, sound=True):
        if icon == NOTIFICATION_WARNING:
            color = Colors.Yellow
        elif icon == NOTIFICATION_ERROR:
            color = Colors.Red
        else:
            color = Colors.White

        self.print_heading(heading, align_right=True, color=color)
        self.print_line(message, color=color)
        self.print_line("=" * 120, color)


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
        self.__properties = {}

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

        return self.__path or ""

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


class DialogProgress(KodiStub):
    def __init__(self):
        """ Kodi's progress dialog class (Duh!) """

        super(DialogProgress, self).__init__()

    def create(self, heading, message=""):
        """
        Create and show a progress dialog.

        :param str heading:       dialog heading.
        :param str|None message:  line #1 multi-line text.

        It is preferred to only use line1 as it is actually a multi-line text.
        In this case line2 and line3 must be omitted.

        Use update() to update lines and progressbar.

        """

        self.print_heading(heading)
        self.print_line(message)

    def update(self, percent, message=""):
        """ Updates the progress dialog.

        :param int percent:         Percent complete. (0:100)
        :param str|None message:    Message to show.

        """

        self.print_line("{}{}%{}: {}".format(Colors.Yellow, percent, Colors.EndColor, message))

    def close(self):
        """ Close the progress dialog. """
        self.print_line("="*120, color=Colors.Yellow)

    def iscanceled(self):
        """ Checks progress is canceled. """
        return False


# noinspection PyArgumentList
class DialogProgressBG(KodiStub):
    def __init__(self):
        super(DialogProgressBG, self).__init__()

    def create(self, heading, message=""):
        """
        Create and show a progress background dialog.

        :param str heading:       dialog heading.
        :param str|None message:  line #1 multi-line text.

        It is preferred to only use line1 as it is actually a multi-line text.
        In this case line2 and line3 must be omitted.

        Use update() to update lines and progressbar.

        """

        self.print_heading(heading, align_right=True)
        self.print_line(message)

    def update(self, percent, heading="", message=""):
        """ Updates the progress dialog.

        :param int percent:         Percent complete. (0:100)
        :param str|None heading:    Dialog heading.
        :param str|None message:    Message to show.

        """

        if heading:
            self.print_line("{}{}%: {}{} - {}".format(Colors.Yellow, percent, heading, Colors.EndColor, message))
        else:
            self.print_line("{}{}%{}: {}".format(Colors.Yellow, percent, Colors.EndColor, message))

    def close(self):
        """ Close the progress dialog. """
        self.print_line("=" * 120, color=Colors.Yellow)

    # noinspection PyPep8Naming
    def isFinished(self):
        """ Checks progress is canceled. """
        return False
