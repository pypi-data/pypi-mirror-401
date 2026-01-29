"""
ARIA Simulator
Deterministic, configurable simulation of ARIA predictive behavior.
Implements ARIA API Reference v0.2 without requiring a real cognitive engine.
"""

from __future__ import annotations

import asyncio
import random
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Iterator

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class PredictMode(str, Enum):
    """Prediction simulation mode."""
    DETERMINISTIC = "deterministic"
    RANDOM = "random"
    SCRIPTED = "scripted"


class SimulatorConfig(BaseModel):
    """Simulator configuration."""
    # Predict settings
    predict_mode: PredictMode = PredictMode.DETERMINISTIC
    predict_latency_ms: int = 200
    predict_confidence_base: float = 0.5
    predict_streaming_chunks: int = 3
    
    # Mesh settings
    mesh_nodes: int = 3
    mesh_roles: list[str] = Field(default_factory=lambda: ["core", "edge"])
    mesh_latency_range_ms: tuple[int, int] = (5, 50)
    
    # Error injection
    error_rate: float = 0.0  # 0.0 to 1.0
    timeout_rate: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE ENVELOPE
# ═══════════════════════════════════════════════════════════════════════════════

class ResponseMeta(BaseModel):
    """Standard response metadata."""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    contract_version: str = "0.2"
    engine_version: str = "simulator-0.1"
    latency_ms: float = 0.0


class AriaResponse(BaseModel):
    """Standard ARIA response envelope."""
    status: str  # "ok", "partial", "error"
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICT SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PredictScript:
    """Scripted prediction sequence."""
    predictions: list[dict[str, Any]]
    current_index: int = 0
    
    def next(self) -> dict[str, Any]:
        """Get next prediction from script."""
        if self.current_index >= len(self.predictions):
            self.current_index = 0
        result = self.predictions[self.current_index]
        self.current_index += 1
        return result


class PredictSimulator:
    """Simulates ARIA predict API."""
    
    DETERMINISTIC_PREDICTIONS = [
        {"prediction": "optimize_buffer", "action": "scale_horizontally"},
        {"prediction": "reduce_latency", "action": "enable_caching"},
        {"prediction": "balance_load", "action": "redistribute_traffic"},
        {"prediction": "heal_connection", "action": "retry_with_backoff"},
        {"prediction": "throttle_requests", "action": "apply_rate_limit"},
    ]
    
    def __init__(self, config: SimulatorConfig):
        self.config = config
        self.deterministic_index = 0
        self.script: PredictScript | None = None
        
    def set_script(self, predictions: list[dict[str, Any]]) -> None:
        """Set scripted prediction sequence."""
        self.script = PredictScript(predictions=predictions)
        
    def _get_base_prediction(self, context: dict[str, Any]) -> dict[str, Any]:
        """Get base prediction based on mode."""
        if self.config.predict_mode == PredictMode.SCRIPTED and self.script:
            return self.script.next()
        elif self.config.predict_mode == PredictMode.RANDOM:
            return random.choice(self.DETERMINISTIC_PREDICTIONS)
        else:
            # Deterministic - cycle through predictions
            pred = self.DETERMINISTIC_PREDICTIONS[self.deterministic_index]
            self.deterministic_index = (self.deterministic_index + 1) % len(self.DETERMINISTIC_PREDICTIONS)
            return pred
            
    def _calculate_confidence(self, stage: str) -> float:
        """Calculate confidence score based on stage."""
        base = self.config.predict_confidence_base
        if stage == "coarse":
            return base * 0.5 + random.uniform(0, 0.1)
        elif stage == "refined":
            return base * 0.75 + random.uniform(0, 0.15)
        else:  # final
            return min(0.99, base + random.uniform(0.2, 0.4))
            
    def predict(self, context: dict[str, Any]) -> AriaResponse:
        """Synchronous prediction."""
        start = time.time()
        
        # Simulate latency
        time.sleep(self.config.predict_latency_ms / 1000)
        
        # Check for error injection
        if random.random() < self.config.error_rate:
            return AriaResponse(
                status="error",
                error={"code": "SIMULATED_ERROR", "message": "Injected error for testing"},
                meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
            )
            
        base = self._get_base_prediction(context)
        confidence = self._calculate_confidence("final")
        
        return AriaResponse(
            status="ok",
            result={
                **base,
                "confidence": round(confidence, 3),
                "details": {"stage": "final", "context_size": len(str(context))},
            },
            meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
        )
        
    def predict_stream(self, context: dict[str, Any]) -> Iterator[AriaResponse]:
        """Streaming prediction with partial results."""
        start = time.time()
        base = self._get_base_prediction(context)
        stages = ["coarse", "refined", "final"]
        chunk_delay = self.config.predict_latency_ms / 1000 / len(stages)
        
        for i, stage in enumerate(stages):
            time.sleep(chunk_delay)
            
            is_final = stage == "final"
            confidence = self._calculate_confidence(stage)
            progress = (i + 1) / len(stages)
            
            yield AriaResponse(
                status="ok" if is_final else "partial",
                result={
                    **base,
                    "confidence": round(confidence, 3),
                    "details": {"stage": stage, "progress": round(progress, 2)},
                },
                meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
            )
            
    async def predict_async(self, context: dict[str, Any]) -> AriaResponse:
        """Async prediction."""
        start = time.time()
        await asyncio.sleep(self.config.predict_latency_ms / 1000)
        
        if random.random() < self.config.error_rate:
            return AriaResponse(
                status="error",
                error={"code": "SIMULATED_ERROR", "message": "Injected error"},
                meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
            )
            
        base = self._get_base_prediction(context)
        confidence = self._calculate_confidence("final")
        
        return AriaResponse(
            status="ok",
            result={**base, "confidence": round(confidence, 3), "details": {"stage": "final"}},
            meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
        )
        
    async def predict_stream_async(self, context: dict[str, Any]) -> AsyncIterator[AriaResponse]:
        """Async streaming prediction."""
        start = time.time()
        base = self._get_base_prediction(context)
        stages = ["coarse", "refined", "final"]
        chunk_delay = self.config.predict_latency_ms / 1000 / len(stages)
        
        for i, stage in enumerate(stages):
            await asyncio.sleep(chunk_delay)
            
            is_final = stage == "final"
            confidence = self._calculate_confidence(stage)
            
            yield AriaResponse(
                status="ok" if is_final else "partial",
                result={
                    **base,
                    "confidence": round(confidence, 3),
                    "details": {"stage": stage, "progress": round((i + 1) / len(stages), 2)},
                },
                meta=ResponseMeta(latency_ms=(time.time() - start) * 1000)
            )


# ═══════════════════════════════════════════════════════════════════════════════
# MESH SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════

class MeshNode(BaseModel):
    """Simulated mesh node."""
    id: str
    role: str  # "core", "edge"
    status: str = "active"  # "active", "degraded", "offline"
    latency_ms: float = 10.0
    capabilities: list[str] = Field(default_factory=list)
    

class MeshLink(BaseModel):
    """Simulated mesh link."""
    source_id: str
    target_id: str
    latency_ms: float = 10.0
    bandwidth_mbps: float = 1000.0
    status: str = "healthy"


class MeshTopology(BaseModel):
    """Full mesh topology."""
    nodes: list[MeshNode]
    links: list[MeshLink]
    timestamp: float = Field(default_factory=time.time)


class MeshSimulator:
    """Simulates ARIA mesh operations."""
    
    def __init__(self, config: SimulatorConfig):
        self.config = config
        self.nodes: dict[str, MeshNode] = {}
        self.links: list[MeshLink] = []
        self._initialize_topology()
        
    def _initialize_topology(self) -> None:
        """Create initial mesh topology."""
        roles = self.config.mesh_roles
        lat_min, lat_max = self.config.mesh_latency_range_ms
        
        # Create nodes
        for i in range(self.config.mesh_nodes):
            node_id = f"node-{i:03d}"
            role = roles[i % len(roles)]
            latency = random.uniform(lat_min, lat_max)
            
            self.nodes[node_id] = MeshNode(
                id=node_id,
                role=role,
                latency_ms=latency,
                capabilities=["predict", "explain"] if role == "core" else ["relay"]
            )
            
        # Create links (mesh - everyone connected to everyone)
        node_ids = list(self.nodes.keys())
        for i, src in enumerate(node_ids):
            for dst in node_ids[i + 1:]:
                self.links.append(MeshLink(
                    source_id=src,
                    target_id=dst,
                    latency_ms=random.uniform(lat_min, lat_max),
                ))
                
    def scan(self) -> AriaResponse:
        """Scan mesh topology."""
        topology = MeshTopology(
            nodes=list(self.nodes.values()),
            links=self.links,
        )
        return AriaResponse(
            status="ok",
            result=topology.model_dump(),
        )
        
    def status(self, node_id: str | None = None) -> AriaResponse:
        """Get mesh status."""
        if node_id:
            if node_id not in self.nodes:
                return AriaResponse(
                    status="error",
                    error={"code": "NODE_NOT_FOUND", "message": f"Node {node_id} not found"},
                )
            return AriaResponse(
                status="ok",
                result=self.nodes[node_id].model_dump(),
            )
        else:
            return AriaResponse(
                status="ok",
                result={
                    "total_nodes": len(self.nodes),
                    "active_nodes": len([n for n in self.nodes.values() if n.status == "active"]),
                    "total_links": len(self.links),
                    "healthy_links": len([l for l in self.links if l.status == "healthy"]),
                },
            )
            
    def connect(self, node_id: str) -> AriaResponse:
        """Connect to a mesh node."""
        if node_id not in self.nodes:
            return AriaResponse(
                status="error",
                error={"code": "NODE_NOT_FOUND", "message": f"Node {node_id} not found"},
            )
            
        node = self.nodes[node_id]
        # Simulate connection latency
        time.sleep(node.latency_ms / 1000)
        
        return AriaResponse(
            status="ok",
            result={
                "connected": True,
                "node_id": node_id,
                "role": node.role,
                "latency_ms": node.latency_ms,
            },
        )
        
    def inject_failure(self, node_id: str) -> None:
        """Inject a node failure for testing."""
        if node_id in self.nodes:
            self.nodes[node_id].status = "offline"
            
    def recover_node(self, node_id: str) -> None:
        """Recover a failed node."""
        if node_id in self.nodes:
            self.nodes[node_id].status = "active"


# ═══════════════════════════════════════════════════════════════════════════════
# CAPABILITY SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════

class CapabilitySimulator:
    """Simulates capability negotiation."""
    
    def __init__(self, config: SimulatorConfig):
        self.config = config
        
    def get_capabilities(self) -> AriaResponse:
        """Return full capability matrix."""
        return AriaResponse(
            status="ok",
            result={
                "predict": {
                    "enabled": True,
                    "streaming": True,
                    "modes": ["deterministic", "random", "scripted"],
                    "max_context_tokens": 4096,
                },
                "mesh": {
                    "enabled": True,
                    "max_nodes": 100,
                    "roles": ["core", "edge"],
                },
                "files": {
                    "enabled": True,
                    "compress": True,
                    "extract": True,
                    "max_size_mb": 100,
                },
                "explain": {
                    "enabled": True,
                    "styles": ["narrative", "technical", "diagnostic"],
                },
            },
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════

class ErrorSimulator:
    """Simulates various error conditions."""
    
    ERROR_TYPES = [
        ("TIMEOUT", "Operation timed out"),
        ("RATE_LIMITED", "Too many requests"),
        ("RESOURCE_EXHAUSTED", "Insufficient resources"),
        ("INVALID_INPUT", "Malformed request"),
        ("INTERNAL_ERROR", "Internal simulator error"),
    ]
    
    def __init__(self, config: SimulatorConfig):
        self.config = config
        
    def maybe_inject_error(self) -> AriaResponse | None:
        """Maybe return an error based on error_rate."""
        if random.random() < self.config.error_rate:
            error_type, message = random.choice(self.ERROR_TYPES)
            return AriaResponse(
                status="error",
                error={"code": error_type, "message": message},
            )
        return None
        
    def timeout_error(self) -> AriaResponse:
        """Return a timeout error."""
        return AriaResponse(
            status="error",
            error={"code": "TIMEOUT", "message": "Operation timed out"},
        )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SIMULATOR CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class AriaSimulator:
    """
    Main ARIA Simulator class.
    Implements ARIA API Reference v0.2 without requiring a real cognitive engine.
    """
    
    def __init__(self, config: SimulatorConfig | None = None):
        self.config = config or SimulatorConfig()
        self.predict = PredictSimulator(self.config)
        self.mesh = MeshSimulator(self.config)
        self.capability = CapabilitySimulator(self.config)
        self.error = ErrorSimulator(self.config)
        
    def status(self) -> AriaResponse:
        """Get simulator status and capabilities."""
        return self.capability.get_capabilities()
        
    def configure(self, **kwargs) -> None:
        """Update simulator configuration."""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                
    def reset(self) -> None:
        """Reset simulator state."""
        self.predict.deterministic_index = 0
        self.predict.script = None
        self.mesh._initialize_topology()


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_simulator(
    mode: str = "deterministic",
    latency_ms: int = 200,
    mesh_nodes: int = 3,
    error_rate: float = 0.0,
) -> AriaSimulator:
    """Create a configured simulator instance."""
    config = SimulatorConfig(
        predict_mode=PredictMode(mode),
        predict_latency_ms=latency_ms,
        mesh_nodes=mesh_nodes,
        error_rate=error_rate,
    )
    return AriaSimulator(config)
