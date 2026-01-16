from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("vvpg_robots_go2_sdk")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from .unitree.sport_streamer import SportConfig, UnitreeMoveStreamer

__all__ = ["__version__", "SportConfig", "UnitreeMoveStreamer"]
