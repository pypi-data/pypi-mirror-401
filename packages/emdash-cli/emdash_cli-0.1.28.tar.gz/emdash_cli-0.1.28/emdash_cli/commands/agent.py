"""Agent CLI commands."""

import os
import threading

import click
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from ..client import EmdashClient
from ..keyboard import KeyListener
from ..server_manager import get_server_manager
from ..sse_renderer import SSERenderer

console = Console()


class AgentMode(Enum):
    """Agent operation modes."""
    PLAN = "plan"
    CODE = "code"


# Slash commands available in interactive mode
SLASH_COMMANDS = {
    # Mode switching
    "/plan": "Switch to plan mode (explore codebase, create plans)",
    "/code": "Switch to code mode (execute file changes)",
    "/mode": "Show current mode",
    # Generation commands
    "/pr [url]": "Review a pull request",
    "/projectmd": "Generate PROJECT.md for the codebase",
    "/research [goal]": "Deep research on a topic",
    # Status commands
    "/status": "Show index and PROJECT.md status",
    # Session management
    "/spec": "Show current specification",
    "/reset": "Reset session state",
    "/save": "Save current spec to disk",
    "/help": "Show available commands",
    "/quit": "Exit the agent",
}


@click.group()
def agent():
    """AI agent commands."""
    pass


@agent.command("code")
@click.argument("task", required=False)
@click.option("--model", "-m", default=None, help="Model to use")
@click.option("--mode", type=click.Choice(["plan", "code"]), default="code",
              help="Starting mode")
@click.option("--quiet", "-q", is_flag=True, help="Less verbose output")
@click.option("--max-iterations", default=int(os.getenv("EMDASH_MAX_ITERATIONS", "100")), help="Max agent iterations")
@click.option("--no-graph-tools", is_flag=True, help="Skip graph exploration tools")
@click.option("--save", is_flag=True, help="Save specs to specs/<feature>/")
def agent_code(
    task: str | None,
    model: str | None,
    mode: str,
    quiet: bool,
    max_iterations: int,
    no_graph_tools: bool,
    save: bool,
):
    """Start the coding agent.

    With TASK: Run single task and exit
    Without TASK: Start interactive REPL mode

    MODES:
      plan   - Explore codebase and create plans (read-only)
      code   - Execute code changes (default)

    SLASH COMMANDS (in interactive mode):
      /plan   - Switch to plan mode
      /code   - Switch to code mode
      /help   - Show available commands
      /reset  - Reset session

    Examples:
        emdash                                         # Interactive code mode
        emdash agent code                              # Same as above
        emdash agent code --mode plan                  # Start in plan mode
        emdash agent code "Fix the login bug"          # Single task
    """
    # Get server URL (starts server if needed)
    server = get_server_manager()
    base_url = server.get_server_url()

    client = EmdashClient(base_url)
    renderer = SSERenderer(console=console, verbose=not quiet)

    options = {
        "mode": mode,
        "no_graph_tools": no_graph_tools,
        "save": save,
    }

    if task:
        # Single task mode
        _run_single_task(client, renderer, task, model, max_iterations, options)
    else:
        # Interactive REPL mode
        _run_interactive(client, renderer, model, max_iterations, options)


def _get_clarification_response(clarification: dict) -> str | None:
    """Get user response for clarification with interactive selection.

    Args:
        clarification: Dict with question, context, and options

    Returns:
        User's selected option or typed response, or None if cancelled
    """
    from prompt_toolkit import Application, PromptSession
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl
    from prompt_toolkit.styles import Style

    options = clarification.get("options", [])

    if not options:
        # No options, just get free-form input
        session = PromptSession()
        try:
            return session.prompt("response > ").strip() or None
        except (KeyboardInterrupt, EOFError):
            return None

    selected_index = [0]
    result = [None]

    # Key bindings
    kb = KeyBindings()

    @kb.add("up")
    @kb.add("k")
    def move_up(event):
        selected_index[0] = (selected_index[0] - 1) % len(options)

    @kb.add("down")
    @kb.add("j")
    def move_down(event):
        selected_index[0] = (selected_index[0] + 1) % len(options)

    @kb.add("enter")
    def select(event):
        result[0] = options[selected_index[0]]
        event.app.exit()

    # Number key shortcuts (1-9)
    for i in range(min(9, len(options))):
        @kb.add(str(i + 1))
        def select_by_number(event, idx=i):
            result[0] = options[idx]
            event.app.exit()

    @kb.add("c-c")
    @kb.add("escape")
    def cancel(event):
        result[0] = None
        event.app.exit()

    @kb.add("o")  # 'o' for Other - custom input
    def other_input(event):
        result[0] = "OTHER_INPUT"
        event.app.exit()

    def get_formatted_options():
        lines = []
        for i, opt in enumerate(options):
            if i == selected_index[0]:
                lines.append(("class:selected", f"  ❯ [{i+1}] {opt}\n"))
            else:
                lines.append(("class:option", f"    [{i+1}] {opt}\n"))
        lines.append(("class:hint", "\n↑/↓ to move, Enter to select, 1-9 for quick select, o for other"))
        return lines

    # Style
    style = Style.from_dict({
        "selected": "#00cc66 bold",
        "option": "#888888",
        "hint": "#444444 italic",
    })

    # Calculate height based on options
    height = len(options) + 2  # options + hint line + padding

    # Layout
    layout = Layout(
        HSplit([
            Window(
                FormattedTextControl(get_formatted_options),
                height=height,
            ),
        ])
    )

    # Application
    app = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=False,
    )

    console.print()

    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        return None

    # Handle "other" option - get custom input
    if result[0] == "OTHER_INPUT":
        session = PromptSession()
        console.print()
        try:
            return session.prompt("response > ").strip() or None
        except (KeyboardInterrupt, EOFError):
            return None

    # Check if selected option is an "other/explain" type that needs text input
    if result[0]:
        lower_result = result[0].lower()
        needs_input = any(phrase in lower_result for phrase in [
            "something else",
            "other",
            "i'll explain",
            "i will explain",
            "let me explain",
            "custom",
            "none of the above",
        ])
        if needs_input:
            session = PromptSession()
            console.print()
            console.print("[dim]Please explain:[/dim]")
            try:
                custom_input = session.prompt("response > ").strip()
                if custom_input:
                    return custom_input
            except (KeyboardInterrupt, EOFError):
                return None

    return result[0]


def _show_plan_approval_menu() -> tuple[str, str]:
    """Show plan approval menu with simple approve/reject options.

    Returns:
        Tuple of (choice, feedback) where feedback is only set for 'reject'
    """
    from prompt_toolkit import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl
    from prompt_toolkit.styles import Style

    options = [
        ("approve", "Approve and start implementation"),
        ("reject", "Reject and provide feedback"),
    ]

    selected_index = [0]  # Use list to allow mutation in closure
    result = [None]

    # Key bindings
    kb = KeyBindings()

    @kb.add("up")
    @kb.add("k")
    def move_up(event):
        selected_index[0] = (selected_index[0] - 1) % len(options)

    @kb.add("down")
    @kb.add("j")
    def move_down(event):
        selected_index[0] = (selected_index[0] + 1) % len(options)

    @kb.add("enter")
    def select(event):
        result[0] = options[selected_index[0]][0]
        event.app.exit()

    @kb.add("1")
    @kb.add("y")
    def select_approve(event):
        result[0] = "approve"
        event.app.exit()

    @kb.add("2")
    @kb.add("n")
    def select_reject(event):
        result[0] = "reject"
        event.app.exit()

    @kb.add("c-c")
    @kb.add("q")
    @kb.add("escape")
    def cancel(event):
        result[0] = "reject"
        event.app.exit()

    def get_formatted_options():
        lines = [("class:title", "Approve this plan?\n\n")]
        for i, (key, desc) in enumerate(options):
            if i == selected_index[0]:
                lines.append(("class:selected", f"  ❯ {key:8} "))
                lines.append(("class:selected-desc", f"- {desc}\n"))
            else:
                lines.append(("class:option", f"    {key:8} "))
                lines.append(("class:desc", f"- {desc}\n"))
        lines.append(("class:hint", "\n↑/↓ to move, Enter to select, y/n for quick select"))
        return lines

    # Style
    style = Style.from_dict({
        "title": "#00ccff bold",
        "selected": "#00cc66 bold",
        "selected-desc": "#00cc66",
        "option": "#888888",
        "desc": "#666666",
        "hint": "#444444 italic",
    })

    # Layout
    layout = Layout(
        HSplit([
            Window(
                FormattedTextControl(get_formatted_options),
                height=6,
            ),
        ])
    )

    # Application
    app = Application(
        layout=layout,
        key_bindings=kb,
        style=style,
        full_screen=False,
    )

    console.print()

    try:
        app.run()
    except (KeyboardInterrupt, EOFError):
        result[0] = "reject"

    choice = result[0] or "reject"

    # Get feedback if reject was chosen
    feedback = ""
    if choice == "reject":
        from prompt_toolkit import PromptSession
        console.print()
        console.print("[dim]What changes would you like?[/dim]")
        try:
            session = PromptSession()
            feedback = session.prompt("feedback > ").strip()
        except (KeyboardInterrupt, EOFError):
            return "reject", ""

    return choice, feedback


def _render_with_interrupt(renderer: SSERenderer, stream) -> dict:
    """Render stream with ESC key interrupt support.

    Args:
        renderer: SSE renderer instance
        stream: SSE stream iterator

    Returns:
        Result dict from renderer, with 'interrupted' flag
    """
    interrupt_event = threading.Event()

    def on_escape():
        interrupt_event.set()

    listener = KeyListener(on_escape)

    try:
        listener.start()
        result = renderer.render_stream(stream, interrupt_event=interrupt_event)
        return result
    finally:
        listener.stop()


def _run_single_task(
    client: EmdashClient,
    renderer: SSERenderer,
    task: str,
    model: str | None,
    max_iterations: int,
    options: dict,
):
    """Run a single agent task."""
    try:
        stream = client.agent_chat_stream(
            message=task,
            model=model,
            max_iterations=max_iterations,
            options=options,
        )
        result = _render_with_interrupt(renderer, stream)
        if result.get("interrupted"):
            console.print("[dim]Task interrupted. You can continue or start a new task.[/dim]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


def _run_slash_command_task(
    client: EmdashClient,
    renderer: SSERenderer,
    model: str | None,
    max_iterations: int,
    task: str,
    options: dict,
):
    """Run a task from a slash command."""
    try:
        stream = client.agent_chat_stream(
            message=task,
            model=model,
            max_iterations=max_iterations,
            options=options,
        )
        result = _render_with_interrupt(renderer, stream)
        if result.get("interrupted"):
            console.print("[dim]Task interrupted.[/dim]")
        console.print()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def _run_interactive(
    client: EmdashClient,
    renderer: SSERenderer,
    model: str | None,
    max_iterations: int,
    options: dict,
):
    """Run interactive REPL mode with slash commands."""
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
    from pathlib import Path

    # Current mode
    current_mode = AgentMode(options.get("mode", "code"))
    session_id = None
    current_spec = None
    # Attached images for next message
    attached_images: list[dict] = []

    # Style for prompt
    PROMPT_STYLE = Style.from_dict({
        "prompt.mode.plan": "#ffcc00 bold",
        "prompt.mode.code": "#00cc66 bold",
        "prompt.prefix": "#888888",
        "prompt.image": "#00ccff",
        "completion-menu": "bg:#1a1a2e #ffffff",
        "completion-menu.completion": "bg:#1a1a2e #ffffff",
        "completion-menu.completion.current": "bg:#4a4a6e #ffffff bold",
        "completion-menu.meta.completion": "bg:#1a1a2e #888888",
        "completion-menu.meta.completion.current": "bg:#4a4a6e #aaaaaa",
        "command": "#00ccff bold",
    })

    class SlashCommandCompleter(Completer):
        """Completer for slash commands."""

        def get_completions(self, document, complete_event):
            text = document.text_before_cursor
            if not text.startswith("/"):
                return
            for cmd, description in SLASH_COMMANDS.items():
                # Extract base command (e.g., "/pr" from "/pr [url]")
                base_cmd = cmd.split()[0]
                if base_cmd.startswith(text):
                    yield Completion(
                        base_cmd,
                        start_position=-len(text),
                        display=cmd,
                        display_meta=description,
                    )

    # Setup history file
    history_file = Path.home() / ".emdash" / "cli_history"
    history_file.parent.mkdir(parents=True, exist_ok=True)
    history = FileHistory(str(history_file))

    # Key bindings: Enter submits, Alt+Enter inserts newline
    # Note: Shift+Enter is indistinguishable from Enter in most terminals
    kb = KeyBindings()

    @kb.add("enter")
    def submit_on_enter(event):
        """Submit on Enter."""
        event.current_buffer.validate_and_handle()

    @kb.add("escape", "enter")  # Alt+Enter (Escape then Enter)
    @kb.add("c-j")  # Ctrl+J as alternative for newline
    def insert_newline_alt(event):
        """Insert a newline character with Alt+Enter or Ctrl+J."""
        event.current_buffer.insert_text("\n")

    @kb.add("c-v")  # Ctrl+V to paste (check for images)
    def paste_with_image_check(event):
        """Paste text or attach image from clipboard."""
        nonlocal attached_images
        from ..clipboard import get_clipboard_image

        # Try to get image from clipboard
        image_data = get_clipboard_image()
        if image_data:
            base64_data, img_format = image_data
            attached_images.append({"data": base64_data, "format": img_format})
            console.print(f"[green]📎 Image attached[/green] [dim]({img_format})[/dim]")
        else:
            # No image, do normal paste
            event.current_buffer.paste_clipboard_data(event.app.clipboard.get_data())

    session = PromptSession(
        history=history,
        completer=SlashCommandCompleter(),
        style=PROMPT_STYLE,
        complete_while_typing=True,
        multiline=True,
        prompt_continuation="... ",
        key_bindings=kb,
    )

    def get_prompt():
        """Get formatted prompt."""
        nonlocal attached_images
        parts = []
        # Add image indicator if images attached
        if attached_images:
            parts.append(("class:prompt.image", f"📎{len(attached_images)} "))
        parts.append(("class:prompt.prefix", "> "))
        return parts

    def show_help():
        """Show available commands."""
        console.print()
        console.print("[bold cyan]Available Commands[/bold cyan]")
        console.print()
        for cmd, desc in SLASH_COMMANDS.items():
            console.print(f"  [cyan]{cmd:12}[/cyan] {desc}")
        console.print()
        console.print("[dim]Type your task or question to interact with the agent.[/dim]")
        console.print()

    def handle_slash_command(cmd: str) -> bool:
        """Handle a slash command. Returns True if should continue, False to exit."""
        nonlocal current_mode, session_id, current_spec

        cmd_parts = cmd.strip().split(maxsplit=1)
        command = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""

        if command == "/quit" or command == "/exit" or command == "/q":
            return False

        elif command == "/help":
            show_help()

        elif command == "/plan":
            current_mode = AgentMode.PLAN
            console.print("[yellow]Switched to plan mode[/yellow]")

        elif command == "/code":
            current_mode = AgentMode.CODE
            console.print("[green]Switched to code mode[/green]")

        elif command == "/mode":
            console.print(f"Current mode: [bold]{current_mode.value}[/bold]")

        elif command == "/reset":
            session_id = None
            current_spec = None
            console.print("[dim]Session reset[/dim]")

        elif command == "/spec":
            if current_spec:
                console.print(Panel(Markdown(current_spec), title="Current Spec"))
            else:
                console.print("[dim]No spec available. Use plan mode to create one.[/dim]")

        elif command == "/save":
            if current_spec:
                # TODO: Save spec via API
                console.print("[yellow]Save not implemented yet[/yellow]")
            else:
                console.print("[dim]No spec to save[/dim]")

        elif command == "/pr":
            # PR review
            if not args:
                console.print("[yellow]Usage: /pr <pr-url-or-number>[/yellow]")
                console.print("[dim]Example: /pr 123 or /pr https://github.com/org/repo/pull/123[/dim]")
            else:
                console.print(f"[cyan]Reviewing PR: {args}[/cyan]")
                _run_slash_command_task(
                    client, renderer, model, max_iterations,
                    f"Review this pull request and provide feedback: {args}",
                    {"mode": "code"}
                )

        elif command == "/projectmd":
            # Generate PROJECT.md
            console.print("[cyan]Generating PROJECT.md...[/cyan]")
            _run_slash_command_task(
                client, renderer, model, max_iterations,
                "Analyze this codebase and generate a comprehensive PROJECT.md file that describes the architecture, main components, how to get started, and key design decisions.",
                {"mode": "code"}
            )

        elif command == "/research":
            # Deep research
            if not args:
                console.print("[yellow]Usage: /research <goal>[/yellow]")
                console.print("[dim]Example: /research How does authentication work in this codebase?[/dim]")
            else:
                console.print(f"[cyan]Researching: {args}[/cyan]")
                _run_slash_command_task(
                    client, renderer, model, 50,  # More iterations for research
                    f"Conduct deep research on: {args}\n\nExplore the codebase thoroughly, analyze relevant code, and provide a comprehensive answer with references to specific files and functions.",
                    {"mode": "plan"}  # Use plan mode for research
                )

        elif command == "/status":
            # Show index and PROJECT.md status
            from datetime import datetime

            console.print("\n[bold cyan]Status[/bold cyan]\n")

            # Index status
            console.print("[bold]Index Status[/bold]")
            try:
                status = client.index_status(str(Path.cwd()))
                is_indexed = status.get("is_indexed", False)
                console.print(f"  Indexed: {'[green]Yes[/green]' if is_indexed else '[yellow]No[/yellow]'}")

                if is_indexed:
                    console.print(f"  Files: {status.get('file_count', 0)}")
                    console.print(f"  Functions: {status.get('function_count', 0)}")
                    console.print(f"  Classes: {status.get('class_count', 0)}")
                    console.print(f"  Communities: {status.get('community_count', 0)}")
                    if status.get("last_indexed"):
                        console.print(f"  Last indexed: {status.get('last_indexed')}")
                    if status.get("last_commit"):
                        console.print(f"  Last commit: {status.get('last_commit')}")
            except Exception as e:
                console.print(f"  [red]Error fetching index status: {e}[/red]")

            console.print()

            # PROJECT.md status
            console.print("[bold]PROJECT.md Status[/bold]")
            projectmd_path = Path.cwd() / "PROJECT.md"
            if projectmd_path.exists():
                stat = projectmd_path.stat()
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                size_kb = stat.st_size / 1024
                console.print(f"  Exists: [green]Yes[/green]")
                console.print(f"  Path: {projectmd_path}")
                console.print(f"  Size: {size_kb:.1f} KB")
                console.print(f"  Last modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                console.print(f"  Exists: [yellow]No[/yellow]")
                console.print("[dim]  Run /projectmd to generate it[/dim]")

            console.print()

        else:
            console.print(f"[yellow]Unknown command: {command}[/yellow]")
            console.print("[dim]Type /help for available commands[/dim]")

        return True

    # Show welcome message
    from .. import __version__
    import subprocess

    # Get current working directory
    cwd = Path.cwd()

    # Get git repo name (if in a git repo)
    git_repo = None
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=cwd
        )
        if result.returncode == 0:
            git_repo = Path(result.stdout.strip()).name
    except Exception:
        pass

    console.print()

    while True:
        try:
            # Get user input
            user_input = session.prompt(get_prompt()).strip()

            if not user_input:
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                if not handle_slash_command(user_input):
                    break
                continue

            # Handle quit shortcuts
            if user_input.lower() in ("quit", "exit", "q"):
                break

            # Build options with current mode
            request_options = {
                **options,
                "mode": current_mode.value,
            }

            # Run agent with current mode
            try:
                # Prepare images for API call
                images_to_send = attached_images if attached_images else None

                if session_id:
                    stream = client.agent_continue_stream(
                        session_id, user_input, images=images_to_send
                    )
                else:
                    stream = client.agent_chat_stream(
                        message=user_input,
                        model=model,
                        max_iterations=max_iterations,
                        options=request_options,
                        images=images_to_send,
                    )

                # Clear attached images after sending
                attached_images = []

                # Render the stream and capture any spec output
                result = _render_with_interrupt(renderer, stream)

                # Check if we got a session ID back
                if result and result.get("session_id"):
                    session_id = result["session_id"]

                # Check for spec output
                if result and result.get("spec"):
                    current_spec = result["spec"]

                # Handle clarification with options (interactive selection)
                clarification = result.get("clarification")
                if clarification and clarification.get("options") and session_id:
                    response = _get_clarification_response(clarification)
                    if response:
                        # Continue session with user's choice
                        stream = client.agent_continue_stream(session_id, response)
                        result = _render_with_interrupt(renderer, stream)

                        # Update mode if user chose code
                        if "code" in response.lower():
                            current_mode = AgentMode.CODE

                # Handle plan mode completion (show approval menu)
                # Only show menu when agent explicitly submits a plan via exit_plan tool
                content = result.get("content", "")
                plan_submitted = result.get("plan_submitted")
                should_show_plan_menu = (
                    current_mode == AgentMode.PLAN and
                    session_id and
                    plan_submitted is not None  # Agent called exit_plan tool
                )
                if should_show_plan_menu:
                    choice, feedback = _show_plan_approval_menu()

                    if choice == "approve":
                        current_mode = AgentMode.CODE
                        # Reset mode state to CODE
                        from emdash_core.agent.tools.modes import ModeState, AgentMode as CoreMode
                        ModeState.get_instance().current_mode = CoreMode.CODE
                        stream = client.agent_continue_stream(
                            session_id,
                            "The plan has been approved. Start implementing it now."
                        )
                        _render_with_interrupt(renderer, stream)
                    elif choice == "reject":
                        if feedback:
                            stream = client.agent_continue_stream(
                                session_id,
                                f"The plan was rejected. Please revise based on this feedback: {feedback}"
                            )
                            _render_with_interrupt(renderer, stream)
                        else:
                            console.print("[dim]Plan rejected[/dim]")
                            session_id = None
                            current_spec = None

                console.print()

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted[/dim]")
            break
        except EOFError:
            break


@agent.command("sessions")
def list_sessions():
    """List active agent sessions."""
    server = get_server_manager()
    base_url = server.get_server_url()

    client = EmdashClient(base_url)
    sessions = client.list_sessions()

    if not sessions:
        console.print("[dim]No active sessions[/dim]")
        return

    for s in sessions:
        console.print(
            f"  {s['session_id'][:8]}... "
            f"[dim]({s.get('model', 'unknown')}, "
            f"{s.get('message_count', 0)} messages)[/dim]"
        )
