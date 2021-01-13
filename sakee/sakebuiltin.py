# SPDX-License-Identifier: GPL-3.0
import os
import re

from sakee import addoninfo


class BuiltinApi(object):
    __ADDON_INFO = None

    def __init__(self):
        """ Initialise the Built-in API Implementation. """
        if BuiltinApi.__ADDON_INFO is None:
            BuiltinApi.__ADDON_INFO = addoninfo.get_add_on_info_from_calling_script()

    def handle(self, function):
        """ Handle the Built-in function.

        :param obj function:            The built-in function call.

        """
        method, params = re.search(r'^([^\(\s]*)(?:\((.*?)\))?', function).groups()
        if not method:
            raise ValueError('Invalid function: %s' % function)

        try:
            # Replace . with _ since we have function-names with dots in it.
            method_reference = getattr(self, method.replace('.', '_'))
        except AttributeError:
            raise NotImplementedError

        if params:
            method_reference(*params.split(','))
        else:
            method_reference()

    @staticmethod
    def _run_plugin_uri(plugin_uri):
        """ Execute a plugin:// uri in the background. """

        def run_background(entrypoint, *args):
            import sys
            orig_sys_argv = sys.argv
            sys.argv = args
            with open(entrypoint, 'rb') as fdesc:
                try:
                    exec(compile(fdesc.read(), entrypoint, 'exec'), {
                        '__name__': '__main__',
                        '__file__': entrypoint,
                    })
                except SystemExit:
                    # Continue in case the Add-on does an exit()
                    pass
            sys.argv = orig_sys_argv

        # Find the Add-on that belongs to this plugin://-uri.
        addon, path, params = re.search(r'^plugin://([^?\s/]*)([^?\s]*)(\?.*)?', plugin_uri).groups()

        try:
            addon_info = addoninfo.read_addon_xml(os.path.join(BuiltinApi.__ADDON_INFO.kodi_home_path, 'addons', addon, 'addon.xml'))
        except FileNotFoundError:
            raise ValueError('Addon %s not found' % addon)

        addon_entry = os.path.join(BuiltinApi.__ADDON_INFO.kodi_home_path, 'addons', addon, addon_info.get('pluginsource'))
        addon_route = 'plugin://' + addon + path
        addon_params = params or ''

        import threading
        background = threading.Thread(target=run_background, args=(addon_entry, addon_route, '-1', addon_params, 'resume:false'))
        background.start()

    @staticmethod
    def RunPlugin(plugin):
        """ Runs the plugin. Full path must be specified. Does not work for folder plugins.

        :param str plugin:              plugin:// URL to script.

        """
        BuiltinApi._run_plugin_uri(plugin)

    @staticmethod
    def PlayMedia(media):
        """ Plays the media. This can be a playlist, music, or video file, directory, plugin or a url.
        The optional parameter ",isdir" can be used for playing a directory. ",1" will start the media without switching to fullscreen.
        If media is a playlist, you can use playoffset=xx where xx is the position to start playback from.
        Set "resume" to force resuming.
        Set "noresume" to force not resuming.

        :param str media:               Media to play, this can be a playlist, music, or video file, directory, plugin or a url.

        """
        import xbmc

        if media.startswith('plugin://'):
            # Play plugin://-url
            BuiltinApi._run_plugin_uri(media)

        else:
            # Play normal file or url
            player = xbmc.Player()
            player.play(media)

    @staticmethod
    def PlayerControl(command):
        """ Allows control of music and videos.
        Play will either pause, resume, or stop ffwding or rewinding.
        Random toggles random playback and Repeat cycles through the repeat modes (these both take an optional second parameter, Notify, that notifies the user
        of the new state).
        Partymode(music/video) toggles the appropriate partymode, defaults to music if no parameter is given, besides the default music or video partymode
        you can also pass a path to a custom smartplaylist (.xsp) as parameter.

        Reset only applies to games and will reset the currently playing game.

        :param str command:             The command may be one of Play, Stop, Forward, Rewind, Next, Previous, BigSkipForward, BigSkipBackward,
                                        SmallSkipForward, SmallSkipBackward, FrameAdvance(#), TempoUp, TempoDown, Tempo(value), Random, RandomOn, RandomOff,
                                        Repeat, RepeatOne, RepeatAll, RepeatOff, Partymode(music) or Partymode(video) or Partymode(path to .xsp file) or Reset.

        """
        import xbmc
        player = xbmc.Player()

        if command == 'Play':
            player.pause()
        elif command == 'Stop':
            player.stop()
        elif command == 'Forward':
            pass  # Not implemented
        elif command == 'Rewind':
            pass  # Not implemented
        elif command == 'Next':
            player.playnext()
        elif command == 'Previous':
            player.playprevious()
        elif command == 'BigSkipForward':
            player.seekTime(player.getTime() + 600)  # timeseekforwardbig
        elif command == 'BigSkipBackward':
            player.seekTime(player.getTime() - 600)  # timeseekbackwardbig
        elif command == 'SmallSkipForward':
            player.seekTime(player.getTime() + 30)  # timeseekforward
        elif command == 'SmallSkipBackward':
            player.seekTime(player.getTime() - 30)  # timeseekbackward
        elif command.startswith('FrameAdvance('):
            pass  # Not implemented
        elif command == 'TempoUp':
            pass  # Not implemented
        elif command == 'TempoDown':
            pass  # Not implemented
        elif command.startswith('Tempo('):
            pass  # Not implemented
        elif command == 'Random':
            pass  # Not implemented
        elif command == 'RandomOn':
            pass  # Not implemented
        elif command == 'RandomOff':
            pass  # Not implemented
        elif command == 'Repeat':
            pass  # Not implemented
        elif command == 'RepeatOne':
            pass  # Not implemented
        elif command == 'RepeatAll':
            pass  # Not implemented
        elif command == 'RepeatOff':
            pass  # Not implemented
        elif command.startswith('Partymode('):
            pass  # Not implemented
        else:
            raise ValueError('Unknown command %s', command)
