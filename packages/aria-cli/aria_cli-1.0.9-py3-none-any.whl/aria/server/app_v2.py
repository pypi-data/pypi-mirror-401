"""
ARIA FastAPI Server v2
Enhanced REST API + WebSocket streaming for ARIA cognitive services.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    FastAPI = None

from pydantic import BaseModel, Field

from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot, MetricValue
from aria.core.engine import CognitiveEngine, EngineConfig
from aria.core.session import SessionRecorder
from aria.simulator import AriaSimulator, SimulatorConfig, PredictMode
from aria.chronicle import ChronicleIndex, ChronicleWriter, ChronicleQuery
from aria.flow import PredictiveFlowRunner, FlowConfig, PredictionType
from aria.brain.manager import BrainManager
from aria.holomap.validator import validate_holomap
from aria.holomap.diff import diff_snapshots


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class ExplainRequest(BaseModel):
    """Request for cognitive explanation."""
    snapshot: WorldSnapshot
    style: str = "narrative"
    brain: str | None = None
    stream: bool = False


class ExplainResponse(BaseModel):
    """Response from cognitive explanation."""
    status: str
    summary: str
    confidence: float
    details: list[str] = Field(default_factory=list)
    latency_ms: float
    brain: str
    meta: dict[str, Any] = Field(default_factory=dict)


class PredictRequest(BaseModel):
    """Request for prediction."""
    snapshot: WorldSnapshot
    prediction_type: str = "action"
    stream: bool = False
    prompt_pack: str | None = None
    grounding_rules: list[str] = Field(default_factory=list)


class PredictResponse(BaseModel):
    """Response from prediction."""
    status: str
    prediction: str
    prediction_type: str
    confidence: float
    reasoning: str | None = None
    latency_ms: float
    flow_id: str
    meta: dict[str, Any] = Field(default_factory=dict)


class StatusResponse(BaseModel):
    """Server status response."""
    status: str
    version: str
    engine: str
    brains: list[dict[str, Any]]
    capabilities: dict[str, Any]
    uptime_seconds: float


class HolomapValidateRequest(BaseModel):
    """Request to validate a holomap."""
    data: dict[str, Any]


class HolomapDiffRequest(BaseModel):
    """Request to diff two snapshots."""
    old: WorldSnapshot
    new: WorldSnapshot


class SessionStartRequest(BaseModel):
    """Request to start a session."""
    name: str
    brain: str | None = None
    tags: list[str] = Field(default_factory=list)


class SessionEventRequest(BaseModel):
    """Request to record a session event."""
    session_id: str
    snapshot: WorldSnapshot
    response: dict[str, Any]


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER STATE
# ═══════════════════════════════════════════════════════════════════════════════

class ServerState:
    """Global server state."""
    
    def __init__(self):
        self.start_time = time.time()
        self.engine: CognitiveEngine | None = None
        self.simulator: AriaSimulator | None = None
        self.brain_manager = BrainManager()
        self.chronicle = ChronicleIndex()
        self.flow_runner: PredictiveFlowRunner | None = None
        self.active_sessions: dict[str, SessionRecorder] = {}
        self.websocket_connections: list[Any] = []
        self.use_simulator = False
        self.current_brain = "tinyllama"
        
    def get_engine(self, brain: str | None = None) -> CognitiveEngine | AriaSimulator:
        """Get the cognitive engine or simulator."""
        if self.use_simulator:
            if not self.simulator:
                self.simulator = AriaSimulator()
            return self.simulator
            
        target_brain = brain or self.current_brain
        
        if not self.engine or self.current_brain != target_brain:
            if self.engine:
                self.engine.close()
            config = EngineConfig(brain=target_brain, graceful_degradation=True)
            self.engine = CognitiveEngine(config=config)
            self.current_brain = target_brain
            
        return self.engine
        
    def get_flow_runner(self, brain: str | None = None) -> PredictiveFlowRunner:
        """Get the predictive flow runner."""
        engine = self.get_engine(brain)
        return PredictiveFlowRunner(engine=engine)


# Global state
_state: ServerState | None = None


def get_state() -> ServerState:
    """Get global server state."""
    global _state
    if _state is None:
        _state = ServerState()
    return _state


# ═══════════════════════════════════════════════════════════════════════════════
# APP FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def create_app() -> "FastAPI":
    """Create the FastAPI application."""
    if not HAS_FASTAPI:
        raise ImportError("FastAPI not installed. Run: pip install fastapi uvicorn")
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan handler."""
        state = get_state()
        print("🧠 ARIA Server starting...")
        yield
        if state.engine:
            state.engine.close()
        for session in state.active_sessions.values():
            session.close()
        print("🧠 ARIA Server stopped.")
    
    app = FastAPI(
        title="ARIA Server",
        description="Adaptive Runtime Intelligence Architecture - REST API & WebSocket",
        version="0.2.0",
        lifespan=lifespan,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ═══════════════════════════════════════════════════════════════════════
    # HEALTH & STATUS ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "ARIA Server", "version": "0.2.0", "docs": "/docs"}
    
    @app.get("/health")
    async def health():
        """Health check."""
        return {"status": "healthy", "timestamp": time.time()}
    
    @app.get("/status", response_model=StatusResponse)
    async def status():
        """Get server status and capabilities."""
        state = get_state()
        brains = state.brain_manager.list_brains()
        
        return StatusResponse(
            status="ok",
            version="0.2.0",
            engine="simulator" if state.use_simulator else "cognitive",
            brains=[{"name": b.name, "status": b.status, "size": b.size} for b in brains],
            capabilities={
                "explain": {"enabled": True, "streaming": True, "styles": ["narrative", "technical", "diagnostic"]},
                "predict": {"enabled": True, "streaming": True, "types": ["action", "outcome", "diagnosis", "optimization"]},
                "mesh": {"enabled": True},
                "session": {"enabled": True},
                "chronicle": {"enabled": True},
            },
            uptime_seconds=time.time() - state.start_time,
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # BRAIN ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.get("/brains")
    async def list_brains():
        """List available brains."""
        state = get_state()
        brains = state.brain_manager.list_brains()
        return {
            "brains": [b.model_dump() for b in brains],
            "current": state.current_brain,
        }
    
    @app.post("/brains/select/{brain}")
    async def select_brain(brain: str):
        """Select the active brain."""
        state = get_state()
        brains = state.brain_manager.list_brains()
        available = [b.name for b in brains if b.status == "installed"]
        
        if brain not in available:
            raise HTTPException(404, f"Brain '{brain}' not found or not installed")
            
        state.current_brain = brain
        if state.engine:
            state.engine.close()
            state.engine = None
            
        return {"status": "ok", "brain": brain}
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXPLAIN ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.post("/explain", response_model=ExplainResponse)
    async def explain(request: ExplainRequest):
        """Generate cognitive explanation."""
        state = get_state()
        start_time = time.time()
        
        try:
            engine = state.get_engine(request.brain)
            
            if hasattr(engine, "explain"):
                response = engine.explain(request.snapshot, style=request.style)
                summary = response.summary
                confidence = response.confidence
                details = response.details
            else:
                result = engine.predict.predict({"snapshot": request.snapshot.model_dump()})
                summary = str(result.result.get("prediction", "")) if result.result else ""
                confidence = result.result.get("confidence", 0.5) if result.result else 0.5
                details = []
                
            latency_ms = (time.time() - start_time) * 1000
            
            return ExplainResponse(
                status="ok",
                summary=summary,
                confidence=confidence,
                details=details,
                latency_ms=latency_ms,
                brain=request.brain or state.current_brain,
                meta={"style": request.style},
            )
            
        except Exception as e:
            raise HTTPException(500, str(e))
    
    @app.post("/explain/stream")
    async def explain_stream(request: ExplainRequest):
        """Stream cognitive explanation."""
        state = get_state()
        
        async def generate():
            start_time = time.time()
            engine = state.get_engine(request.brain)
            
            if hasattr(engine, "predict") and hasattr(engine.predict, "predict_stream"):
                for response in engine.predict.predict_stream({"snapshot": request.snapshot.model_dump()}):
                    chunk = {
                        "status": response.status,
                        "content": response.result.get("prediction", "") if response.result else "",
                        "confidence": response.result.get("confidence", 0) if response.result else 0,
                        "stage": response.result.get("details", {}).get("stage", "") if response.result else "",
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    await asyncio.sleep(0)
            else:
                response = engine.explain(request.snapshot, style=request.style)
                yield f"data: {json.dumps({'status': 'ok', 'content': response.summary, 'confidence': response.confidence})}\n\n"
                
            yield f"data: {json.dumps({'status': 'done', 'latency_ms': (time.time() - start_time) * 1000})}\n\n"
            
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PREDICT ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.post("/predict", response_model=PredictResponse)
    async def predict(request: PredictRequest):
        """Generate prediction."""
        state = get_state()
        start_time = time.time()
        
        try:
            runner = state.get_flow_runner()
            config = FlowConfig(
                prediction_type=PredictionType(request.prediction_type),
                streaming=False,
                prompt_pack=request.prompt_pack,
                grounding_rules=request.grounding_rules,
            )
            
            result = runner.run(request.snapshot, config)
            latency_ms = (time.time() - start_time) * 1000
            
            return PredictResponse(
                status="ok",
                prediction=result.prediction,
                prediction_type=result.prediction_type.value,
                confidence=result.confidence,
                reasoning=result.reasoning,
                latency_ms=latency_ms,
                flow_id=result.flow_id,
            )
            
        except Exception as e:
            raise HTTPException(500, str(e))
    
    @app.post("/predict/stream")
    async def predict_stream(request: PredictRequest):
        """Stream prediction."""
        state = get_state()
        
        async def generate():
            runner = state.get_flow_runner()
            config = FlowConfig(
                prediction_type=PredictionType(request.prediction_type),
                streaming=True,
                prompt_pack=request.prompt_pack,
                grounding_rules=request.grounding_rules,
            )
            
            for chunk in runner.run_stream(request.snapshot, config):
                yield f"data: {json.dumps(chunk.model_dump())}\n\n"
                await asyncio.sleep(0)
                
            yield f"data: {json.dumps({'status': 'done'})}\n\n"
            
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    # ═══════════════════════════════════════════════════════════════════════
    # HOLOMAP ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.post("/holomap/validate")
    async def holomap_validate(request: HolomapValidateRequest):
        """Validate a holomap."""
        result = validate_holomap(request.data)
        return {
            "valid": result.valid,
            "errors": result.errors,
            "warnings": result.warnings,
            "stats": result.stats,
        }
    
    @app.post("/holomap/diff")
    async def holomap_diff(request: HolomapDiffRequest):
        """Diff two snapshots."""
        result = diff_snapshots(request.old, request.new)
        return result.model_dump()
    
    # ═══════════════════════════════════════════════════════════════════════
    # SESSION ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.post("/session/start")
    async def session_start(request: SessionStartRequest):
        """Start a new session."""
        state = get_state()
        session_id = str(uuid.uuid4())
        
        output_dir = Path.home() / ".aria" / "sessions"
        recorder = SessionRecorder(
            name=request.name,
            output_dir=output_dir,
            brain=request.brain,
        )
        recorder.__enter__()
        
        state.active_sessions[session_id] = recorder
        
        return {
            "session_id": session_id,
            "name": request.name,
            "brain": request.brain,
        }
    
    @app.post("/session/{session_id}/event")
    async def session_event(session_id: str, request: SessionEventRequest):
        """Record a session event."""
        state = get_state()
        if session_id not in state.active_sessions:
            raise HTTPException(404, "Session not found")
            
        recorder = state.active_sessions[session_id]
        from aria.core.response import ExplainerResponse
        response = ExplainerResponse(
            summary=request.response.get("summary", ""),
            confidence=request.response.get("confidence", 0.0),
            details=request.response.get("details", []),
        )
        
        recorder.record(request.snapshot, response)
        
        return {"status": "ok", "event_count": recorder.event_count}
    
    @app.post("/session/{session_id}/end")
    async def session_end(session_id: str):
        """End a session."""
        state = get_state()
        if session_id not in state.active_sessions:
            raise HTTPException(404, "Session not found")
            
        recorder = state.active_sessions[session_id]
        recorder.__exit__(None, None, None)
        del state.active_sessions[session_id]
        
        return {"status": "ok", "session_id": session_id}
    
    @app.get("/sessions")
    async def list_sessions(limit: int = Query(50, ge=1, le=100)):
        """List sessions from chronicle."""
        state = get_state()
        sessions = state.chronicle.list_sessions(limit=limit)
        return {"sessions": [s.model_dump() for s in sessions]}
    
    # ═══════════════════════════════════════════════════════════════════════
    # CHRONICLE ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.get("/chronicle/stats")
    async def chronicle_stats():
        """Get chronicle statistics."""
        state = get_state()
        stats = state.chronicle.get_stats()
        return stats.model_dump()
    
    @app.get("/chronicle/events")
    async def chronicle_events(
        session_id: str | None = None,
        event_type: str | None = None,
        brain: str | None = None,
        min_confidence: float | None = None,
        limit: int = Query(100, ge=1, le=1000),
    ):
        """Query chronicle events."""
        state = get_state()
        query = ChronicleQuery(
            session_id=session_id,
            event_type=event_type,
            brain=brain,
            min_confidence=min_confidence,
            limit=limit,
        )
        events = state.chronicle.get_events(query)
        return {"events": [e.model_dump() for e in events]}
    
    @app.get("/chronicle/brain/{brain}/performance")
    async def brain_performance(brain: str):
        """Get brain performance metrics."""
        state = get_state()
        return state.chronicle.get_brain_performance(brain)
    
    # ═══════════════════════════════════════════════════════════════════════
    # WEBSOCKET ENDPOINTS
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket endpoint for real-time cognitive streaming."""
        state = get_state()
        await websocket.accept()
        state.websocket_connections.append(websocket)
        
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                action = message.get("action")
                
                if action == "explain":
                    snapshot = WorldSnapshot.model_validate(message.get("snapshot", {}))
                    brain = message.get("brain")
                    
                    engine = state.get_engine(brain)
                    
                    if hasattr(engine, "predict") and hasattr(engine.predict, "predict_stream"):
                        for response in engine.predict.predict_stream({"snapshot": snapshot.model_dump()}):
                            await websocket.send_json({
                                "type": "chunk",
                                "status": response.status,
                                "content": response.result.get("prediction", "") if response.result else "",
                                "confidence": response.result.get("confidence", 0) if response.result else 0,
                            })
                    else:
                        response = engine.explain(snapshot)
                        await websocket.send_json({
                            "type": "result",
                            "summary": response.summary,
                            "confidence": response.confidence,
                        })
                        
                    await websocket.send_json({"type": "done"})
                    
                elif action == "predict":
                    snapshot = WorldSnapshot.model_validate(message.get("snapshot", {}))
                    prediction_type = message.get("prediction_type", "action")
                    
                    runner = state.get_flow_runner()
                    config = FlowConfig(
                        prediction_type=PredictionType(prediction_type),
                        streaming=True,
                    )
                    
                    for chunk in runner.run_stream(snapshot, config):
                        await websocket.send_json({
                            "type": "chunk",
                            **chunk.model_dump(),
                        })
                        
                    await websocket.send_json({"type": "done"})
                    
                elif action == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": time.time()})
                    
        except WebSocketDisconnect:
            state.websocket_connections.remove(websocket)
        except Exception as e:
            await websocket.send_json({"type": "error", "message": str(e)})
            if websocket in state.websocket_connections:
                state.websocket_connections.remove(websocket)
    
    # ═══════════════════════════════════════════════════════════════════════
    # SIMULATOR MODE
    # ═══════════════════════════════════════════════════════════════════════
    
    @app.post("/simulator/enable")
    async def simulator_enable():
        """Enable simulator mode."""
        state = get_state()
        state.use_simulator = True
        state.simulator = AriaSimulator()
        return {"status": "ok", "mode": "simulator"}
    
    @app.post("/simulator/disable")
    async def simulator_disable():
        """Disable simulator mode."""
        state = get_state()
        state.use_simulator = False
        return {"status": "ok", "mode": "cognitive"}
    
    @app.post("/simulator/configure")
    async def simulator_configure(config: dict[str, Any]):
        """Configure the simulator."""
        state = get_state()
        if not state.simulator:
            state.simulator = AriaSimulator()
        state.simulator.configure(**config)
        return {"status": "ok", "config": config}
    
    return app


# ═══════════════════════════════════════════════════════════════════════════════
# CLI RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the ARIA server."""
    if not HAS_FASTAPI:
        raise ImportError("FastAPI not installed. Run: pip install fastapi uvicorn")
        
    import uvicorn
    app = create_app()
    uvicorn.run(app, host=host, port=port)


# Create default app instance
app = create_app() if HAS_FASTAPI else None
