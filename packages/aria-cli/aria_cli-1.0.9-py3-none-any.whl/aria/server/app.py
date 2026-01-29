"""
ARIA Server - FastAPI Application

REST API and WebSocket server for cognitive runtime.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from pydantic import BaseModel

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from fastapi.responses import StreamingResponse
    import uvicorn
except ImportError:
    FastAPI = None
    uvicorn = None


# API Models
class ExplainRequest(BaseModel):
    """Request body for explain endpoint."""
    snapshot: dict[str, Any]
    focus: str | None = None
    style: str = "narrative"


class ExplainResponse(BaseModel):
    """Response from explain endpoint."""
    summary: str
    details: str
    focus_nodes: list[str]
    confidence: float
    is_degraded: bool


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    brain: str
    version: str


class SessionInfo(BaseModel):
    """Session information."""
    session_id: str
    started_at: str
    events: int


def create_app(brain: str = "tinyllama") -> "FastAPI":
    """Create the FastAPI application."""
    if FastAPI is None:
        raise RuntimeError(
            "FastAPI is required for the server. "
            "Install it with: pip install aria-cli[server]"
        )
    
    from aria.core.engine import AsyncCognitiveEngine, EngineConfig
    from aria.core.snapshot import WorldSnapshot
    from aria.core.session import SessionManager
    
    # Engine instance (lazily loaded)
    engine: AsyncCognitiveEngine | None = None
    sessions = SessionManager()
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan manager."""
        nonlocal engine
        config = EngineConfig(brain=brain)
        engine = AsyncCognitiveEngine(config)
        yield
        if engine:
            engine.close()
    
    app = FastAPI(
        title="ARIA Cognitive Runtime API",
        description="REST API for cognitive explanations of holomap systems",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Health check endpoint."""
        return HealthResponse(
            status="healthy",
            brain=brain,
            version="1.0.0",
        )
    
    @app.post("/explain", response_model=ExplainResponse)
    async def explain(request: ExplainRequest):
        """Generate cognitive explanation for a snapshot."""
        if engine is None:
            raise HTTPException(503, "Engine not ready")
        
        try:
            snapshot = WorldSnapshot.from_json(request.snapshot)
            if request.focus:
                snapshot = snapshot.with_focus(request.focus.split(","))
            
            response = await engine.explain_async(snapshot, style=request.style)
            
            return ExplainResponse(
                summary=response.summary,
                details=response.details,
                focus_nodes=response.focus_nodes,
                confidence=response.confidence,
                is_degraded=response.is_degraded,
            )
        except Exception as e:
            raise HTTPException(500, str(e))
    
    @app.post("/explain/stream")
    async def explain_stream(request: ExplainRequest):
        """Stream cognitive explanation tokens."""
        if engine is None:
            raise HTTPException(503, "Engine not ready")
        
        async def generate():
            try:
                snapshot = WorldSnapshot.from_json(request.snapshot)
                async for token in engine.stream_explanation(snapshot, style=request.style):
                    yield f"data: {token}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: [ERROR] {e}\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket for real-time explanations."""
        await websocket.accept()
        
        try:
            while True:
                data = await websocket.receive_json()
                
                if data.get("type") == "explain":
                    snapshot = WorldSnapshot.from_json(data.get("snapshot", {}))
                    response = await engine.explain_async(snapshot)
                    await websocket.send_json({
                        "type": "explanation",
                        "summary": response.summary,
                        "details": response.details,
                        "focus_nodes": response.focus_nodes,
                    })
                
                elif data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                
        except WebSocketDisconnect:
            pass
    
    @app.get("/sessions")
    async def list_sessions():
        """List all sessions."""
        return [
            SessionInfo(
                session_id=s.session_id,
                started_at=s.started_at.isoformat(),
                events=len(s.events),
            )
            for s in sessions.list_sessions()
        ]
    
    return app


def run_server(
    brain: str = "tinyllama",
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    """Run the ARIA server."""
    if uvicorn is None:
        raise RuntimeError(
            "uvicorn is required for the server. "
            "Install it with: pip install aria-cli[server]"
        )
    
    app = create_app(brain)
    uvicorn.run(app, host=host, port=port)
