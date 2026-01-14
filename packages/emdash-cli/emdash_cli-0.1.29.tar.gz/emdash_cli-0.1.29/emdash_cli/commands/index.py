"""Index command - parse and index a codebase."""

import json
import os

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table

from ..client import EmdashClient
from ..server_manager import get_server_manager

console = Console()


@click.group()
def index():
    """Index a codebase into the knowledge graph."""
    pass


@index.command("start")
@click.argument("repo_path", required=False)
@click.option("--changed-only", is_flag=True, help="Only index changed files")
@click.option("--skip-git", is_flag=True, help="Skip git history indexing")
@click.option("--github-prs", default=0, help="Number of GitHub PRs to index")
@click.option("--detect-communities", is_flag=True, default=True, help="Run community detection")
@click.option("--describe-communities", is_flag=True, help="Use LLM to describe communities")
@click.option("--model", "-m", default=None, help="Model for community descriptions")
def index_start(
    repo_path: str | None,
    changed_only: bool,
    skip_git: bool,
    github_prs: int,
    detect_communities: bool,
    describe_communities: bool,
    model: str | None,
):
    """Index a repository into the knowledge graph.

    If REPO_PATH is not provided, indexes the current directory.

    Examples:
        emdash index start                    # Index current directory
        emdash index start /path/to/repo      # Index specific repo
        emdash index start --changed-only     # Only index changed files
        emdash index start --github-prs 50    # Also index 50 PRs
    """
    # Default to current directory
    if not repo_path:
        repo_path = os.getcwd()

    # Ensure server is running
    server = get_server_manager()
    client = EmdashClient(server.get_server_url())

    console.print(f"\n[bold cyan]Indexing[/bold cyan] {repo_path}\n")

    # Build options
    options = {
        "changed_only": changed_only,
        "index_git": not skip_git,
        "index_github": github_prs,
        "detect_communities": detect_communities,
        "describe_communities": describe_communities,
    }
    if model:
        options["model"] = model

    try:
        # Stream indexing progress with progress bar
        final_stats = {}

        with Progress(
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(bar_width=40, complete_style="cyan", finished_style="green"),
            TaskProgressColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Starting...", total=100)

            for line in client.index_start_stream(repo_path, changed_only):
                line = line.strip()
                if line.startswith("event: "):
                    continue
                if line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        step = data.get("step") or data.get("message", "")
                        percent = data.get("percent")

                        # Capture final stats from response event
                        if data.get("success") and data.get("stats"):
                            final_stats = data.get("stats", {})

                        if step:
                            progress.update(task, description=step)
                        if percent is not None:
                            progress.update(task, completed=percent)
                    except json.JSONDecodeError:
                        pass

            # Complete the progress bar
            progress.update(task, completed=100, description="Complete")

        # Show completion with sense of accomplishment
        _show_completion(repo_path, final_stats, client)

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise click.Abort()


def _show_completion(repo_path: str, stats: dict, client: EmdashClient) -> None:
    """Show a nice completion message with stats."""
    # If we don't have stats from the stream, fetch from status endpoint
    if not stats:
        try:
            status_data = client.index_status(repo_path)
            stats = {
                "files": status_data.get("file_count", 0),
                "functions": status_data.get("function_count", 0),
                "classes": status_data.get("class_count", 0),
                "communities": status_data.get("community_count", 0),
            }
        except Exception:
            stats = {}

    # Build completion message
    console.print()

    if stats:
        # Create a summary table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Label", style="dim")
        table.add_column("Value", style="bold")

        if stats.get("files"):
            table.add_row("Files", str(stats["files"]))
        if stats.get("functions"):
            table.add_row("Functions", str(stats["functions"]))
        if stats.get("classes"):
            table.add_row("Classes", str(stats["classes"]))
        if stats.get("communities"):
            table.add_row("Communities", str(stats["communities"]))

        panel = Panel(
            table,
            title="[bold green]Indexing Complete[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        console.print(panel)
    else:
        console.print("[bold green]Indexing complete![/bold green]")

    console.print()


@index.command("status")
@click.argument("repo_path", required=False)
def index_status(repo_path: str | None):
    """Show current indexing status.

    If REPO_PATH is not provided, checks the current directory.

    Example:
        emdash index status
        emdash index status /path/to/repo
    """
    # Default to current directory
    if not repo_path:
        repo_path = os.getcwd()

    server = get_server_manager()
    client = EmdashClient(server.get_server_url())

    try:
        status = client.index_status(repo_path)

        console.print("\n[bold]Index Status[/bold]")
        console.print(f"  Indexed: {'[green]Yes[/green]' if status.get('is_indexed') else '[yellow]No[/yellow]'}")

        if status.get("is_indexed"):
            console.print(f"  Files: {status.get('file_count', 0)}")
            console.print(f"  Functions: {status.get('function_count', 0)}")
            console.print(f"  Classes: {status.get('class_count', 0)}")
            console.print(f"  Communities: {status.get('community_count', 0)}")

            if status.get("last_indexed"):
                console.print(f"  Last indexed: {status.get('last_indexed')}")
            if status.get("last_commit"):
                console.print(f"  Last commit: {status.get('last_commit')}")

        console.print()

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise click.Abort()
