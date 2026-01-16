# osp-tools

[![python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![platform](https://img.shields.io/badge/platform-macos%20|%20linux%20|%20windows-lightgrey.svg)]()

python tools for managing openswim mp3 players.

## features

- **device detection**: automatically finds openswim device path on macos, linux, and windows.
- **youtube**: downloads audio via yt-dlp wrapper. supports videos, playlists, shorts.
- **spotify**: scrapes track metadata without api keys. supports tracks, albums, playlists, artist top tracks.
- **bulk**: threaded processing for multiple queries.

## installation

### pip (recommended)

```sh
pip install osp-tools
```

### manual build

```sh
git clone https://github.com/1etu/osp-tools.git
cd osp-tools
pip install build
python -m build
pip install dist/osp_tools-*.whl
```

### development

```sh
git clone https://github.com/1etu/osp-tools.git
cd osp-tools
pip install -e ".[dev]"
```

## usage

```sh
osp --help
```

### device management

```sh
osp device              # show device info, storage usage
osp ls                  # list tracks on device
```

### youtube download

```sh
osp dl "https://youtube.com/watch?v=..."             # download single video
osp dl "https://youtube.com/playlist?list=..."       # download entire playlist
osp dl dQw4w9WgXcQ                                   # download by video id
osp dl "..." --device                                # download directly to openswim
osp dl "..." -q 320                                  # 320kbps quality
osp dl "..." -o ./music                              # custom output directory
```

### youtube search

```sh
osp search "song name"                # search youtube, get video ids
osp search "artist - track" -n 10     # limit results
```

### spotify (no api keys)

```sh
osp spotify "https://open.spotify.com/track/..."     # single track
osp spotify "https://open.spotify.com/album/..."     # full album
osp spotify "https://open.spotify.com/playlist/..."  # playlist
osp spotify "https://open.spotify.com/artist/..."    # artist top tracks
osp spotify "..." --info                             # show track list only
osp spotify "..." --device                           # download to openswim
osp spotify "..." -w 8                               # 8 parallel downloads
osp spotify "..." --fast                             # skip transcoding (~2x speed)
```

### sync local files

```sh
osp sync ./downloads              # sync folder to device (skip existing)
osp sync ./downloads --all        # overwrite all
```

## dependencies

- python 3.9+
- yt-dlp
- ffmpeg (for audio conversion)

## structure

- `osp/core`: device discovery and mount point logic.
- `osp/download`: youtube/spotify scrapers and downloaders.

## license

MIT
