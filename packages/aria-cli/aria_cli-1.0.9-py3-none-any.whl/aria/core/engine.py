"""
ARIA Core - Cognitive Engine
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from aria.core.snapshot import WorldSnapshot
    from aria.core.response import ExplainerResponse


class EngineConfig(BaseModel):
    """Configuration for the cognitive engine."""
    brain: str = "tinyllama"
    model_path: Path | None = None
    context_size: int = 2048
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    timeout: float = 30.0
    graceful_degradation: bool = False


class CognitiveEngine:
    """
    The cognitive engine that generates explanations from world snapshots.
    
    This is the core of ARIA - it takes a WorldSnapshot and produces
    an ExplainerResponse using an LLM brain.
    
    Example:
        engine = CognitiveEngine(brain="tinyllama")
        response = engine.explain(snapshot)
        print(response.summary)
    """
    
    def __init__(
        self,
        brain: str = "tinyllama",
        config: EngineConfig | None = None,
    ) -> None:
        self.config = config or EngineConfig(brain=brain)
        self._llm = None
        self._loaded = False
        self._load_error: str | None = None
    
    def _ensure_loaded(self) -> None:
        """Lazy-load the LLM."""
        if self._loaded:
            return
        
        from aria.brain.loader import load_brain
        try:
            self._llm = load_brain(self.config.brain, self.config)
            self._loaded = True
        except Exception as e:
            if self.config.graceful_degradation:
                self._load_error = str(e)
                self._loaded = True  # Mark as loaded to prevent retries
            else:
                raise
    
    def explain(
        self,
        snapshot: "WorldSnapshot",
        style: str = "narrative",
        focus: list[str] | None = None,
    ) -> "ExplainerResponse":
        """
        Generate an explanation from a world snapshot.
        
        Args:
            snapshot: The world state to explain
            style: Explanation style (narrative, technical, brief)
            focus: Optional list of node IDs to focus on
            
        Returns:
            ExplainerResponse with summary, details, and focus nodes
        """
        self._ensure_loaded()
        
        from aria.core.prompt import build_prompt
        from aria.core.parser import parse_response
        from aria.core.response import ExplainerResponse
        
        # Handle load error in graceful degradation mode
        if self._llm is None and self._load_error:
            return ExplainerResponse(
                summary=f"Brain unavailable: {self._load_error}",
                details=[],
                focus_nodes=[],
                confidence=0.0,
            )
        
        # Build prompt
        prompt = build_prompt(snapshot, style=style, focus=focus)
        
        # Run completion
        try:
            raw_response = self._llm.complete(
                prompt,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            # Parse response
            response = parse_response(raw_response, snapshot)
            
        except Exception as e:
            # Graceful degradation
            response = ExplainerResponse(
                summary=f"Cognition unavailable: {str(e)}",
                details=[],
                focus_nodes=[],
                confidence=0.0,
            )
        
        return response
    
    def close(self) -> None:
        """Release resources."""
        if self._llm is not None:
            self._llm.close()
            self._llm = None
            self._loaded = False
    
    def __enter__(self) -> "CognitiveEngine":
        return self
    
    def __exit__(self, *args) -> None:
        self.close()


class AsyncCognitiveEngine:
    """
    Async version of the cognitive engine.
    
    Example:
        async with AsyncCognitiveEngine(brain="phi2") as engine:
            response = await engine.explain_async(snapshot)
    """
    
    def __init__(
        self,
        brain: str = "tinyllama",
        config: EngineConfig | None = None,
    ) -> None:
        self.config = config or EngineConfig(brain=brain)
        self._llm = None
        self._loaded = False
        self._lock = asyncio.Lock()
    
    async def _ensure_loaded(self) -> None:
        """Lazy-load the LLM."""
        async with self._lock:
            if self._loaded:
                return
            
            from aria.brain.loader import load_brain
            self._llm = load_brain(self.config.brain, self.config)
            self._loaded = True
    
    async def explain_async(
        self,
        snapshot: "WorldSnapshot",
        style: str = "narrative",
        focus: list[str] | None = None,
    ) -> "ExplainerResponse":
        """
        Generate an explanation asynchronously.
        
        Args:
            snapshot: The world state to explain
            style: Explanation style
            focus: Optional focus nodes
            
        Returns:
            ExplainerResponse
        """
        await self._ensure_loaded()
        
        from aria.core.prompt import build_prompt
        from aria.core.parser import parse_response
        from aria.core.response import ExplainerResponse
        
        prompt = build_prompt(snapshot, style=style, focus=focus)
        
        try:
            # Run in executor for non-blocking
            loop = asyncio.get_event_loop()
            raw_response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: self._llm.complete(
                        prompt,
                        max_tokens=self.config.max_tokens,
                        temperature=self.config.temperature,
                    )
                ),
                timeout=self.config.timeout
            )
            
            response = parse_response(raw_response, snapshot)
            
        except asyncio.TimeoutError:
            response = ExplainerResponse(
                summary="Cognition timed out; retaining prior state.",
                details=[],
                focus_nodes=[],
                confidence=0.0,
            )
        except Exception as e:
            response = ExplainerResponse(
                summary=f"Cognition unavailable: {str(e)}",
                details=[],
                focus_nodes=[],
                confidence=0.0,
            )
        
        return response
    
    async def close(self) -> None:
        """Release resources."""
        if self._llm is not None:
            self._llm.close()
            self._llm = None
            self._loaded = False
    
    async def __aenter__(self) -> "AsyncCognitiveEngine":
        return self
    
    async def __aexit__(self, *args) -> None:
        await self.close()
