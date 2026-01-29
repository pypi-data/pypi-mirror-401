"""
ARIA Predictive Flow Runner
Cognitive loop integration for predictive events.
Enables Lenix/ARIA systems to run predictive cognitive events.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Callable, Iterator

from pydantic import BaseModel, Field

from aria.core.snapshot import WorldSnapshot
from aria.core.response import ExplainerResponse


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTIVE FLOW MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class FlowState(str, Enum):
    """Predictive flow execution state."""
    PENDING = "pending"
    RUNNING = "running"
    STREAMING = "streaming"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PredictionType(str, Enum):
    """Type of prediction to generate."""
    ACTION = "action"           # What action to take
    OUTCOME = "outcome"         # What will happen
    DIAGNOSIS = "diagnosis"     # What's wrong
    OPTIMIZATION = "optimization"  # How to improve
    ANOMALY = "anomaly"        # What's unusual


class FlowConfig(BaseModel):
    """Configuration for a predictive flow."""
    prediction_type: PredictionType = PredictionType.ACTION
    streaming: bool = True
    timeout_ms: int = 30000
    max_retries: int = 3
    confidence_threshold: float = 0.5
    include_reasoning: bool = True
    grounding_rules: list[str] = Field(default_factory=list)
    prompt_pack: str | None = None


class PredictiveResult(BaseModel):
    """Result of a predictive flow."""
    flow_id: str
    prediction: str
    prediction_type: PredictionType
    confidence: float
    reasoning: str | None = None
    suggested_actions: list[str] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = 0.0
    timestamp: float = Field(default_factory=time.time)


class StreamChunk(BaseModel):
    """A chunk of streaming prediction output."""
    flow_id: str
    chunk_index: int
    content: str
    stage: str  # "coarse", "refined", "final"
    confidence: float
    is_final: bool = False


class FlowEvent(BaseModel):
    """Event emitted during flow execution."""
    flow_id: str
    event_type: str  # "started", "progress", "chunk", "completed", "failed"
    timestamp: float = Field(default_factory=time.time)
    data: dict[str, Any] = Field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# GROUNDING RULES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GroundingRule:
    """A rule for grounding predictions in reality."""
    name: str
    condition: Callable[[WorldSnapshot], bool]
    context: str  # Additional context to inject when rule matches
    priority: int = 0


class GroundingEngine:
    """Applies grounding rules to prediction context."""
    
    def __init__(self):
        self.rules: list[GroundingRule] = []
        self._load_default_rules()
        
    def _load_default_rules(self) -> None:
        """Load default grounding rules."""
        self.rules = [
            GroundingRule(
                name="high_error_rate",
                condition=lambda s: any(
                    any(m.name == "error_rate" and m.value > 5 for m in n.metrics)
                    for n in s.nodes
                ),
                context="System is experiencing elevated error rates. Prioritize stability.",
                priority=10,
            ),
            GroundingRule(
                name="high_latency",
                condition=lambda s: any(
                    any(m.name == "latency" and m.value > 200 for m in n.metrics)
                    for n in s.nodes
                ),
                context="High latency detected. Consider caching or scaling.",
                priority=8,
            ),
            GroundingRule(
                name="resource_exhaustion",
                condition=lambda s: any(
                    n.status == "critical" for n in s.nodes
                ),
                context="Critical resource exhaustion. Immediate action required.",
                priority=15,
            ),
            GroundingRule(
                name="degraded_service",
                condition=lambda s: any(
                    n.status == "degraded" for n in s.nodes
                ),
                context="Service degradation detected. Monitor closely.",
                priority=5,
            ),
        ]
        
    def add_rule(self, rule: GroundingRule) -> None:
        """Add a custom grounding rule."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -r.priority)
        
    def apply(self, snapshot: WorldSnapshot) -> list[str]:
        """Apply grounding rules and return matching contexts."""
        contexts = []
        for rule in self.rules:
            try:
                if rule.condition(snapshot):
                    contexts.append(f"[{rule.name}] {rule.context}")
            except Exception:
                pass  # Skip failing rules
        return contexts


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT PACKS
# ═══════════════════════════════════════════════════════════════════════════════

class PromptPack(BaseModel):
    """A prompt template pack for predictions."""
    name: str
    description: str
    system_prompt: str
    prediction_template: str
    streaming_template: str | None = None
    variables: dict[str, str] = Field(default_factory=dict)


class PromptPackRegistry:
    """Registry of prompt packs."""
    
    DEFAULT_PACKS: dict[str, PromptPack] = {
        "default": PromptPack(
            name="default",
            description="General-purpose prediction pack",
            system_prompt="You are ARIA, an adaptive runtime intelligence system.",
            prediction_template="""
Analyze the following system state and provide a {prediction_type} prediction.

System Context:
{context}

Grounding:
{grounding}

Nodes: {node_count}
Focus: {focus_nodes}

Provide a clear, actionable prediction with confidence level.
""",
        ),
        "incident": PromptPack(
            name="incident",
            description="Incident response prediction pack",
            system_prompt="You are ARIA in incident response mode. Prioritize rapid diagnosis and mitigation.",
            prediction_template="""
INCIDENT ANALYSIS

Current State:
{context}

Symptoms:
{grounding}

Affected Components: {focus_nodes}

Provide:
1. Root cause hypothesis (with confidence)
2. Immediate mitigation steps
3. Long-term fix recommendation
""",
        ),
        "optimization": PromptPack(
            name="optimization",
            description="Performance optimization pack",
            system_prompt="You are ARIA in optimization mode. Focus on efficiency and scalability.",
            prediction_template="""
PERFORMANCE ANALYSIS

Current Metrics:
{context}

Observations:
{grounding}

Target Components: {focus_nodes}

Suggest optimizations with expected impact and implementation effort.
""",
        ),
    }
    
    def __init__(self):
        self.packs = dict(self.DEFAULT_PACKS)
        
    def get(self, name: str) -> PromptPack | None:
        """Get a prompt pack by name."""
        return self.packs.get(name)
        
    def register(self, pack: PromptPack) -> None:
        """Register a custom prompt pack."""
        self.packs[pack.name] = pack
        
    def list_packs(self) -> list[str]:
        """List available prompt pack names."""
        return list(self.packs.keys())


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTIVE FLOW RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

class PredictiveFlowRunner:
    """
    Runs predictive cognitive flows.
    
    Integrates with CognitiveEngine or AriaSimulator to generate predictions
    based on WorldSnapshot state.
    """
    
    def __init__(
        self,
        engine: Any = None,  # CognitiveEngine or AriaSimulator
        grounding: GroundingEngine | None = None,
        prompts: PromptPackRegistry | None = None,
    ):
        self.engine = engine
        self.grounding = grounding or GroundingEngine()
        self.prompts = prompts or PromptPackRegistry()
        self._active_flows: dict[str, FlowState] = {}
        self._event_handlers: list[Callable[[FlowEvent], None]] = []
        
    def on_event(self, handler: Callable[[FlowEvent], None]) -> None:
        """Register an event handler."""
        self._event_handlers.append(handler)
        
    def _emit_event(self, event: FlowEvent) -> None:
        """Emit an event to all handlers."""
        for handler in self._event_handlers:
            try:
                handler(event)
            except Exception:
                pass
                
    def _build_prompt(
        self,
        snapshot: WorldSnapshot,
        config: FlowConfig,
    ) -> str:
        """Build the prediction prompt."""
        pack = self.prompts.get(config.prompt_pack or "default")
        if not pack:
            pack = self.prompts.get("default")
            
        # Apply grounding rules
        grounding_contexts = self.grounding.apply(snapshot)
        grounding_contexts.extend(config.grounding_rules)
        
        # Build context
        context = snapshot.context or "No context provided"
        focus_nodes = ", ".join(snapshot.focus_node_ids) if snapshot.focus_node_ids else "all"
        
        return pack.prediction_template.format(
            prediction_type=config.prediction_type.value,
            context=context,
            grounding="\n".join(grounding_contexts) or "None",
            node_count=len(snapshot.nodes),
            focus_nodes=focus_nodes,
        )
        
    def run(
        self,
        snapshot: WorldSnapshot,
        config: FlowConfig | None = None,
    ) -> PredictiveResult:
        """
        Run a synchronous predictive flow.
        
        Args:
            snapshot: Current world state
            config: Flow configuration
            
        Returns:
            PredictiveResult with prediction and confidence
        """
        config = config or FlowConfig()
        flow_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        self._active_flows[flow_id] = FlowState.RUNNING
        self._emit_event(FlowEvent(flow_id=flow_id, event_type="started"))
        
        try:
            prompt = self._build_prompt(snapshot, config)
            
            # Use engine if available
            if self.engine:
                if hasattr(self.engine, "explain"):
                    # CognitiveEngine
                    response = self.engine.explain(snapshot, style="diagnostic")
                    prediction = response.summary
                    confidence = response.confidence
                    reasoning = "\n".join(response.details) if response.details else None
                elif hasattr(self.engine, "predict"):
                    # AriaSimulator
                    result = self.engine.predict.predict({"prompt": prompt})
                    prediction = result.result.get("prediction", "unknown") if result.result else "unknown"
                    confidence = result.result.get("confidence", 0.5) if result.result else 0.5
                    reasoning = None
                else:
                    raise ValueError("Engine must have 'explain' or 'predict' method")
            else:
                # No engine - return placeholder
                prediction = f"[{config.prediction_type.value}] Analysis required"
                confidence = 0.0
                reasoning = "No cognitive engine available"
                
            latency_ms = (time.time() - start_time) * 1000
            
            result = PredictiveResult(
                flow_id=flow_id,
                prediction=prediction,
                prediction_type=config.prediction_type,
                confidence=confidence,
                reasoning=reasoning if config.include_reasoning else None,
                latency_ms=latency_ms,
            )
            
            self._active_flows[flow_id] = FlowState.COMPLETED
            self._emit_event(FlowEvent(
                flow_id=flow_id,
                event_type="completed",
                data={"confidence": confidence, "latency_ms": latency_ms}
            ))
            
            return result
            
        except Exception as e:
            self._active_flows[flow_id] = FlowState.FAILED
            self._emit_event(FlowEvent(
                flow_id=flow_id,
                event_type="failed",
                data={"error": str(e)}
            ))
            raise
            
    def run_stream(
        self,
        snapshot: WorldSnapshot,
        config: FlowConfig | None = None,
    ) -> Iterator[StreamChunk]:
        """
        Run a streaming predictive flow.
        
        Yields StreamChunk objects as prediction develops.
        """
        config = config or FlowConfig(streaming=True)
        flow_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        self._active_flows[flow_id] = FlowState.STREAMING
        self._emit_event(FlowEvent(flow_id=flow_id, event_type="started"))
        
        try:
            prompt = self._build_prompt(snapshot, config)
            
            if self.engine and hasattr(self.engine, "predict"):
                # Use simulator streaming
                chunk_index = 0
                for response in self.engine.predict.predict_stream({"prompt": prompt}):
                    is_final = response.status == "ok"
                    stage = response.result.get("details", {}).get("stage", "unknown") if response.result else "unknown"
                    confidence = response.result.get("confidence", 0.5) if response.result else 0.5
                    
                    chunk = StreamChunk(
                        flow_id=flow_id,
                        chunk_index=chunk_index,
                        content=response.result.get("prediction", "") if response.result else "",
                        stage=stage,
                        confidence=confidence,
                        is_final=is_final,
                    )
                    
                    self._emit_event(FlowEvent(
                        flow_id=flow_id,
                        event_type="chunk",
                        data=chunk.model_dump()
                    ))
                    
                    yield chunk
                    chunk_index += 1
            else:
                # Fallback - single chunk
                yield StreamChunk(
                    flow_id=flow_id,
                    chunk_index=0,
                    content=f"[{config.prediction_type.value}] Analysis required",
                    stage="final",
                    confidence=0.0,
                    is_final=True,
                )
                
            self._active_flows[flow_id] = FlowState.COMPLETED
            self._emit_event(FlowEvent(
                flow_id=flow_id,
                event_type="completed",
                data={"latency_ms": (time.time() - start_time) * 1000}
            ))
            
        except Exception as e:
            self._active_flows[flow_id] = FlowState.FAILED
            self._emit_event(FlowEvent(
                flow_id=flow_id,
                event_type="failed",
                data={"error": str(e)}
            ))
            raise
            
    async def run_async(
        self,
        snapshot: WorldSnapshot,
        config: FlowConfig | None = None,
    ) -> PredictiveResult:
        """Async version of run()."""
        config = config or FlowConfig()
        flow_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        self._active_flows[flow_id] = FlowState.RUNNING
        
        try:
            prompt = self._build_prompt(snapshot, config)
            
            if self.engine and hasattr(self.engine, "predict"):
                response = await self.engine.predict.predict_async({"prompt": prompt})
                prediction = response.result.get("prediction", "unknown") if response.result else "unknown"
                confidence = response.result.get("confidence", 0.5) if response.result else 0.5
            else:
                prediction = f"[{config.prediction_type.value}] Analysis required"
                confidence = 0.0
                
            latency_ms = (time.time() - start_time) * 1000
            
            self._active_flows[flow_id] = FlowState.COMPLETED
            
            return PredictiveResult(
                flow_id=flow_id,
                prediction=prediction,
                prediction_type=config.prediction_type,
                confidence=confidence,
                latency_ms=latency_ms,
            )
            
        except Exception as e:
            self._active_flows[flow_id] = FlowState.FAILED
            raise
            
    async def run_stream_async(
        self,
        snapshot: WorldSnapshot,
        config: FlowConfig | None = None,
    ) -> AsyncIterator[StreamChunk]:
        """Async streaming version."""
        config = config or FlowConfig(streaming=True)
        flow_id = str(uuid.uuid4())[:8]
        
        self._active_flows[flow_id] = FlowState.STREAMING
        
        try:
            prompt = self._build_prompt(snapshot, config)
            
            if self.engine and hasattr(self.engine, "predict"):
                chunk_index = 0
                async for response in self.engine.predict.predict_stream_async({"prompt": prompt}):
                    is_final = response.status == "ok"
                    stage = response.result.get("details", {}).get("stage", "unknown") if response.result else "unknown"
                    confidence = response.result.get("confidence", 0.5) if response.result else 0.5
                    
                    yield StreamChunk(
                        flow_id=flow_id,
                        chunk_index=chunk_index,
                        content=response.result.get("prediction", "") if response.result else "",
                        stage=stage,
                        confidence=confidence,
                        is_final=is_final,
                    )
                    chunk_index += 1
            else:
                yield StreamChunk(
                    flow_id=flow_id,
                    chunk_index=0,
                    content=f"[{config.prediction_type.value}] Analysis required",
                    stage="final",
                    confidence=0.0,
                    is_final=True,
                )
                
            self._active_flows[flow_id] = FlowState.COMPLETED
            
        except Exception as e:
            self._active_flows[flow_id] = FlowState.FAILED
            raise
            
    def cancel(self, flow_id: str) -> bool:
        """Cancel a running flow."""
        if flow_id in self._active_flows:
            self._active_flows[flow_id] = FlowState.CANCELLED
            self._emit_event(FlowEvent(flow_id=flow_id, event_type="cancelled"))
            return True
        return False
        
    def get_state(self, flow_id: str) -> FlowState | None:
        """Get the state of a flow."""
        return self._active_flows.get(flow_id)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_flow_runner(engine: Any = None) -> PredictiveFlowRunner:
    """Create a predictive flow runner."""
    return PredictiveFlowRunner(engine=engine)


def quick_predict(
    snapshot: WorldSnapshot,
    engine: Any = None,
    prediction_type: str = "action",
) -> PredictiveResult:
    """Quick one-shot prediction."""
    runner = PredictiveFlowRunner(engine=engine)
    config = FlowConfig(
        prediction_type=PredictionType(prediction_type),
        streaming=False,
    )
    return runner.run(snapshot, config)
