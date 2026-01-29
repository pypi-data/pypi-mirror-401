"""
ARIA Watch - File Monitor

Watch for holomap changes and trigger explanations.
"""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent
except ImportError:
    Observer = None
    FileSystemEventHandler = object


@dataclass
class WatchEvent:
    """An event from watching a file or directory."""
    path: str
    event_type: str  # modified, created, deleted
    timestamp: float
    explanation: str | None = None


class HolomapEventHandler(FileSystemEventHandler):
    """Handle file system events for holomap files."""
    
    def __init__(
        self,
        callback: Callable[[WatchEvent], None],
        patterns: list[str] | None = None,
    ) -> None:
        self.callback = callback
        self.patterns = patterns or ["*.json"]
        self._last_modified: dict[str, float] = {}
        self._debounce_ms = 500
    
    def on_modified(self, event: "FileModifiedEvent") -> None:
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        
        # Check if matches patterns
        if not any(path.match(p) for p in self.patterns):
            return
        
        # Debounce rapid modifications
        now = time.time()
        last = self._last_modified.get(str(path), 0)
        if (now - last) * 1000 < self._debounce_ms:
            return
        
        self._last_modified[str(path)] = now
        
        self.callback(WatchEvent(
            path=str(path),
            event_type="modified",
            timestamp=now,
        ))


class HolomapWatcher:
    """Watch directories for holomap changes."""
    
    def __init__(
        self,
        paths: list[Path],
        patterns: list[str] | None = None,
    ) -> None:
        if Observer is None:
            raise RuntimeError(
                "watchdog is required for file watching. "
                "Install it with: pip install watchdog"
            )
        
        self.paths = paths
        self.patterns = patterns or ["*.json", "*.holomap"]
        self._observer: Observer | None = None
        self._callbacks: list[Callable[[WatchEvent], None]] = []
        self._running = False
    
    def on_change(self, callback: Callable[[WatchEvent], None]) -> None:
        """Register a callback for change events."""
        self._callbacks.append(callback)
    
    def _handle_event(self, event: WatchEvent) -> None:
        """Dispatch event to all callbacks."""
        for callback in self._callbacks:
            try:
                callback(event)
            except Exception:
                pass  # Don't let callback errors stop the watcher
    
    def start(self) -> None:
        """Start watching for changes."""
        if self._running:
            return
        
        self._observer = Observer()
        handler = HolomapEventHandler(
            callback=self._handle_event,
            patterns=self.patterns,
        )
        
        for path in self.paths:
            if path.exists():
                self._observer.schedule(
                    handler,
                    str(path),
                    recursive=True,
                )
        
        self._observer.start()
        self._running = True
    
    def stop(self) -> None:
        """Stop watching."""
        if self._observer and self._running:
            self._observer.stop()
            self._observer.join()
            self._running = False
    
    @property
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self._running


class CognitiveWatcher:
    """Watch for changes and generate cognitive explanations."""
    
    def __init__(
        self,
        paths: list[Path],
        engine: "AsyncCognitiveEngine | None" = None,
    ) -> None:
        self.watcher = HolomapWatcher(paths)
        self.engine = engine
        self._event_log: list[WatchEvent] = []
    
    async def start_async(self, on_event: Callable[[WatchEvent], None] | None = None) -> None:
        """Start watching with async explanation generation."""
        
        async def handle_change(event: WatchEvent) -> None:
            self._event_log.append(event)
            
            # Generate explanation if engine available
            if self.engine:
                try:
                    from aria.core.snapshot import WorldSnapshot
                    
                    with open(event.path) as f:
                        data = json.load(f)
                    
                    snapshot = WorldSnapshot.from_json(data)
                    response = await self.engine.explain_async(snapshot, style="brief")
                    event.explanation = response.summary
                except Exception:
                    pass
            
            if on_event:
                on_event(event)
        
        # Wrap async handler for sync callback
        loop = asyncio.get_event_loop()
        
        def sync_handler(event: WatchEvent) -> None:
            asyncio.run_coroutine_threadsafe(handle_change(event), loop)
        
        self.watcher.on_change(sync_handler)
        self.watcher.start()
        
        # Keep running
        try:
            while self.watcher.is_running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            self.watcher.stop()
    
    def stop(self) -> None:
        """Stop watching."""
        self.watcher.stop()
    
    @property
    def events(self) -> list[WatchEvent]:
        """Get logged events."""
        return self._event_log
