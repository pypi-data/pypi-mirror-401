"""
Tests for aria.holomap
"""

import pytest
from aria.holomap import validate_holomap, calculate_stats, diff_snapshots
from aria.core.snapshot import WorldSnapshot, NodeSnapshot, FlowSnapshot


class TestHolomapValidator:
    """Tests for holomap validation."""
    
    def test_valid_holomap(self, sample_snapshot_data):
        """Test validating a valid holomap."""
        result = validate_holomap(sample_snapshot_data)
        
        assert result.valid is True
        assert result.stats["nodes"] == 3
        assert result.stats["flows"] == 2
    
    def test_missing_node_id(self):
        """Test validation catches missing node ID."""
        data = {
            "nodes": [{"type": "test"}],
            "flows": [],
        }
        
        result = validate_holomap(data)
        
        assert result.valid is False
        assert any("ID" in e.message for e in result.errors)
    
    def test_invalid_flow_reference(self, sample_snapshot_data):
        """Test validation catches invalid flow references."""
        data = sample_snapshot_data.copy()
        data["flows"] = [{"source": "nonexistent", "target": "core"}]
        
        result = validate_holomap(data)
        
        assert result.valid is False


class TestHolomapStats:
    """Tests for holomap statistics."""
    
    def test_calculate_stats(self):
        """Test calculating statistics."""
        snapshot = WorldSnapshot(
            nodes=[
                NodeSnapshot(id="core", type="processor", label="Core"),
                NodeSnapshot(id="input", type="io", label="Input"),
                NodeSnapshot(id="output", type="io", label="Output"),
            ],
            flows=[
                FlowSnapshot(id="f1", source_id="input", target_id="core"),
                FlowSnapshot(id="f2", source_id="core", target_id="output"),
            ],
        )
        stats = calculate_stats(snapshot)
        
        assert stats.nodes.total == 3
        assert stats.flows.total == 2
        assert stats.complexity_score > 0


class TestHolomapDiff:
    """Tests for holomap diff."""
    
    def test_no_changes(self):
        """Test diff with no changes."""
        snapshot = WorldSnapshot(
            nodes=[NodeSnapshot(id="core", type="processor", label="Core")],
            flows=[],
        )
        diff = diff_snapshots(snapshot, snapshot)
        
        assert diff.is_empty is True
    
    def test_added_node(self):
        """Test diff with added node."""
        old = WorldSnapshot(
            nodes=[NodeSnapshot(id="core", type="processor", label="Core")],
            flows=[],
        )
        
        new = WorldSnapshot(
            nodes=[
                NodeSnapshot(id="core", type="processor", label="Core"),
                NodeSnapshot(id="new", type="test", label="New Node"),
            ],
            flows=[],
        )
        
        diff = diff_snapshots(old, new)
        
        assert len(diff.nodes_added) == 1
        assert diff.nodes_added[0].node_id == "new"
