"""
ARIA Server Package - Enhanced REST API + WebSocket streaming.
"""

from aria.server.app_v2 import create_app, run_server, app, ServerState, get_state
from aria.server.app_v2 import (
    ExplainRequest,
    ExplainResponse,
    PredictRequest,
    PredictResponse,
    StatusResponse,
    HolomapValidateRequest,
    HolomapDiffRequest,
    SessionStartRequest,
    SessionEventRequest,
)

__all__ = [
    # App factory
    "create_app",
    "run_server",
    "app",
    # State
    "ServerState",
    "get_state",
    # Request/Response models
    "ExplainRequest",
    "ExplainResponse",
    "PredictRequest",
    "PredictResponse",
    "StatusResponse",
    "HolomapValidateRequest",
    "HolomapDiffRequest",
    "SessionStartRequest",
    "SessionEventRequest",
]
