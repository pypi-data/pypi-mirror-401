"""Launch the Rust viewer binary."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def find_viewer_binary() -> Path | None:
    """Find the mangleframes-viewer binary."""
    import sys

    pkg_dir = Path(__file__).parent
    pkg_binary = pkg_dir / "bin" / "mangleframes-viewer"
    if pkg_binary.exists():
        return pkg_binary

    venv_binary = Path(sys.executable).parent / "mangleframes-viewer"
    if venv_binary.exists():
        return venv_binary

    path_binary = shutil.which("mangleframes-viewer")
    if path_binary:
        return Path(path_binary)

    return None


def launch_viewer(socket_path: Path, port: int = 8765) -> subprocess.Popen:
    """Launch the viewer binary as a subprocess."""
    binary = find_viewer_binary()
    if binary is None:
        raise RuntimeError(
            "mangleframes-viewer binary not found. "
            "Install with: uv pip install mangleframes[viewer]"
        )

    env = os.environ.copy()
    env["RUST_LOG"] = env.get("RUST_LOG", "info")

    return subprocess.Popen(
        [str(binary), "--socket", str(socket_path), "--port", str(port), "--no-browser"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


