"""
ARIA Connection CLI Commands
============================
Click command group for the live connection system.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
import json
import time

from .live import (
    LiveConnection,
    Message,
    MessageType,
    ConnectionState,
    Node,
    CONNECTION_HOME,
    NODES_DIR
)

console = Console()


@click.group(name="connection")
def connection():
    """Live folder-based connection system for ARIA nodes."""
    pass


@connection.command()
@click.option('--name', '-n', default='', help='Node name')
@click.option('--watch', '-w', is_flag=True, help='Keep watching for messages')
def start(name: str, watch: bool):
    """Start a new connection node and listen for messages."""
    conn = LiveConnection(name=name)
    
    console.print(Panel.fit(
        f"[green]Node Started[/green]\n\n"
        f"[bold]ID:[/bold] {conn.node_id}\n"
        f"[bold]Name:[/bold] {conn.name}\n"
        f"[bold]Inbox:[/bold] {conn.inbox}\n"
        f"[bold]Outbox:[/bold] {conn.outbox}",
        title="🔌 ARIA Live Connection"
    ))
    
    if watch:
        conn.on('text', lambda msg: console.print(
            f"[cyan][{msg.sender[:8]}][/cyan]: {msg.payload.get('text', '')}"
        ))
        conn.start()
        
        try:
            console.print("\n[dim]Watching for messages... (Ctrl+C to stop)[/dim]\n")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            conn.stop()
            console.print("\n[yellow]Connection stopped.[/yellow]")


@connection.command()
@click.argument('target')
@click.argument('message', nargs=-1)
def send(target: str, message: tuple):
    """Send a text message to a target node."""
    text = ' '.join(message)
    
    conn = LiveConnection()
    success = conn.send_text(text, target)
    
    if success:
        console.print(f"[green]✓[/green] Message sent to [bold]{target}[/bold]")
    else:
        console.print(f"[red]✗[/red] Failed to send message to {target}")


@connection.command()
def peers():
    """List all discovered peer nodes."""
    conn = LiveConnection()
    peers = conn.discover_peers()
    
    if not peers:
        console.print("[yellow]No peers discovered.[/yellow]")
        return
    
    table = Table(title="Discovered Peers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Last Seen", style="dim")
    table.add_column("Capabilities", style="blue")
    
    for peer in peers:
        last_seen = "N/A"
        if peer.last_seen > 0:
            age = int(time.time() - peer.last_seen)
            if age < 60:
                last_seen = f"{age}s ago"
            elif age < 3600:
                last_seen = f"{age // 60}m ago"
            else:
                last_seen = f"{age // 3600}h ago"
        
        caps = ", ".join(peer.capabilities[:3])
        if len(peer.capabilities) > 3:
            caps += "..."
        
        table.add_row(
            peer.id,
            peer.name or "-",
            peer.state,
            last_seen,
            caps
        )
    
    console.print(table)


@connection.command()
def status():
    """Show status of all local nodes."""
    registry = CONNECTION_HOME / "registry"
    
    if not registry.exists():
        console.print("[yellow]No nodes registered.[/yellow]")
        return
    
    table = Table(title="Registered Nodes")
    table.add_column("Node ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Created", style="dim")
    
    for node_file in registry.glob("*.json"):
        try:
            data = json.loads(node_file.read_text())
            table.add_row(
                data.get("id", "?")[:12],
                data.get("name", "-"),
                data.get("state", "unknown"),
                data.get("created", "?")[:19]
            )
        except Exception:
            pass
    
    console.print(table)


@connection.command()
@click.argument('target')
@click.argument('prompt', nargs=-1)
def llm(target: str, prompt: tuple):
    """Send an LLM request to a target node."""
    prompt_text = ' '.join(prompt)
    
    conn = LiveConnection()
    request_id = conn.send_llm_request(prompt_text, target)
    
    console.print(f"[green]✓[/green] LLM request sent to [bold]{target}[/bold]")
    console.print(f"[dim]Request ID: {request_id}[/dim]")


@connection.command()
@click.option('--node', '-n', default=None, help='Specific node ID')
@click.option('--limit', '-l', default=10, help='Max messages to show')
def inbox(node: str, limit: int):
    """View inbox messages for a node."""
    if node:
        inbox_dir = NODES_DIR / node / "inbox"
    else:
        # Find first node
        registry = CONNECTION_HOME / "registry"
        if registry.exists():
            node_files = list(registry.glob("*.json"))
            if node_files:
                node = node_files[0].stem
                inbox_dir = NODES_DIR / node / "inbox"
            else:
                console.print("[yellow]No nodes found.[/yellow]")
                return
        else:
            console.print("[yellow]No registry found.[/yellow]")
            return
    
    if not inbox_dir.exists():
        console.print(f"[yellow]No inbox for node {node}[/yellow]")
        return
    
    messages = list(inbox_dir.glob("*.json"))[:limit]
    
    if not messages:
        console.print(f"[dim]Inbox empty for {node}[/dim]")
        return
    
    table = Table(title=f"Inbox: {node[:12]}")
    table.add_column("ID", style="cyan")
    table.add_column("From", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("Preview", style="white")
    
    for msg_file in messages:
        try:
            msg = json.loads(msg_file.read_text())
            payload = msg.get("payload", {})
            preview = str(payload.get("text", payload))[:30]
            
            table.add_row(
                msg.get("id", "?")[:8],
                msg.get("sender", "?")[:8],
                msg.get("type", "?"),
                preview + ("..." if len(preview) >= 30 else "")
            )
        except Exception:
            pass
    
    console.print(table)


@connection.command()
@click.option('--all', '-a', 'clean_all', is_flag=True, help='Clean all nodes')
def clean(clean_all: bool):
    """Clean up old messages and expired nodes."""
    import shutil
    
    cleaned = 0
    
    if clean_all:
        # Clean all processed messages
        if NODES_DIR.exists():
            for node_dir in NODES_DIR.iterdir():
                if node_dir.is_dir():
                    processed = node_dir / "processed"
                    if processed.exists():
                        for f in processed.glob("*.json"):
                            f.unlink()
                            cleaned += 1
    else:
        # Clean only expired
        if NODES_DIR.exists():
            for node_dir in NODES_DIR.iterdir():
                if node_dir.is_dir():
                    for folder in ["inbox", "processed"]:
                        folder_path = node_dir / folder
                        if folder_path.exists():
                            for f in folder_path.glob("*.json"):
                                try:
                                    msg = json.loads(f.read_text())
                                    ttl = msg.get("ttl", 300)
                                    ts = msg.get("timestamp", 0)
                                    if time.time() - ts > ttl:
                                        f.unlink()
                                        cleaned += 1
                                except Exception:
                                    pass
    
    console.print(f"[green]✓[/green] Cleaned {cleaned} messages")


@connection.command()
def heartbeat():
    """Send a heartbeat to all peers."""
    conn = LiveConnection()
    conn.heartbeat()
    peers = conn.discover_peers()
    
    console.print(f"[green]✓[/green] Heartbeat sent to {len(peers)} peers")
