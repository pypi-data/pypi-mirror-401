"""
CLI for zwarm orchestration.

Commands:
- zwarm orchestrate: Start an orchestrator session
- zwarm exec: Run a single executor directly (for testing)
- zwarm status: Show current state
- zwarm history: Show event history
- zwarm configs: Manage configurations
"""

from __future__ import annotations

import asyncio
import sys
from enum import Enum
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Create console for rich output
console = Console()


def _resolve_task(task: str | None, task_file: Path | None) -> str | None:
    """
    Resolve task from multiple sources (priority order):
    1. --task flag
    2. --task-file flag
    3. stdin (if not a tty)
    """
    # Direct task takes priority
    if task:
        return task

    # Then file
    if task_file:
        if not task_file.exists():
            console.print(f"[red]Error:[/] Task file not found: {task_file}")
            raise typer.Exit(1)
        return task_file.read_text().strip()

    # Finally stdin (only if piped, not interactive)
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read().strip()
        if stdin_content:
            return stdin_content

    return None

# Main app with rich help
app = typer.Typer(
    name="zwarm",
    help="""
[bold cyan]zwarm[/] - Multi-Agent CLI Orchestration Research Platform

[bold]DESCRIPTION[/]
    Orchestrate multiple CLI coding agents (Codex, Claude Code) with
    delegation, conversation, and trajectory alignment (watchers).

[bold]QUICK START[/]
    [dim]# Test an executor directly[/]
    $ zwarm exec --task "What is 2+2?"

    [dim]# Run the orchestrator[/]
    $ zwarm orchestrate --task "Build a hello world function"

    [dim]# Check state after running[/]
    $ zwarm status

[bold]COMMANDS[/]
    [cyan]orchestrate[/]  Start orchestrator to delegate tasks to executors
    [cyan]exec[/]         Run a single executor directly (for testing)
    [cyan]status[/]       Show current state (sessions, tasks, events)
    [cyan]history[/]      Show event history log
    [cyan]configs[/]      Manage configuration files

[bold]CONFIGURATION[/]
    Create [cyan]config.toml[/] or use [cyan]--config[/] flag with YAML files.
    See [cyan]zwarm configs list[/] for available configurations.

[bold]ADAPTERS[/]
    [cyan]codex_mcp[/]    Codex via MCP server (sync conversations)
    [cyan]claude_code[/]  Claude Code CLI

[bold]WATCHERS[/] (trajectory aligners)
    [cyan]progress[/]     Detects stuck/spinning agents
    [cyan]budget[/]       Monitors step/session limits
    [cyan]scope[/]        Detects scope creep
    [cyan]pattern[/]      Custom regex pattern matching
    [cyan]quality[/]      Code quality checks
    """,
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
)

# Configs subcommand group
configs_app = typer.Typer(
    name="configs",
    help="""
Manage zwarm configurations.

[bold]SUBCOMMANDS[/]
    [cyan]list[/]   List available configuration files
    [cyan]show[/]   Display a configuration file's contents
    """,
    rich_markup_mode="rich",
    no_args_is_help=True,
)
app.add_typer(configs_app, name="configs")


class AdapterType(str, Enum):
    codex_mcp = "codex_mcp"
    claude_code = "claude_code"


class ModeType(str, Enum):
    sync = "sync"
    async_ = "async"


@app.command()
def orchestrate(
    task: Annotated[Optional[str], typer.Option("--task", "-t", help="The task to accomplish")] = None,
    task_file: Annotated[Optional[Path], typer.Option("--task-file", "-f", help="Read task from file")] = None,
    config: Annotated[Optional[Path], typer.Option("--config", "-c", help="Path to config YAML")] = None,
    overrides: Annotated[Optional[list[str]], typer.Option("--set", help="Override config (key=value)")] = None,
    working_dir: Annotated[Path, typer.Option("--working-dir", "-w", help="Working directory")] = Path("."),
    resume: Annotated[bool, typer.Option("--resume", help="Resume from previous state")] = False,
    max_steps: Annotated[Optional[int], typer.Option("--max-steps", help="Maximum orchestrator steps")] = None,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show detailed output")] = False,
):
    """
    Start an orchestrator session.

    The orchestrator breaks down tasks and delegates to executor agents
    (Codex, Claude Code). It can have sync conversations or fire-and-forget
    async delegations.

    [bold]Examples:[/]
        [dim]# Simple task[/]
        $ zwarm orchestrate --task "Add a logout button to the navbar"

        [dim]# Task from file[/]
        $ zwarm orchestrate -f task.md

        [dim]# Task from stdin[/]
        $ cat task.md | zwarm orchestrate
        $ zwarm orchestrate < task.md

        [dim]# With config file[/]
        $ zwarm orchestrate -c configs/base.yaml --task "Refactor auth"

        [dim]# Override settings[/]
        $ zwarm orchestrate --task "Fix bug" --set executor.adapter=claude_code

        [dim]# Resume interrupted session[/]
        $ zwarm orchestrate --task "Continue work" --resume
    """
    from zwarm.orchestrator import build_orchestrator

    # Resolve task from: --task, --task-file, or stdin
    resolved_task = _resolve_task(task, task_file)
    if not resolved_task:
        console.print("[red]Error:[/] No task provided. Use --task, --task-file, or pipe from stdin.")
        raise typer.Exit(1)

    task = resolved_task

    # Build overrides list
    override_list = list(overrides or [])
    if max_steps:
        override_list.append(f"orchestrator.max_steps={max_steps}")

    console.print(f"[bold]Starting orchestrator...[/]")
    console.print(f"  Task: {task}")
    console.print(f"  Working dir: {working_dir.absolute()}")
    console.print()

    # Output handler to show orchestrator messages
    def output_handler(msg: str) -> None:
        if msg.strip():
            console.print(f"[dim][orchestrator][/] {msg}")

    orchestrator = None
    try:
        orchestrator = build_orchestrator(
            config_path=config,
            task=task,
            working_dir=working_dir.absolute(),
            overrides=override_list,
            resume=resume,
            output_handler=output_handler,
        )

        if resume:
            console.print("  [dim]Resuming from previous state...[/]")

        # Run the orchestrator loop
        console.print("[bold]--- Orchestrator running ---[/]\n")
        result = orchestrator.run(task=task)

        console.print(f"\n[bold green]--- Orchestrator finished ---[/]")
        console.print(f"  Steps: {result.get('steps', 'unknown')}")

        # Show exit message if any
        exit_msg = getattr(orchestrator, "_exit_message", "")
        if exit_msg:
            console.print(f"  Exit: {exit_msg[:200]}")

        # Save state for potential resume
        orchestrator.save_state()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted.[/]")
        if orchestrator:
            orchestrator.save_state()
            console.print("[dim]State saved. Use --resume to continue.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/] {e}")
        if verbose:
            console.print_exception()
        sys.exit(1)


@app.command()
def exec(
    task: Annotated[str, typer.Option("--task", "-t", help="Task to execute")],
    adapter: Annotated[AdapterType, typer.Option("--adapter", "-a", help="Executor adapter")] = AdapterType.codex_mcp,
    mode: Annotated[ModeType, typer.Option("--mode", "-m", help="Execution mode")] = ModeType.sync,
    working_dir: Annotated[Path, typer.Option("--working-dir", "-w", help="Working directory")] = Path("."),
    model: Annotated[Optional[str], typer.Option("--model", help="Model override")] = None,
):
    """
    Run a single executor directly (for testing).

    Useful for testing adapters without the full orchestrator loop.

    [bold]Examples:[/]
        [dim]# Test Codex[/]
        $ zwarm exec --task "What is 2+2?"

        [dim]# Test Claude Code[/]
        $ zwarm exec -a claude_code --task "List files in current dir"

        [dim]# Async mode[/]
        $ zwarm exec --task "Build feature" --mode async
    """
    from zwarm.adapters.codex_mcp import CodexMCPAdapter
    from zwarm.adapters.claude_code import ClaudeCodeAdapter

    console.print(f"[bold]Running executor directly...[/]")
    console.print(f"  Adapter: [cyan]{adapter.value}[/]")
    console.print(f"  Mode: {mode.value}")
    console.print(f"  Task: {task}")

    if adapter == AdapterType.codex_mcp:
        executor = CodexMCPAdapter()
    elif adapter == AdapterType.claude_code:
        executor = ClaudeCodeAdapter(model=model)
    else:
        console.print(f"[red]Unknown adapter:[/] {adapter}")
        sys.exit(1)

    async def run():
        try:
            session = await executor.start_session(
                task=task,
                working_dir=working_dir.absolute(),
                mode=mode.value,
                model=model,
            )

            console.print(f"\n[green]Session started:[/] {session.id[:8]}")

            if mode == ModeType.sync:
                response = session.messages[-1].content if session.messages else "(no response)"
                console.print(f"\n[bold]Response:[/]\n{response}")

                # Interactive loop for sync mode
                while True:
                    try:
                        user_input = console.input("\n[dim]> (type message or 'exit')[/] ")
                        if user_input.lower() == "exit" or not user_input:
                            break

                        response = await executor.send_message(session, user_input)
                        console.print(f"\n[bold]Response:[/]\n{response}")
                    except KeyboardInterrupt:
                        break
            else:
                console.print("[dim]Async mode - session running in background.[/]")
                console.print("Use 'zwarm status' to check progress.")

        finally:
            await executor.cleanup()

    asyncio.run(run())


@app.command()
def status(
    working_dir: Annotated[Path, typer.Option("--working-dir", "-w", help="Working directory")] = Path("."),
):
    """
    Show current state (sessions, tasks, events).

    Displays active sessions, pending tasks, and recent events
    from the .zwarm state directory.

    [bold]Example:[/]
        $ zwarm status
    """
    from zwarm.core.state import StateManager

    state_dir = working_dir / ".zwarm"
    if not state_dir.exists():
        console.print("[yellow]No zwarm state found in this directory.[/]")
        console.print("[dim]Run 'zwarm orchestrate' to start.[/]")
        return

    state = StateManager(state_dir)
    state.load()

    # Sessions table
    sessions = state.list_sessions()
    console.print(f"\n[bold]Sessions[/] ({len(sessions)})")
    if sessions:
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID", style="dim")
        table.add_column("Mode")
        table.add_column("Status")
        table.add_column("Task")

        for s in sessions:
            status_style = {"active": "green", "completed": "blue", "failed": "red"}.get(s.status.value, "white")
            table.add_row(
                s.id[:8],
                s.mode.value,
                f"[{status_style}]{s.status.value}[/]",
                s.task_description[:50] + "..." if len(s.task_description) > 50 else s.task_description,
            )
        console.print(table)
    else:
        console.print("  [dim](none)[/]")

    # Tasks table
    tasks = state.list_tasks()
    console.print(f"\n[bold]Tasks[/] ({len(tasks)})")
    if tasks:
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID", style="dim")
        table.add_column("Status")
        table.add_column("Description")

        for t in tasks:
            status_style = {"pending": "yellow", "in_progress": "cyan", "completed": "green", "failed": "red"}.get(t.status.value, "white")
            table.add_row(
                t.id[:8],
                f"[{status_style}]{t.status.value}[/]",
                t.description[:50] + "..." if len(t.description) > 50 else t.description,
            )
        console.print(table)
    else:
        console.print("  [dim](none)[/]")

    # Recent events
    events = state.get_events(limit=5)
    console.print(f"\n[bold]Recent Events[/]")
    if events:
        for e in events:
            console.print(f"  [dim]{e.timestamp.strftime('%H:%M:%S')}[/] {e.kind}")
    else:
        console.print("  [dim](none)[/]")


@app.command()
def history(
    working_dir: Annotated[Path, typer.Option("--working-dir", "-w", help="Working directory")] = Path("."),
    kind: Annotated[Optional[str], typer.Option("--kind", "-k", help="Filter by event kind")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n", help="Number of events")] = 20,
):
    """
    Show event history.

    Displays the append-only event log with timestamps and details.

    [bold]Examples:[/]
        [dim]# Show last 20 events[/]
        $ zwarm history

        [dim]# Show more events[/]
        $ zwarm history --limit 50

        [dim]# Filter by kind[/]
        $ zwarm history --kind session_started
    """
    from zwarm.core.state import StateManager

    state_dir = working_dir / ".zwarm"
    if not state_dir.exists():
        console.print("[yellow]No zwarm state found.[/]")
        return

    state = StateManager(state_dir)
    events = state.get_events(kind=kind, limit=limit)

    console.print(f"\n[bold]Event History[/] (last {limit})\n")

    if not events:
        console.print("[dim]No events found.[/]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Time", style="dim")
    table.add_column("Event")
    table.add_column("Session/Task")
    table.add_column("Details")

    for e in events:
        details = ""
        if e.payload:
            details = ", ".join(f"{k}={str(v)[:30]}" for k, v in list(e.payload.items())[:2])

        table.add_row(
            e.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            e.kind,
            (e.session_id or e.task_id or "-")[:8],
            details[:60],
        )

    console.print(table)


@configs_app.command("list")
def configs_list(
    config_dir: Annotated[Optional[Path], typer.Option("--dir", "-d", help="Directory to search")] = None,
):
    """
    List available agent/experiment configuration files (YAML).

    Note: config.toml is for user environment settings and is loaded
    automatically - use YAML files for agent configurations.

    [bold]Example:[/]
        $ zwarm configs list
    """
    search_dirs = [
        config_dir or Path.cwd(),
        Path.cwd() / "configs",
        Path.cwd() / ".zwarm",
    ]

    console.print("\n[bold]Available Configurations[/]\n")
    found = False

    for d in search_dirs:
        if not d.exists():
            continue
        for pattern in ["*.yaml", "*.yml"]:
            for f in d.glob(pattern):
                found = True
                try:
                    rel = f.relative_to(Path.cwd())
                    console.print(f"  [cyan]{rel}[/]")
                except ValueError:
                    console.print(f"  [cyan]{f}[/]")

    if not found:
        console.print("  [dim]No configuration files found.[/]")
        console.print("\n  [dim]Create a YAML config in configs/ to get started.[/]")

    # Check for config.toml and mention it
    config_toml = Path.cwd() / "config.toml"
    if config_toml.exists():
        console.print(f"\n[dim]Environment: config.toml (loaded automatically)[/]")


@configs_app.command("show")
def configs_show(
    config_path: Annotated[Path, typer.Argument(help="Path to configuration file")],
):
    """
    Show a configuration file's contents.

    Loads and displays the resolved configuration including
    any inherited values from 'extends:' directives.

    [bold]Example:[/]
        $ zwarm configs show configs/base.yaml
    """
    from zwarm.core.config import load_config
    import json

    if not config_path.exists():
        console.print(f"[red]File not found:[/] {config_path}")
        raise typer.Exit(1)

    try:
        config = load_config(config_path=config_path)
        console.print(f"\n[bold]Configuration:[/] {config_path}\n")
        console.print_json(json.dumps(config.to_dict(), indent=2))
    except Exception as e:
        console.print(f"[red]Error loading config:[/] {e}")
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: Annotated[bool, typer.Option("--version", "-V", help="Show version")] = False,
):
    """Main callback for version flag."""
    if version:
        console.print("[bold cyan]zwarm[/] version [green]0.1.0[/]")
        raise typer.Exit()


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
