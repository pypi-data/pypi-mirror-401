"""Unix socket server for DataFrame communication."""
from __future__ import annotations

import os
import socket
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from .protocol import dispatch_command

if TYPE_CHECKING:
    from pyspark.sql import DataFrame

SOCKET_DIR = Path("/tmp")
BUFFER_SIZE = 4096


class DataFrameServer:
    """Unix socket server that serves DataFrame data to viewers."""

    def __init__(self, registry: dict[str, DataFrame]) -> None:
        self._registry = registry
        self._socket_path: Path | None = None
        self._server_socket: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._running = False
        self._on_update: Callable[[], None] | None = None

    @property
    def socket_path(self) -> Path | None:
        return self._socket_path

    @property
    def is_running(self) -> bool:
        return self._running

    def set_update_callback(self, callback: Callable[[], None]) -> None:
        self._on_update = callback

    def start(self) -> Path:
        """Start the server and return the socket path."""
        if self._running:
            return self._socket_path

        self._socket_path = SOCKET_DIR / f"mangleframes-{os.getpid()}.sock"

        if self._socket_path.exists():
            self._socket_path.unlink()

        self._server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server_socket.bind(str(self._socket_path))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)

        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

        return self._socket_path

    def stop(self) -> None:
        """Stop the server and clean up resources."""
        self._running = False

        if self._server_socket:
            self._server_socket.close()
            self._server_socket = None

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
            self._thread = None

        if self._socket_path and self._socket_path.exists():
            self._socket_path.unlink()
            self._socket_path = None

    def _serve(self) -> None:
        """Main server loop accepting connections."""
        while self._running:
            try:
                conn, _ = self._server_socket.accept()
                self._handle_connection(conn)
            except socket.timeout:
                continue
            except OSError:
                if self._running:
                    raise
                break

    def _handle_connection(self, conn: socket.socket) -> None:
        """Handle a single client connection."""
        try:
            data = b""
            while b"\n" not in data:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                data += chunk

            if data:
                command = data.decode("utf-8").split("\n")[0]
                response = dispatch_command(self._registry, command)
                conn.sendall(response)
        finally:
            conn.close()
