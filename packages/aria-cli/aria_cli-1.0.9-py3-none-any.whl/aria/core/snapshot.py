"""
ARIA Core - World Snapshot

The input contract for the cognitive engine.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class MetricValue(BaseModel):
    """A metric observation."""
    name: str
    value: float
    unit: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class NodeSnapshot(BaseModel):
    """Snapshot of a single node in the world."""
    id: str
    type: str
    label: str
    district: str = ""
    status: str = "active"
    metrics: list[MetricValue] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @property
    def summary(self) -> str:
        """One-line summary of the node."""
        metric_str = ", ".join(f"{m.name}={m.value}{m.unit}" for m in self.metrics[:3])
        return f"{self.label} ({self.type}) [{metric_str}]"


class FlowSnapshot(BaseModel):
    """Snapshot of a data flow between nodes."""
    id: str
    source_id: str
    target_id: str
    label: str = ""
    rate: float = 0.0
    rate_unit: str = "events/sec"
    status: str = "active"
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @property
    def summary(self) -> str:
        """One-line summary of the flow."""
        return f"{self.source_id} → {self.target_id}: {self.rate} {self.rate_unit}"


class WorldSnapshot(BaseModel):
    """
    Complete snapshot of the world state.
    
    This is the input contract for the cognitive engine.
    A WorldSnapshot captures everything the engine needs to
    generate an explanation.
    """
    
    id: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    nodes: list[NodeSnapshot] = Field(default_factory=list)
    flows: list[FlowSnapshot] = Field(default_factory=list)
    focus_node_ids: list[str] = Field(default_factory=list)
    context: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @classmethod
    def from_file(cls, path: str | Path) -> "WorldSnapshot":
        """Load a snapshot from a JSON file."""
        path = Path(path)
        with open(path) as f:
            data = json.load(f)
        return cls.model_validate(data)
    
    @classmethod
    def from_json(cls, json_str: str) -> "WorldSnapshot":
        """Load a snapshot from a JSON string."""
        data = json.loads(json_str)
        return cls.model_validate(data)
    
    @classmethod
    def from_url(cls, url: str) -> "WorldSnapshot":
        """Load a snapshot from a URL."""
        import httpx
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        return cls.model_validate(response.json())
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorldSnapshot":
        """Load a snapshot from a dictionary."""
        return cls.model_validate(data)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump(mode="json")
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=indent)
    
    def with_focus(self, node_ids: list[str]) -> "WorldSnapshot":
        """Return a new snapshot with the given focus nodes."""
        return self.model_copy(update={"focus_node_ids": node_ids})
    
    def get_node(self, node_id: str) -> NodeSnapshot | None:
        """Get a node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
    
    def get_flow(self, flow_id: str) -> FlowSnapshot | None:
        """Get a flow by ID."""
        for flow in self.flows:
            if flow.id == flow_id:
                return flow
        return None
    
    def get_focus_nodes(self) -> list[NodeSnapshot]:
        """Get the focus nodes."""
        return [n for n in self.nodes if n.id in self.focus_node_ids]
    
    def get_connected_flows(self, node_id: str) -> list[FlowSnapshot]:
        """Get all flows connected to a node."""
        return [f for f in self.flows if f.source_id == node_id or f.target_id == node_id]
    
    @property
    def node_count(self) -> int:
        """Number of nodes."""
        return len(self.nodes)
    
    @property
    def flow_count(self) -> int:
        """Number of flows."""
        return len(self.flows)
    
    @property
    def summary(self) -> str:
        """One-line summary of the world."""
        return f"World: {self.node_count} nodes, {self.flow_count} flows"
