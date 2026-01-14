"""Swarm multi-agent CLI commands."""

import click
from rich.console import Console

from ..client import EmdashClient
from ..server_manager import get_server_manager
from ..sse_renderer import SSERenderer

console = Console()


@click.group()
def swarm():
    """Multi-agent parallel execution with git worktrees."""
    pass


@swarm.command("run")
@click.argument("tasks", nargs=-1, required=True)
@click.option("--model", "-m", default=None, help="Model to use")
@click.option("--auto-merge", is_flag=True, help="Automatically merge completed tasks")
@click.option("--quiet", "-q", is_flag=True, help="Hide progress output")
def swarm_run(tasks: tuple, model: str, auto_merge: bool, quiet: bool):
    """Run multiple tasks in parallel using git worktrees.

    Each task runs in its own worktree with a dedicated agent.
    Tasks can be merged after completion.

    Examples:
        emdash swarm run "Fix login bug" "Add logout button"
        emdash swarm run "Task 1" "Task 2" "Task 3" --auto-merge
    """
    server = get_server_manager()
    client = EmdashClient(server.get_server_url())
    renderer = SSERenderer(console=console, verbose=not quiet)

    try:
        console.print(f"[cyan]Starting swarm with {len(tasks)} tasks...[/cyan]")
        console.print()

        stream = client.swarm_run_stream(
            tasks=list(tasks),
            model=model,
            auto_merge=auto_merge,
        )
        renderer.render_stream(stream)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


@swarm.command("status")
def swarm_status():
    """Show status of current swarm execution."""
    server = get_server_manager()
    client = EmdashClient(server.get_server_url())

    try:
        status = client.swarm_status()

        if not status.get("active"):
            console.print("[dim]No active swarm execution[/dim]")
            return

        console.print("[bold]Swarm Status[/bold]")
        console.print()

        tasks = status.get("tasks", [])
        for task in tasks:
            task_status = task.get("status", "unknown")
            name = task.get("name", "Unknown task")

            if task_status == "completed":
                console.print(f"  [green]✓[/green] {name}")
            elif task_status == "running":
                console.print(f"  [cyan]⟳[/cyan] {name}")
            elif task_status == "failed":
                console.print(f"  [red]✗[/red] {name}")
            else:
                console.print(f"  [dim]○[/dim] {name}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()
