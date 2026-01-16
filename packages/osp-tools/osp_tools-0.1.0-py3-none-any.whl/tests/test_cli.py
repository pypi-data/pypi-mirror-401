from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from osp.core.device import Device, find, list_music, AUDIO_EXTS, _matches_device
from osp.download.youtube import Downloader, is_youtube, is_playlist


class TestDevice:
    def test_matches_openswim(self):
        assert _matches_device("OpenSwim") is True
        assert _matches_device("OPENSWIM") is True
        assert _matches_device("Shokz") is True
        assert _matches_device("SHOKZ OpenSwim Pro") is True
    
    def test_no_match(self):
        assert _matches_device("USB Drive") is False
        assert _matches_device("Macintosh HD") is False
    
    def test_device_properties(self):
        dev = Device(
            name="OpenSwim",
            path=Path("/Volumes/OpenSwim"),
            total=32 * 1024 * 1024,
            free=16 * 1024 * 1024,
            used=16 * 1024 * 1024,
        )
        assert dev.total_mb == 32.0
        assert dev.free_mb == 16.0
        assert dev.usage_pct == 50.0
    
    def test_list_music_mock(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            (tmp / "song1.mp3").touch()
            (tmp / "song2.wav").touch()
            (tmp / "notes.txt").touch()
            
            dev = Device(name="Test", path=tmp, total=1000, free=500, used=500)
            files = list_music(dev)
            
            assert len(files) == 2
            names = {f.name for f in files}
            assert "song1.mp3" in names
            assert "song2.wav" in names
            assert "notes.txt" not in names


class TestYoutube:
    def test_is_youtube_valid(self):
        assert is_youtube("https://youtube.com/watch?v=abc123") is True
        assert is_youtube("https://www.youtube.com/watch?v=def456") is True
        assert is_youtube("https://youtu.be/xyz789") is True
        assert is_youtube("https://youtube.com/shorts/short1") is True
    
    def test_is_youtube_invalid(self):
        assert is_youtube("https://vimeo.com/123") is False
        assert is_youtube("https://spotify.com/track/abc") is False
        assert is_youtube("not a url") is False
    
    def test_is_playlist(self):
        assert is_playlist("https://youtube.com/playlist?list=PLabc") is True
        assert is_playlist("https://youtube.com/watch?v=abc&list=PLdef") is True
        assert is_playlist("https://youtube.com/watch?v=abc") is False
    
    def test_downloader_init(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dl = Downloader(tmpdir, fmt="mp3", quality="320")
            assert dl.out_dir == Path(tmpdir)
            assert dl.fmt == "mp3"
            assert dl.quality == "320"


class TestCLI:
    def test_import(self):
        from osp.cli.main import cli, device, list_cmd, download, sync
        assert cli is not None
    
    def test_wave_bar(self):
        from osp.cli.main import WaveBar
        bar = WaveBar()
        assert bar.bar_width == 35


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
