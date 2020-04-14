# SPDX-License-Identifier: GPL-3.0

from xbmcgui import ListItem
from stub import KodiStub
from colors import Colors


SORT_METHOD_ALBUM = 14
SORT_METHOD_ALBUM_IGNORE_THE = 15
SORT_METHOD_ARTIST = 11
SORT_METHOD_ARTIST_IGNORE_THE = 13
SORT_METHOD_BITRATE = 43
SORT_METHOD_CHANNEL = 41
SORT_METHOD_COUNTRY = 17
SORT_METHOD_DATE = 3
SORT_METHOD_DATEADDED = 21
SORT_METHOD_DATE_TAKEN = 44
SORT_METHOD_DRIVE_TYPE = 6
SORT_METHOD_DURATION = 8
SORT_METHOD_EPISODE = 24
SORT_METHOD_FILE = 5
SORT_METHOD_FULLPATH = 35
SORT_METHOD_GENRE = 16
SORT_METHOD_LABEL = 1
SORT_METHOD_LABEL_IGNORE_FOLDERS = 36
SORT_METHOD_LABEL_IGNORE_THE = 2
SORT_METHOD_LASTPLAYED = 37
SORT_METHOD_LISTENERS = 39
SORT_METHOD_MPAA_RATING = 31
SORT_METHOD_NONE = 0
SORT_METHOD_PLAYCOUNT = 38
SORT_METHOD_PLAYLIST_ORDER = 23
SORT_METHOD_PRODUCTIONCODE = 28
SORT_METHOD_PROGRAM_COUNT = 22
SORT_METHOD_SIZE = 4
SORT_METHOD_SONG_RATING = 29
SORT_METHOD_SONG_USER_RATING = 30
SORT_METHOD_STUDIO = 33
SORT_METHOD_STUDIO_IGNORE_THE = 34
SORT_METHOD_TITLE = 9
SORT_METHOD_TITLE_IGNORE_THE = 10
SORT_METHOD_TRACKNUM = 7
SORT_METHOD_UNSORTED = 40
SORT_METHOD_VIDEO_RATING = 19
SORT_METHOD_VIDEO_RUNTIME = 32
SORT_METHOD_VIDEO_SORT_TITLE = 26
SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE = 27
SORT_METHOD_VIDEO_TITLE = 25
SORT_METHOD_VIDEO_USER_RATING = 20
SORT_METHOD_VIDEO_YEAR = 18

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

# noinspection PyUnresolvedReferences
__handle_info = dict()  # type: dict[int, dict]


# noinspection PyUnusedLocal,PyPep8Naming
def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=0):  # NOSONAR
    """ Callback function to pass directory contents back to Kodi.

    :param int handle:              Handle the plugin was started with.
    :param str url:                 Url of the entry. would be plugin:// for another virtual directory
    :param ListItem listitem:       Item to add.
    :param isFolder:                True=folder / False=not a folder(default).
    :param int totalItems:          Total number of items that will be passed.(used for progressbar)

    :return: Returns a bool for successful completion.
    :rtype: bool

    NOTE: You can use the above as keywords for arguments and skip certain optional arguments.
          Once you use a keyword, all following arguments require the keyword.

    """

    if isFolder:
        print("*F: %s [%s]" % (KodiStub.replace_colors(str(listitem)), url))
    else:
        print("*V: %s [%s]" % (KodiStub.replace_colors(str(listitem)), url))

    handle_info = __handle_info.get(handle, dict())
    handle_info["count"] = handle_info.get("count", 0) + 1
    __handle_info[handle] = handle_info
    return True


# noinspection PyUnusedLocal,PyPep8Naming
def addDirectoryItems(handle, items, totalItems=0):  # NOSONAR
    """ Callback function to pass directory contents back to Kodi as a list.

    :param int handle:                          Handle the plugin was started with.
    :param list[(str, ListItem, bool)] items:   List of (url, listitem[, isFolder]) as a tuple to add.
    :param int totalItems:                      Total number of items that will be
                                                 passed. (used for progressbar)

    :return: Returns a bool for successful completion.
    :rtype: bool

    NOTE: Large lists benefit over using the standard addDirectoryItem(). You may call this more
          than once to add items in chunks.

    """

    result = True
    for item in items:
        url, item, is_folder = item
        result = result and addDirectoryItem(handle, url, item, is_folder, totalItems)

    return result


# noinspection PyPep8Naming,PyUnusedLocal
def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):  # NOSONAR
    """ Callback function to tell Kodi that the end of the directory listing in a virtual
    Python folder module is reached.

    :param int handle:      Handle the plugin was started with.
    :param bool succeeded:  True=script completed successfully(Default)/False=Script did not.
    :param updateListing:   True=this folder should update the current listing/False=Folder
                             is a subfolder(Default).
    :param cacheToDisc:     True=Folder will cache if extended time(default)/False=this folder
                             will never cache to disc.

    """

    handle_info = __handle_info.get(handle, dict())
    handle_info["update_listing"] = updateListing
    handle_info["cache_to_disc"] = cacheToDisc
    handle_info["succeeded"] = succeeded
    __handle_info[handle] = handle_info

    KodiStub.print_heading(
        "End of Folder (items={},success={},content={},sort={},cache={},update={})".format(
            handle_info.get("count", 0),
            succeeded,
            handle_info.get("content", "not-set"),
            "+".join([str(i) for i in handle_info.get("sort_methods", [])]),
            cacheToDisc,
            updateListing
        ), align_right=True)


# noinspection PyPep8Naming,PyUnusedLocal
def addSortMethod(handle, sortMethod, label2Mask="%D"):  # NOSONAR
    """ Adds a sorting method for the media list.

    :param int handle:      Handle the plugin was started with.
    :param int sortMethod:  See available sort methods at the bottom (or see SortFileItem.h).
    :param str label2Mask:  The label mask to use for the second label. Defaults to %D
    :return:

    softMethod can have: SORT_METHOD_NONE, SORT_METHOD_LABEL, SORT_METHOD_LABEL_IGNORE_THE,
    SORT_METHOD_DATE, SORT_METHOD_SIZE, SORT_METHOD_FILE, SORT_METHOD_DRIVE_TYPE,
    SORT_METHOD_TRACKNUM, SORT_METHOD_DURATION, SORT_METHOD_TITLE, SORT_METHOD_TITLE_IGNORE_THE,
    SORT_METHOD_ARTIST, SORT_METHOD_ARTIST_IGNORE_THE, SORT_METHOD_ALBUM,
    SORT_METHOD_ALBUM_IGNORE_THE, SORT_METHOD_GENRE, xbmcplugin.SORT_SORT_METHOD_VIDEO_YEAR,
    SORT_METHOD_YEAR, SORT_METHOD_VIDEO_RATING, SORT_METHOD_PROGRAM_COUNT,
    SORT_METHOD_PLAYLIST_ORDER, SORT_METHOD_EPISODE, SORT_METHOD_VIDEO_TITLE,
    SORT_METHOD_VIDEO_SORT_TITLE, SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE,
    SORT_METHOD_PRODUCTIONCODE, SORT_METHOD_SONG_RATING, SORT_METHOD_MPAA_RATING,
    SORT_METHOD_VIDEO_RUNTIME, SORT_METHOD_STUDIO, SORT_METHOD_STUDIO_IGNORE_THE,
    SORT_METHOD_UNSORTED, SORT_METHOD_BITRATE, SORT_METHOD_LISTENERS, SORT_METHOD_COUNTRY,
    SORT_METHOD_DATEADDED, SORT_METHOD_FULLPATH, SORT_METHOD_LABEL_IGNORE_FOLDERS,
    SORT_METHOD_LASTPLAYED, SORT_METHOD_PLAYCOUNT, SORT_METHOD_CHANNEL, SORT_METHOD_DATE_TAKEN,
    SORT_METHOD_VIDEO_USER_RATING, SORT_METHOD_SONG_USER_RATING

    label2Mask applies to: SORT_METHOD_NONE, SORT_METHOD_UNSORTED, SORT_METHOD_VIDEO_TITLE,
        SORT_METHOD_TRACKNUM, SORT_METHOD_FILE, SORT_METHOD_TITLE, SORT_METHOD_TITLE_IGNORE_THE,
        SORT_METHOD_LABEL, SORT_METHOD_LABEL_IGNORE_THE, SORT_METHOD_VIDEO_SORT_TITLE,
        SORT_METHOD_FULLPATH, SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE,
        SORT_METHOD_LABEL_IGNORE_FOLDERS, SORT_METHOD_CHANNEL

    """

    KodiStub.print_line("{}>{} Added sortmethod: {:02d} - {}".format(
        Colors.Yellow, Colors.EndColor, sortMethod, __sort_method_names.get(sortMethod, "<unknown")))

    handle_info = __handle_info.get(handle, dict())
    if "sort_methods" not in handle_info:
        handle_info["sort_methods"] = []
    handle_info["sort_methods"].append(sortMethod)
    __handle_info[handle] = handle_info


# noinspection PyPep8Naming,PyUnusedLocal
def setContent(handle, content):  # NOSONAR
    """ Sets the plugins content.

    :param int handle:  Handle the plugin was started with.
    :param str content: Content type (eg. movies)


    Available content strings: files, songs, artists, albums, movies, tvshows, episodes,
        musicvideos, videos, images, games,

    Remarks: Use videos for all videos which do not apply to the more specific mentioned ones like
        "movies", "episodes" etc. A good example is youtube.

    """

    handle_info = __handle_info.get(handle, dict())
    handle_info["content"] = content
    __handle_info[handle] = handle_info


# noinspection PyPep8Naming,PyUnusedLocal
def setResolvedUrl(handle, succeeded, listitem):  # NOSONAR
    """ Callback function to tell Kodi that the file plugin has been resolved to a url

    :param int handle:          Handle the plugin was started with.
    :param bool succeeded:      True=script completed successfully/False=Script did not.
    :param ListItem listitem:   Item the file plugin resolved to for playback.

    """

    if succeeded:
        KodiStub.print_line("Item resolved to: {}".format(listitem), color=Colors.Blue)
    else:
        KodiStub.print_line("Item failed to resolve: {}".format(listitem), color=Colors.Red)


# noinspection PyPep8Naming,PyUnusedLocal
def setPluginCategory(handle, category):  # NOSONAR
    """ Sets the plugins name for skins to display.

    :param int handle:      Handle the plugin was started with.
    :param str category:    Plugins sub category.

    """

    KodiStub.print_line("> {}".format(category), color=Colors.Blue)
