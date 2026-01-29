"""
ARIA Connection Module
======================
Folder-based live connection system for real-time messaging
between nodes, controlled by local LLM.
"""

from .live import LiveConnection, Message, MessageType, ConnectionState, Node
from .commands import connection

__all__ = [
    "LiveConnection",
    "Message", 
    "MessageType",
    "ConnectionState",
    "Node",
    "connection",
]
