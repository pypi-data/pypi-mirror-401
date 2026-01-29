"""
ARIA Live Connection - Core Module
===================================
A live connection system using folder-based message passing,
controlled by local LLM via aria-cli.

Architecture:
- Each node has an inbox/ and outbox/ folder
- Messages are JSON files written to folders
- Watchers monitor for new messages
- LLM processes messages and generates responses
"""

import os
import sys
import json
import time
import uuid
import hashlib
import threading
import queue
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ARIA base directory
ARIA_HOME = Path.home() / ".aria"
CONNECTION_HOME = ARIA_HOME / "connection"
NODES_DIR = CONNECTION_HOME / "nodes"
SHARED_DIR = CONNECTION_HOME / "shared"
CACHE_DIR = CONNECTION_HOME / "cache"


class MessageType(Enum):
    """Message types for the live connection protocol."""
    TEXT = "text"
    COMMAND = "command"
    FILE = "file"
    HEARTBEAT = "heartbeat"
    HANDSHAKE = "handshake"
    ACK = "ack"
    BROADCAST = "broadcast"
    LLM_REQUEST = "llm_request"
    LLM_RESPONSE = "llm_response"
    SYNC = "sync"


class ConnectionState(Enum):
    """Connection states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    LISTENING = "listening"
    ERROR = "error"


@dataclass
class Message:
    """Message structure for folder-based communication."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: str = "text"
    sender: str = ""
    receiver: str = "*"  # * = broadcast
    payload: Any = None
    timestamp: float = field(default_factory=time.time)
    ttl: int = 300  # Time to live in seconds
    priority: int = 5  # 1-10, higher = more important
    requires_ack: bool = False
    chain_id: Optional[str] = None  # For chained messages
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(**data)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        return cls.from_dict(json.loads(json_str))
    
    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl


@dataclass
class Node:
    """Represents a node in the live connection network."""
    id: str
    name: str = ""
    inbox: Path = None
    outbox: Path = None
    state: str = "idle"
    last_seen: float = 0
    capabilities: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if self.inbox is None:
            self.inbox = NODES_DIR / self.id / "inbox"
        if self.outbox is None:
            self.outbox = NODES_DIR / self.id / "outbox"


class LiveConnection:
    """
    Live folder-based connection system.
    
    Architecture:
    - Each node has an inbox/ and outbox/ folder
    - Messages are JSON files written to folders
    - Watchers monitor for new messages
    - LLM processes messages and generates responses
    """
    
    def __init__(self, node_id: Optional[str] = None, name: str = ""):
        self.node_id = node_id or self._generate_node_id()
        self.name = name or f"node_{self.node_id[:4]}"
        self.state = ConnectionState.DISCONNECTED
        
        # Paths
        self.node_dir = NODES_DIR / self.node_id
        self.inbox = self.node_dir / "inbox"
        self.outbox = self.node_dir / "outbox"
        self.pending = self.node_dir / "pending"
        self.processed = self.node_dir / "processed"
        self.peers = self.node_dir / "peers"
        
        # Runtime
        self.message_queue: queue.Queue = queue.Queue()
        self.handlers: Dict[str, Callable] = {}
        self.peers_list: Dict[str, Node] = {}
        self.running = False
        self.watcher_thread: Optional[threading.Thread] = None
        
        # LLM integration
        self.llm_enabled = False
        self.llm_callback: Optional[Callable] = None
        
        # Initialize directories
        self._init_directories()
        self._register_node()
    
    def _generate_node_id(self) -> str:
        """Generate unique node ID based on machine + random."""
        machine_id = hashlib.md5(str(uuid.getnode()).encode()).hexdigest()[:4]
        random_part = str(uuid.uuid4())[:4]
        return f"{machine_id}{random_part}"
    
    def _init_directories(self):
        """Create all necessary directories."""
        for dir_path in [self.inbox, self.outbox, self.pending, 
                         self.processed, self.peers, SHARED_DIR, CACHE_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _register_node(self):
        """Register this node in the network."""
        node_info = {
            "id": self.node_id,
            "name": self.name,
            "inbox": str(self.inbox),
            "outbox": str(self.outbox),
            "state": "active",
            "last_seen": time.time(),
            "capabilities": ["text", "command", "llm", "file", "sync"],
            "created": datetime.now().isoformat()
        }
        
        # Write node registration
        node_file = CONNECTION_HOME / "registry" / f"{self.node_id}.json"
        node_file.parent.mkdir(parents=True, exist_ok=True)
        node_file.write_text(json.dumps(node_info, indent=2))
        
        # Also in local node state
        state_file = self.node_dir / "state.json"
        state_file.write_text(json.dumps(node_info, indent=2))
    
    def discover_peers(self) -> List[Node]:
        """Discover other nodes in the network."""
        registry_dir = CONNECTION_HOME / "registry"
        peers = []
        
        if registry_dir.exists():
            for node_file in registry_dir.glob("*.json"):
                if node_file.stem != self.node_id:
                    try:
                        data = json.loads(node_file.read_text())
                        node = Node(
                            id=data["id"],
                            name=data.get("name", ""),
                            inbox=Path(data["inbox"]),
                            outbox=Path(data["outbox"]),
                            state=data.get("state", "unknown"),
                            last_seen=data.get("last_seen", 0),
                            capabilities=data.get("capabilities", [])
                        )
                        peers.append(node)
                        self.peers_list[node.id] = node
                    except Exception:
                        pass
        
        return peers
    
    def send(self, message: Message, target_node: Optional[str] = None) -> bool:
        """Send a message to target node or broadcast."""
        message.sender = self.node_id
        
        if target_node and target_node != "*":
            # Direct message to specific node
            message.receiver = target_node
            target_inbox = NODES_DIR / target_node / "inbox"
            if target_inbox.exists():
                msg_file = target_inbox / f"{message.id}.json"
                msg_file.write_text(message.to_json())
                return True
            return False
        else:
            # Broadcast to all peers
            message.receiver = "*"
            self.discover_peers()
            for peer_id, peer in self.peers_list.items():
                if peer.inbox.exists():
                    msg_file = peer.inbox / f"{message.id}.json"
                    msg_file.write_text(message.to_json())
            return True
    
    def send_text(self, text: str, target: Optional[str] = None) -> bool:
        """Convenience method to send a text message."""
        msg = Message(
            type=MessageType.TEXT.value,
            payload={"text": text}
        )
        return self.send(msg, target)
    
    def send_command(self, command: str, args: Dict = None, target: Optional[str] = None) -> bool:
        """Send a command to be executed by target node."""
        msg = Message(
            type=MessageType.COMMAND.value,
            payload={"command": command, "args": args or {}},
            requires_ack=True
        )
        return self.send(msg, target)
    
    def send_llm_request(self, prompt: str, target: Optional[str] = None) -> str:
        """Send a request to be processed by target's LLM."""
        msg = Message(
            type=MessageType.LLM_REQUEST.value,
            payload={"prompt": prompt},
            requires_ack=True
        )
        self.send(msg, target)
        return msg.id
    
    def _process_message(self, msg: Message):
        """Process an incoming message."""
        # Move to processed
        msg_file = self.inbox / f"{msg.id}.json"
        if msg_file.exists():
            processed_file = self.processed / f"{msg.id}.json"
            msg_file.rename(processed_file)
        
        # Handle by type
        msg_type = msg.type
        
        if msg_type == MessageType.HEARTBEAT.value:
            self._send_ack(msg)
            
        elif msg_type == MessageType.TEXT.value:
            if "text" in self.handlers:
                self.handlers["text"](msg)
            else:
                print(f"[{msg.sender}]: {msg.payload.get('text', '')}")
        
        elif msg_type == MessageType.COMMAND.value:
            if "command" in self.handlers:
                result = self.handlers["command"](msg)
                if msg.requires_ack:
                    self._send_ack(msg, result)
        
        elif msg_type == MessageType.LLM_REQUEST.value:
            if self.llm_enabled and self.llm_callback:
                prompt = msg.payload.get("prompt", "")
                response = self.llm_callback(prompt)
                self._send_llm_response(msg, response)
            else:
                self._send_llm_response(msg, "LLM not available on this node")
        
        elif msg_type == MessageType.LLM_RESPONSE.value:
            if "llm_response" in self.handlers:
                self.handlers["llm_response"](msg)
            else:
                print(f"[LLM Response]: {msg.payload.get('response', '')}")
        
        elif msg_type in self.handlers:
            self.handlers[msg_type](msg)
    
    def _send_ack(self, original_msg: Message, result: Any = None):
        """Send acknowledgment for a message."""
        ack = Message(
            type=MessageType.ACK.value,
            receiver=original_msg.sender,
            payload={"ack_for": original_msg.id, "result": result}
        )
        self.send(ack, original_msg.sender)
    
    def _send_llm_response(self, original_msg: Message, response: str):
        """Send LLM response back to requester."""
        resp = Message(
            type=MessageType.LLM_RESPONSE.value,
            receiver=original_msg.sender,
            payload={"response": response, "request_id": original_msg.id}
        )
        self.send(resp, original_msg.sender)
    
    def _watcher_loop(self):
        """Watch inbox for new messages."""
        processed_ids = set()
        
        while self.running:
            try:
                for msg_file in self.inbox.glob("*.json"):
                    if msg_file.stem not in processed_ids:
                        try:
                            msg = Message.from_json(msg_file.read_text())
                            if not msg.is_expired():
                                self._process_message(msg)
                            processed_ids.add(msg_file.stem)
                        except Exception as e:
                            print(f"Error processing {msg_file}: {e}")
                
                # Cleanup old processed files
                for proc_file in self.processed.glob("*.json"):
                    if time.time() - proc_file.stat().st_mtime > 3600:
                        proc_file.unlink()
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Watcher error: {e}")
                time.sleep(1)
    
    def start(self):
        """Start the live connection listener."""
        if self.running:
            return
        
        self.running = True
        self.state = ConnectionState.LISTENING
        self._update_state("listening")
        
        self.watcher_thread = threading.Thread(target=self._watcher_loop, daemon=True)
        self.watcher_thread.start()
        
        print(f"[ARIA] Live connection started: {self.node_id}")
        print(f"[ARIA] Inbox: {self.inbox}")
    
    def stop(self):
        """Stop the live connection."""
        self.running = False
        self.state = ConnectionState.DISCONNECTED
        self._update_state("stopped")
        
        if self.watcher_thread:
            self.watcher_thread.join(timeout=2)
        
        print(f"[ARIA] Live connection stopped: {self.node_id}")
    
    def _update_state(self, state: str):
        """Update node state file."""
        state_file = self.node_dir / "state.json"
        if state_file.exists():
            data = json.loads(state_file.read_text())
            data["state"] = state
            data["last_seen"] = time.time()
            state_file.write_text(json.dumps(data, indent=2))
    
    def on(self, event_type: str, handler: Callable):
        """Register a message handler."""
        self.handlers[event_type] = handler
        return self
    
    def enable_llm(self, callback: Callable[[str], str]):
        """Enable LLM processing with given callback."""
        self.llm_enabled = True
        self.llm_callback = callback
        return self
    
    def heartbeat(self):
        """Send heartbeat to all peers."""
        msg = Message(
            type=MessageType.HEARTBEAT.value,
            payload={"timestamp": time.time()}
        )
        self.send(msg)
