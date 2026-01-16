from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import yt_dlp


class _NullLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


@dataclass
class Progress:
    status: str
    filename: str
    downloaded: int
    total: Optional[int]
    speed: Optional[float]
    eta: Optional[int]

    @property
    def pct(self) -> float:
        if not self.total:
            return 0.0
        return (self.downloaded / self.total) * 100


@dataclass
class Result:
    ok: bool
    path: Optional[Path]
    title: str
    artist: Optional[str]
    duration: int
    error: Optional[str] = None


ProgressHook = Callable[[Progress], None]


YOUTUBE_PATTERNS = [
    r"(https?://)?(www\.)?youtube\.com/watch\?v=",
    r"(https?://)?(www\.)?youtube\.com/playlist\?list=",
    r"(https?://)?(www\.)?youtu\.be/",
    r"(https?://)?(www\.)?youtube\.com/shorts/",
]


def is_youtube(url: str) -> bool:
    return any(re.match(p, url) for p in YOUTUBE_PATTERNS)


def is_playlist(url: str) -> bool:
    return "playlist?list=" in url or "&list=" in url


class Downloader:
    def __init__(self, out_dir: Union[Path, str], fmt: str = "mp3", quality: str = "192"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.fmt = fmt
        self.quality = quality
        self._hook: Optional[ProgressHook] = None

    def get(self, url: str, on_progress: Optional[ProgressHook] = None) -> Result:
        self._hook = on_progress
        opts = self._opts()

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    return Result(False, None, "Unknown", None, 0, "No info extracted")

                if "entries" in info:
                    entries = list(info["entries"])
                    info = entries[0] if entries else None
                    if not info:
                        return Result(False, None, "Unknown", None, 0, "Empty playlist")

                return Result(
                    ok=True,
                    path=self._find_file(info),
                    title=info.get("title", "Unknown"),
                    artist=info.get("artist") or info.get("uploader"),
                    duration=info.get("duration", 0),
                )

        except yt_dlp.utils.DownloadError as e:
            return Result(False, None, "Unknown", None, 0, str(e))
        except Exception as e:
            return Result(False, None, "Unknown", None, 0, f"Error: {e}")

    def get_playlist(self, url: str, on_progress: Optional[ProgressHook] = None) -> List[Result]:
        self._hook = on_progress
        results = []
        opts = self._opts()

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info or "entries" not in info:
                    return results

                for entry in info["entries"]:
                    if not entry:
                        continue
                    video_url = entry.get("webpage_url") or entry.get("url")
                    if video_url:
                        results.append(self.get(video_url, on_progress))
        except Exception as e:
            results.append(Result(False, None, "Playlist Error", None, 0, str(e)))

        return results

    def _opts(self) -> Dict:
        return {
            "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
            "outtmpl": str(self.out_dir / "%(title)s.%(ext)s"),
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": self.fmt, "preferredquality": self.quality},
            ],
            "writethumbnail": False,
            "progress_hooks": [self._on_progress],
            "logger": _NullLogger(),
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "ignoreerrors": True,
            "geo_bypass": True,
            "socket_timeout": 15,
            "retries": 2,
            "extract_flat": False,
            "nocheckcertificate": True,
        }

    def _on_progress(self, data: Dict) -> None:
        if not self._hook:
            return
        self._hook(Progress(
            status=data.get("status", "unknown"),
            filename=data.get("filename", ""),
            downloaded=data.get("downloaded_bytes", 0),
            total=data.get("total_bytes"),
            speed=data.get("speed"),
            eta=data.get("eta"),
        ))

    def _find_file(self, info: Dict) -> Optional[Path]:
        title = info.get("title", "")
        clean = re.sub(r'[<>:"/\\|?*]', "", title).strip().lower()

        for ext in [f".{self.fmt}", ".mp3", ".m4a", ".wav"]:
            for f in self.out_dir.iterdir():
                if f.suffix.lower() == ext and clean in f.stem.lower():
                    return f

        files = [f for f in self.out_dir.iterdir() if f.is_file()]
        return max(files, key=lambda x: x.stat().st_mtime) if files else None
