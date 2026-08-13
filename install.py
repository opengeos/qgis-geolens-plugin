#!/usr/bin/env python3
"""Install or remove GeoLens in the current user's default QGIS profile."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

PLUGIN_NAME = "geolens_qgis"


def default_plugin_dir() -> Path:
    home = Path.home()
    if sys.platform.startswith("linux"):
        return home / ".local/share/QGIS/QGIS3/profiles/default/python/plugins"
    if sys.platform == "darwin":
        return (
            home
            / "Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins"
        )
    if sys.platform == "win32":
        return (
            Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
            / "QGIS/QGIS3/profiles/default/python/plugins"
        )
    raise RuntimeError(f"Unsupported platform: {sys.platform}")


def install(source: Path, plugin_dir: Path) -> Path:
    target = plugin_dir / PLUGIN_NAME
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-dir", type=Path)
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    target = (args.plugin_dir or default_plugin_dir()) / PLUGIN_NAME
    if args.remove:
        if target.exists():
            shutil.rmtree(target)
            print(f"Removed {target}")
        return 0
    installed = install(Path(__file__).parent / PLUGIN_NAME, target.parent)
    print(f"Installed GeoLens at {installed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
