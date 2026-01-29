"""
ARIA Holomap - Validator

Validate holomap data structures.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class HolomapValidationError:
    """A validation error in holomap data."""
    path: str
    message: str
    severity: str = "error"


@dataclass
class HolomapValidationResult:
    """Result from validating holomap data."""
    source: str
    valid: bool
    errors: list[HolomapValidationError]
    warnings: list[HolomapValidationError]
    stats: dict[str, Any]


def validate_holomap(data: dict[str, Any] | str | Path, source: str = "unknown") -> HolomapValidationResult:
    """
    Validate holomap data structure.
    
    Args:
        data: Either a dict of holomap data or a path to a JSON file
        source: Identifier for error messages
        
    Returns:
        HolomapValidationResult with errors and warnings
    """
    # Handle file path input
    if isinstance(data, (str, Path)):
        path = Path(data)
        source = str(path)
        try:
            with open(path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return HolomapValidationResult(
                source=source,
                valid=False,
                errors=[HolomapValidationError("", f"Invalid JSON: {e}")],
                warnings=[],
                stats={},
            )
        except Exception as e:
            return HolomapValidationResult(
                source=source,
                valid=False,
                errors=[HolomapValidationError("", f"Cannot read file: {e}")],
                warnings=[],
                stats={},
            )
    
    errors: list[HolomapValidationError] = []
    warnings: list[HolomapValidationError] = []
    stats = {
        "nodes": 0,
        "flows": 0,
        "metrics": 0,
        "has_positions": False,
        "has_metadata": False,
    }
    
    # Check for nodes
    nodes = data.get("nodes", [])
    if not isinstance(nodes, list):
        errors.append(HolomapValidationError("nodes", "nodes must be an array"))
    else:
        stats["nodes"] = len(nodes)
        
        node_ids = set()
        for i, node in enumerate(nodes):
            prefix = f"nodes[{i}]"
            
            if not isinstance(node, dict):
                errors.append(HolomapValidationError(prefix, "node must be an object"))
                continue
            
            # Required fields
            if "id" not in node:
                errors.append(HolomapValidationError(f"{prefix}.id", "node ID is required"))
            else:
                node_id = node["id"]
                if node_id in node_ids:
                    errors.append(HolomapValidationError(f"{prefix}.id", f"duplicate node ID: {node_id}"))
                node_ids.add(node_id)
            
            if "type" not in node:
                warnings.append(HolomapValidationError(
                    f"{prefix}.type",
                    "node type not specified",
                    severity="warning",
                ))
            
            # Check for position data
            if "position" in node or ("x" in node and "y" in node):
                stats["has_positions"] = True
            
            # Check for metadata
            if "metadata" in node:
                stats["has_metadata"] = True
    
    # Check for flows
    flows = data.get("flows", [])
    if not isinstance(flows, list):
        errors.append(HolomapValidationError("flows", "flows must be an array"))
    else:
        stats["flows"] = len(flows)
        
        for i, flow in enumerate(flows):
            prefix = f"flows[{i}]"
            
            if not isinstance(flow, dict):
                errors.append(HolomapValidationError(prefix, "flow must be an object"))
                continue
            
            # Check source and target
            source_id = flow.get("source") or flow.get("from")
            target_id = flow.get("target") or flow.get("to")
            
            if not source_id:
                errors.append(HolomapValidationError(f"{prefix}.source", "flow source is required"))
            elif source_id not in node_ids:
                errors.append(HolomapValidationError(
                    f"{prefix}.source",
                    f"flow references unknown node: {source_id}",
                ))
            
            if not target_id:
                errors.append(HolomapValidationError(f"{prefix}.target", "flow target is required"))
            elif target_id not in node_ids:
                errors.append(HolomapValidationError(
                    f"{prefix}.target",
                    f"flow references unknown node: {target_id}",
                ))
    
    # Check for metrics
    metrics = data.get("metrics", {})
    if isinstance(metrics, dict):
        stats["metrics"] = len(metrics)
    
    return HolomapValidationResult(
        source=source,
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        stats=stats,
    )


def validate_holomap_file(path: Path) -> HolomapValidationResult:
    """Validate a holomap JSON file."""
    try:
        with open(path) as f:
            data = json.load(f)
        return validate_holomap(data, source=str(path))
    except json.JSONDecodeError as e:
        return HolomapValidationResult(
            source=str(path),
            valid=False,
            errors=[HolomapValidationError("file", f"Invalid JSON: {e}")],
            warnings=[],
            stats={},
        )
    except Exception as e:
        return HolomapValidationResult(
            source=str(path),
            valid=False,
            errors=[HolomapValidationError("file", f"Failed to read: {e}")],
            warnings=[],
            stats={},
        )
