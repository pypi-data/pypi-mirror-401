from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import List, Optional, Union
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass(frozen=True)
class Track:
    id: str
    name: str
    artists: tuple
    album: str = ""
    duration_ms: int = 0
    isrc: str = ""
    
    @property
    def artist(self) -> str:
        return self.artists[0] if self.artists else ""
    
    @property
    def artist_str(self) -> str:
        return ", ".join(self.artists)
    
    @property
    def duration_sec(self) -> int:
        return self.duration_ms // 1000
    
    @property
    def duration_fmt(self) -> str:
        s = self.duration_sec
        return f"{s // 60}:{s % 60:02d}"
    
    def search_query(self) -> str:
        if self.isrc:
            return self.isrc
        return f"{self.artist_str} - {self.name}"


@dataclass
class Album:
    id: str
    name: str
    artist: str
    tracks: List[Track] = field(default_factory=list)
    year: int = 0
    cover_url: str = ""
    
    @property
    def duration_sec(self) -> int:
        return sum(t.duration_sec for t in self.tracks)


@dataclass
class Playlist:
    id: str
    name: str
    owner: str = ""
    description: str = ""
    tracks: List[Track] = field(default_factory=list)
    cover_url: str = ""
    
    @property
    def duration_sec(self) -> int:
        return sum(t.duration_sec for t in self.tracks)


@dataclass
class SpotifyResult:
    type: str  # 'track', 'album', 'playlist', 'artist'
    tracks: List[Track] = field(default_factory=list)
    name: str = ""
    owner: str = ""
    cover_url: str = ""


PATTERNS = {
    'track': re.compile(r'(?:spotify[:/]|open\.spotify\.com/)track[/:]([a-zA-Z0-9]+)'),
    'album': re.compile(r'(?:spotify[:/]|open\.spotify\.com/)album[/:]([a-zA-Z0-9]+)'),
    'playlist': re.compile(r'(?:spotify[:/]|open\.spotify\.com/)playlist[/:]([a-zA-Z0-9]+)'),
    'artist': re.compile(r'(?:spotify[:/]|open\.spotify\.com/)artist[/:]([a-zA-Z0-9]+)'),
}


def detect_type(url: str) -> tuple:
    for url_type, pattern in PATTERNS.items():
        m = pattern.search(url)
        if m:
            return (url_type, m.group(1))
    return (None, None)


def is_spotify(url: str) -> bool:
    return detect_type(url)[0] is not None


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/json",
    "Accept-Language": "en-US,en;q=0.9",
}


def _fetch(url: str, timeout: int = 10) -> Optional[str]:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8")
    except (URLError, HTTPError, TimeoutError):
        return None


def _fetch_json(url: str, timeout: int = 10) -> Optional[dict]:
    content = _fetch(url, timeout)
    if content:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
    return None

def _parse_track_from_dict(data: dict) -> Optional[Track]:
    if not data:
        return None
    
    name = data.get("name") or data.get("title", "")
    if not name:
        return None
    
    artists = []
    if "artists" in data:
        for a in data.get("artists", []):
            if isinstance(a, dict):
                artists.append(a.get("name", ""))
            elif isinstance(a, str):
                artists.append(a)
    elif "subtitle" in data:
        artists = [data["subtitle"]]
    
    track_id = data.get("id", "")
    if not track_id and "uri" in data:
        parts = data["uri"].split(":")
        if len(parts) == 3:
            track_id = parts[2]
    
    duration = data.get("duration_ms", 0) or data.get("duration", 0)
    
    return Track(
        id=track_id,
        name=name,
        artists=tuple(artists) if artists else ("Unknown",),
        album=data.get("album", {}).get("name", "") if isinstance(data.get("album"), dict) else str(data.get("album", "")),
        duration_ms=duration,
        isrc=data.get("external_ids", {}).get("isrc", "") if isinstance(data.get("external_ids"), dict) else "",
    )


def _scrape_embed(content_type: str, content_id: str) -> Optional[dict]:
    url = f"https://open.spotify.com/embed/{content_type}/{content_id}"
    html = _fetch(url)
    if not html:
        return None
    
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>([^<]+)</script>', html)
    if m:
        try:
            data = json.loads(m.group(1))
            props = data.get("props", {}).get("pageProps", {})
            return props.get("state", {}).get("data", {}).get("entity", props)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
    
    m = re.search(r'Spotify\.Entity\s*=\s*(\{.*?\});', html, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    
    m = re.search(r'"entity":\s*(\{[^}]+(?:\{[^}]*\}[^}]*)*\})', html)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    
    return None


def _scrape_oembed(content_type: str, content_id: str) -> Optional[dict]:
    url = f"https://open.spotify.com/oembed?url=spotify:{content_type}:{content_id}"
    return _fetch_json(url)


def _scrape_html_meta(content_type: str, content_id: str) -> dict:
    url = f"https://open.spotify.com/{content_type}/{content_id}"
    html = _fetch(url)
    if not html:
        return {}
    
    result = {}
    
    m = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html)
    if m:
        result["title"] = m.group(1)
    
    m = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"', html)
    if m:
        result["description"] = m.group(1)
    
    m = re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"', html)
    if m:
        result["image"] = m.group(1)
    
    return result


def get_track(track_id: str) -> Optional[Track]:
    data = _scrape_embed("track", track_id)
    if data:
        track = _parse_track_from_dict(data)
        if track:
            return track
    
    oembed = _scrape_oembed("track", track_id)
    if oembed:
        title = oembed.get("title", "")
        return Track(
            id=track_id,
            name=title,
            artists=(oembed.get("description", "").split(" · ")[0],) if oembed.get("description") else ("Unknown",),
            album="",
            duration_ms=0,
        )
    
    meta = _scrape_html_meta("track", track_id)
    if meta.get("title"):
        desc_parts = meta.get("description", "").split(" · ")
        return Track(
            id=track_id,
            name=meta["title"],
            artists=(desc_parts[0],) if desc_parts else ("Unknown",),
            album=desc_parts[1] if len(desc_parts) > 1 else "",
        )
    
    return None


def get_album(album_id: str) -> Optional[Album]:
    data = _scrape_embed("album", album_id)
    
    if data:
        tracks = []
        track_list = data.get("tracks", {}).get("items", []) or data.get("trackList", [])
        
        for t in track_list:
            track = _parse_track_from_dict(t)
            if track:
                tracks.append(track)
        
        return Album(
            id=album_id,
            name=data.get("name", ""),
            artist=data.get("artists", [{}])[0].get("name", "") if data.get("artists") else "",
            tracks=tracks,
            year=int(data.get("release_date", "0")[:4]) if data.get("release_date") else 0,
            cover_url=data.get("images", [{}])[0].get("url", "") if data.get("images") else "",
        )
    
    meta = _scrape_html_meta("album", album_id)
    if meta.get("title"):
        return Album(
            id=album_id,
            name=meta["title"],
            artist=meta.get("description", "").split(" · ")[0] if meta.get("description") else "",
            cover_url=meta.get("image", ""),
        )
    
    return None


def get_playlist(playlist_id: str) -> Optional[Playlist]:
    data = _scrape_embed("playlist", playlist_id)
    
    if data:
        tracks = []
        track_list = data.get("tracks", {}).get("items", []) or data.get("trackList", [])
        
        for item in track_list:
            t = item.get("track", item) if isinstance(item, dict) else item
            track = _parse_track_from_dict(t)
            if track:
                tracks.append(track)
        
        return Playlist(
            id=playlist_id,
            name=data.get("name", ""),
            owner=data.get("owner", {}).get("display_name", "") if isinstance(data.get("owner"), dict) else str(data.get("owner", "")),
            description=data.get("description", ""),
            tracks=tracks,
            cover_url=data.get("images", [{}])[0].get("url", "") if data.get("images") else "",
        )
    
    return _scrape_playlist_fallback(playlist_id)


def _scrape_playlist_fallback(playlist_id: str) -> Optional[Playlist]:
    url = f"https://open.spotify.com/embed/playlist/{playlist_id}"
    html = _fetch(url)
    if not html:
        return None
    
    tracks = []
    
    pattern = r'"name":\s*"([^"]+)",\s*"artists":\s*\[\{"name":\s*"([^"]+)"'
    for name, artist in re.findall(pattern, html):
        if name and artist and not name.startswith("Spotify"):
            tracks.append(Track(
                id="",
                name=name,
                artists=(artist,),
            ))
    
    meta = _scrape_html_meta("playlist", playlist_id)
    
    return Playlist(
        id=playlist_id,
        name=meta.get("title", "Unknown Playlist"),
        owner=meta.get("description", "").split(" · ")[0] if meta.get("description") else "",
        tracks=tracks,
    ) if tracks else None


def get_artist_top(artist_id: str) -> List[Track]:
    url = f"https://open.spotify.com/artist/{artist_id}"
    html = _fetch(url)
    if not html:
        return []
    
    tracks = []
    
    pattern = r'"track":\s*\{[^}]*"name":\s*"([^"]+)"[^}]*"artists":\s*\[\{"name":\s*"([^"]+)"'
    for name, artist in re.findall(pattern, html):
        if name and artist:
            tracks.append(Track(id="", name=name, artists=(artist,)))
    
    return tracks[:10] 

def parse(url: str) -> SpotifyResult:
    url_type, content_id = detect_type(url)
    
    if not url_type or not content_id:
        return SpotifyResult(type="unknown")
    
    if url_type == "track":
        track = get_track(content_id)
        return SpotifyResult(
            type="track",
            tracks=[track] if track else [],
            name=track.name if track else "",
        )
    
    elif url_type == "album":
        album = get_album(content_id)
        return SpotifyResult(
            type="album",
            tracks=album.tracks if album else [],
            name=album.name if album else "",
            owner=album.artist if album else "",
            cover_url=album.cover_url if album else "",
        )
    
    elif url_type == "playlist":
        playlist = get_playlist(content_id)
        return SpotifyResult(
            type="playlist",
            tracks=playlist.tracks if playlist else [],
            name=playlist.name if playlist else "",
            owner=playlist.owner if playlist else "",
            cover_url=playlist.cover_url if playlist else "",
        )
    
    elif url_type == "artist":
        tracks = get_artist_top(content_id)
        return SpotifyResult(
            type="artist",
            tracks=tracks,
            name="Top Tracks",
        )
    
    return SpotifyResult(type="unknown")


def parse_tracks(url: str) -> List[Track]:
    return parse(url).tracks


def playlist_tracks(url: str) -> List[Track]:
    return parse_tracks(url)
