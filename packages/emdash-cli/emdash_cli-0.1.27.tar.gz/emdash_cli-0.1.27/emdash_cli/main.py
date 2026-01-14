"""Main CLI entry point for emdash-cli."""

import os

import click

from .commands import (
    agent,
    db,
    auth,
    analyze,
    embed,
    index,
    plan,
    rules,
    search,
    server,
    skills,
    team,
    swarm,
    projectmd,
    research,
    spec,
    tasks,
)


@click.group()
@click.version_option()
def cli():
    """EmDash - The 'Senior Engineer' Context Engine.

    A graph-based coding intelligence system powered by AI.
    """
    pass


# Register command groups
cli.add_command(agent)
cli.add_command(db)
cli.add_command(auth)
cli.add_command(analyze)
cli.add_command(embed)
cli.add_command(index)
cli.add_command(plan)
cli.add_command(rules)
cli.add_command(server)
cli.add_command(skills)
cli.add_command(team)
cli.add_command(swarm)

# Register standalone commands
cli.add_command(search)
cli.add_command(projectmd)
cli.add_command(research)
cli.add_command(spec)
cli.add_command(tasks)

# Add killall as top-level alias for server killall
from .commands.server import server_killall
cli.add_command(server_killall, name="killall")


# Direct entry point for `em` command - wraps agent_code with click
@click.command()
@click.argument("task", required=False)
@click.option("--model", "-m", default=None, help="Model to use")
@click.option("--mode", type=click.Choice(["plan", "tasks", "code"]), default="code",
              help="Starting mode")
@click.option("--quiet", "-q", is_flag=True, help="Less verbose output")
@click.option("--max-iterations", default=int(os.getenv("EMDASH_MAX_ITERATIONS", "100")), help="Max agent iterations")
@click.option("--no-graph-tools", is_flag=True, help="Skip graph exploration tools")
@click.option("--save", is_flag=True, help="Save specs to specs/<feature>/")
def start_coding_agent(
    task: str | None,
    model: str | None,
    mode: str,
    quiet: bool,
    max_iterations: int,
    no_graph_tools: bool,
    save: bool,
):
    """EmDash Coding Agent - AI-powered code assistant.

    Start interactive mode or run a single task.

    Examples:
        em                        # Interactive mode
        em "Fix the login bug"    # Single task
        em --mode plan            # Start in plan mode
    """
    # Import and call agent_code directly
    from .commands.agent import agent_code as _agent_code
    ctx = click.Context(_agent_code)
    ctx.invoke(
        _agent_code,
        task=task,
        model=model,
        mode=mode,
        quiet=quiet,
        max_iterations=max_iterations,
        no_graph_tools=no_graph_tools,
        save=save,
    )


if __name__ == "__main__":
    cli()
