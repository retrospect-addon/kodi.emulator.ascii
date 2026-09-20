import unittest
from unittest.mock import patch

import xbmc
import xbmcgui
from sakee.stub import KodiStub


class XbmcGuiTest(unittest.TestCase):

    def test_dialog_input(self):
        text = "This is a test"
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(text)

        dlg = xbmcgui.Dialog()
        value = dlg.input('Heading')
        self.assertEqual(text, value)

    def test_dialog_input_empty(self):
        text = "This is a default value"
        dlg = xbmcgui.Dialog()
        value = dlg.input('Heading', defaultt=text)
        self.assertEqual(text, value)

    def test_dialog_numeric(self):
        text = "1234"
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(text)

        dlg = xbmcgui.Dialog()
        value = dlg.numeric(0, 'Heading', text)
        self.assertEqual(text, value)

    def test_dialog_numeric_empty(self):
        text = "5555"
        dlg = xbmcgui.Dialog()
        value = dlg.numeric(0, 'Heading', defaultt=text)
        self.assertEqual(text, value)

    def test_dialog_browse_single(self):
        default_filename = '/tmp/default'

        dlg = xbmcgui.Dialog()
        value = dlg.browseSingle(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertEqual(default_filename, value)

        entered_filename = '/tmp/entered'
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(entered_filename)

        dlg = xbmcgui.Dialog()
        value = dlg.browseSingle(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertEqual(entered_filename, value)

    def test_dialog_browse_multiple(self):
        default_filename = '/tmp/default'

        dlg = xbmcgui.Dialog()
        value = dlg.browseMultiple(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertListEqual([default_filename], value)

        entered_filename = '/tmp/entered'
        kb = xbmc.Keyboard()
        stub = kb.get_keyboard_stub()
        stub.add_input(entered_filename)

        dlg = xbmcgui.Dialog()
        value = dlg.browseMultiple(0, 'Heading', shares='local', defaultt=default_filename)
        self.assertListEqual([entered_filename], value)

    def test_list_item_path(self):
        path = "https://test/path"
        item = xbmcgui.ListItem(path=path)
        self.assertEqual(path, item.getPath())
        self.assertEqual(path, item.getProperty("path"))

    def test_video_metadata_matches_legacy_output(self):
        item = xbmcgui.ListItem("Episode")
        tag = item.getVideoInfoTag()
        self.assertIsInstance(tag, xbmc.InfoTagVideo)
        self.assertIs(tag, item.getVideoInfoTag())
        tag.setTitle("Episode title")
        tag.setMediaType("episode")
        tag.setYear(2026)
        tag.setDuration(120)
        genres = ["Drama", "Comedy"]
        tag.setGenres(genres)
        genres.append("Not part of the tag")
        tag.setPlot("Episode plot")
        tag.setTvShowTitle("Series")
        tag.setSeason(2)
        tag.setEpisode(3)
        tag.setFirstAired("2026-09-20")
        tag.setTrackNumber(4)
        item.setDateTime("2026-09-20")

        legacy = xbmcgui.ListItem("Episode")
        legacy.setInfo("video", {
            "Title": "Episode title", "mediatype": "episode", "Year": 2026,
            "Duration": 120, "Genre": ["Drama", "Comedy"], "Plot": "Episode plot",
            "TVShowTitle": "Series", "Season": 2, "Episode": 3,
            "Aired": "2026-09-20", "TrackNumber": 4, "Date": "2026-09-20",
        })
        with patch.object(KodiStub, "is_verbose", True):
            self.assertEqual(str(legacy), str(item))
        self.assertEqual("2026-09-20", item.getDateTime())

    def test_music_metadata_matches_legacy_output(self):
        item = xbmcgui.ListItem("Song")
        tag = item.getMusicInfoTag()
        self.assertIsInstance(tag, xbmc.InfoTagMusic)
        self.assertIs(tag, item.getMusicInfoTag())
        tag.setTitle("Song title")
        tag.setMediaType("song")
        tag.setYear(2025)
        tag.setDuration(90)
        tag.setGenres(["Classical"])
        tag.setTrack(5)
        tag.setArtist("Performer A / Performer B")
        tag.setAlbumArtist("Composer")

        legacy = xbmcgui.ListItem("Song")
        legacy.setInfo("music", {
            "Title": "Song title", "mediatype": "song", "Year": 2025,
            "Duration": 90, "Genre": ["Classical"], "TrackNumber": 5,
            "Artist": "Performer A / Performer B", "AlbumArtist": "Composer",
        })
        with patch.object(KodiStub, "is_verbose", True):
            self.assertEqual(str(legacy), str(item))

    def test_standalone_info_tags(self):
        for tag_type in (xbmc.InfoTagVideo, xbmc.InfoTagMusic):
            with self.subTest(tag_type=tag_type):
                tag = tag_type(offscreen=True)
                other = tag_type()
                tag.setTitle("Standalone title")
                self.assertEqual("Standalone title", tag.getTitle())
                self.assertEqual("", other.getTitle())

    def test_legacy_metadata_is_visible_to_info_tag(self):
        item = xbmcgui.ListItem()
        tag = item.getVideoInfoTag()
        item.setInfo("video", {"Title": "Legacy title"})
        self.assertEqual("Legacy title", tag.getTitle())
        tag.setTitle("New title")
        self.assertEqual("New title", item.getVideoInfoTag().getTitle())

    def test_metadata_is_attached_to_each_item(self):
        first = xbmcgui.ListItem()
        second = xbmcgui.ListItem()
        first.getVideoInfoTag().setTitle("Only the first item")
        first.setDateTime("2026-09-20T12:30:00Z")
        self.assertIsNot(first.getVideoInfoTag(), second.getVideoInfoTag())
        self.assertIsNot(first.getMusicInfoTag(), second.getMusicInfoTag())
        self.assertEqual("", second.getDateTime())
        with patch.object(KodiStub, "is_verbose", True):
            self.assertNotIn("Only the first item", str(second))
            self.assertNotIn("2026-09-20", str(second))
