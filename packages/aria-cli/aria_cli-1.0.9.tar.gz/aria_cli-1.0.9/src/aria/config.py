"""
ARIA Config

Configuration management for ARIA CLI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


@dataclass
class BrainConfig:
    """Brain configuration."""
    default: str = "tinyllama"
    model_dir: str = ""
    context_size: int = 2048
    temperature: float = 0.7


@dataclass
class ServerConfig:
    """Server configuration."""
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False


@dataclass
class SessionConfig:
    """Session configuration."""
    output_dir: str = ""
    format: str = "json"  # json, jsonl
    compress: bool = False


@dataclass
class AriaConfig:
    """Complete ARIA configuration."""
    brain: BrainConfig = field(default_factory=BrainConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    session: SessionConfig = field(default_factory=SessionConfig)
    
    # Custom paths
    project_dir: str = ""
    tours_dir: str = ""
    holomaps_dir: str = ""


# Default config locations
CONFIG_PATHS = [
    Path.cwd() / "aria.toml",
    Path.cwd() / ".aria" / "config.toml",
    Path.home() / ".aria" / "config.toml",
    Path.home() / ".config" / "aria" / "config.toml",
]


def load_config(path: Path | None = None) -> AriaConfig:
    """Load configuration from TOML file."""
    if tomllib is None:
        return AriaConfig()
    
    # Find config file
    config_path = path
    if config_path is None:
        for candidate in CONFIG_PATHS:
            if candidate.exists():
                config_path = candidate
                break
    
    if config_path is None or not config_path.exists():
        return AriaConfig()
    
    # Load TOML
    with open(config_path, "rb") as f:
        data = tomllib.load(f)
    
    return parse_config(data)


def parse_config(data: dict[str, Any]) -> AriaConfig:
    """Parse configuration from dict."""
    config = AriaConfig()
    
    # Brain settings
    if "brain" in data:
        brain = data["brain"]
        config.brain = BrainConfig(
            default=brain.get("default", "tinyllama"),
            model_dir=brain.get("model_dir", ""),
            context_size=brain.get("context_size", 2048),
            temperature=brain.get("temperature", 0.7),
        )
    
    # Server settings
    if "server" in data:
        server = data["server"]
        config.server = ServerConfig(
            host=server.get("host", "127.0.0.1"),
            port=server.get("port", 8000),
            reload=server.get("reload", False),
        )
    
    # Session settings
    if "session" in data:
        session = data["session"]
        config.session = SessionConfig(
            output_dir=session.get("output_dir", ""),
            format=session.get("format", "json"),
            compress=session.get("compress", False),
        )
    
    # Paths
    if "paths" in data:
        paths = data["paths"]
        config.project_dir = paths.get("project", "")
        config.tours_dir = paths.get("tours", "")
        config.holomaps_dir = paths.get("holomaps", "")
    
    return config


def save_config(config: AriaConfig, path: Path) -> None:
    """Save configuration to TOML file."""
    lines = [
        "# ARIA CLI Configuration",
        "",
        "[brain]",
        f'default = "{config.brain.default}"',
        f"context_size = {config.brain.context_size}",
        f"temperature = {config.brain.temperature}",
    ]
    
    if config.brain.model_dir:
        lines.append(f'model_dir = "{config.brain.model_dir}"')
    
    lines.extend([
        "",
        "[server]",
        f'host = "{config.server.host}"',
        f"port = {config.server.port}",
        f"reload = {str(config.server.reload).lower()}",
        "",
        "[session]",
        f'format = "{config.session.format}"',
        f"compress = {str(config.session.compress).lower()}",
    ])
    
    if config.session.output_dir:
        lines.append(f'output_dir = "{config.session.output_dir}"')
    
    if config.project_dir or config.tours_dir or config.holomaps_dir:
        lines.extend([
            "",
            "[paths]",
        ])
        if config.project_dir:
            lines.append(f'project = "{config.project_dir}"')
        if config.tours_dir:
            lines.append(f'tours = "{config.tours_dir}"')
        if config.holomaps_dir:
            lines.append(f'holomaps = "{config.holomaps_dir}"')
    
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(lines))


def get_default_model_dir() -> Path:
    """Get the default model directory."""
    return Path.home() / ".aria" / "models"


def get_default_session_dir() -> Path:
    """Get the default session directory."""
    return Path.home() / ".aria" / "sessions"
