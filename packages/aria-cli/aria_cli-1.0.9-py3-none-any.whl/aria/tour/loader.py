"""
ARIA Tour - Tour Loader

Load and parse tour definition files.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TourStep:
    """A single step in a tour."""
    id: str
    title: str
    description: str
    focus_nodes: list[str] = field(default_factory=list)
    auto_advance: bool = False
    delay_ms: int = 0
    trigger_explainer: bool = False
    explainer_style: str = "narrative"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Tour:
    """A complete tour definition."""
    id: str
    name: str
    description: str
    steps: list[TourStep]
    version: str = "1.0"
    author: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


def load_tour(path: Path) -> Tour:
    """Load a tour from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    
    steps = []
    for step_data in data.get("steps", []):
        steps.append(TourStep(
            id=step_data.get("id", ""),
            title=step_data.get("title", ""),
            description=step_data.get("description", ""),
            focus_nodes=step_data.get("focus_nodes", []),
            auto_advance=step_data.get("auto_advance", False),
            delay_ms=step_data.get("delay_ms", 0),
            trigger_explainer=step_data.get("trigger_explainer", False),
            explainer_style=step_data.get("explainer_style", "narrative"),
            metadata=step_data.get("metadata", {}),
        ))
    
    return Tour(
        id=data.get("id", path.stem),
        name=data.get("name", path.stem),
        description=data.get("description", ""),
        steps=steps,
        version=data.get("version", "1.0"),
        author=data.get("author", ""),
        metadata=data.get("metadata", {}),
    )


def list_tours(tour_dir: Path | str) -> list[Tour]:
    """List all tours in a directory."""
    tours = []
    tour_dir = Path(tour_dir)
    
    if not tour_dir.exists():
        return tours
    
    for path in tour_dir.glob("*.json"):
        try:
            tours.append(load_tour(path))
        except Exception:
            continue
    
    return tours


def find_tour(name: str, tour_dirs: list[Path]) -> Tour | None:
    """Find a tour by name in multiple directories."""
    for dir_path in tour_dirs:
        # Try exact match first
        path = dir_path / f"{name}.json"
        if path.exists():
            return load_tour(path)
        
        # Try partial match
        for tour_path in dir_path.glob("*.json"):
            if name.lower() in tour_path.stem.lower():
                return load_tour(tour_path)
    
    return None
