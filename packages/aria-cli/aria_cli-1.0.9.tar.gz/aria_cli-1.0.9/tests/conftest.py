"""
ARIA Test Suite
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_snapshot_data():
    """Sample snapshot data for testing."""
    return {
        "nodes": [
            {"id": "core", "type": "processor", "label": "Main Core"},
            {"id": "input", "type": "io", "label": "Input"},
            {"id": "output", "type": "io", "label": "Output"},
        ],
        "flows": [
            {"source": "input", "target": "core"},
            {"source": "core", "target": "output"},
        ],
        "metrics": {
            "throughput": {"value": 100, "unit": "ops/sec"},
        },
    }


@pytest.fixture
def sample_tour_data():
    """Sample tour data for testing."""
    return {
        "id": "test-tour",
        "name": "Test Tour",
        "description": "A test tour",
        "steps": [
            {
                "id": "step1",
                "title": "Step 1",
                "description": "First step",
            },
            {
                "id": "step2",
                "title": "Step 2",
                "description": "Second step",
                "trigger_explainer": True,
            },
        ],
    }
