"""
ARIA CLI - Main entry point
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

ARIA_BANNER = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║     █████╗ ██████╗ ██╗ █████╗                        ║
    ║    ██╔══██╗██╔══██╗██║██╔══██╗                       ║
    ║    ███████║██████╔╝██║███████║                       ║
    ║    ██╔══██║██╔══██╗██║██╔══██║                       ║
    ║    ██║  ██║██║  ██║██║██║  ██║                       ║
    ║    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                       ║
    ║                                                       ║
    ║    Adaptive Runtime Intelligence Architecture         ║
    ║    The cognitive layer for self-narrating systems     ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
"""


@click.group()
@click.version_option(version="0.1.0", prog_name="aria")
@click.pass_context
def main(ctx: click.Context) -> None:
    """ARIA - Adaptive Runtime Intelligence Architecture
    
    The cognitive CLI for self-narrating systems.
    
    Examples:
    
        aria brain download tinyllama
        
        aria explain --snapshot state.json
        
        aria serve --brain phi2
        
        aria tour run cognitive-loop.json
    """
    ctx.ensure_object(dict)


# ============================================================================
# BRAIN COMMANDS
# ============================================================================

@main.group()
def brain() -> None:
    """Manage LLM brains for cognition."""
    pass


@brain.command("list")
def brain_list() -> None:
    """List available brains."""
    from aria.brain.manager import BrainManager
    
    manager = BrainManager()
    brains = manager.list_brains()
    
    if not brains:
        console.print("[yellow]No brains installed. Use 'aria brain download' to get started.[/yellow]")
        return
    
    from rich.table import Table
    table = Table(title="Installed Brains")
    table.add_column("Name", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Model", style="blue")
    table.add_column("Status", style="yellow")
    
    for b in brains:
        table.add_row(b.name, b.size, b.model, b.status)
    
    console.print(table)


@brain.command("download")
@click.argument("name", type=click.Choice(["tinyllama", "phi2", "qwen2", "llama3"]))
@click.option("--force", is_flag=True, help="Force re-download")
def brain_download(name: str, force: bool) -> None:
    """Download a brain model."""
    from aria.brain.manager import BrainManager
    
    manager = BrainManager()
    
    console.print(f"[cyan]Downloading brain: {name}[/cyan]")
    
    with console.status(f"Downloading {name}..."):
        manager.download(name, force=force)
    
    console.print(f"[green]✓ Brain '{name}' downloaded successfully![/green]")


@brain.command("info")
@click.argument("name")
def brain_info(name: str) -> None:
    """Show brain details."""
    from aria.brain.manager import BrainManager
    
    manager = BrainManager()
    info = manager.get_info(name)
    
    console.print(Panel(
        f"[bold]{info.name}[/bold]\n\n"
        f"Model: {info.model}\n"
        f"Size: {info.size}\n"
        f"Context: {info.context_size} tokens\n"
        f"License: {info.license}\n"
        f"Path: {info.path}",
        title="Brain Info"
    ))


@brain.command("benchmark")
@click.option("--iterations", default=3, help="Number of iterations")
def brain_benchmark(iterations: int) -> None:
    """Benchmark all installed brains."""
    from aria.brain.benchmark import run_benchmark
    
    console.print("[cyan]Running brain benchmark...[/cyan]")
    results = run_benchmark(iterations=iterations)
    
    from rich.table import Table
    table = Table(title="Benchmark Results")
    table.add_column("Brain", style="cyan")
    table.add_column("Tokens/sec", style="green")
    table.add_column("Latency (ms)", style="yellow")
    table.add_column("Quality", style="blue")
    
    for r in results:
        table.add_row(r.name, f"{r.tokens_per_sec:.1f}", f"{r.latency_ms:.0f}", r.quality)
    
    console.print(table)


# ============================================================================
# EXPLAIN COMMANDS
# ============================================================================

@main.command("explain")
@click.option("--snapshot", "-s", type=click.Path(exists=True), help="Snapshot file")
@click.option("--url", "-u", help="Live endpoint URL")
@click.option("--stdin", is_flag=True, help="Read from stdin")
@click.option("--focus", "-f", multiple=True, help="Focus on specific nodes")
@click.option("--style", type=click.Choice(["technical", "narrative", "brief"]), default="narrative")
@click.option("--brain", "-b", default="tinyllama", help="Brain to use")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def explain(snapshot: str | None, url: str | None, stdin: bool, 
            focus: tuple[str, ...], style: str, brain: str, as_json: bool) -> None:
    """Generate an explanation from system state."""
    from aria.core.engine import CognitiveEngine
    from aria.core.snapshot import WorldSnapshot
    import json
    import sys
    
    # Load snapshot
    if snapshot:
        world = WorldSnapshot.from_file(snapshot)
    elif url:
        world = WorldSnapshot.from_url(url)
    elif stdin:
        data = sys.stdin.read()
        world = WorldSnapshot.from_json(data)
    else:
        console.print("[red]Error: Provide --snapshot, --url, or --stdin[/red]")
        raise SystemExit(1)
    
    # Apply focus
    if focus:
        world = world.with_focus(list(focus))
    
    # Generate explanation
    engine = CognitiveEngine(brain=brain)
    response = engine.explain(world, style=style)
    
    if as_json:
        click.echo(json.dumps(response.to_dict(), indent=2))
    else:
        console.print(Panel(
            response.summary,
            title="[bold cyan]Explanation[/bold cyan]",
            border_style="cyan"
        ))
        
        if response.details:
            for detail in response.details:
                console.print(f"  • {detail}")
        
        if response.focus_nodes:
            console.print(f"\n[dim]Focus: {', '.join(response.focus_nodes)}[/dim]")


# ============================================================================
# SERVE COMMANDS
# ============================================================================

@main.command("serve")
@click.option("--brain", "-b", default="tinyllama", help="Brain to use")
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind")
@click.option("--port", "-p", default=7777, help="Port to bind")
@click.option("--reload", is_flag=True, help="Auto-reload on changes")
def serve(brain: str, host: str, port: int, reload: bool) -> None:
    """Start the cognitive server."""
    console.print(ARIA_BANNER)
    console.print(f"[cyan]Starting ARIA server...[/cyan]")
    console.print(f"  Brain: [green]{brain}[/green]")
    console.print(f"  Endpoint: [blue]http://{host}:{port}[/blue]")
    console.print()
    
    from aria.server.app import create_app
    import uvicorn
    
    app = create_app(brain=brain)
    uvicorn.run(app, host=host, port=port, reload=reload)


# ============================================================================
# TOUR COMMANDS
# ============================================================================

@main.group()
def tour() -> None:
    """Run guided cognitive tours."""
    pass


@tour.command("list")
@click.option("--dir", "-d", "directory", default=".", help="Directory to search")
def tour_list(directory: str) -> None:
    """List available tours."""
    from aria.tour.loader import list_tours
    
    tours = list_tours(directory)
    
    if not tours:
        console.print("[yellow]No tours found.[/yellow]")
        return
    
    from rich.table import Table
    table = Table(title="Available Tours")
    table.add_column("Name", style="cyan")
    table.add_column("Steps", style="green")
    table.add_column("Description", style="dim")
    
    for t in tours:
        table.add_row(t.name, str(len(t.steps)), t.description or "")
    
    console.print(table)


@tour.command("run")
@click.argument("file", type=click.Path(exists=True))
@click.option("--brain", "-b", default="tinyllama", help="Brain to use")
@click.option("--record", is_flag=True, help="Record session")
def tour_run(file: str, brain: str, record: bool) -> None:
    """Run a guided tour."""
    from aria.tour.runner import TourRunner
    
    runner = TourRunner(brain=brain, record=record)
    
    console.print(f"[cyan]Starting tour: {file}[/cyan]")
    console.print()
    
    runner.run(file)


@tour.command("validate")
@click.argument("file", type=click.Path(exists=True))
def tour_validate(file: str) -> None:
    """Validate a tour file."""
    from aria.tour.validator import validate_tour
    
    errors = validate_tour(file)
    
    if errors:
        console.print(f"[red]✗ Validation failed with {len(errors)} errors:[/red]")
        for e in errors:
            console.print(f"  • {e}")
    else:
        console.print("[green]✓ Tour is valid![/green]")


# ============================================================================
# SESSION COMMANDS
# ============================================================================

@main.group()
def session() -> None:
    """Record and replay cognitive sessions."""
    pass


@session.command("start")
@click.option("--name", "-n", required=True, help="Session name")
def session_start(name: str) -> None:
    """Start recording a session."""
    from aria.core.session import SessionRecorder
    
    recorder = SessionRecorder.start(name)
    console.print(f"[green]✓ Session '{name}' started[/green]")
    console.print(f"  ID: {recorder.session_id}")


@session.command("stop")
def session_stop() -> None:
    """Stop the current recording session."""
    from aria.core.session import SessionRecorder
    
    session = SessionRecorder.stop_current()
    if session:
        console.print(f"[green]✓ Session stopped and saved[/green]")
        console.print(f"  Events: {session.event_count}")
        console.print(f"  File: {session.output_path}")
    else:
        console.print("[yellow]No active session to stop[/yellow]")


@session.command("list")
def session_list() -> None:
    """List all recorded sessions."""
    from aria.core.session import SessionManager
    
    manager = SessionManager()
    sessions = manager.list_sessions()
    
    if not sessions:
        console.print("[yellow]No sessions found.[/yellow]")
        return
    
    from rich.table import Table
    table = Table(title="Recorded Sessions")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Events", style="blue")
    
    for s in sessions:
        table.add_row(s.id[:8], s.name, s.date, str(s.event_count))
    
    console.print(table)


@session.command("show")
@click.argument("session_id")
def session_show(session_id: str) -> None:
    """Show session details."""
    from aria.core.session import SessionManager
    
    manager = SessionManager()
    session = manager.get_session(session_id)
    
    if not session:
        console.print(f"[red]Session not found: {session_id}[/red]")
        raise SystemExit(1)
    
    console.print(Panel(
        f"[bold]{session.name}[/bold]\n\n"
        f"ID: {session.id}\n"
        f"Date: {session.date}\n"
        f"Duration: {session.duration}\n"
        f"Events: {session.event_count}\n"
        f"File: {session.output_path}",
        title="Session Details"
    ))


@session.command("replay")
@click.argument("session_id")
@click.option("--speed", default=1.0, help="Replay speed multiplier")
def session_replay(session_id: str, speed: float) -> None:
    """Replay a recorded session."""
    from aria.core.session import SessionManager
    
    manager = SessionManager()
    console.print(f"[cyan]Replaying session: {session_id}[/cyan]")
    manager.replay(session_id, speed=speed)


# ============================================================================
# HOLOMAP COMMANDS
# ============================================================================

@main.group()
def holomap() -> None:
    """Manage Holomap world files."""
    pass


@holomap.command("validate")
@click.argument("file", type=click.Path(exists=True))
def holomap_validate(file: str) -> None:
    """Validate a holomap file."""
    from aria.holomap.validator import validate_holomap
    
    result = validate_holomap(file)
    
    if result.errors:
        console.print(f"[red]✗ Validation failed with {len(result.errors)} errors:[/red]")
        for e in result.errors:
            console.print(f"  [red]✗[/red] {e.path}: {e.message}" if e.path else f"  [red]✗[/red] {e.message}")
    
    if result.warnings:
        console.print(f"[yellow]⚠ {len(result.warnings)} warnings:[/yellow]")
        for w in result.warnings:
            console.print(f"  [yellow]⚠[/yellow] {w.path}: {w.message}" if w.path else f"  [yellow]⚠[/yellow] {w.message}")
    
    if result.valid:
        console.print("[green]✓ Holomap is valid![/green]")
        console.print(f"  Nodes: {result.stats.get('nodes', 0)}")
        console.print(f"  Flows: {result.stats.get('flows', 0)}")


@holomap.command("diff")
@click.argument("old_file", type=click.Path(exists=True))
@click.argument("new_file", type=click.Path(exists=True))
def holomap_diff(old_file: str, new_file: str) -> None:
    """Diff two holomap files."""
    from aria.holomap.diff import diff_holomaps
    
    changes = diff_holomaps(old_file, new_file)
    
    console.print(f"[cyan]Changes: {old_file} → {new_file}[/cyan]")
    console.print()
    
    for change in changes:
        if change.type == "added":
            console.print(f"  [green]+[/green] {change.description}")
        elif change.type == "removed":
            console.print(f"  [red]-[/red] {change.description}")
        else:
            console.print(f"  [yellow]~[/yellow] {change.description}")


@holomap.command("stats")
@click.argument("file", type=click.Path(exists=True))
def holomap_stats(file: str) -> None:
    """Show holomap statistics."""
    from aria.holomap.stats import get_stats
    
    stats = get_stats(file)
    
    console.print(Panel(
        f"Nodes: {stats.node_count}\n"
        f"Flows: {stats.flow_count}\n"
        f"Districts: {stats.district_count}\n"
        f"Metrics: {stats.metric_count}\n"
        f"Tours: {stats.tour_count}",
        title=f"Holomap: {file}"
    ))


# ============================================================================
# WATCH COMMAND
# ============================================================================

@main.command("watch")
@click.argument("url")
@click.option("--interval", "-i", default=5, help="Poll interval in seconds")
@click.option("--brain", "-b", default="tinyllama", help="Brain to use")
def watch(url: str, interval: int, brain: str) -> None:
    """Live monitoring with real-time narration."""
    from aria.watch.monitor import Monitor
    
    console.print(f"[cyan]Watching: {url}[/cyan]")
    console.print(f"[dim]Press Ctrl+C to stop[/dim]")
    console.print()
    
    monitor = Monitor(url, brain=brain, interval=interval)
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching[/yellow]")


# ============================================================================
# INIT COMMAND
# ============================================================================

@main.command("init")
@click.option("--brain", "-b", default="tinyllama", help="Default brain to download")
def init(brain: str) -> None:
    """Initialize ARIA (download default brain, create config)."""
    console.print(ARIA_BANNER)
    console.print("[cyan]Initializing ARIA...[/cyan]")
    console.print()
    
    from aria.config import create_default_config
    from aria.brain.manager import BrainManager
    
    # Create config
    config_path = create_default_config()
    console.print(f"  [green]✓[/green] Config created: {config_path}")
    
    # Download brain
    console.print(f"  [cyan]⟳[/cyan] Downloading brain: {brain}")
    manager = BrainManager()
    manager.download(brain)
    console.print(f"  [green]✓[/green] Brain downloaded: {brain}")
    
    console.print()
    console.print("[green]ARIA is ready![/green]")
    console.print()
    console.print("Try:")
    console.print("  [cyan]aria explain --snapshot state.json[/cyan]")
    console.print("  [cyan]aria serve[/cyan]")


# ============================================================================
# CONNECTION COMMAND
# ============================================================================

# Import and register connection command group
try:
    from aria.connection import connection
    main.add_command(connection)
except ImportError:
    pass  # Connection module not installed

if __name__ == "__main__":
    main()

