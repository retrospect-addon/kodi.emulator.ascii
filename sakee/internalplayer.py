# SPDX-License-Identifier: GPL-3.0

import threading

from sakee.stub import KodiStub


class KodiInteralPlayer(KodiStub):  # NOSONAR
    STATUS_INIT = 'init'
    STATUS_STOPPED = 'stopped'
    STATUS_PLAYING = 'playing'
    STATUS_PAUSED = 'paused'
    __kodi_player = None

    @staticmethod
    def instance():
        """ The Kodi player instance

        :return: The stub for the internal Kodi player
        :rtype: KodiInteralPlayer

        """

        if KodiInteralPlayer.__kodi_player is None:
            KodiInteralPlayer.__kodi_player = KodiInteralPlayer()

        return KodiInteralPlayer.__kodi_player

    def __init__(self):
        super(KodiInteralPlayer, self).__init__()

        self.status = KodiInteralPlayer.STATUS_STOPPED
        self.file = None
        self.current_time = 0
        self.total_time = 0

        self._stop_event = threading.Event()

        # Keep track of players
        self.__players = []

        # The play thread
        self.__play_thread = None
        self.__kill_play_thread = False

    # noinspection PyUnusedLocal
    def play_resolved_item(self, path, item):  # NOSONAR
        """ Sets the resolved item to play

        :param str path:
        :param ListItem item:

        """

        self.file = path
        self.play(path)

    def play(self, path):
        self.file = path
        self.status = KodiInteralPlayer.STATUS_INIT
        self.total_time = 5  # 5 seconds
        self._stop_event.clear()

        # Start the playback simulation thread
        self.__play_thread = threading.Thread(target=self.__loop)
        self.__play_thread.start()

    def stop_playback(self, force=False):
        """ Stops playback. If `force=True` no stop events are raised.

        :param bool force:      Force stops the player.

        """

        if self.__play_thread is None:
            return

        if force and self.__play_thread:
            self.__kill_play_thread = True
            return

        self._stop_event.set()
        self.__play_thread.join(2)
        self.__play_thread = None
        self.__kill_play_thread = False

    def register_player(self, player):
        """ Register a xbmc.Player instance

        :param Player player: The player to register

        """

        self.__players.append(player)

    def unregister_player(self, player):
        """ Unregister a xbmc.Player instance

        :param Player player: The player to unregister

        """

        self.__players.remove(player)

    def __loop(self):
        """ Background playback loop. """
        from datetime import timedelta

        for player in self.__players:
            player.onPlayBackStarted()

        while not self._stop_event.wait(1):
            if self.__kill_play_thread:
                return

            KodiStub.print_line(
                'Player: [{status}] {pos}/{total}'.format(
                    status=self.status,
                    pos=timedelta(seconds=self.current_time),
                    total=timedelta(seconds=self.total_time)
                ), verbose=True)

            if self.status == KodiInteralPlayer.STATUS_INIT:
                self.status = KodiInteralPlayer.STATUS_PLAYING
                self.current_time = 0
                for player in self.__players:
                    player.onAVStarted()
                    player.onAVChange()
                continue

            if self.status == KodiInteralPlayer.STATUS_PLAYING:
                self.current_time += 1
                if self.current_time > self.total_time:
                    for player in self.__players:
                        player.stop()

            if self.status == KodiInteralPlayer.STATUS_STOPPED:
                break

        for player in self.__players:
            player.onPlayBackStopped()
