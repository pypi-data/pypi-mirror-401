"""
ARIA Example - Running Tours

Demonstrates how to run guided tours with explanations.
"""

import asyncio
from pathlib import Path
from aria.tour import load_tour, TourRunner
from aria.core.engine import AsyncCognitiveEngine, EngineConfig
from aria.core.snapshot import WorldSnapshot

async def main():
    # Load a tour
    tour_path = Path(__file__).parent.parent / "tours" / "tinyllama-demo.json"
    tour = load_tour(tour_path)
    
    print(f"Tour: {tour.name}")
    print(f"Steps: {len(tour.steps)}")
    print()
    
    # Create engine (mock mode for demo)
    config = EngineConfig(brain="mock")
    engine = AsyncCognitiveEngine(config)
    
    # Load snapshot
    snapshot_path = Path(__file__).parent.parent / "holomaps" / "demo-system.json"
    snapshot = WorldSnapshot.from_file(snapshot_path)
    
    # Create runner
    def on_step(result):
        status = "✓" if result.success else "✗"
        print(f"{status} {result.step.title}")
        if result.explanation:
            print(f"  → {result.explanation[:60]}...")
    
    runner = TourRunner(engine=engine, on_step=on_step)
    
    # Run tour
    print("Starting tour...")
    print("-" * 40)
    results = await runner.run(tour, snapshot)
    print("-" * 40)
    print(f"Completed: {sum(1 for r in results if r.success)}/{len(results)} steps")

if __name__ == "__main__":
    asyncio.run(main())
