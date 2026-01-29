"""
ARIA Core - Explainer Response

The output contract for the cognitive engine.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ExplainerResponse(BaseModel):
    """
    Response from the cognitive engine.
    
    This is the output contract - every explanation
    the engine produces follows this structure.
    """
    
    summary: str
    """One-sentence summary of what's happening."""
    
    details: list[str] = Field(default_factory=list)
    """Additional detail points."""
    
    focus_nodes: list[str] = Field(default_factory=list)
    """Node IDs that are the focus of this explanation."""
    
    confidence: float = 1.0
    """Confidence score (0.0 - 1.0)."""
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    """When this response was generated."""
    
    metadata: dict[str, Any] = Field(default_factory=dict)
    """Additional metadata."""
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(mode="json")
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=indent)
    
    @property
    def is_valid(self) -> bool:
        """Check if the response is valid."""
        return bool(self.summary) and self.confidence > 0
    
    @property
    def is_degraded(self) -> bool:
        """Check if this is a degraded/fallback response."""
        return self.confidence == 0.0 or "unavailable" in self.summary.lower()
    
    def __str__(self) -> str:
        return self.summary
    
    def __repr__(self) -> str:
        return f"ExplainerResponse(summary={self.summary!r}, confidence={self.confidence})"
