from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed

import yt_dlp


class _NullLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


@dataclass(frozen=True)
class SearchResult:
    id: str
    title: str
    channel: str
    duration: int
    url: str


_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": True,
    "skip_download": True,
    "logger": _NullLogger(),
}


def search(query: str, limit: int = 5) -> List[SearchResult]:
    search_url = f"ytsearch{limit}:{query}"
    
    with yt_dlp.YoutubeDL(_OPTS) as ydl:
        try:
            info = ydl.extract_info(search_url, download=False)
        except Exception:
            return []
    
    if not info or "entries" not in info:
        return []
    
    results = []
    for e in info["entries"]:
        if not e:
            continue
        results.append(SearchResult(
            id=e.get("id", ""),
            title=e.get("title", ""),
            channel=e.get("channel", "") or e.get("uploader", ""),
            duration=e.get("duration", 0) or 0,
            url=e.get("url", "") or f"https://youtube.com/watch?v={e.get('id', '')}",
        ))
    
    return results


def search_one(query: str) -> Optional[SearchResult]:
    results = search(query, limit=1)
    return results[0] if results else None


def search_batch(queries: List[str], limit: int = 1, workers: int = 4) -> dict:
    results = {}
    
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(search, q, limit): q for q in queries}
        for future in as_completed(futures):
            query = futures[future]
            try:
                results[query] = future.result()
            except Exception:
                results[query] = []
    
    return results


def iter_search(query: str, limit: int = 10) -> Iterator[SearchResult]:
    for r in search(query, limit):
        yield r
