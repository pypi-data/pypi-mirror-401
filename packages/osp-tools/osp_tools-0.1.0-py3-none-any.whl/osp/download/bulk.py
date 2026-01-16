from __future__ import annotations

import queue
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional, Union

from .search import search_one, SearchResult
from .spotify import Track
from .youtube import Downloader, Result as DlResult


@dataclass
class BulkConfig:
    search_workers: int = 8     
    download_workers: int = 4     
    fast_mode: bool = False       

@dataclass
class TrackProgress:
    track: Track
    phase: str = "queued"  #  queued, searchinf, matched, downlaoding, done, failed
    matched_url: str = ""
    matched_title: str = ""
    error: str = ""


@dataclass
class BulkProgress:
    total: int
    searched: int = 0
    matched: int = 0
    downloaded: int = 0
    failed: int = 0
    
    @property
    def search_pct(self) -> float:
        return (self.searched / self.total) * 100 if self.total else 0
    
    @property
    def download_pct(self) -> float:
        return (self.downloaded / self.total) * 100 if self.total else 0
    
    @property
    def complete(self) -> int:
        return self.downloaded + self.failed


ProgressCallback = Callable[[BulkProgress, Optional[TrackProgress]], None]


@dataclass
class TrackResult:
    track: Track
    ok: bool
    path: Optional[Path] = None
    youtube_url: str = ""
    youtube_title: str = ""
    error: str = ""


@dataclass
class BulkResult:
    results: List[TrackResult]
    
    @property
    def success_count(self) -> int:
        return sum(1 for r in self.results if r.ok)
    
    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if not r.ok)
    
    @property
    def success_rate(self) -> float:
        return (self.success_count / len(self.results)) * 100 if self.results else 0
    
    def failed_tracks(self) -> List[TrackResult]:
        return [r for r in self.results if not r.ok]
    
    def successful_tracks(self) -> List[TrackResult]:
        return [r for r in self.results if r.ok]

class FastDownloader:
    def __init__(self, out_dir: Union[Path, str]):
        import yt_dlp
        import shutil
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.yt_dlp = yt_dlp
        self._has_aria2c = shutil.which("aria2c") is not None
    
    def get(self, url: str) -> DlResult:
        opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.out_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "ignoreerrors": False,
            "geo_bypass": True,
            "socket_timeout": 15,
            "retries": 3,
            "nocheckcertificate": True,
        }
        
        if self._has_aria2c:
            opts["external_downloader"] = "aria2c"
            opts["external_downloader_args"] = {"default": ["-x", "16", "-k", "1M", "-j", "16"]}
        
        try:
            with self.yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    return DlResult(False, None, "Unknown", None, 0, "No info")
                
                if "entries" in info:
                    entries = list(info["entries"])
                    info = entries[0] if entries else None
                    if not info:
                        return DlResult(False, None, "Unknown", None, 0, "Empty")
                
                title = info.get("title", "")
                path = self._find_file(title)
                
                return DlResult(
                    ok=True,
                    path=path,
                    title=info.get("title", "Unknown"),
                    artist=info.get("artist") or info.get("uploader"),
                    duration=info.get("duration", 0),
                )
        except Exception as e:
            if self._has_aria2c:
                return self._get_fallback(url)
            return DlResult(False, None, "Unknown", None, 0, str(e))
    
    def _get_fallback(self, url: str) -> DlResult:
        opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.out_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "ignoreerrors": False,
            "geo_bypass": True,
            "socket_timeout": 15,
            "retries": 3,
            "nocheckcertificate": True,
        }
        
        try:
            with self.yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    return DlResult(False, None, "Unknown", None, 0, "No info")
                
                if "entries" in info:
                    entries = list(info["entries"])
                    info = entries[0] if entries else None
                    if not info:
                        return DlResult(False, None, "Unknown", None, 0, "Empty")
                
                title = info.get("title", "")
                path = self._find_file(title)
                
                return DlResult(
                    ok=True,
                    path=path,
                    title=info.get("title", "Unknown"),
                    artist=info.get("artist") or info.get("uploader"),
                    duration=info.get("duration", 0),
                )
        except Exception as e:
            return DlResult(False, None, "Unknown", None, 0, str(e))
    
    def _find_file(self, title: str) -> Optional[Path]:
        import re
        clean = re.sub(r'[<>:"/\\|?*]', "", title).strip().lower()
        
        for ext in [".m4a", ".webm", ".opus", ".mp3"]:
            for f in self.out_dir.iterdir():
                if f.suffix.lower() == ext and clean in f.stem.lower():
                    return f
        
        files = [f for f in self.out_dir.iterdir() if f.is_file()]
        return max(files, key=lambda x: x.stat().st_mtime) if files else None


class BulkDownloader:
    def __init__(
        self,
        out_dir: Union[Path, str],
        fmt: str = "mp3",
        quality: str = "192",
        config: Optional[BulkConfig] = None,
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.fmt = fmt
        self.quality = quality
        self.config = config or BulkConfig()
        self._lock = threading.Lock()
    
    def fetch(
        self,
        tracks: List[Track],
        on_progress: Optional[ProgressCallback] = None,
    ) -> BulkResult:
        if not tracks:
            return BulkResult(results=[])
        
        progress = BulkProgress(total=len(tracks))
        results: List[TrackResult] = []
        results_lock = threading.Lock()
        download_queue: queue.Queue = queue.Queue()
        search_done = threading.Event()
        
        def search_worker():
            def do_search(track: Track) -> tuple[Track, Optional[SearchResult]]:
                try:
                    result = search_one(track.search_query())
                    return (track, result)
                except Exception:
                    return (track, None)
            
            with ThreadPoolExecutor(max_workers=self.config.search_workers) as pool:
                futures = {pool.submit(do_search, t): t for t in tracks}
                
                for future in as_completed(futures):
                    track, result = future.result()
                    
                    with self._lock:
                        progress.searched += 1
                        if result:
                            progress.matched += 1
                    
                    if result:
                        download_queue.put((track, result))
                    else:
                        with results_lock:
                            results.append(TrackResult(
                                track=track,
                                ok=False,
                                error="No YouTube match found",
                            ))
                        with self._lock:
                            progress.failed += 1
                    
                    if on_progress:
                        on_progress(progress, TrackProgress(
                            track=track,
                            phase="matched" if result else "failed",
                            matched_url=result.url if result else "",
                            matched_title=result.title if result else "",
                            error="" if result else "No match",
                        ))
            
            search_done.set()
        
        def download_worker():
            if self.config.fast_mode:
                downloader = FastDownloader(self.out_dir)
            else:
                downloader = Downloader(self.out_dir, fmt=self.fmt, quality=self.quality)
            
            while True:
                try:
                    item = download_queue.get(timeout=0.5)
                except queue.Empty:
                    if search_done.is_set() and download_queue.empty():
                        break
                    continue
                
                track, sr = item
                
                if on_progress:
                    on_progress(progress, TrackProgress(
                        track=track,
                        phase="downloading",
                        matched_url=sr.url,
                        matched_title=sr.title,
                    ))
                
                try:
                    dl_result = downloader.get(sr.url)
                    
                    result = TrackResult(
                        track=track,
                        ok=dl_result.ok,
                        path=dl_result.path,
                        youtube_url=sr.url,
                        youtube_title=sr.title,
                        error=dl_result.error or "",
                    )
                    
                    with self._lock:
                        if dl_result.ok:
                            progress.downloaded += 1
                        else:
                            progress.failed += 1
                    
                except Exception as e:
                    result = TrackResult(
                        track=track,
                        ok=False,
                        youtube_url=sr.url,
                        youtube_title=sr.title,
                        error=str(e),
                    )
                    with self._lock:
                        progress.failed += 1
                
                with results_lock:
                    results.append(result)
                
                if on_progress:
                    on_progress(progress, TrackProgress(
                        track=track,
                        phase="done" if result.ok else "failed",
                        matched_url=sr.url,
                        matched_title=sr.title,
                        error=result.error,
                    ))
                
                download_queue.task_done()
        
        search_thread = threading.Thread(target=search_worker, daemon=True)
        search_thread.start()
        
        download_threads = []
        for _ in range(self.config.download_workers):
            t = threading.Thread(target=download_worker, daemon=True)
            t.start()
            download_threads.append(t)
        
        search_thread.join()
        for t in download_threads:
            t.join()
        
        return BulkResult(results=results)


def bulk_download(
    tracks: List[Track],
    out_dir: Union[Path, str] = "./downloads",
    fmt: str = "mp3",
    quality: str = "192",
    on_progress: Optional[ProgressCallback] = None,
    config: Optional[BulkConfig] = None,
) -> BulkResult:
    downloader = BulkDownloader(out_dir, fmt, quality, config)
    return downloader.fetch(tracks, on_progress)
