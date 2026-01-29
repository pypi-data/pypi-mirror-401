"""
Tests for aria.core.session
"""

import pytest
from pathlib import Path
from aria.core.session import (
    SessionRecorder,
    SessionManager,
    CognitiveEvent,
    CognitiveSession,
    SessionMetadata,
)
from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot
from aria.core.response import ExplainerResponse


class TestSessionRecorder:
    """Tests for SessionRecorder."""
    
    def test_context_manager(self, tmp_path):
        """Test using recorder as context manager."""
        with SessionRecorder("test-session", output_dir=tmp_path) as recorder:
            assert recorder._active is True
            assert recorder.session_id is not None
        
        # After exiting, should be inactive
        assert recorder._active is False
    
    def test_record_event(self, tmp_path):
        """Test recording events to a session."""
        with SessionRecorder("test-session", output_dir=tmp_path) as recorder:
            # Create a snapshot and response to record
            snapshot = WorldSnapshot.from_dict({
                "nodes": [{"id": "n1", "type": "test", "label": "Test Node"}],
                "flows": []
            })
            response = ExplainerResponse(
                summary="Test summary",
                details=["Test details"],
            )
            
            recorder.record(snapshot, response)
            
            assert recorder.event_count == 1
    
    def test_record_custom_event(self, tmp_path):
        """Test recording custom events."""
        with SessionRecorder("test-session", output_dir=tmp_path) as recorder:
            event = CognitiveEvent(type="CustomEvent")
            recorder.record_event(event)
            
            assert recorder.event_count == 1
            assert recorder.session.events[0].type == "CustomEvent"
    
    def test_save_session(self, tmp_path):
        """Test saving session to file."""
        with SessionRecorder("test-session", output_dir=tmp_path) as recorder:
            snapshot = WorldSnapshot.from_dict({
                "nodes": [{"id": "n1", "type": "test", "label": "Test"}],
                "flows": []
            })
            response = ExplainerResponse(summary="Test", details=["Details"])
            recorder.record(snapshot, response)
        
        # Check file was created (JSONL format)
        files = list(tmp_path.glob("*.jsonl"))
        assert len(files) == 1
    
    def test_classmethod_start(self, tmp_path):
        """Test starting a session via classmethod."""
        recorder = SessionRecorder.start("test-session", output_dir=tmp_path)
        
        assert recorder._active is True
        assert SessionRecorder.get_current() is recorder
        
        # Stop the current session
        session = SessionRecorder.stop_current()
        
        assert session is not None
        assert SessionRecorder.get_current() is None


class TestCognitiveSession:
    """Tests for CognitiveSession."""
    
    def test_session_properties(self):
        """Test session properties."""
        session = CognitiveSession(
            metadata=SessionMetadata(name="test")
        )
        
        assert session.name == "test"
        assert session.event_count == 0
        assert session.id is not None
    
    def test_session_duration(self):
        """Test duration calculation."""
        session = CognitiveSession(
            metadata=SessionMetadata(name="test")
        )
        
        # No events = 0s duration
        assert session.duration == "0s"


class TestSessionManager:
    """Tests for SessionManager."""
    
    def test_list_sessions(self, tmp_path):
        """Test listing sessions."""
        # Create a session
        with SessionRecorder("test-session", output_dir=tmp_path) as recorder:
            pass
        
        manager = SessionManager(session_dir=tmp_path)
        sessions = manager.list_sessions()
        
        assert len(sessions) >= 1
