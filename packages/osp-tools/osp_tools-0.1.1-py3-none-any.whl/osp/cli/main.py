from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, BarColumn, TaskProgressColumn, TimeRemainingColumn, TextColumn
from rich.style import Style
from rich.text import Text

from osp import __version__
from osp.core.device import find, list_music, AUDIO_EXTS
from osp.download.youtube import Downloader, is_youtube, is_playlist, Progress as DlProgress
from osp.download.spotify import is_spotify, parse as parse_spotify
from osp.download.search import search, search_one
from osp.download.bulk import BulkDownloader, BulkProgress, TrackProgress, BulkConfig

console = Console()

DEEP = "#0d4f6e"
OCEAN = "#0a7c8f"
TEAL = "#14b8a6"
AQUA = "#22d3ee"
FOAM = "#67e8f9"
LIGHT = "#a5f3fc"
WHITE = "#ecfeff"

SEA = [DEEP, OCEAN, TEAL, AQUA, FOAM, LIGHT]


def wave_banner():
    frames = [
        r"     ~  ~  ~  ~  ~  ~  ~  ~  ~  ~     ",
        r"   ~   ~   ~   ~   ~   ~   ~   ~   ~  ",
        r"  ~  ~~~  ~~~  ~~~  ~~~  ~~~  ~~~  ~  ",
        r"     ~   ~   ~   ~   ~   ~   ~   ~    ",
        r"   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ",
    ]
    
    wave_art = [
        r"        .-~~~-.                      ",
        r"    .-~~       ~~-.                  ",
        r" .-~               ~-.    .-~~~-.    ",
        r"~                     ~~-~       ~~  ",
        r"  ~   ~   ~   ~   ~   ~   ~   ~   ~  ",
    ]
    
    for i, line in enumerate(wave_art):
        t = Text()
        for j, char in enumerate(line):
            color = SEA[(i + j) % len(SEA)]
            t.append(char, Style(color=color))
        console.print(t)
    
    console.print()
    t = Text()
    t.append("  osp ", Style(color=AQUA, bold=True))
    t.append(__version__, Style(color=TEAL, dim=True))
    t.append("  ", Style())
    t.append("openswim pro tools", Style(color=OCEAN, dim=True))
    console.print(t)
    console.print()


def animate_wave():
    chars = ["~", "~", "≈", "≋", "≈", "~", "~"]
    width = 40
    
    for frame in range(12):
        line = Text()
        for i in range(width):
            idx = (i + frame) % len(chars)
            color = SEA[(i + frame) % len(SEA)]
            line.append(chars[idx], Style(color=color))
        console.print(line, end="\r")
        time.sleep(0.04)
    console.print(" " * width, end="\r")


class WaveBar(BarColumn):
    def __init__(self):
        super().__init__(bar_width=35)
        self.frame = 0
    
    def render(self, task):
        self.frame += 1
        total = task.total or 1
        filled = int(self.bar_width * (task.completed / total))
        
        bar = Text()
        for i in range(filled):
            offset = (i + self.frame // 2) % len(SEA)
            bar.append("━", Style(color=SEA[offset]))
        
        bar.append("─" * (self.bar_width - filled), Style(color="#1e3a4a"))
        return bar


def msg(text: str, color: str = AQUA):
    console.print(Text(f"  {text}", Style(color=color)))


def err(text: str):
    console.print(Text(f"  x {text}", Style(color="#f87171")))


def ok(text: str):
    console.print(Text(f"  + {text}", Style(color=FOAM)))


def show_help():
    """Display styled help with all commands."""
    animate_wave()
    wave_banner()
    
    console.print()
    t = Text("  commands", Style(color=TEAL, bold=True))
    console.print(t)
    console.print()
    
    commands = [
        ("device", "show your openswim device info & storage"),
        ("ls", "list all tracks on your device"),
        ("dl", "download from youtube (video, playlist, or id)"),
        ("search", "search youtube for songs"),
        ("spotify", "download from spotify (no api key needed)"),
        ("sync", "copy local music folder to device"),
    ]
    
    for cmd, desc in commands:
        cmd_text = Text(f"  osp {cmd:<10}", Style(color=AQUA, bold=True))
        desc_text = Text(desc, Style(color=OCEAN))
        console.print(cmd_text, desc_text, sep="")
    
    console.print()
    t = Text("  quick start", Style(color=TEAL, bold=True))
    console.print(t)
    console.print()
    
    examples = [
        ("download a song", "osp dl \"song name or youtube url\""),
        ("from spotify", "osp spotify \"spotify playlist url\""),
        ("to device", "osp dl \"...\" --device"),
    ]
    
    for label, example in examples:
        label_text = Text(f"  {label:<16}", Style(color=OCEAN, dim=True))
        example_text = Text(example, Style(color=FOAM))
        console.print(label_text, example_text, sep="")
    
    console.print()
    t = Text("  tip: ", Style(color=DEEP))
    t.append("use ", Style(color=OCEAN))
    t.append("osp <command> --help", Style(color=AQUA))
    t.append(" for detailed options", Style(color=OCEAN))
    console.print(t)
    console.print()


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="osp")
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        show_help()


@cli.command()
def device():
    animate_wave()
    console.print()
    msg("device", TEAL)
    console.print()
    
    dev = find()
    if not dev:
        err("no device found")
        msg("connect openswim via usb", OCEAN)
        sys.exit(1)

    msg(f"name     {dev.name}", AQUA)
    msg(f"path     {dev.path}", OCEAN)
    msg(f"total    {dev.total_mb:.0f} mb", OCEAN)
    
    bar_width = 25
    filled = int(bar_width * (dev.usage_pct / 100))
    bar = Text("  used     ")
    for i in range(filled):
        bar.append("▓", Style(color=SEA[i % len(SEA)]))
    bar.append("░" * (bar_width - filled), Style(color="#1e3a4a"))
    bar.append(f" {dev.usage_pct:.0f}%", Style(color=TEAL, dim=True))
    console.print(bar)
    
    msg(f"free     {dev.free_mb:.0f} mb", TEAL)
    console.print()


@cli.command("ls")
def list_cmd():
    animate_wave()
    console.print()
    msg("library", TEAL)
    console.print()
    
    dev = find()
    if not dev:
        err("no device found")
        sys.exit(1)

    files = list_music(dev)
    if not files:
        msg("empty", OCEAN)
        return

    for i, f in enumerate(files, 1):
        size = f.stat().st_size / (1024 * 1024)
        idx = Text(f"  {i:>3}  ", Style(color=DEEP))
        name = Text(f.name, Style(color=AQUA))
        sz = Text(f"  {size:.1f}mb", Style(color=OCEAN, dim=True))
        console.print(idx, name, sz, sep="")

    console.print()
    total = sum(f.stat().st_size for f in files) / (1024 * 1024)
    msg(f"{len(files)} tracks  {total:.0f}mb", TEAL)
    console.print()


@cli.command("dl")
@click.argument("url_or_id")
@click.option("-o", "--out", type=click.Path(), default="./downloads")
@click.option("-q", "--quality", type=click.Choice(["128", "192", "256", "320"]), default="192")
@click.option("--device", "to_device", is_flag=True)
def download(url_or_id: str, out: str, quality: str, to_device: bool):
    animate_wave()
    console.print()
    msg("download", TEAL)
    console.print()
    
    if not is_youtube(url_or_id) and len(url_or_id) == 11:
        url = f"https://www.youtube.com/watch?v={url_or_id}"
    elif is_youtube(url_or_id):
        url = url_or_id
    else:
        err("invalid youtube url or video id")
        sys.exit(1)

    if to_device:
        dev = find()
        if not dev:
            err("no device found")
            sys.exit(1)
        out_dir = dev.path
        msg(f"target   {dev.name}", OCEAN)
    else:
        out_dir = Path(out)
        msg(f"target   {out_dir}", OCEAN)

    dl = Downloader(out_dir, quality=quality)
    console.print()

    with Progress(
        TextColumn("{task.description}", style=OCEAN),
        WaveBar(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
        refresh_per_second=10,
    ) as prog:
        task = prog.add_task("  preparing", total=100)

        def on_progress(p: DlProgress):
            if p.status == "downloading":
                name = Path(p.filename).stem[:25]
                prog.update(task, completed=p.pct, description=f"  {name}")
            elif p.status == "finished":
                prog.update(task, completed=100, description="  converting")

        if is_playlist(url):
            results = dl.get_playlist(url, on_progress)
            wins = sum(1 for r in results if r.ok)
            fails = len(results) - wins
            console.print()
            if wins:
                ok(f"{wins} tracks downloaded")
            if fails:
                err(f"{fails} failed")
        else:
            r = dl.get(url, on_progress)
            console.print()
            if r.ok:
                ok(r.title)
                if r.path:
                    msg(f"saved    {r.path.name}", OCEAN)
                if r.duration:
                    msg(f"length   {r.duration // 60}:{r.duration % 60:02d}", OCEAN)
            else:
                err(r.error or "download failed")
                sys.exit(1)
    
    console.print()


@cli.command()
@click.argument("src", type=click.Path(exists=True))
@click.option("--all", "sync_all", is_flag=True)
def sync(src: str, sync_all: bool):
    animate_wave()
    console.print()
    msg("sync", TEAL)
    console.print()
    
    dev = find()
    if not dev:
        err("no device found")
        sys.exit(1)

    src_path = Path(src)
    src_files = [f for f in src_path.iterdir() if f.is_file() and f.suffix.lower() in AUDIO_EXTS]

    if not src_files:
        msg("no audio files", OCEAN)
        return

    on_device = {f.name.lower() for f in list_music(dev)}
    to_copy = src_files if sync_all else [f for f in src_files if f.name.lower() not in on_device]

    if not to_copy:
        msg("already synced", TEAL)
        return

    msg(f"copying {len(to_copy)} files", OCEAN)
    console.print()
    
    with Progress(
        TextColumn("{task.description}", style=OCEAN),
        WaveBar(),
        TaskProgressColumn(),
        console=console,
        transient=True,
        refresh_per_second=10,
    ) as prog:
        task = prog.add_task("  syncing", total=len(to_copy))
        copied = 0
        for f in to_copy:
            prog.update(task, description=f"  {f.stem[:25]}")
            try:
                shutil.copy2(f, dev.path / f.name)
                copied += 1
            except OSError as e:
                err(f"{f.name}")
            prog.advance(task)

    console.print()
    ok(f"{copied} files synced")
    console.print()


@cli.command("search")
@click.argument("query", nargs=-1, required=True)
@click.option("-n", "--num", default=5, help="number of results")
def search_cmd(query: tuple, num: int):
    animate_wave()
    console.print()
    msg("search", TEAL)
    console.print()
    
    query_str = " ".join(query)
    msg(f"query    {query_str}", OCEAN)
    console.print()
    
    results = search(query_str, limit=num)
    
    if not results:
        msg("no results", OCEAN)
        return
    
    for i, r in enumerate(results, 1):
        dur_sec = int(r.duration) if r.duration else 0
        dur = f"{dur_sec // 60}:{dur_sec % 60:02d}" if dur_sec else "?"
        views = f"{r.views:,}" if hasattr(r, 'views') and r.views else ""
        
        idx = Text(f"  {i:>2}  ", Style(color=DEEP))
        title = Text(r.title[:50], Style(color=AQUA))
        console.print(idx, title, sep="")
        console.print(Text(f"      id: {r.id}  {dur}  {r.channel[:20]}", Style(color=OCEAN, dim=True)))
    
    console.print()
    msg("download with: osp dl <id>", TEAL)
    console.print()


@cli.command("spotify")
@click.argument("url")
@click.option("-o", "--out", type=click.Path(), default="./downloads")
@click.option("-q", "--quality", type=click.Choice(["128", "192", "256", "320"]), default="192")
@click.option("--device", "to_device", is_flag=True)
@click.option("--info", "info_only", is_flag=True, help="show info only, don't download")
@click.option("-w", "--workers", type=int, default=4, help="parallel downloads")
@click.option("--fast", "fast_mode", is_flag=True, help="skip transcoding (m4a, ~2x faster)")
def spotify_cmd(url: str, out: str, quality: str, to_device: bool, info_only: bool, workers: int, fast_mode: bool):
    animate_wave()
    console.print()
    msg("spotify", TEAL)
    console.print()
    
    if not is_spotify(url):
        err("invalid spotify url")
        sys.exit(1)
    
    msg("parsing", OCEAN)
    result = parse_spotify(url)
    
    if not result.tracks:
        err("no tracks found")
        sys.exit(1)
    
    type_label = result.type
    if result.name:
        msg(f"{type_label}   {result.name}", AQUA)
    if result.owner:
        msg(f"by       {result.owner}", OCEAN)
    msg(f"tracks   {len(result.tracks)}", OCEAN)
    console.print()
    
    if info_only:
        for i, t in enumerate(result.tracks[:20], 1):
            idx = Text(f"  {i:>2}  ", Style(color=DEEP))
            title = Text(t.name[:40], Style(color=AQUA))
            meta = Text(f"  {t.duration_fmt}  {t.artist[:20]}", Style(color=OCEAN, dim=True))
            console.print(idx, title, meta, sep="")
        if len(result.tracks) > 20:
            msg(f"... and {len(result.tracks) - 20} more", OCEAN)
        console.print()
        return
    
    if to_device:
        dev = find()
        if not dev:
            err("no device found")
            sys.exit(1)
        out_dir = dev.path
        msg(f"target   {dev.name}", OCEAN)
    else:
        out_dir = Path(out)
        msg(f"target   {out_dir}", OCEAN)
    
    msg(f"workers  {workers}", OCEAN)
    if fast_mode:
        msg("mode     fast (no transcoding)", AQUA)
    console.print()
    
    config = BulkConfig(
        search_workers=8,
        download_workers=workers,
        fast_mode=fast_mode,
    )
    
    bulk_dl = BulkDownloader(out_dir, quality=quality, config=config)
    
    with Progress(
        TextColumn("{task.description}", style=OCEAN),
        WaveBar(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
        refresh_per_second=10,
    ) as prog:
        search_task = prog.add_task("  searching", total=len(result.tracks))
        download_task = prog.add_task("  downloading", total=len(result.tracks))
        
        last_searched = 0
        last_downloaded = 0
        
        def on_progress(bulk_prog: BulkProgress, track_prog: TrackProgress | None):
            nonlocal last_searched, last_downloaded
            
            if bulk_prog.searched > last_searched:
                prog.update(search_task, completed=bulk_prog.searched)
                last_searched = bulk_prog.searched
            
            completed = bulk_prog.downloaded + bulk_prog.failed
            completed = bulk_prog.downloaded + bulk_prog.failed
            if completed > last_downloaded:
                prog.update(download_task, completed=completed)
                last_downloaded = completed
            
            if track_prog and track_prog.phase == "downloading":
                name = track_prog.track.name[:25]
                prog.update(download_task, description=f"  {name}")
        
        bulk_result = bulk_dl.fetch(result.tracks, on_progress=on_progress)
    
    console.print()
    if bulk_result.success_count:
        ok(f"{bulk_result.success_count} tracks downloaded")
    if bulk_result.failed_count:
        err(f"{bulk_result.failed_count} failed")
        for fail in bulk_result.failed_tracks()[:3]:
            msg(f"  • {fail.track.name[:40]} - {fail.error[:30]}", DEEP)
    console.print()


def main():
    cli()


if __name__ == "__main__":
    main()
