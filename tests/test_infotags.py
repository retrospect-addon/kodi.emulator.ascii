# SPDX-License-Identifier: GPL-3.0

import unittest
from datetime import datetime

import xbmc
import xbmcgui

# Python-facing getters/setters from Kodi's InfoTagVideo and InfoTagMusic references.
VIDEO_METHODS = """
getDbId getDirector getDirectors getWritingCredits getWriters getGenre getGenres getTagLine
getPlotOutline getPlot getPictureURL getTitle getTVShowTitle getMediaType getVotes getVotesAsInt
getCast getActors getFile getPath getFilenameAndPath getIMDBNumber getSeason getEpisode getYear
getRating getUserRating getPlayCount getLastPlayed getLastPlayedAsW3C getOriginalTitle
getOriginalLanguage getPremiered getPremieredAsW3C getFirstAired getFirstAiredAsW3C getTrailer
getArtist getAlbum getTrack getDuration getResumeTime getResumeTimeTotal getUniqueID setUniqueID
setUniqueIDs setDbId setYear setEpisode setSeason setSortEpisode setSortSeason setEpisodeGuide
setTop250 setSetId setTrackNumber setRating setRatings setUserRating setPlaycount setMpaa
setPlot setPlotOutline setTitle setOriginalTitle setOriginalLanguage setSortTitle setTagLine
setTvShowTitle setTvShowStatus setGenres setCountries setDirectors setStudios setWriters
setDuration setPremiered setSet setSetOverview setTags setVideoAssetTitle setProductionCode
setFirstAired setLastPlayed setAlbum setVotes setTrailer setPath setFilenameAndPath
setIMDBNumber setDateAdded setMediaType setShowLinks setArtists setCast setResumePoint
setAvailableFanart
""".split()
MUSIC_METHODS = """
getDbId getURL getTitle getMediaType getArtist getAlbum getAlbumArtist getGenre getGenres
getDuration getYear getRating getUserRating getTrack getDisc getReleaseDate getListeners
getPlayCount getLastPlayed getLastPlayedAsW3C getComment getLyrics getMusicBrainzTrackID
getMusicBrainzArtistID getMusicBrainzAlbumID getMusicBrainzReleaseGroupID
getMusicBrainzAlbumArtistID getSongVideoURL setDbId setURL setMediaType setTrack setDisc
setDuration setYear setReleaseDate setListeners setPlayCount setGenres setAlbum setArtist
setAlbumArtist setTitle setRating setUserRating setLyrics setLastPlayed setMusicBrainzTrackID
setMusicBrainzArtistID setMusicBrainzAlbumID setMusicBrainzReleaseGroupID
setMusicBrainzAlbumArtistID setComment setSongVideoURL
""".split()


class InfoTagTest(unittest.TestCase):
    def test_documented_api_is_available(self):
        for tag_type, methods in ((xbmc.InfoTagVideo, VIDEO_METHODS),
                                  (xbmc.InfoTagMusic, MUSIC_METHODS)):
            for method in methods:
                with self.subTest(tag=tag_type.__name__, method=method):
                    self.assertTrue(callable(getattr(tag_type, method, None)))

    def test_shared_dictionary_in_both_directions(self):
        for tag_type in (xbmc.InfoTagVideo, xbmc.InfoTagMusic):
            with self.subTest(tag=tag_type.__name__):
                info = {}
                tag = tag_type(info=info)
                tag.setTitle("Title")
                self.assertEqual("Title", info["Title"])
                info["Title"] = "Changed externally"
                self.assertEqual("Changed externally", tag.getTitle())
                self.assertEqual("", tag_type().getTitle())

    def test_common_metadata_round_trips(self):
        values = [
            ("setTitle", "getTitle", "Title"),
            ("setMediaType", "getMediaType", "movie"),
            ("setYear", "getYear", 2026),
            ("setDuration", "getDuration", 3600),
            ("setGenres", "getGenres", ["Drama", "Comedy"]),
            ("setAlbum", "getAlbum", "Album"),
            ("setUserRating", "getUserRating", 9),
        ]
        for tag_type in (xbmc.InfoTagVideo, xbmc.InfoTagMusic):
            tag = tag_type()
            for setter, getter, value in values:
                with self.subTest(tag=tag_type.__name__, setter=setter):
                    getattr(tag, setter)(value)
                    self.assertEqual(value, getattr(tag, getter)())

    def test_video_metadata_round_trips(self):
        tag = xbmc.InfoTagVideo()
        values = [
            ("setDbId", "getDbId", 42),
            ("setPlot", "getPlot", "Plot"),
            ("setPlotOutline", "getPlotOutline", "Outline"),
            ("setTvShowTitle", "getTVShowTitle", "Series"),
            ("setSeason", "getSeason", 2),
            ("setEpisode", "getEpisode", 3),
            ("setTrackNumber", "getTrack", 4),
            ("setPlaycount", "getPlayCount", 5),
            ("setDirectors", "getDirectors", ["Director A", "Director B"]),
            ("setWriters", "getWriters", ["Writer A", "Writer B"]),
            ("setTagLine", "getTagLine", "Tagline"),
            ("setOriginalTitle", "getOriginalTitle", "Original title"),
            ("setOriginalLanguage", "getOriginalLanguage", "nl"),
            ("setTrailer", "getTrailer", "https://example.com/trailer"),
            ("setArtists", "getArtist", ["Artist A", "Artist B"]),
            ("setPath", "getPath", "/videos/"),
            ("setFilenameAndPath", "getFilenameAndPath", "/videos/movie.mkv"),
        ]
        for setter, getter, value in values:
            with self.subTest(setter=setter):
                getattr(tag, setter)(value)
                self.assertEqual(value, getattr(tag, getter)())
        self.assertEqual("Director A / Director B", tag.getDirector())
        self.assertEqual("Writer A / Writer B", tag.getWritingCredits())

    def test_music_metadata_round_trips(self):
        tag = xbmc.InfoTagMusic()
        tag.setDbId(42, "song")
        self.assertEqual(42, tag.getDbId())
        self.assertEqual("song", tag.getMediaType())
        values = [
            ("setURL", "getURL", "https://example.com/song"),
            ("setArtist", "getArtist", "Artist A / Artist B"),
            ("setAlbumArtist", "getAlbumArtist", "Album artist"),
            ("setTrack", "getTrack", 2),
            ("setDisc", "getDisc", 3),
            ("setReleaseDate", "getReleaseDate", "2026-09-20"),
            ("setListeners", "getListeners", 100),
            ("setPlayCount", "getPlayCount", 5),
            ("setComment", "getComment", "Comment"),
            ("setLyrics", "getLyrics", "Lyrics"),
            ("setMusicBrainzTrackID", "getMusicBrainzTrackID", "track-id"),
            ("setMusicBrainzArtistID", "getMusicBrainzArtistID", ["artist-id"]),
            ("setMusicBrainzAlbumID", "getMusicBrainzAlbumID", "album-id"),
            ("setMusicBrainzReleaseGroupID", "getMusicBrainzReleaseGroupID", "release-id"),
            ("setMusicBrainzAlbumArtistID", "getMusicBrainzAlbumArtistID", ["album-artist-id"]),
            ("setSongVideoURL", "getSongVideoURL", "https://example.com/video"),
        ]
        for setter, getter, value in values:
            with self.subTest(setter=setter):
                getattr(tag, setter)(value)
                self.assertEqual(value, getattr(tag, getter)())
        tag.setRating(8.75)
        self.assertEqual(8, tag.getRating())  # Kodi's music getter returns an integer.

    def test_video_ratings_and_votes(self):
        tag = xbmc.InfoTagVideo()
        self.assertEqual(0.0, tag.getRating())
        self.assertEqual(0, tag.getVotesAsInt())
        tag.setRating(8.5, 100, "imdb", True)
        tag.setRating(7.5, 50, "tmdb")
        self.assertEqual(8.5, tag.getRating())
        self.assertEqual(7.5, tag.getRating("tmdb"))
        self.assertEqual("100", tag.getVotes())
        tag.setVotes(101)
        self.assertEqual(101, tag.getVotesAsInt())
        self.assertEqual(50, tag.getVotesAsInt("tmdb"))
        tag.setRatings({"imdb": (9.0, 200), "tmdb": (8.0, 80)}, "tmdb")
        self.assertEqual(8.0, tag.getRating())
        self.assertEqual(80, tag.getVotesAsInt())
        self.assertEqual(0.0, tag.getRating("missing"))

    def test_unique_ids_and_default_id(self):
        tag = xbmc.InfoTagVideo()
        tag.setUniqueID("tt123", "imdb", True)
        tag.setUniqueID("456", "tmdb")
        self.assertEqual("tt123", tag.getIMDBNumber())
        self.assertEqual("456", tag.getUniqueID("tmdb"))
        tag.setUniqueIDs({"imdb": "tt789", "tvdb": "321"}, "tvdb")
        self.assertEqual("321", tag.getUniqueID(""))
        tag.setIMDBNumber("654")
        self.assertEqual("654", tag.getUniqueID("tvdb"))
        self.assertEqual("", tag.getUniqueID("missing"))

    def test_resume_updates_preserve_total_when_omitted(self):
        tag = xbmc.InfoTagVideo()
        self.assertEqual(0.0, tag.getResumeTime())
        self.assertEqual(0.0, tag.getResumeTimeTotal())
        tag.setResumePoint(12.5, 100.0)
        tag.setResumePoint(25.5)
        self.assertEqual(25.5, tag.getResumeTime())
        self.assertEqual(100.0, tag.getResumeTimeTotal())

    def test_cast(self):
        tag = xbmc.InfoTagVideo()
        cast = [xbmc.Actor("A", "Lead"), xbmc.Actor("B", order=1)]
        tag.setCast(cast)
        self.assertEqual(["A", "B"], [actor.getName() for actor in tag.getActors()])
        self.assertEqual("A as Lead\nB", tag.getCast())
        cast.clear()
        self.assertEqual(2, len(tag.getActors()))

    def test_dates(self):
        for tag_type in (xbmc.InfoTagVideo, xbmc.InfoTagMusic):
            tag = tag_type()
            self.assertEqual("", tag.getLastPlayed())
            self.assertEqual("", tag.getLastPlayedAsW3C())
            tag.setLastPlayed("2026-09-20 12:30:45")
            self.assertEqual("2026-09-20T12:30:45", tag.getLastPlayedAsW3C())
            self.assertEqual(datetime(2026, 9, 20, 12, 30, 45).strftime("%x %X"),
                             tag.getLastPlayed())
        tag = xbmc.InfoTagVideo()
        tag.setFirstAired("2026-09-20")
        tag.setPremiered("2025-01-02")
        self.assertEqual("2026-09-20", tag.getFirstAiredAsW3C())
        self.assertEqual("2025-01-02", tag.getPremieredAsW3C())
        self.assertEqual(datetime(2026, 9, 20).strftime("%x"), tag.getFirstAired())
        self.assertEqual(datetime(2025, 1, 2).strftime("%x"), tag.getPremiered())

    def test_list_values_do_not_leak_between_tags(self):
        item = xbmcgui.ListItem()
        tag = item.getVideoInfoTag()
        genres = ["Drama"]
        tag.setGenres(genres)
        genres.append("Comedy")
        tag.getGenres().append("Action")
        self.assertEqual(["Drama"], tag.getGenres())
        self.assertEqual("Drama", tag.getGenre())
        self.assertEqual([], xbmc.InfoTagVideo().getGenres())

    def test_video_setter_only_fields_use_shared_dictionary(self):
        info = {}
        tag = xbmc.InfoTagVideo(info=info)
        values = [
            ("setSortEpisode", "SortEpisode", 2),
            ("setSortSeason", "SortSeason", 3),
            ("setEpisodeGuide", "EpisodeGuide", "guide"),
            ("setTop250", "Top250", 42),
            ("setSetId", "SetId", 12),
            ("setMpaa", "MPAA", "PG"),
            ("setSortTitle", "SortTitle", "Sort title"),
            ("setTvShowStatus", "TVShowStatus", "Continuing"),
            ("setCountries", "Country", ["NL"]),
            ("setStudios", "Studio", ["Studio"]),
            ("setSet", "Set", "Collection"),
            ("setSetOverview", "SetOverview", "Overview"),
            ("setTags", "Tag", ["Tag"]),
            ("setVideoAssetTitle", "VideoAssetTitle", "Edition"),
            ("setProductionCode", "Code", "ABC"),
            ("setDateAdded", "DateAdded", "2026-09-20 12:00:00"),
            ("setShowLinks", "ShowLink", ["Series"]),
            ("setAvailableFanart", "AvailableFanart", [{"image": "https://example.com/fanart"}]),
        ]
        for setter, key, value in values:
            with self.subTest(setter=setter):
                getattr(tag, setter)(value)
                self.assertEqual(value, info[key])
