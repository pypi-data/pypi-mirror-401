"""
ARIA Example - Basic Explanation

Demonstrates how to use ARIA to explain a holomap snapshot.
"""

from aria import CognitiveEngine, WorldSnapshot

# Create a simple snapshot
snapshot = WorldSnapshot.from_json({
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
})

# Create engine (uses mock mode if no brain installed)
engine = CognitiveEngine(brain="mock")

# Get explanation
response = engine.explain(snapshot)

print("Summary:", response.summary)
print("Details:", response.details)
print("Confidence:", response.confidence)
