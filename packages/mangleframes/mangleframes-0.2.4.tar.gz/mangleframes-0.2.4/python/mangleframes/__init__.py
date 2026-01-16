"""MangleFrames - PySpark DataFrame viewer with modern web UI."""
from __future__ import annotations

import atexit
import os
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING

from .launcher import launch_viewer
from .protocol import clear_arrow_cache, clear_stats_cache
from .server import DataFrameServer

if TYPE_CHECKING:
    from pyspark.sql import DataFrame

__version__ = "0.2.4"
__all__ = ["register", "unregister", "show", "cleanup"]

_registry: dict[str, DataFrame] = {}
_server: DataFrameServer | None = None
_viewer_process: subprocess.Popen | None = None
_cleanup_registered = False


def _clean_stale_sockets() -> None:
    """Remove socket files from PIDs that no longer exist."""
    socket_dir = Path("/tmp")
    for sock in socket_dir.glob("mangleframes-*.sock"):
        try:
            pid_str = sock.stem.split("-")[1]
            pid = int(pid_str)
            if not _pid_exists(pid):
                sock.unlink()
        except (IndexError, ValueError, OSError):
            pass


def _pid_exists(pid: int) -> bool:
    """Check if a process with given PID exists."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def cleanup() -> None:
    """Clean up all MangleFrames resources."""
    global _server, _viewer_process, _registry

    if _viewer_process is not None:
        _viewer_process.terminate()
        try:
            _viewer_process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            _viewer_process.kill()
        _viewer_process = None

    if _server is not None:
        _server.stop()
        _server = None

    _registry.clear()
    clear_stats_cache()
    clear_arrow_cache()


def register(name: str, df: DataFrame) -> None:
    """Register a DataFrame for viewing."""
    global _server, _cleanup_registered

    if not _cleanup_registered:
        atexit.register(cleanup)
        _cleanup_registered = True
        _clean_stale_sockets()

    _registry[name] = df
    clear_stats_cache(name)
    clear_arrow_cache(name)

    if _server is None:
        _server = DataFrameServer(_registry)
        _server.start()


def unregister(name: str) -> None:
    """Remove a DataFrame from the viewer."""
    if name in _registry:
        del _registry[name]
        clear_stats_cache(name)
        clear_arrow_cache(name)


def show(port: int = 8765, block: bool = True) -> None:
    """Open the viewer in a browser, launching the viewer if needed.

    Args:
        port: Port for the viewer web server.
        block: If True, block until Ctrl+C (keeps server alive).
    """
    global _viewer_process, _server

    if _server is None or not _server.is_running:
        if not _registry:
            raise RuntimeError("No DataFrames registered. Call register() first.")
        _server = DataFrameServer(_registry)
        _server.start()

    if _viewer_process is None or _viewer_process.poll() is not None:
        _viewer_process = launch_viewer(_server.socket_path, port)

    if block:
        try:
            print(f"MangleFrames viewer running at http://localhost:{port}")
            print("Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping MangleFrames...")
            cleanup()
