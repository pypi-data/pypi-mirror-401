from __future__ import annotations

import pytest

from osp.download.spotify import (
    Track, Album, Playlist, SpotifyResult,
    detect_type, is_spotify, parse, parse_tracks,
    _parse_track_from_dict,
)


class TestURLDetection:
    def test_track_url(self):
        assert detect_type("https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT") == ("track", "4cOdK2wGLETKBW3PvgPWqT")
    
    def test_album_url(self):
        assert detect_type("https://open.spotify.com/album/4aawyAB9vmqN3uQ7FjRGTy") == ("album", "4aawyAB9vmqN3uQ7FjRGTy")
    
    def test_playlist_url(self):
        assert detect_type("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M") == ("playlist", "37i9dQZF1DXcBWIGoYBM5M")
    
    def test_spotify_uri(self):
        assert detect_type("spotify:track:4cOdK2wGLETKBW3PvgPWqT") == ("track", "4cOdK2wGLETKBW3PvgPWqT")
        assert detect_type("spotify:album:4aawyAB9vmqN3uQ7FjRGTy") == ("album", "4aawyAB9vmqN3uQ7FjRGTy")
    
    def test_invalid_url(self):
        assert detect_type("https://youtube.com/watch?v=abc") == (None, None)
        assert detect_type("not a url") == (None, None)


class TestIsSpotify:
    def test_valid(self):
        assert is_spotify("https://open.spotify.com/track/abc") is True
        assert is_spotify("spotify:track:abc") is True
    
    def test_invalid(self):
        assert is_spotify("https://youtube.com") is False
        assert is_spotify("") is False


class TestTrackParsing:
    def test_api_format(self):
        data = {
            "id": "abc123",
            "name": "Test Song",
            "artists": [{"name": "Artist One"}, {"name": "Artist Two"}],
            "duration_ms": 180000,
        }
        track = _parse_track_from_dict(data)
        assert track is not None
        assert track.name == "Test Song"
        assert track.artists == ("Artist One", "Artist Two")
        assert track.duration_ms == 180000
    
    def test_embed_format(self):
        data = {
            "uri": "spotify:track:xyz789",
            "title": "Embed Song",
            "subtitle": "Embed Artist",
            "duration": 200000,
        }
        track = _parse_track_from_dict(data)
        assert track is not None
        assert track.id == "xyz789"
        assert track.name == "Embed Song"
        assert track.artist == "Embed Artist"
        assert track.duration_ms == 200000
    
    def test_empty_data(self):
        assert _parse_track_from_dict({}) is None
        assert _parse_track_from_dict(None) is None


class TestTrackDataclass:
    def test_search_query(self):
        track = Track(id="1", name="Song", artists=("Artist",))
        assert track.search_query() == "Artist - Song"
    
    def test_search_query_with_isrc(self):
        track = Track(id="1", name="Song", artists=("Artist",), isrc="USRC12345678")
        assert track.search_query() == "USRC12345678"
    
    def test_duration_fmt(self):
        track = Track(id="1", name="Song", artists=("Artist",), duration_ms=185000)
        assert track.duration_fmt == "3:05"
    
    def test_artist_str(self):
        track = Track(id="1", name="Song", artists=("A", "B", "C"))
        assert track.artist_str == "A, B, C"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
