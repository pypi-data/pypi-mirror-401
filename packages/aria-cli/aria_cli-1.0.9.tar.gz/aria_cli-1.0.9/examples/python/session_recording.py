"""
ARIA Example - Session Recording

Demonstrates how to record cognitive sessions for lineage tracking.
"""

import asyncio
from aria import CognitiveEngine, WorldSnapshot, SessionRecorder

async def main():
    # Create session recorder
    recorder = SessionRecorder(output_dir="./sessions")
    
    # Start session
    recorder.start()
    
    # Create engine
    engine = CognitiveEngine(brain="mock")
    
    # Create snapshots and record explanations
    for i in range(3):
        snapshot = WorldSnapshot.from_json({
            "nodes": [
                {"id": f"node-{i}", "type": "test", "label": f"Test Node {i}"},
            ],
            "flows": [],
            "metrics": {"iteration": {"value": i}},
        })
        
        # Get explanation
        response = engine.explain(snapshot)
        
        # Record to session
        recorder.add_event("explain", {
            "snapshot_id": f"snapshot-{i}",
            "summary": response.summary,
            "confidence": response.confidence,
        })
        
        print(f"Iteration {i}: {response.summary[:50]}...")
    
    # Save session
    session = recorder.stop()
    print(f"\nSession saved: {session.session_id}")
    print(f"Events recorded: {len(session.events)}")

if __name__ == "__main__":
    asyncio.run(main())
