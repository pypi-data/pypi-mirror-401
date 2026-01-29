"""
ARIA Core - Session Recording

Records cognitive events as lineage artifacts.
"""

from __future__ import annotations

import json
import gzip
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from aria.core.snapshot import WorldSnapshot
from aria.core.response import ExplainerResponse


class CognitiveEvent(BaseModel):
    """A single cognitive event."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    snapshot: WorldSnapshot | None = None
    response: ExplainerResponse | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionMetadata(BaseModel):
    """Metadata about a recording session."""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime | None = None
    brain: str = ""
    version: str = "1.0.0"
    metadata: dict[str, Any] = Field(default_factory=dict)


class CognitiveSession(BaseModel):
    """A recorded cognitive session."""
    metadata: SessionMetadata
    events: list[CognitiveEvent] = Field(default_factory=list)
    
    @property
    def id(self) -> str:
        return self.metadata.id
    
    @property
    def name(self) -> str:
        return self.metadata.name
    
    @property
    def event_count(self) -> int:
        return len(self.events)
    
    @property
    def duration(self) -> str:
        if not self.events:
            return "0s"
        
        start = self.events[0].timestamp
        end = self.events[-1].timestamp
        delta = end - start
        
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    @property
    def date(self) -> str:
        return self.metadata.started_at.strftime("%Y-%m-%d %H:%M")
    
    @property
    def output_path(self) -> str:
        return f"~/.aria/sessions/{self.id}.jsonl"
    
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
    
    def to_json(self, indent: int = 2) -> str:
        return self.model_dump_json(indent=indent)


class SessionRecorder:
    """
    Records cognitive events during a session.
    
    Example:
        with SessionRecorder("my-session") as recorder:
            response = engine.explain(snapshot)
            recorder.record(snapshot, response)
    """
    
    _current: "SessionRecorder | None" = None
    
    def __init__(
        self,
        name: str,
        output_dir: Path | None = None,
        brain: str = "",
    ) -> None:
        self.session = CognitiveSession(
            metadata=SessionMetadata(name=name, brain=brain)
        )
        self.output_dir = output_dir or Path.home() / ".aria" / "sessions"
        self._active = False
    
    @property
    def session_id(self) -> str:
        return self.session.id
    
    @property
    def event_count(self) -> int:
        return self.session.event_count
    
    def record(
        self,
        snapshot: WorldSnapshot,
        response: ExplainerResponse,
        event_type: str = "ExplanationGenerated",
    ) -> None:
        """Record a cognitive event."""
        event = CognitiveEvent(
            type=event_type,
            snapshot=snapshot,
            response=response,
        )
        self.session.events.append(event)
    
    def record_event(self, event: CognitiveEvent) -> None:
        """Record a pre-constructed event."""
        self.session.events.append(event)
    
    def save(self, compress: bool = False) -> Path:
        """Save the session to disk."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Update end time
        self.session.metadata.ended_at = datetime.utcnow()
        
        if compress:
            path = self.output_dir / f"{self.session_id}.json.gz"
            with gzip.open(path, "wt", encoding="utf-8") as f:
                f.write(self.session.to_json())
        else:
            path = self.output_dir / f"{self.session_id}.json"
            with open(path, "w") as f:
                f.write(self.session.to_json())
        
        return path
    
    def save_as_jsonl(self) -> Path:
        """Save as JSON Lines (streaming format)."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        path = self.output_dir / f"{self.session_id}.jsonl"
        with open(path, "w") as f:
            # Write metadata
            f.write(json.dumps({"type": "session_start", **self.session.metadata.model_dump(mode="json")}))
            f.write("\n")
            
            # Write events
            for event in self.session.events:
                f.write(json.dumps(event.model_dump(mode="json")))
                f.write("\n")
            
            # Write end
            f.write(json.dumps({"type": "session_end", "timestamp": datetime.utcnow().isoformat()}))
            f.write("\n")
        
        return path
    
    @classmethod
    def start(cls, name: str, **kwargs) -> "SessionRecorder":
        """Start a new recording session."""
        recorder = cls(name, **kwargs)
        recorder._active = True
        cls._current = recorder
        return recorder
    
    @classmethod
    def stop_current(cls) -> CognitiveSession | None:
        """Stop the current recording session."""
        if cls._current is None:
            return None
        
        recorder = cls._current
        recorder._active = False
        recorder.save_as_jsonl()
        
        session = recorder.session
        cls._current = None
        
        return session
    
    @classmethod
    def get_current(cls) -> "SessionRecorder | None":
        """Get the current active recorder."""
        return cls._current
    
    def __enter__(self) -> "SessionRecorder":
        self._active = True
        SessionRecorder._current = self
        return self
    
    def __exit__(self, *args) -> None:
        self._active = False
        self.save_as_jsonl()
        if SessionRecorder._current is self:
            SessionRecorder._current = None


class SessionManager:
    """Manages recorded sessions."""
    
    def __init__(self, session_dir: Path | None = None) -> None:
        self.session_dir = session_dir or Path.home() / ".aria" / "sessions"
    
    def list_sessions(self) -> list[CognitiveSession]:
        """List all recorded sessions."""
        if not self.session_dir.exists():
            return []
        
        sessions = []
        
        # Check both .json and .jsonl files
        for pattern in ["*.json", "*.jsonl"]:
            for path in self.session_dir.glob(pattern):
                # Skip .json.gz files in the .json glob
                if path.suffix == ".gz":
                    continue
                try:
                    if path.suffix == ".jsonl":
                        # Parse JSONL format
                        session = self._load_jsonl_session(path)
                        if session:
                            sessions.append(session)
                    else:
                        with open(path) as f:
                            data = json.load(f)
                        sessions.append(CognitiveSession.model_validate(data))
                except Exception:
                    pass
        
        return sorted(sessions, key=lambda s: s.metadata.started_at, reverse=True)
    
    def _load_jsonl_session(self, path: Path) -> CognitiveSession | None:
        """Load a session from JSONL format."""
        metadata = None
        events = []
        
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("type") == "session_start":
                        # Remove 'type' key and parse as metadata
                        data.pop("type", None)
                        metadata = SessionMetadata.model_validate(data)
                    elif data.get("type") == "session_end":
                        pass  # End marker
                    else:
                        events.append(CognitiveEvent.model_validate(data))
                except Exception:
                    pass
        
        if metadata:
            return CognitiveSession(metadata=metadata, events=events)
        return None
    
    def get_session(self, session_id: str) -> CognitiveSession | None:
        """Get a session by ID."""
        # Try exact match
        path = self.session_dir / f"{session_id}.json"
        if path.exists():
            with open(path) as f:
                return CognitiveSession.model_validate(json.load(f))
        
        # Try prefix match
        for p in self.session_dir.glob(f"{session_id}*.json"):
            with open(p) as f:
                return CognitiveSession.model_validate(json.load(f))
        
        return None
    
    def replay(self, session_id: str, speed: float = 1.0) -> None:
        """Replay a session."""
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        import time
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console()
        
        console.print(f"[cyan]Replaying: {session.name}[/cyan]")
        console.print()
        
        prev_time = None
        for event in session.events:
            # Wait for appropriate delay
            if prev_time is not None:
                delay = (event.timestamp - prev_time).total_seconds() / speed
                if delay > 0:
                    time.sleep(min(delay, 5.0))  # Cap at 5 seconds
            
            # Show event
            if event.response:
                console.print(Panel(
                    event.response.summary,
                    title=f"[{event.type}]",
                    border_style="cyan"
                ))
            
            prev_time = event.timestamp
        
        console.print()
        console.print("[green]Replay complete[/green]")
