"""
ARIA - Adaptive Runtime Intelligence Architecture

The cognitive layer for self-narrating systems.
"""

__version__ = "0.1.0"
__author__ = "Lenix Project"

from aria.core.engine import CognitiveEngine, AsyncCognitiveEngine
from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot
from aria.core.response import ExplainerResponse
from aria.core.session import SessionRecorder, CognitiveSession

__all__ = [
    "CognitiveEngine",
    "AsyncCognitiveEngine",
    "WorldSnapshot",
    "NodeSnapshot",
    "FlowSnapshot",
    "ExplainerResponse",
    "SessionRecorder",
    "CognitiveSession",
]
