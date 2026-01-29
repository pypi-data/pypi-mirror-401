"""
ARIA Session Chronicle Index
Long-term lineage tracking system for session replay, analytics, and fine-tuning.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# CHRONICLE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class ChronicleEntry(BaseModel):
    """A single entry in the chronicle index."""
    id: str
    session_id: str
    event_type: str  # "explain", "predict", "tour", "mesh"
    timestamp: float
    brain: str | None = None
    snapshot_hash: str | None = None
    response_hash: str | None = None
    confidence: float | None = None
    latency_ms: float | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionSummary(BaseModel):
    """Summary of a session for the chronicle."""
    session_id: str
    name: str
    brain: str | None = None
    start_time: float
    end_time: float | None = None
    event_count: int = 0
    avg_confidence: float | None = None
    avg_latency_ms: float | None = None
    tags: list[str] = Field(default_factory=list)
    source_file: str | None = None


class ChronicleQuery(BaseModel):
    """Query parameters for chronicle search."""
    session_id: str | None = None
    event_type: str | None = None
    brain: str | None = None
    min_confidence: float | None = None
    max_confidence: float | None = None
    start_time: float | None = None
    end_time: float | None = None
    tags: list[str] | None = None
    limit: int = 100
    offset: int = 0


class ChronicleStats(BaseModel):
    """Chronicle statistics."""
    total_sessions: int
    total_events: int
    brains_used: list[str]
    event_types: dict[str, int]
    avg_confidence: float | None
    avg_latency_ms: float | None
    date_range: tuple[str, str] | None


# ═══════════════════════════════════════════════════════════════════════════════
# CHRONICLE INDEX
# ═══════════════════════════════════════════════════════════════════════════════

class ChronicleIndex:
    """
    Long-term lineage tracking system for ARIA sessions.
    
    Features:
    - Session indexing and search
    - Event lineage tracking
    - Analytics and statistics
    - Fine-tuning data export
    - Replay support
    """
    
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        brain TEXT,
        start_time REAL NOT NULL,
        end_time REAL,
        event_count INTEGER DEFAULT 0,
        avg_confidence REAL,
        avg_latency_ms REAL,
        tags TEXT,
        source_file TEXT,
        created_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        timestamp REAL NOT NULL,
        brain TEXT,
        snapshot_hash TEXT,
        response_hash TEXT,
        confidence REAL,
        latency_ms REAL,
        tags TEXT,
        metadata TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    );
    
    CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
    CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
    CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
    CREATE INDEX IF NOT EXISTS idx_events_brain ON events(brain);
    CREATE INDEX IF NOT EXISTS idx_events_confidence ON events(confidence);
    """
    
    def __init__(self, db_path: Path | str | None = None):
        """Initialize chronicle index."""
        if db_path is None:
            db_path = Path.home() / ".aria" / "chronicle.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()
        
    def _initialize_db(self) -> None:
        """Initialize database schema."""
        with self._connect() as conn:
            conn.executescript(self.SCHEMA)
            
    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
            
    # ═══════════════════════════════════════════════════════════════════════
    # SESSION OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    def register_session(self, summary: SessionSummary) -> None:
        """Register a session in the chronicle."""
        with self._connect() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sessions 
                (session_id, name, brain, start_time, end_time, event_count, 
                 avg_confidence, avg_latency_ms, tags, source_file)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.session_id,
                summary.name,
                summary.brain,
                summary.start_time,
                summary.end_time,
                summary.event_count,
                summary.avg_confidence,
                summary.avg_latency_ms,
                json.dumps(summary.tags),
                summary.source_file,
            ))
            
    def get_session(self, session_id: str) -> SessionSummary | None:
        """Get a session by ID."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM sessions WHERE session_id = ?",
                (session_id,)
            ).fetchone()
            
            if row:
                return SessionSummary(
                    session_id=row["session_id"],
                    name=row["name"],
                    brain=row["brain"],
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    event_count=row["event_count"],
                    avg_confidence=row["avg_confidence"],
                    avg_latency_ms=row["avg_latency_ms"],
                    tags=json.loads(row["tags"] or "[]"),
                    source_file=row["source_file"],
                )
            return None
            
    def list_sessions(
        self, 
        limit: int = 50, 
        offset: int = 0,
        brain: str | None = None,
    ) -> list[SessionSummary]:
        """List sessions with optional filtering."""
        with self._connect() as conn:
            query = "SELECT * FROM sessions"
            params: list[Any] = []
            
            if brain:
                query += " WHERE brain = ?"
                params.append(brain)
                
            query += " ORDER BY start_time DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            rows = conn.execute(query, params).fetchall()
            
            return [
                SessionSummary(
                    session_id=row["session_id"],
                    name=row["name"],
                    brain=row["brain"],
                    start_time=row["start_time"],
                    end_time=row["end_time"],
                    event_count=row["event_count"],
                    avg_confidence=row["avg_confidence"],
                    avg_latency_ms=row["avg_latency_ms"],
                    tags=json.loads(row["tags"] or "[]"),
                    source_file=row["source_file"],
                )
                for row in rows
            ]
            
    # ═══════════════════════════════════════════════════════════════════════
    # EVENT OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════
    
    def record_event(self, entry: ChronicleEntry) -> None:
        """Record an event in the chronicle."""
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO events 
                (id, session_id, event_type, timestamp, brain, snapshot_hash,
                 response_hash, confidence, latency_ms, tags, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id,
                entry.session_id,
                entry.event_type,
                entry.timestamp,
                entry.brain,
                entry.snapshot_hash,
                entry.response_hash,
                entry.confidence,
                entry.latency_ms,
                json.dumps(entry.tags),
                json.dumps(entry.metadata),
            ))
            
            # Update session event count
            conn.execute("""
                UPDATE sessions 
                SET event_count = event_count + 1
                WHERE session_id = ?
            """, (entry.session_id,))
            
    def get_events(self, query: ChronicleQuery) -> list[ChronicleEntry]:
        """Query events from the chronicle."""
        with self._connect() as conn:
            sql = "SELECT * FROM events WHERE 1=1"
            params: list[Any] = []
            
            if query.session_id:
                sql += " AND session_id = ?"
                params.append(query.session_id)
                
            if query.event_type:
                sql += " AND event_type = ?"
                params.append(query.event_type)
                
            if query.brain:
                sql += " AND brain = ?"
                params.append(query.brain)
                
            if query.min_confidence is not None:
                sql += " AND confidence >= ?"
                params.append(query.min_confidence)
                
            if query.max_confidence is not None:
                sql += " AND confidence <= ?"
                params.append(query.max_confidence)
                
            if query.start_time is not None:
                sql += " AND timestamp >= ?"
                params.append(query.start_time)
                
            if query.end_time is not None:
                sql += " AND timestamp <= ?"
                params.append(query.end_time)
                
            sql += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([query.limit, query.offset])
            
            rows = conn.execute(sql, params).fetchall()
            
            return [
                ChronicleEntry(
                    id=row["id"],
                    session_id=row["session_id"],
                    event_type=row["event_type"],
                    timestamp=row["timestamp"],
                    brain=row["brain"],
                    snapshot_hash=row["snapshot_hash"],
                    response_hash=row["response_hash"],
                    confidence=row["confidence"],
                    latency_ms=row["latency_ms"],
                    tags=json.loads(row["tags"] or "[]"),
                    metadata=json.loads(row["metadata"] or "{}"),
                )
                for row in rows
            ]
            
    # ═══════════════════════════════════════════════════════════════════════
    # ANALYTICS
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_stats(self) -> ChronicleStats:
        """Get chronicle statistics."""
        with self._connect() as conn:
            # Total counts
            session_count = conn.execute(
                "SELECT COUNT(*) FROM sessions"
            ).fetchone()[0]
            
            event_count = conn.execute(
                "SELECT COUNT(*) FROM events"
            ).fetchone()[0]
            
            # Brains used
            brains = conn.execute(
                "SELECT DISTINCT brain FROM events WHERE brain IS NOT NULL"
            ).fetchall()
            brains_used = [b[0] for b in brains]
            
            # Event types
            type_rows = conn.execute(
                "SELECT event_type, COUNT(*) FROM events GROUP BY event_type"
            ).fetchall()
            event_types = {row[0]: row[1] for row in type_rows}
            
            # Averages
            avgs = conn.execute(
                "SELECT AVG(confidence), AVG(latency_ms) FROM events"
            ).fetchone()
            
            # Date range
            date_range = None
            if event_count > 0:
                range_row = conn.execute(
                    "SELECT MIN(timestamp), MAX(timestamp) FROM events"
                ).fetchone()
                if range_row[0]:
                    date_range = (
                        datetime.fromtimestamp(range_row[0], tz=timezone.utc).isoformat(),
                        datetime.fromtimestamp(range_row[1], tz=timezone.utc).isoformat(),
                    )
                    
            return ChronicleStats(
                total_sessions=session_count,
                total_events=event_count,
                brains_used=brains_used,
                event_types=event_types,
                avg_confidence=round(avgs[0], 3) if avgs[0] else None,
                avg_latency_ms=round(avgs[1], 2) if avgs[1] else None,
                date_range=date_range,
            )
            
    def get_brain_performance(self, brain: str) -> dict[str, Any]:
        """Get performance metrics for a specific brain."""
        with self._connect() as conn:
            row = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(confidence) as avg_confidence,
                    AVG(latency_ms) as avg_latency,
                    MIN(confidence) as min_confidence,
                    MAX(confidence) as max_confidence
                FROM events WHERE brain = ?
            """, (brain,)).fetchone()
            
            return {
                "brain": brain,
                "total_events": row["total"],
                "avg_confidence": round(row["avg_confidence"], 3) if row["avg_confidence"] else None,
                "avg_latency_ms": round(row["avg_latency"], 2) if row["avg_latency"] else None,
                "min_confidence": round(row["min_confidence"], 3) if row["min_confidence"] else None,
                "max_confidence": round(row["max_confidence"], 3) if row["max_confidence"] else None,
            }
            
    # ═══════════════════════════════════════════════════════════════════════
    # EXPORT FOR FINE-TUNING
    # ═══════════════════════════════════════════════════════════════════════
    
    def export_for_finetuning(
        self, 
        output_path: Path,
        min_confidence: float = 0.7,
        brain: str | None = None,
    ) -> int:
        """Export high-quality events for fine-tuning."""
        query = ChronicleQuery(
            min_confidence=min_confidence,
            brain=brain,
            limit=10000,
        )
        events = self.get_events(query)
        
        # Export as JSONL
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            for event in events:
                f.write(json.dumps(event.model_dump()) + "\n")
                
        return len(events)
        
    # ═══════════════════════════════════════════════════════════════════════
    # LINEAGE TRACKING
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_lineage(self, snapshot_hash: str) -> list[ChronicleEntry]:
        """Get all events related to a specific snapshot."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM events WHERE snapshot_hash = ? ORDER BY timestamp",
                (snapshot_hash,)
            ).fetchall()
            
            return [
                ChronicleEntry(
                    id=row["id"],
                    session_id=row["session_id"],
                    event_type=row["event_type"],
                    timestamp=row["timestamp"],
                    brain=row["brain"],
                    snapshot_hash=row["snapshot_hash"],
                    response_hash=row["response_hash"],
                    confidence=row["confidence"],
                    latency_ms=row["latency_ms"],
                    tags=json.loads(row["tags"] or "[]"),
                    metadata=json.loads(row["metadata"] or "{}"),
                )
                for row in rows
            ]


# ═══════════════════════════════════════════════════════════════════════════════
# CHRONICLE WRITER (integrates with SessionRecorder)
# ═══════════════════════════════════════════════════════════════════════════════

class ChronicleWriter:
    """
    Writes session events to the chronicle index.
    Designed to integrate with SessionRecorder.
    """
    
    def __init__(self, index: ChronicleIndex | None = None):
        self.index = index or ChronicleIndex()
        self._current_session: SessionSummary | None = None
        self._event_count = 0
        self._total_confidence = 0.0
        self._total_latency = 0.0
        
    def start_session(
        self, 
        session_id: str, 
        name: str, 
        brain: str | None = None,
        tags: list[str] | None = None,
    ) -> None:
        """Start a new session."""
        self._current_session = SessionSummary(
            session_id=session_id,
            name=name,
            brain=brain,
            start_time=time.time(),
            tags=tags or [],
        )
        self._event_count = 0
        self._total_confidence = 0.0
        self._total_latency = 0.0
        
    def record_event(
        self,
        event_type: str,
        snapshot: Any,
        response: Any,
        latency_ms: float | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record an event to the chronicle."""
        if not self._current_session:
            raise RuntimeError("No active session. Call start_session() first.")
            
        # Hash snapshot and response
        snapshot_json = json.dumps(snapshot, default=str, sort_keys=True)
        response_json = json.dumps(response, default=str, sort_keys=True)
        
        snapshot_hash = hashlib.sha256(snapshot_json.encode()).hexdigest()[:16]
        response_hash = hashlib.sha256(response_json.encode()).hexdigest()[:16]
        
        # Extract confidence if present
        confidence = None
        if isinstance(response, dict) and "confidence" in response:
            confidence = response["confidence"]
        elif hasattr(response, "confidence"):
            confidence = response.confidence
            
        entry = ChronicleEntry(
            id=f"{self._current_session.session_id}-{self._event_count:04d}",
            session_id=self._current_session.session_id,
            event_type=event_type,
            timestamp=time.time(),
            brain=self._current_session.brain,
            snapshot_hash=snapshot_hash,
            response_hash=response_hash,
            confidence=confidence,
            latency_ms=latency_ms,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        self.index.record_event(entry)
        self._event_count += 1
        
        if confidence is not None:
            self._total_confidence += confidence
        if latency_ms is not None:
            self._total_latency += latency_ms
            
    def end_session(self, source_file: str | None = None) -> SessionSummary:
        """End the current session and update the summary."""
        if not self._current_session:
            raise RuntimeError("No active session.")
            
        self._current_session.end_time = time.time()
        self._current_session.event_count = self._event_count
        self._current_session.source_file = source_file
        
        if self._event_count > 0:
            self._current_session.avg_confidence = round(
                self._total_confidence / self._event_count, 3
            )
            self._current_session.avg_latency_ms = round(
                self._total_latency / self._event_count, 2
            )
            
        self.index.register_session(self._current_session)
        
        result = self._current_session
        self._current_session = None
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_chronicle() -> ChronicleIndex:
    """Get the default chronicle index."""
    return ChronicleIndex()


def create_writer() -> ChronicleWriter:
    """Create a new chronicle writer."""
    return ChronicleWriter()
