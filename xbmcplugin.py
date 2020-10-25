# SPDX-License-Identifier: GPL-3.0

from sakee.colors import Colors
from sakee.internalplayer import KodiInteralPlayer
from sakee.pluginhandler import PluginHandler
from sakee.stub import KodiStub
from xbmcgui import ListItem

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

    handle_info = PluginHandler.get_handle_info(handle)
    handle_info.add_item(listitem, url, isFolder)
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

    handle_info = PluginHandler.get_handle_info(handle)
    handle_info.update_listing = updateListing
    handle_info.cache_to_disc = cacheToDisc
    handle_info.succeeded = succeeded
    handle_info.print_handle()
    PluginHandler.close_handle(handle)

    # In case there was something playing force to stop it now.
    KodiInteralPlayer.instance().stop_playback(force=True)


# noinspection PyPep8Naming,PyUnusedLocal
def addSortMethod(handle, sortMethod, labelMask="", label2Mask="%D"):  # NOSONAR
    """ Adds a sorting method for the media list.

    :param int handle:      Handle the plugin was started with.
    :param int sortMethod:  See available sort methods at the bottom (or see SortFileItem.h).
    :param str labelMask:   The label mask to use for the first label.
    :param str label2Mask:  The label mask to use for the second label. Defaults to %D
    :return:

    sortMethod can have: SORT_METHOD_NONE, SORT_METHOD_LABEL, SORT_METHOD_LABEL_IGNORE_THE,
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

    labelMask applies to:
        SORT_METHOD_TRACKNUM        - Defaults to [%N. ]%T)
        SORT_METHOD_EPISODE         - Defaults to %H. %T
        SORT_METHOD_PRODUCTIONCODE  - Defaults to %H. %T
        All other sort methods      - Defaults to %T

    label2Mask applies to:
        SORT_METHOD_NONE, SORT_METHOD_UNSORTED, SORT_METHOD_VIDEO_TITLE, SORT_METHOD_TRACKNUM,
        SORT_METHOD_FILE, SORT_METHOD_TITLE, SORT_METHOD_TITLE_IGNORE_THE, SORT_METHOD_LABEL,
        SORT_METHOD_LABEL_IGNORE_THE, SORT_METHOD_VIDEO_SORT_TITLE, SORT_METHOD_FULLPATH,
        SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE, SORT_METHOD_LABEL_IGNORE_FOLDERS,
        SORT_METHOD_CHANNEL         - All default to "%D"

    Available metadata masks:

     * %A - Artist
     * %B - Album
     * %C - Programs count
     * %D - Duration
     * %E - episode number
     * %F - FileName
     * %G - Genre
     * %H - season*100+episode
     * %I - Size
     * %J - Date
     * %K - Movie/Game title
     * %L - existing Label
     * %M - number of episodes
     * %N - Track Number
     * %O - mpaa rating
     * %P - production code
     * %Q - file time
     * %R - Movie rating
     * %S - Disc Number
     * %T - Title
     * %U - studio
     * %V - Playcount
     * %W - Listeners
     * %X - Bitrate
     * %Y - Year
     * %Z - tvshow title
     * %a - Date Added
     * %b - Total number of discs
     * %c - Relevance - Used for actors' appearances
     * %d - Date and Time
     * %e - Original release date
     * %f - bpm
     * %p - Last Played
     * %r - User Rating
     * %t - Date Taken (suitable for Pictures)

    """

    handle_info = PluginHandler.get_handle_info(handle)
    handle_info.sort_methods.add(sortMethod)


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

    handle_info = PluginHandler.get_handle_info(handle)
    handle_info.content = content


# noinspection PyPep8Naming,PyUnusedLocal
def setResolvedUrl(handle, succeeded, listitem):  # NOSONAR
    """ Callback function to tell Kodi that the file plugin has been resolved to a url

    :param int handle:          Handle the plugin was started with.
    :param bool succeeded:      True=script completed successfully/False=Script did not.
    :param ListItem listitem:   Item the file plugin resolved to for playback.

    """

    if succeeded:
        KodiStub.print_line("Item resolved to: {}".format(listitem), color=Colors.Blue)
        KodiInteralPlayer.instance().play_resolved_item(listitem.getPath(), listitem)
    else:
        KodiStub.print_line("Item failed to resolve: {}".format(listitem), color=Colors.Red)


# noinspection PyPep8Naming,PyUnusedLocal
def setPluginCategory(handle, category):  # NOSONAR
    """ Sets the plugins name for skins to display.

    :param int handle:      Handle the plugin was started with.
    :param str category:    Plugins sub category.

    """

    KodiStub.print_line("> {}".format(category), color=Colors.Blue)
