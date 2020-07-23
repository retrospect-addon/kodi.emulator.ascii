# SPDX-License-Identifier: GPL-3.0
from sakee.colors import Colors
from sakee.stub import KodiStub
from xbmc import ListItem


class HandleInfo(object):
    # Mapping from SORT_METHOD_ID to names
    __sort_method_names = {
        0: "SORT_METHOD_NONE",
        1: "SORT_METHOD_LABEL",
        2: "SORT_METHOD_LABEL_IGNORE_THE",
        3: "SORT_METHOD_DATE",
        4: "SORT_METHOD_SIZE",
        5: "SORT_METHOD_FILE",
        6: "SORT_METHOD_DRIVE_TYPE",
        7: "SORT_METHOD_TRACKNUM",
        8: "SORT_METHOD_DURATION",
        9: "SORT_METHOD_TITLE",
        10: "SORT_METHOD_TITLE_IGNORE_THE",
        11: "SORT_METHOD_ARTIST",
        13: "SORT_METHOD_ARTIST_IGNORE_THE",
        14: "SORT_METHOD_ALBUM",
        15: "SORT_METHOD_ALBUM_IGNORE_THE",
        16: "SORT_METHOD_GENRE",
        17: "SORT_METHOD_COUNTRY",
        18: "SORT_METHOD_VIDEO_YEAR",
        19: "SORT_METHOD_VIDEO_RATING",
        20: "SORT_METHOD_VIDEO_USER_RATING",
        21: "SORT_METHOD_DATEADDED",
        22: "SORT_METHOD_PROGRAM_COUNT",
        23: "SORT_METHOD_PLAYLIST_ORDER",
        24: "SORT_METHOD_EPISODE",
        25: "SORT_METHOD_VIDEO_TITLE",
        26: "SORT_METHOD_VIDEO_SORT_TITLE",
        27: "SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE",
        28: "SORT_METHOD_PRODUCTIONCODE",
        29: "SORT_METHOD_SONG_RATING",
        30: "SORT_METHOD_SONG_USER_RATING",
        31: "SORT_METHOD_MPAA_RATING",
        32: "SORT_METHOD_VIDEO_RUNTIME",
        33: "SORT_METHOD_STUDIO",
        34: "SORT_METHOD_STUDIO_IGNORE_THE",
        35: "SORT_METHOD_FULLPATH",
        36: "SORT_METHOD_LABEL_IGNORE_FOLDERS",
        37: "SORT_METHOD_LASTPLAYED",
        38: "SORT_METHOD_PLAYCOUNT",
        39: "SORT_METHOD_LISTENERS",
        40: "SORT_METHOD_UNSORTED",
        41: "SORT_METHOD_CHANNEL",
        43: "SORT_METHOD_BITRATE",
        44: "SORT_METHOD_DATE_TAKEN",
    }

    def __init__(self, handle):
        self.handle = handle
        self.update_listing = False
        self.cache_to_disc = False
        self.succeeded = False
        self.content = "not-set"
        self.sort_methods = set()

        self.__items = []

    def add_item(self, list_item, url, is_folder):
        """ Add a new ListItem object with an url

        :param ListItem list_item:  The ListItem
        :param str url:             The url for the item
        :param bool is_folder:      Indiction whether it is a folder or not

        """

        self.__items.append((list_item, url, is_folder))

    @property
    def count(self):
        """ The number for items in the handle.

        :return: the number for items
        :rtype: int

        """

        return len(self.__items)

    @property
    def items(self):
        """ The current items for the handle

        :return: iterator for the items
        :rtype: list_iterator

        """

        return iter(self.__items)

    def print_handle(self):
        """ Prints the content for this handle """

        KodiStub.print_heading("Listing for handle {}".format(self.handle))

        for listitem, url, is_folder in self.items:
            if is_folder:
                print("*F: %s [%s]" % (KodiStub.replace_colors(str(listitem)), url))
            else:
                print("*V: %s [%s]" % (KodiStub.replace_colors(str(listitem)), url))

        for sort_method in self.sort_methods:
            KodiStub.print_line("{}>{} Added sortmethod: {:02d} - {}".format(
                Colors.Yellow, Colors.EndColor, sort_method,
                HandleInfo.__sort_method_names.get(sort_method, "<unknown")))

        KodiStub.print_heading(
            "End of Folder (items={},success={},content={},sort={},cache={},update={})".format(
                self.count,
                self.succeeded,
                self.content,
                "+".join([str(i) for i in self.sort_methods]),
                self.cache_to_disc,
                self.update_listing
            ), align_right=True)


class PluginHandler(object):
    __handles = dict()

    @staticmethod
    def get_handle_info(handle):
        """ Retrieves the info object for the Handle

        :param int handle:  The handle ID from Kodi

        :rtype: HandleInfo
        :returns: A complete HandleInfo object

        """

        if handle not in PluginHandler.__handles:
            PluginHandler.__handles[handle] = HandleInfo(handle)

        return PluginHandler.__handles[handle]

    @staticmethod
    def close_handle(handle):
        """ Closes a handle and removes it from the pool

        :param int handle:      The handle to close

        """

        if handle not in PluginHandler.__handles:
            return

        del PluginHandler.__handles[handle]
