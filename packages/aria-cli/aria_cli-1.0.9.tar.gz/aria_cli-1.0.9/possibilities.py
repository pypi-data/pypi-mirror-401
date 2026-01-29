#!/usr/bin/env python3
"""
ARIA Possibilities Explorer
What can you do with a cognitive runtime intelligence system?
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.tree import Tree
from rich.columns import Columns

console = Console()

def main():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🌌 ARIA Possibilities Explorer[/bold cyan]\n"
        "[dim]What can you build with cognitive runtime intelligence?[/dim]",
        border_style="cyan"
    ))
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 1: Real-Time System Understanding
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 1. REAL-TIME SYSTEM UNDERSTANDING ━━━[/bold magenta]")
    console.print()
    
    capabilities_1 = """
    ARIA can analyze live system state and generate human-readable explanations:
    
    • **Incident Triage** - "Why is latency spiking?" → LLM analyzes metrics & topology
    • **Architecture Tours** - Guide new engineers through complex systems
    • **Change Impact** - "What happens if we scale down service X?"
    • **Anomaly Narration** - Translate alerts into actionable insights
    """
    console.print(Markdown(capabilities_1))

    # Demo: Multi-brain comparison
    console.print("[yellow]Demo: Multi-Brain Analysis[/yellow]")
    console.print()
    
    from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot, MetricValue
    from aria.core.engine import CognitiveEngine, EngineConfig

    incident_snapshot = WorldSnapshot(
        id="incident-001",
        context="Database connection pool exhausted, 503 errors spiking",
        nodes=[
            NodeSnapshot(id="api", type="service", label="API Server", status="degraded",
                        metrics=[MetricValue(name="error_rate", value=23.5, unit="%")]),
            NodeSnapshot(id="db", type="database", label="PostgreSQL", status="critical",
                        metrics=[MetricValue(name="connections", value=100, unit="max")]),
            NodeSnapshot(id="cache", type="cache", label="Redis", status="active",
                        metrics=[MetricValue(name="hit_rate", value=45.2, unit="%")]),
        ],
        flows=[
            FlowSnapshot(id="f1", source_id="api", target_id="db", rate=8500, status="congested"),
            FlowSnapshot(id="f2", source_id="api", target_id="cache", rate=2000),
        ],
        focus_node_ids=["db"],
    )

    # Quick analysis with tinyllama
    engine = CognitiveEngine(config=EngineConfig(brain="tinyllama", max_tokens=200))
    response = engine.explain(incident_snapshot, style="diagnostic")
    engine.close()

    console.print(Panel(
        response.summary[:500],
        title="[red]🚨 Incident Analysis (TinyLlama)[/red]",
        border_style="red"
    ))
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 2: Cognitive Workflows
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 2. COGNITIVE WORKFLOWS ━━━[/bold magenta]")
    console.print()

    workflow_tree = Tree("[bold]Cognitive Workflow Patterns[/bold]")
    
    runbook = workflow_tree.add("📋 [cyan]Automated Runbooks[/cyan]")
    runbook.add("Load snapshot from monitoring system")
    runbook.add("Generate LLM diagnosis")
    runbook.add("Suggest remediation steps")
    runbook.add("Execute approved actions")
    
    review = workflow_tree.add("🔍 [cyan]Architecture Review[/cyan]")
    review.add("Diff current vs baseline topology")
    review.add("Identify drift and anomalies")
    review.add("Generate compliance report")
    
    onboard = workflow_tree.add("🎓 [cyan]Developer Onboarding[/cyan]")
    onboard.add("Load system holomap")
    onboard.add("Run guided tour with explanations")
    onboard.add("Quiz understanding with checkpoints")
    
    console.print(workflow_tree)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 3: Integration Patterns
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 3. INTEGRATION PATTERNS ━━━[/bold magenta]")
    console.print()

    integrations = Table(title="ARIA Integration Points", show_header=True)
    integrations.add_column("Source", style="cyan")
    integrations.add_column("Integration", style="white")
    integrations.add_column("Use Case", style="green")
    
    integrations.add_row("Prometheus", "Metrics → WorldSnapshot", "Real-time cognitive dashboards")
    integrations.add_row("Kubernetes", "Pod topology → Nodes/Flows", "Cluster understanding")
    integrations.add_row("Jaeger/Zipkin", "Traces → Flow analysis", "Distributed tracing explanation")
    integrations.add_row("PagerDuty", "Alerts → Context injection", "Intelligent incident response")
    integrations.add_row("Terraform", "IaC → Baseline holomaps", "Drift detection")
    integrations.add_row("GitHub Actions", "CI/CD → Session recording", "Deployment cognition")
    integrations.add_row("Slack/Teams", "Chat → aria explain", "Conversational ops")
    integrations.add_row("Grafana", "Panels → ARIA widgets", "Embedded explanations")

    console.print(integrations)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 4: Advanced Brain Modes
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 4. ADVANCED BRAIN CAPABILITIES ━━━[/bold magenta]")
    console.print()

    brain_modes = Table(title="Brain Selection Strategy", show_header=True)
    brain_modes.add_column("Brain", style="cyan")
    brain_modes.add_column("Best For", style="white")
    brain_modes.add_column("Latency", style="yellow")
    brain_modes.add_column("Quality", style="green")
    
    brain_modes.add_row("tinyllama", "Quick triage, high-volume alerts", "~1s", "★★☆☆☆")
    brain_modes.add_row("phi2", "Balanced reasoning, code context", "~3s", "★★★☆☆")
    brain_modes.add_row("qwen2", "Multi-language, documentation", "~2s", "★★★☆☆")
    brain_modes.add_row("llama3", "Deep analysis, architecture review", "~2s", "★★★★☆")
    brain_modes.add_row("(custom)", "Fine-tuned on your systems", "varies", "★★★★★")

    console.print(brain_modes)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 5: Session & Learning
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 5. SESSION LEARNING & REPLAY ━━━[/bold magenta]")
    console.print()

    console.print(Markdown("""
    **Session Recording** captures cognitive events for:
    
    - 🔄 **Replay** - Re-run past incidents with different brains
    - 📊 **Analytics** - Track explanation quality over time
    - 🎯 **Fine-tuning** - Use sessions as training data
    - 📝 **Audit Trail** - Compliance & post-mortem documentation
    - 🧪 **A/B Testing** - Compare brain performance on same inputs
    """))
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 6: Code Examples
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 6. QUICK CODE PATTERNS ━━━[/bold magenta]")
    console.print()

    code_examples = """
```python
# Pattern 1: Prometheus → ARIA
from aria.integrations.prometheus import PrometheusAdapter
adapter = PrometheusAdapter("http://prometheus:9090")
snapshot = adapter.to_snapshot(query="up{job='api'}")
explanation = engine.explain(snapshot)

# Pattern 2: Kubernetes → ARIA  
from aria.integrations.k8s import K8sAdapter
adapter = K8sAdapter()
snapshot = adapter.namespace_snapshot("production")
diff = diff_snapshots(baseline, snapshot)

# Pattern 3: Webhook Handler
@app.post("/aria/explain")
async def explain_webhook(payload: dict):
    snapshot = WorldSnapshot.model_validate(payload)
    return engine.explain(snapshot).model_dump()

# Pattern 4: Streaming Explanations
async for chunk in engine.explain_stream(snapshot):
    await websocket.send(chunk)

# Pattern 5: Multi-Brain Ensemble
responses = await asyncio.gather(*[
    CognitiveEngine(brain=b).explain(snapshot)
    for b in ["tinyllama", "phi2", "llama3"]
])
consensus = ensemble.aggregate(responses)
```
    """
    console.print(Markdown(code_examples))

    # ═══════════════════════════════════════════════════════════════════════
    # CAPABILITY 7: Future Roadmap
    # ═══════════════════════════════════════════════════════════════════════
    console.print("[bold magenta]━━━ 7. ROADMAP & EXTENSIONS ━━━[/bold magenta]")
    console.print()

    roadmap = Table(title="ARIA Roadmap", show_header=True)
    roadmap.add_column("Feature", style="cyan")
    roadmap.add_column("Status", style="yellow")
    roadmap.add_column("Description", style="white")
    
    roadmap.add_row("Core Engine", "[green]✓ Complete[/green]", "Local LLM inference")
    roadmap.add_row("Session Recording", "[green]✓ Complete[/green]", "JSONL persistence")
    roadmap.add_row("Holomap Validation", "[green]✓ Complete[/green]", "Schema validation & stats")
    roadmap.add_row("Tour System", "[green]✓ Complete[/green]", "Guided cognitive walkthroughs")
    roadmap.add_row("REST API", "[yellow]○ Planned[/yellow]", "FastAPI server mode")
    roadmap.add_row("WebSocket Streaming", "[yellow]○ Planned[/yellow]", "Real-time explanation stream")
    roadmap.add_row("Unity Integration", "[yellow]○ In Progress[/yellow]", "Lenix Holomap bridge")
    roadmap.add_row("Prometheus Adapter", "[yellow]○ Planned[/yellow]", "Metrics → Snapshot")
    roadmap.add_row("K8s Adapter", "[yellow]○ Planned[/yellow]", "Cluster topology extraction")
    roadmap.add_row("Fine-tuning Pipeline", "[dim]◇ Future[/dim]", "Train on session data")
    roadmap.add_row("Multi-Modal", "[dim]◇ Future[/dim]", "Images, diagrams, video")

    console.print(roadmap)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════
    # FINAL: What You Can Build Today
    # ═══════════════════════════════════════════════════════════════════════
    console.print(Panel(
        "[bold]What You Can Build Today:[/bold]\n\n"
        "🔧 [cyan]CLI Tool[/cyan] - Integrate into existing scripts & pipelines\n"
        "🌐 [cyan]Python API[/cyan] - Embed cognitive explanations in any app\n"
        "📊 [cyan]Dashboards[/cyan] - Add LLM insights to monitoring tools\n"
        "🤖 [cyan]ChatOps[/cyan] - Slack/Teams bot for system questions\n"
        "📚 [cyan]Documentation[/cyan] - Auto-generate architecture docs\n"
        "🎓 [cyan]Training[/cyan] - Interactive system tutorials\n"
        "🚨 [cyan]Incident Response[/cyan] - Cognitive runbook automation\n\n"
        "[dim]All running locally with your choice of LLM brain.[/dim]",
        title="[bold green]🚀 ARIA is Ready[/bold green]",
        border_style="green"
    ))
    console.print()


if __name__ == "__main__":
    main()
