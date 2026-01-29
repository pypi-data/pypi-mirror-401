"""
ARIA Tour - Tour Runner

Execute tours with cognitive explanations.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import AsyncIterator, Callable

from aria.tour.loader import Tour, TourStep


@dataclass
class StepResult:
    """Result from executing a tour step."""
    step: TourStep
    success: bool
    explanation: str | None = None
    error: str | None = None
    duration_ms: float = 0


class TourRunner:
    """Runs tours with optional cognitive explanations."""
    
    def __init__(
        self,
        engine: "AsyncCognitiveEngine | None" = None,
        on_step: Callable[[StepResult], None] | None = None,
    ) -> None:
        self.engine = engine
        self.on_step = on_step
        self._running = False
        self._current_step = 0
    
    async def run(
        self,
        tour: Tour,
        snapshot: "WorldSnapshot | None" = None,
    ) -> list[StepResult]:
        """Run a complete tour."""
        from aria.core.snapshot import WorldSnapshot
        
        self._running = True
        self._current_step = 0
        results = []
        
        # Use empty snapshot if none provided
        if snapshot is None:
            snapshot = WorldSnapshot(nodes=[], flows=[], metrics={})
        
        for i, step in enumerate(tour.steps):
            if not self._running:
                break
            
            self._current_step = i
            result = await self._run_step(step, snapshot)
            results.append(result)
            
            if self.on_step:
                self.on_step(result)
            
            # Handle auto-advance delay
            if step.auto_advance and step.delay_ms > 0:
                await asyncio.sleep(step.delay_ms / 1000)
        
        self._running = False
        return results
    
    async def run_streaming(
        self,
        tour: Tour,
        snapshot: "WorldSnapshot | None" = None,
    ) -> AsyncIterator[StepResult]:
        """Run a tour and yield results as they complete."""
        from aria.core.snapshot import WorldSnapshot
        
        self._running = True
        
        if snapshot is None:
            snapshot = WorldSnapshot(nodes=[], flows=[], metrics={})
        
        for i, step in enumerate(tour.steps):
            if not self._running:
                break
            
            self._current_step = i
            result = await self._run_step(step, snapshot)
            yield result
            
            if step.auto_advance and step.delay_ms > 0:
                await asyncio.sleep(step.delay_ms / 1000)
        
        self._running = False
    
    async def _run_step(
        self,
        step: TourStep,
        snapshot: "WorldSnapshot",
    ) -> StepResult:
        """Execute a single tour step."""
        start = time.perf_counter()
        
        explanation = None
        error = None
        
        if step.trigger_explainer and self.engine:
            try:
                # Focus on specific nodes if specified
                focused_snapshot = snapshot
                if step.focus_nodes:
                    focused_snapshot = snapshot.with_focus(step.focus_nodes)
                
                response = await self.engine.explain_async(
                    focused_snapshot,
                    style=step.explainer_style,
                )
                explanation = response.summary
            except Exception as e:
                error = str(e)
        
        duration = (time.perf_counter() - start) * 1000
        
        return StepResult(
            step=step,
            success=error is None,
            explanation=explanation,
            error=error,
            duration_ms=duration,
        )
    
    def stop(self) -> None:
        """Stop the running tour."""
        self._running = False
    
    @property
    def is_running(self) -> bool:
        """Check if a tour is running."""
        return self._running
    
    @property
    def current_step(self) -> int:
        """Get the current step index."""
        return self._current_step
