"""SSE event renderer for Rich terminal output."""

import json
import sys
import time
import threading
from typing import Iterator, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text


# Spinner frames for loading animation
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class SSERenderer:
    """Renders SSE events to Rich terminal output with live updates.

    Features:
    - Animated spinner while tools execute
    - Special UI for spawning sub-agents
    - Clean, minimal output
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        verbose: bool = True,
    ):
        """Initialize the renderer.

        Args:
            console: Rich console to render to (creates one if not provided)
            verbose: Whether to show tool calls and progress
        """
        self.console = console or Console()
        self.verbose = verbose
        self._partial_response = ""
        self._session_id = None
        self._spec = None
        self._spec_submitted = False
        self._plan_submitted = None  # Plan data when submit_plan tool is called
        self._pending_clarification = None

        # Live display state
        self._current_tool = None
        self._tool_count = 0
        self._completed_tools: list[dict] = []
        self._spinner_idx = 0
        self._waiting_for_next = False

        # Sub-agent state (for inline updates)
        self._subagent_tool_count = 0
        self._subagent_current_tool = None

        # Spinner animation thread
        self._spinner_thread: Optional[threading.Thread] = None
        self._spinner_running = False
        self._spinner_message = "thinking"
        self._spinner_lock = threading.Lock()

        # Extended thinking storage
        self._last_thinking: Optional[str] = None

    def render_stream(
        self,
        lines: Iterator[str],
        interrupt_event: Optional[threading.Event] = None,
    ) -> dict:
        """Render SSE stream to terminal.

        Args:
            lines: Iterator of SSE lines from HTTP response
            interrupt_event: Optional event to signal interruption (e.g., ESC pressed)

        Returns:
            Dict with session_id, content, spec, interrupted flag, and other metadata
        """
        current_event = None
        final_response = ""
        interrupted = False
        self._last_thinking = None  # Reset thinking storage

        # Start spinner while waiting for first event
        if self.verbose:
            self._start_spinner("thinking")

        try:
            for line in lines:
                # Check for interrupt signal
                if interrupt_event and interrupt_event.is_set():
                    self._stop_spinner()
                    self.console.print("\n[yellow]Interrupted[/yellow]")
                    interrupted = True
                    break

                line = line.strip()

                if line.startswith("event: "):
                    current_event = line[7:]
                elif line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        # Ensure data is a dict (could be null/None from JSON)
                        if data is None:
                            data = {}
                        if current_event:
                            result = self._handle_event(current_event, data)
                            if result:
                                final_response = result
                    except json.JSONDecodeError:
                        pass
                elif line == ": ping":
                    # SSE keep-alive - ensure spinner is running
                    if self.verbose and not self._spinner_running:
                        self._start_spinner("waiting")
        finally:
            # Always stop spinner when stream ends
            self._stop_spinner()

        return {
            "content": final_response,
            "session_id": self._session_id,
            "spec": self._spec,
            "spec_submitted": self._spec_submitted,
            "plan_submitted": self._plan_submitted,
            "clarification": self._pending_clarification,
            "interrupted": interrupted,
            "thinking": self._last_thinking,
        }

    def _start_spinner(self, message: str = "thinking") -> None:
        """Start the animated spinner in a background thread."""
        if self._spinner_running:
            return

        self._spinner_message = message
        self._spinner_running = True
        self._spinner_thread = threading.Thread(target=self._spinner_loop, daemon=True)
        self._spinner_thread.start()

    def _stop_spinner(self) -> None:
        """Stop the spinner and clear the line."""
        if not self._spinner_running:
            return

        self._spinner_running = False
        if self._spinner_thread:
            self._spinner_thread.join(timeout=0.2)
            self._spinner_thread = None

        # Clear the spinner line
        with self._spinner_lock:
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()

    def _spinner_loop(self) -> None:
        """Background thread that animates the spinner."""
        while self._spinner_running:
            with self._spinner_lock:
                self._spinner_idx = (self._spinner_idx + 1) % len(SPINNER_FRAMES)
                spinner = SPINNER_FRAMES[self._spinner_idx]
                sys.stdout.write(f"\r  \033[33m{spinner}\033[0m \033[2m{self._spinner_message}...\033[0m")
                sys.stdout.flush()
            time.sleep(0.1)

    def _show_waiting(self) -> None:
        """Show waiting animation (starts spinner if not running)."""
        if not self._spinner_running:
            self._start_spinner("waiting")

    def _clear_waiting(self) -> None:
        """Clear waiting line (stops spinner)."""
        self._stop_spinner()
        self._waiting_for_next = False

    def _handle_event(self, event_type: str, data: dict) -> Optional[str]:
        """Handle individual SSE event."""
        # Ensure data is a dict
        if not isinstance(data, dict):
            data = {}

        # Clear waiting indicator when new event arrives
        self._clear_waiting()

        if event_type == "session_start":
            self._render_session_start(data)
        elif event_type == "tool_start":
            self._render_tool_start(data)
        elif event_type == "tool_result":
            self._render_tool_result(data)
            # Start spinner while waiting for next tool/response
            self._waiting_for_next = True
            if self.verbose:
                self._start_spinner("thinking")
        elif event_type == "thinking":
            self._render_thinking(data)
        elif event_type == "progress":
            self._render_progress(data)
        elif event_type == "partial_response":
            self._render_partial(data)
        elif event_type == "response":
            return self._render_response(data)
        elif event_type == "clarification":
            self._render_clarification(data)
        elif event_type == "plan_submitted":
            self._render_plan_submitted(data)
        elif event_type == "error":
            self._render_error(data)
        elif event_type == "warning":
            self._render_warning(data)
        elif event_type == "session_end":
            self._render_session_end(data)
        elif event_type == "context_frame":
            self._render_context_frame(data)

        return None

    def _render_session_start(self, data: dict) -> None:
        """Render session start event."""
        if data.get("session_id"):
            self._session_id = data["session_id"]

        if not self.verbose:
            return

        agent = data.get("agent_name", "Agent")
        model = data.get("model", "unknown")

        # Extract model name from full path
        if "/" in model:
            model = model.split("/")[-1]

        self.console.print()
        self.console.print(f"[bold cyan]{agent}[/bold cyan] [dim]({model})[/dim]")
        self._tool_count = 0
        self._completed_tools = []

    def _render_tool_start(self, data: dict) -> None:
        """Render tool start event."""
        if not self.verbose:
            return

        name = data.get("name", "unknown")
        args = data.get("args", {})
        subagent_id = data.get("subagent_id")
        subagent_type = data.get("subagent_type")

        self._tool_count += 1
        self._current_tool = {"name": name, "args": args, "start_time": time.time()}

        # Special handling for task tool (spawning sub-agents)
        if name == "task":
            self._render_agent_spawn_start(args)
            return

        # Sub-agent events: update in place on single line
        if subagent_id:
            self._subagent_tool_count += 1
            self._subagent_current_tool = name
            self._render_subagent_progress(subagent_type or "Agent", name, args)
            return

        # Format args summary (compact)
        args_summary = self._format_args_summary(args)

        # Show spinner with tool name
        spinner = SPINNER_FRAMES[0]
        self.console.print(
            f"  [dim]┃[/dim] [yellow]{spinner}[/yellow] [bold]{name}[/bold] {args_summary}",
            end="\r"
        )

    def _render_subagent_progress(self, agent_type: str, tool_name: str, args: dict) -> None:
        """Render sub-agent progress on a single updating line."""
        self._spinner_idx = (self._spinner_idx + 1) % len(SPINNER_FRAMES)
        spinner = SPINNER_FRAMES[self._spinner_idx]

        # Get a short summary of what's being done
        summary = ""
        if "path" in args:
            path = str(args["path"])
            # Shorten long paths
            if len(path) > 40:
                summary = "..." + path[-37:]
            else:
                summary = path
        elif "pattern" in args:
            summary = str(args["pattern"])[:30]

        # Clear line and show progress
        line = f"      [dim]│[/dim] [yellow]{spinner}[/yellow] [dim cyan]({agent_type})[/dim cyan] {self._subagent_tool_count} tools... [bold]{tool_name}[/bold] [dim]{summary}[/dim]"
        # Pad to clear previous content
        sys.stdout.write(f"\r{' ' * 120}\r")
        self.console.print(line, end="")

    def _render_agent_spawn_start(self, args: dict) -> None:
        """Render sub-agent spawn start with special UI."""
        agent_type = args.get("subagent_type", "Explore")
        description = args.get("description", "")
        prompt = args.get("prompt", "")

        # Reset sub-agent tracking
        self._subagent_tool_count = 0
        self._subagent_current_tool = None

        # Truncate prompt for display
        prompt_display = prompt[:60] + "..." if len(prompt) > 60 else prompt

        self.console.print()
        self.console.print(
            f"  [bold magenta]◆ Spawning {agent_type} Agent[/bold magenta]"
        )
        if description:
            self.console.print(f"    [dim]{description}[/dim]")
        self.console.print(f"    [cyan]→[/cyan] {prompt_display}")

    def _render_tool_result(self, data: dict) -> None:
        """Render tool result event."""
        name = data.get("name", "unknown")
        success = data.get("success", True)
        summary = data.get("summary")
        subagent_id = data.get("subagent_id")

        # Detect spec submission
        if name == "submit_spec" and success:
            self._spec_submitted = True
            spec_data = data.get("data", {})
            if spec_data:
                self._spec = spec_data.get("content")

        if not self.verbose:
            return

        # Special handling for task tool result
        if name == "task":
            self._render_agent_spawn_result(data)
            return

        # Sub-agent events: don't print result lines, just keep updating progress
        if subagent_id:
            # Progress is already shown by _render_tool_start, nothing to do here
            return

        # Calculate duration
        duration = ""
        if self._current_tool and self._current_tool.get("start_time"):
            elapsed = time.time() - self._current_tool["start_time"]
            if elapsed >= 0.1:
                duration = f" [dim]{elapsed:.1f}s[/dim]"

        args_summary = ""
        if self._current_tool:
            args_summary = self._format_args_summary(self._current_tool.get("args", {}))

        if success:
            status_icon = "[green]✓[/green]"
            result_text = f"[dim]{summary}[/dim]" if summary else ""
        else:
            status_icon = "[red]✗[/red]"
            result_text = f"[red]{summary}[/red]" if summary else "[red]failed[/red]"

        # Overwrite the spinner line
        self.console.print(
            f"  [dim]┃[/dim] {status_icon} [bold]{name}[/bold] {args_summary}{duration} {result_text}"
        )

        self._completed_tools.append({
            "name": name,
            "success": success,
            "summary": summary,
        })
        self._current_tool = None

    def _render_agent_spawn_result(self, data: dict) -> None:
        """Render sub-agent spawn result with special UI."""
        success = data.get("success", True)
        result_data = data.get("data") or {}

        # Clear the progress line
        sys.stdout.write(f"\r{' ' * 120}\r")
        sys.stdout.flush()

        # Calculate duration
        duration = ""
        if self._current_tool and self._current_tool.get("start_time"):
            elapsed = time.time() - self._current_tool["start_time"]
            duration = f" [dim]({elapsed:.1f}s)[/dim]"

        if success:
            agent_type = result_data.get("agent_type", "Agent")
            iterations = result_data.get("iterations", 0)
            files_count = len(result_data.get("files_explored", []))

            self.console.print(
                f"    [green]✓[/green] {agent_type} completed{duration}"
            )
            # Show stats using our tracked tool count
            stats = []
            if iterations > 0:
                stats.append(f"{iterations} turns")
            if files_count > 0:
                stats.append(f"{files_count} files")
            if self._subagent_tool_count > 0:
                stats.append(f"{self._subagent_tool_count} tools")
            if stats:
                self.console.print(f"    [dim]{' · '.join(stats)}[/dim]")
        else:
            error = result_data.get("error", data.get("summary", "failed"))
            self.console.print(f"    [red]✗[/red] Agent failed: {error}")

        self.console.print()
        self._current_tool = None
        self._subagent_tool_count = 0

    def _format_args_summary(self, args: dict) -> str:
        """Format args into a compact summary string."""
        if not args:
            return ""

        parts = []
        for k, v in list(args.items())[:2]:
            v_str = str(v)
            if len(v_str) > 40:
                v_str = v_str[:37] + "..."
            parts.append(f"[dim]{v_str}[/dim]")

        return " ".join(parts)

    def _render_thinking(self, data: dict) -> None:
        """Render thinking event.

        Handles both short progress messages and extended thinking content.
        """
        if not self.verbose:
            return

        message = data.get("message", "")

        # Check if this is extended thinking (long content) vs short progress message
        if len(message) > 200:
            # Extended thinking - show summary with collapsible indicator
            self._stop_spinner()
            lines = message.strip().split("\n")
            preview = lines[0][:80] + "..." if len(lines[0]) > 80 else lines[0]
            line_count = len(lines)
            char_count = len(message)

            self.console.print(f"  [dim]┃[/dim] [dim italic]💭 Thinking ({char_count:,} chars, {line_count} lines)[/dim italic]")
            self.console.print(f"  [dim]┃[/dim] [dim]   {preview}[/dim]")

            # Store thinking for potential later display
            self._last_thinking = message
        else:
            # Short progress message
            self.console.print(f"  [dim]┃[/dim] [dim italic]💭 {message}[/dim italic]")

    def _render_progress(self, data: dict) -> None:
        """Render progress event."""
        if not self.verbose:
            return

        message = data.get("message", "")
        percent = data.get("percent")

        if percent is not None:
            bar_width = 20
            filled = int(bar_width * percent / 100)
            bar = "█" * filled + "░" * (bar_width - filled)
            self.console.print(f"  [dim]┃[/dim] [dim]{bar} {percent:.0f}% {message}[/dim]")
        else:
            self.console.print(f"  [dim]┃[/dim] [dim]{message}[/dim]")

    def _render_partial(self, data: dict) -> None:
        """Render partial response (streaming text)."""
        content = data.get("content", "")
        self._partial_response += content

    def _render_response(self, data: dict) -> str:
        """Render final response."""
        content = data.get("content", "")

        self.console.print()
        self.console.print(Markdown(content))

        return content

    def _render_clarification(self, data: dict) -> None:
        """Render clarification request."""
        question = data.get("question", "")
        context = data.get("context", "")
        options = data.get("options", [])

        self.console.print()
        self.console.print(Panel(
            question,
            title="[yellow]❓ Question[/yellow]",
            border_style="yellow",
            padding=(0, 1),
        ))

        if options:
            for i, opt in enumerate(options, 1):
                self.console.print(f"  [yellow][{i}][/yellow] {opt}")
            self.console.print()

            self._pending_clarification = {
                "question": question,
                "context": context,
                "options": options,
            }
        else:
            self._pending_clarification = None

    def _render_plan_submitted(self, data: dict) -> None:
        """Render plan submission event and store for menu display."""
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text

        title = data.get("title", "Plan")
        summary = data.get("summary", "")
        files_to_modify = data.get("files_to_modify", [])
        implementation_steps = data.get("implementation_steps", [])
        risks = data.get("risks", [])
        testing_strategy = data.get("testing_strategy", "")

        # Store the plan data for the CLI to show the menu
        self._plan_submitted = data

        # Build plan display
        self.console.print()
        self.console.print(Panel(
            f"[bold]{title}[/bold]\n\n{summary}",
            title="[cyan]📋 Plan[/cyan]",
            border_style="cyan",
        ))

        # Critical Files table (always shown)
        if files_to_modify:
            files_table = Table(title="Critical Files", show_header=True, header_style="bold cyan")
            files_table.add_column("File", style="yellow")
            files_table.add_column("Lines", style="dim")
            files_table.add_column("Changes", style="white")

            for f in files_to_modify:
                if isinstance(f, dict):
                    files_table.add_row(
                        f.get("path", ""),
                        f.get("lines", ""),
                        f.get("changes", "")
                    )
                else:
                    files_table.add_row(str(f), "", "")

            self.console.print(files_table)

        # Implementation Steps (only if provided)
        if implementation_steps:
            self.console.print("\n[bold cyan]Implementation Steps[/bold cyan]")
            for i, step in enumerate(implementation_steps, 1):
                self.console.print(f"  [dim]{i}.[/dim] {step}")

        # Risks (only if provided)
        if risks:
            self.console.print("\n[bold yellow]⚠ Risks[/bold yellow]")
            for risk in risks:
                self.console.print(f"  [yellow]•[/yellow] {risk}")

        # Testing (only if provided)
        if testing_strategy:
            self.console.print(f"\n[bold green]Testing:[/bold green] {testing_strategy}")

        self.console.print()

    def _render_error(self, data: dict) -> None:
        """Render error event."""
        message = data.get("message", "Unknown error")
        details = data.get("details")

        self.console.print(f"\n[red bold]✗ Error:[/red bold] {message}")

        if details:
            self.console.print(f"[dim]{details}[/dim]")

    def _render_warning(self, data: dict) -> None:
        """Render warning event."""
        message = data.get("message", "")
        self.console.print(f"[yellow]⚠ {message}[/yellow]")

    def _render_session_end(self, data: dict) -> None:
        """Render session end event."""
        if not self.verbose:
            return

        success = data.get("success", True)
        if not success:
            error = data.get("error", "Unknown error")
            self.console.print(f"\n[red]Session ended with error: {error}[/red]")

    def _render_context_frame(self, data: dict) -> None:
        """Render context frame update (post-agentic loop summary)."""
        adding = data.get("adding") or {}
        reading = data.get("reading") or {}

        # Get stats from the adding data
        step_count = adding.get("step_count", 0)
        entities_found = adding.get("entities_found", 0)
        context_tokens = adding.get("context_tokens", 0)
        context_breakdown = adding.get("context_breakdown", {})

        # Get reading stats
        item_count = reading.get("item_count", 0)

        # Only show if there's something to report
        if step_count == 0 and item_count == 0 and context_tokens == 0:
            return

        self.console.print()
        self.console.print("[dim]───── Context Frame ─────[/dim]")

        # Show total context
        if context_tokens > 0:
            self.console.print(f"  [bold]Total: {context_tokens:,} tokens[/bold]")

        # Show breakdown
        if context_breakdown:
            breakdown_parts = []
            for key, tokens in context_breakdown.items():
                if tokens > 0:
                    breakdown_parts.append(f"{key}: {tokens:,}")
            if breakdown_parts:
                self.console.print(f"  [dim]Breakdown: {' | '.join(breakdown_parts)}[/dim]")

        # Show other stats
        stats = []
        if step_count > 0:
            stats.append(f"{step_count} steps")
        if entities_found > 0:
            stats.append(f"{entities_found} entities")
        if item_count > 0:
            stats.append(f"{item_count} context items")

        if stats:
            self.console.print(f"  [dim]{' · '.join(stats)}[/dim]")
