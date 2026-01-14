"""Server management commands."""

import os
import signal
import subprocess
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.group()
def server():
    """Manage the emdash-core server."""
    pass


@server.command("killall")
def server_killall():
    """Kill all running emdash servers.

    Example:
        emdash server killall
    """
    killed = 0

    # Kill by PID file first
    pid_file = Path.home() / ".emdash" / "server.pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            console.print(f"[green]Killed server process {pid}[/green]")
            killed += 1
        except (ValueError, ProcessLookupError, PermissionError):
            pass
        finally:
            pid_file.unlink(missing_ok=True)

    # Clean up port file
    port_file = Path.home() / ".emdash" / "server.port"
    if port_file.exists():
        port_file.unlink(missing_ok=True)

    # Kill any remaining emdash_core.server processes
    try:
        result = subprocess.run(
            ["pgrep", "-f", "emdash_core.server"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            pids = result.stdout.strip().split("\n")
            for pid_str in pids:
                if pid_str:
                    try:
                        pid = int(pid_str)
                        os.kill(pid, signal.SIGTERM)
                        console.print(f"[green]Killed server process {pid}[/green]")
                        killed += 1
                    except (ValueError, ProcessLookupError, PermissionError):
                        pass
    except FileNotFoundError:
        # pgrep not available, try pkill
        subprocess.run(
            ["pkill", "-f", "emdash_core.server"],
            capture_output=True,
        )

    if killed > 0:
        console.print(f"\n[bold green]Killed {killed} server(s)[/bold green]")
    else:
        console.print("[yellow]No running servers found[/yellow]")


@server.command("status")
def server_status():
    """Show server status.

    Example:
        emdash server status
    """
    port_file = Path.home() / ".emdash" / "server.port"
    pid_file = Path.home() / ".emdash" / "server.pid"

    if not port_file.exists():
        console.print("[yellow]No server running[/yellow]")
        return

    try:
        port = int(port_file.read_text().strip())
    except (ValueError, IOError):
        console.print("[yellow]No server running (invalid port file)[/yellow]")
        return

    # Check if server is responsive
    import httpx
    try:
        response = httpx.get(f"http://localhost:{port}/api/health", timeout=2.0)
        if response.status_code == 200:
            pid = "unknown"
            if pid_file.exists():
                try:
                    pid = pid_file.read_text().strip()
                except IOError:
                    pass

            console.print(f"[bold green]Server running[/bold green]")
            console.print(f"  Port: {port}")
            console.print(f"  PID: {pid}")
            console.print(f"  URL: http://localhost:{port}")
        else:
            console.print(f"[yellow]Server on port {port} not healthy[/yellow]")
    except (httpx.RequestError, httpx.TimeoutException):
        console.print(f"[yellow]Server on port {port} not responding[/yellow]")
