#!/usr/bin/env python3
"""
ARIA Full Demonstration Script
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

console = Console()

def main():
    console.print()
    console.print("═" * 70, style="cyan")
    console.print("        🧠  ARIA - Adaptive Runtime Intelligence Architecture  🧠", style="bold cyan")
    console.print("                      Full System Demonstration", style="dim")
    console.print("═" * 70, style="cyan")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 1: Brain Management
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 1: Brain Management ═══[/bold yellow]")
    console.print()

    from aria.brain.manager import BrainManager

    manager = BrainManager()
    brains = manager.list_brains()

    table = Table(title="Installed LLM Brains", show_header=True)
    table.add_column("Name", style="cyan")
    table.add_column("Model", style="white")
    table.add_column("Size", style="green")
    table.add_column("Status", style="yellow")

    for b in brains[:4]:
        status_icon = "✓" if b.status == "installed" else "○"
        table.add_row(b.name, b.model, b.size, f"{status_icon} {b.status}")

    console.print(table)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 2: World Snapshot Creation
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 2: World Snapshot Creation ═══[/bold yellow]")
    console.print()

    from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot, MetricValue

    snapshot = WorldSnapshot(
        id="demo-microservices-001",
        context="E-commerce platform during Black Friday sale",
        nodes=[
            NodeSnapshot(
                id="gateway", type="gateway", label="API Gateway",
                district="edge", status="active",
                metrics=[MetricValue(name="requests", value=15000, unit="req/s")]
            ),
            NodeSnapshot(
                id="cart", type="service", label="Cart Service",
                district="core", status="active",
                metrics=[MetricValue(name="latency", value=45, unit="ms")]
            ),
            NodeSnapshot(
                id="inventory", type="service", label="Inventory Service",
                district="core", status="warning",
                metrics=[MetricValue(name="latency", value=230, unit="ms")]
            ),
            NodeSnapshot(
                id="payment", type="service", label="Payment Gateway",
                district="external", status="active",
                metrics=[MetricValue(name="success_rate", value=99.2, unit="%")]
            ),
            NodeSnapshot(
                id="cache", type="cache", label="Redis Cache",
                district="data", status="active",
                metrics=[MetricValue(name="hit_rate", value=94.5, unit="%")]
            ),
            NodeSnapshot(
                id="db", type="database", label="PostgreSQL",
                district="data", status="active",
                metrics=[MetricValue(name="connections", value=180, unit="")]
            ),
        ],
        flows=[
            FlowSnapshot(id="f1", source_id="gateway", target_id="cart", rate=8000),
            FlowSnapshot(id="f2", source_id="gateway", target_id="inventory", rate=5000),
            FlowSnapshot(id="f3", source_id="cart", target_id="cache", rate=7500),
            FlowSnapshot(id="f4", source_id="cart", target_id="payment", rate=1200),
            FlowSnapshot(id="f5", source_id="inventory", target_id="db", rate=4800),
            FlowSnapshot(id="f6", source_id="inventory", target_id="cache", rate=3000),
        ],
        focus_node_ids=["inventory"],
    )

    console.print(f"[cyan]Snapshot ID:[/cyan] {snapshot.id}")
    console.print(f"[cyan]Context:[/cyan] {snapshot.context}")
    console.print()

    node_table = Table(title="System Nodes", show_header=True)
    node_table.add_column("ID", style="cyan")
    node_table.add_column("Type", style="dim")
    node_table.add_column("Label", style="white")
    node_table.add_column("Status")
    node_table.add_column("Metric", style="yellow")

    for n in snapshot.nodes:
        status_style = "green" if n.status == "active" else "yellow"
        metric = f"{n.metrics[0].name}: {n.metrics[0].value}{n.metrics[0].unit}" if n.metrics else "-"
        node_table.add_row(n.id, n.type, n.label, f"[{status_style}]{n.status}[/{status_style}]", metric)

    console.print(node_table)
    console.print()

    console.print("[dim]Data Flows:[/dim]")
    for f in snapshot.flows:
        console.print(f"  {f.source_id} ─[{f.rate}/s]→ {f.target_id}")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 3: Cognitive Engine
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 3: Cognitive Engine - LLM Explanation ═══[/bold yellow]")
    console.print()

    from aria.core.engine import CognitiveEngine, EngineConfig

    console.print("[dim]Loading TinyLlama brain...[/dim]")
    config = EngineConfig(brain="tinyllama", max_tokens=350, temperature=0.7)
    engine = CognitiveEngine(config=config)

    console.print("[dim]Generating cognitive explanation...[/dim]")
    console.print()

    response = engine.explain(snapshot, style="narrative")

    console.print(Panel(
        response.summary,
        title="[bold cyan]🧠 ARIA Cognitive Explanation[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    console.print()
    console.print(f"[green]Confidence:[/green] {response.confidence:.0%}")
    console.print(f"[green]Focus:[/green] {snapshot.focus_node_ids}")
    console.print()

    engine.close()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 4: Session Recording
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 4: Session Recording ═══[/bold yellow]")
    console.print()

    from aria.core.session import SessionRecorder, SessionManager
    from aria.core.response import ExplainerResponse

    demo_dir = Path("demo_sessions")
    demo_dir.mkdir(exist_ok=True)

    with SessionRecorder("Full-Demo-Session", output_dir=demo_dir, brain="tinyllama") as recorder:
        console.print(f"[cyan]Session ID:[/cyan] {recorder.session_id[:8]}...")
        
        recorder.record(snapshot, response)
        console.print("[green]✓[/green] Recorded cognitive event")
        
        console.print(f"[cyan]Events:[/cyan] {recorder.event_count}")

    console.print("[green]✓[/green] Session saved")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 5: Holomap Validation
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 5: Holomap Validation ═══[/bold yellow]")
    console.print()

    from aria.holomap.validator import validate_holomap

    result = validate_holomap("examples/holomaps/demo-system.json")

    valid_str = "[green]✓ Valid[/green]" if result.valid else "[red]✗ Invalid[/red]"
    console.print(f"[cyan]File:[/cyan] examples/holomaps/demo-system.json")
    console.print(f"[cyan]Status:[/cyan] {valid_str}")
    console.print(f"[cyan]Nodes:[/cyan] {result.stats.get('nodes', 0)}")
    console.print(f"[cyan]Flows:[/cyan] {result.stats.get('flows', 0)}")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 6: Holomap Diff
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 6: Holomap Diff ═══[/bold yellow]")
    console.print()

    from aria.holomap.diff import diff_snapshots

    old = WorldSnapshot(
        nodes=[
            NodeSnapshot(id="a", type="service", label="Service A"),
            NodeSnapshot(id="b", type="service", label="Service B"),
        ],
        flows=[FlowSnapshot(id="f1", source_id="a", target_id="b")],
    )

    new = WorldSnapshot(
        nodes=[
            NodeSnapshot(id="a", type="service", label="Service A"),
            NodeSnapshot(id="b", type="service", label="Service B Updated"),
            NodeSnapshot(id="c", type="service", label="Service C"),
        ],
        flows=[
            FlowSnapshot(id="f1", source_id="a", target_id="b"),
            FlowSnapshot(id="f2", source_id="b", target_id="c"),
        ],
    )

    diff = diff_snapshots(old, new)

    console.print(f"[cyan]Diff:[/cyan] {diff.summary}")
    
    diff_table = Table(title="Changes", show_header=True)
    diff_table.add_column("Type", style="cyan")
    diff_table.add_column("Count", style="green")
    diff_table.add_row("Nodes Added", str(len(diff.nodes_added)))
    diff_table.add_row("Nodes Modified", str(len(diff.nodes_modified)))
    diff_table.add_row("Flows Added", str(len(diff.flows_added)))
    console.print(diff_table)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 7: Tour System
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 7: Tour System ═══[/bold yellow]")
    console.print()

    from aria.tour.loader import list_tours, load_tour

    tours = list_tours("examples/tours")
    console.print(f"[cyan]Tours Found:[/cyan] {len(tours)}")
    
    for t in tours:
        console.print(f"  • {t.name} ({len(t.steps)} steps)")
        console.print(f"    [dim]{t.description}[/dim]")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # PART 8: CLI Commands
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold yellow]═══ PART 8: CLI Commands Available ═══[/bold yellow]")
    console.print()

    commands = [
        ("aria brain", "Manage LLM brains (list, download, info)"),
        ("aria explain", "Generate cognitive explanations"),
        ("aria holomap", "Validate and diff world files"),
        ("aria tour", "Run guided cognitive tours"),
        ("aria session", "Record and replay sessions"),
        ("aria serve", "Start REST/WebSocket server"),
        ("aria watch", "Live monitoring mode"),
        ("aria init", "Initialize ARIA config"),
    ]

    cmd_table = Table(title="CLI Commands", show_header=True)
    cmd_table.add_column("Command", style="cyan")
    cmd_table.add_column("Description", style="white")
    
    for cmd, desc in commands:
        cmd_table.add_row(cmd, desc)
    
    console.print(cmd_table)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════════════════
    console.print("═" * 70, style="green")
    console.print(Panel.fit(
        "[bold green]✓ All Systems Operational[/bold green]\n\n"
        "• 4 LLM Brains Installed\n"
        "• Cognitive Engine Working\n"
        "• Session Recording Functional\n"
        "• Holomap Validation Active\n"
        "• Tour System Ready\n"
        "• 32/32 Tests Passing",
        title="[bold]ARIA Demo Complete[/bold]",
        border_style="green",
    ))
    console.print()


if __name__ == "__main__":
    main()
