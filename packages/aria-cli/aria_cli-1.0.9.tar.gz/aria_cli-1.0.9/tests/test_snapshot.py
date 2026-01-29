"""
Tests for aria.core.snapshot
"""

import pytest
from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot


class TestWorldSnapshot:
    """Tests for WorldSnapshot."""
    
    def test_from_dict(self, sample_snapshot_data):
        """Test creating snapshot from dict."""
        # Convert to proper format
        nodes = [
            {"id": n["id"], "type": n["type"], "label": n["label"]}
            for n in sample_snapshot_data["nodes"]
        ]
        flows = [
            {
                "id": f"{f['source']}->{f['target']}",
                "source_id": f["source"],
                "target_id": f["target"]
            }
            for f in sample_snapshot_data["flows"]
        ]
        
        snapshot = WorldSnapshot.from_dict({"nodes": nodes, "flows": flows})
        
        assert len(snapshot.nodes) == 3
        assert len(snapshot.flows) == 2
    
    def test_with_focus(self):
        """Test focusing on specific nodes."""
        snapshot = WorldSnapshot(
            nodes=[NodeSnapshot(id="core", type="processor", label="Core")],
            flows=[],
        )
        focused = snapshot.with_focus(["core"])
        
        assert focused.focus_node_ids == ["core"]
    
    def test_node_lookup(self):
        """Test node lookup by ID."""
        snapshot = WorldSnapshot(
            nodes=[
                NodeSnapshot(id="core", type="processor", label="Core"),
                NodeSnapshot(id="input", type="io", label="Input"),
            ],
            flows=[],
        )
        
        assert snapshot.get_node("core") is not None
        assert snapshot.get_node("nonexistent") is None


class TestNodeSnapshot:
    """Tests for NodeSnapshot."""
    
    def test_creation(self):
        """Test creating a node snapshot."""
        node = NodeSnapshot(
            id="test",
            type="processor",
            label="Test Node",
        )
        
        assert node.id == "test"
        assert node.type == "processor"
        assert node.label == "Test Node"
        assert node.metadata == {}


class TestFlowSnapshot:
    """Tests for FlowSnapshot."""
    
    def test_creation(self):
        """Test creating a flow snapshot."""
        flow = FlowSnapshot(
            id="flow1",
            source_id="a",
            target_id="b",
            label="Test Flow",
        )
        
        assert flow.source_id == "a"
        assert flow.target_id == "b"
