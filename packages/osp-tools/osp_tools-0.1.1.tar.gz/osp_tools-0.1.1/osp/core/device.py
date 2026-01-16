from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Device:
    name: str
    path: Path
    total: int
    free: int
    used: int

    @property
    def free_mb(self) -> float:
        return self.free / (1024 * 1024)

    @property
    def total_mb(self) -> float:
        return self.total / (1024 * 1024)

    @property
    def used_mb(self) -> float:
        return self.used / (1024 * 1024)

    @property
    def usage_pct(self) -> float:
        return (self.used / self.total * 100) if self.total else 0.0


class DeviceNotFound(Exception):
    pass


KNOWN_NAMES = ["OpenSwim", "OPENSWIM", "OpenSwim Pro", "SHOKZ", "Shokz"]
AUDIO_EXTS = {".mp3", ".wav", ".m4a", ".flac", ".wma"}


def _matches_device(name: str) -> bool:
    upper = name.upper()
    return any(known.upper() in upper for known in KNOWN_NAMES)


def _get_storage(path: Path) -> tuple:
    try:
        usage = shutil.disk_usage(path)
        return usage.total, usage.free, usage.used
    except OSError:
        return 0, 0, 0


def _make_device(name: str, path: Path) -> Device:
    total, free, used = _get_storage(path)
    return Device(name=name, path=path, total=total, free=free, used=used)


def _scan_macos() -> Optional[Device]:
    volumes = Path("/Volumes")
    if not volumes.exists():
        return None
    for vol in volumes.iterdir():
        if vol.is_dir() and _matches_device(vol.name):
            return _make_device(vol.name, vol)
    return None


def _scan_linux() -> Optional[Device]:
    user = os.environ.get("USER", "")
    bases = [Path(f"/media/{user}"), Path(f"/run/media/{user}"), Path("/mnt")]
    for base in bases:
        if not base.exists():
            continue
        for mount in base.iterdir():
            if mount.is_dir() and _matches_device(mount.name):
                return _make_device(mount.name, mount)
    return None


def _scan_windows() -> Optional[Device]:
    try:
        result = subprocess.run(
            ["wmic", "logicaldisk", "where", "drivetype=2", "get", "name,volumename"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                drive, name = parts[0], " ".join(parts[1:])
                if _matches_device(name):
                    return _make_device(name, Path(drive + "/"))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def find() -> Optional[Device]:
    system = platform.system()
    if system == "Darwin":
        return _scan_macos()
    elif system == "Linux":
        return _scan_linux()
    elif system == "Windows":
        return _scan_windows()
    return None


def find_or_fail() -> Device:
    dev = find()
    if dev is None:
        raise DeviceNotFound("No OpenSwim device found")
    return dev


def list_music(dev: Device) -> List[Path]:
    files = []
    for root, _, names in os.walk(dev.path):
        for name in names:
            p = Path(root) / name
            if p.suffix.lower() in AUDIO_EXTS:
                files.append(p)
    return sorted(files)
