"""Server lifecycle management for emdash-core."""

import atexit
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import httpx


class ServerManager:
    """Manages FastAPI server lifecycle for CLI.

    The ServerManager handles:
    - Discovering running servers via port file
    - Starting new servers when needed
    - Health checking servers
    - Graceful shutdown on CLI exit
    """

    DEFAULT_PORT = 8765
    PORT_FILE = Path.home() / ".emdash" / "server.port"
    PID_FILE = Path.home() / ".emdash" / "server.pid"
    STARTUP_TIMEOUT = 30.0  # seconds
    HEALTH_TIMEOUT = 2.0  # seconds

    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize the server manager.

        Args:
            repo_root: Repository root path (for server to use)
        """
        self.repo_root = repo_root or self._detect_repo_root()
        self.process: Optional[subprocess.Popen] = None
        self.port: Optional[int] = None
        self._started_by_us = False

    def get_server_url(self) -> str:
        """Get URL of running server, starting one if needed.

        Returns:
            Base URL of the running server (e.g., "http://localhost:8765")

        Raises:
            RuntimeError: If server fails to start
        """
        # Check if server already running
        if self.PORT_FILE.exists():
            try:
                port = int(self.PORT_FILE.read_text().strip())
                if self._check_health(port):
                    self.port = port
                    return f"http://localhost:{port}"
            except (ValueError, IOError):
                pass

        # Start new server
        self.port = self._find_free_port()
        self._spawn_server()
        return f"http://localhost:{self.port}"

    def ensure_server(self) -> str:
        """Ensure server is running and return URL.

        Alias for get_server_url() for clearer intent.
        """
        return self.get_server_url()

    def shutdown(self) -> None:
        """Shutdown the server if we started it."""
        if self._started_by_us and self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            finally:
                self._cleanup_files()
                self.process = None

    def _detect_repo_root(self) -> Path:
        """Detect repository root from current directory."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            return Path(result.stdout.strip())
        except subprocess.CalledProcessError:
            return Path.cwd()

    def _find_free_port(self) -> int:
        """Find an available port."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.listen(1)
            return s.getsockname()[1]

    def _spawn_server(self) -> None:
        """Spawn FastAPI server as subprocess."""
        # Find emdash-core module
        core_module = self._find_core_module()

        cmd = [
            sys.executable,
            "-m", "emdash_core.server",
            "--port", str(self.port),
            "--host", "127.0.0.1",
        ]

        if self.repo_root:
            cmd.extend(["--repo-root", str(self.repo_root)])

        # Set environment to include core package
        env = os.environ.copy()
        if core_module:
            python_path = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = f"{core_module}:{python_path}" if python_path else str(core_module)

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        self._started_by_us = True

        # Register cleanup for normal exit
        atexit.register(self.shutdown)

        # Register signal handlers for Ctrl+C and termination
        self._register_signal_handlers()

        # Wait for server ready
        self._wait_for_ready()

    def _register_signal_handlers(self) -> None:
        """Register signal handlers for graceful shutdown."""
        def signal_handler(_signum, _frame):
            self.shutdown()
            sys.exit(0)

        # Handle SIGINT (Ctrl+C) and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def _find_core_module(self) -> Optional[Path]:
        """Find the emdash-core package directory."""
        # Check relative to this file (for development)
        cli_dir = Path(__file__).parent.parent
        core_dir = cli_dir.parent / "core"
        if (core_dir / "emdash_core").exists():
            return core_dir
        return None

    def _check_health(self, port: int) -> bool:
        """Check if server is healthy.

        Args:
            port: Port to check

        Returns:
            True if server responds to health check
        """
        try:
            response = httpx.get(
                f"http://localhost:{port}/api/health",
                timeout=self.HEALTH_TIMEOUT,
            )
            return response.status_code == 200
        except (httpx.RequestError, httpx.TimeoutException):
            return False

    def _wait_for_ready(self) -> None:
        """Wait for server to become ready.

        Raises:
            RuntimeError: If server fails to start within timeout
        """
        assert self.port is not None, "Port must be set before waiting for ready"
        start = time.time()
        while time.time() - start < self.STARTUP_TIMEOUT:
            if self._check_health(self.port):
                return

            # Check if process died
            if self.process and self.process.poll() is not None:
                stderr = self.process.stderr.read().decode() if self.process.stderr else ""
                raise RuntimeError(f"Server process died: {stderr}")

            time.sleep(0.1)

        raise RuntimeError(
            f"Server failed to start within {self.STARTUP_TIMEOUT}s"
        )

    def _cleanup_files(self) -> None:
        """Clean up port and PID files."""
        for file in [self.PORT_FILE, self.PID_FILE]:
            try:
                if file.exists():
                    file.unlink()
            except IOError:
                pass


# Global singleton for CLI commands
_server_manager: Optional[ServerManager] = None


def get_server_manager(repo_root: Optional[Path] = None) -> ServerManager:
    """Get or create the global server manager.

    Args:
        repo_root: Repository root (only used on first call)

    Returns:
        The server manager instance
    """
    global _server_manager
    if _server_manager is None:
        _server_manager = ServerManager(repo_root)
    return _server_manager
