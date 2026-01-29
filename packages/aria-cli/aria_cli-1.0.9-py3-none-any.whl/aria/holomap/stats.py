"""
ARIA Holomap - Stats

Calculate statistics from holomap data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aria.core.snapshot import WorldSnapshot


@dataclass
class NodeStats:
    """Statistics about nodes."""
    total: int
    by_type: dict[str, int]
    with_metadata: int
    isolated: int  # Nodes with no connections


@dataclass
class FlowStats:
    """Statistics about flows."""
    total: int
    by_type: dict[str, int]
    avg_per_node: float


@dataclass
class MetricStats:
    """Statistics about metrics."""
    total: int
    avg_value: float
    min_value: float
    max_value: float


@dataclass
class HolomapStats:
    """Complete statistics for a holomap."""
    source: str
    nodes: NodeStats
    flows: FlowStats
    metrics: MetricStats
    complexity_score: float


def calculate_stats(snapshot: WorldSnapshot, source: str = "snapshot") -> HolomapStats:
    """Calculate statistics for a holomap snapshot."""
    
    # Node stats
    node_count = len(snapshot.nodes)
    nodes_by_type: dict[str, int] = {}
    nodes_with_metadata = 0
    
    for node in snapshot.nodes:
        node_type = node.type or "unknown"
        nodes_by_type[node_type] = nodes_by_type.get(node_type, 0) + 1
        if node.metadata:
            nodes_with_metadata += 1
    
    # Find isolated nodes (no flows connected)
    connected_nodes = set()
    for flow in snapshot.flows:
        connected_nodes.add(flow.source_id)
        connected_nodes.add(flow.target_id)
    
    isolated_nodes = node_count - len(connected_nodes)
    
    node_stats = NodeStats(
        total=node_count,
        by_type=nodes_by_type,
        with_metadata=nodes_with_metadata,
        isolated=isolated_nodes,
    )
    
    # Flow stats
    flow_count = len(snapshot.flows)
    flows_by_type: dict[str, int] = {}
    
    for flow in snapshot.flows:
        flow_type = flow.status or "default"
        flows_by_type[flow_type] = flows_by_type.get(flow_type, 0) + 1
    
    avg_flows_per_node = flow_count / node_count if node_count > 0 else 0
    
    flow_stats = FlowStats(
        total=flow_count,
        by_type=flows_by_type,
        avg_per_node=avg_flows_per_node,
    )
    
    # Metric stats - collect from nodes
    metric_values = []
    for node in snapshot.nodes:
        for metric in node.metrics:
            if isinstance(metric.value, (int, float)):
                metric_values.append(metric.value)
    
    total_metrics = sum(len(n.metrics) for n in snapshot.nodes)
    
    if metric_values:
        metric_stats = MetricStats(
            total=total_metrics,
            avg_value=sum(metric_values) / len(metric_values),
            min_value=min(metric_values),
            max_value=max(metric_values),
        )
    else:
        metric_stats = MetricStats(
            total=total_metrics,
            avg_value=0,
            min_value=0,
            max_value=0,
        )
    
    # Calculate complexity score
    # Based on: node count, flow density, type diversity
    type_diversity = len(nodes_by_type) / max(node_count, 1)
    flow_density = avg_flows_per_node / 2  # Normalize
    
    complexity_score = min(100, (
        (node_count * 0.5) +
        (flow_count * 0.3) +
        (type_diversity * 20) +
        (flow_density * 10)
    ))
    
    return HolomapStats(
        source=source,
        nodes=node_stats,
        flows=flow_stats,
        metrics=metric_stats,
        complexity_score=complexity_score,
    )


def compare_stats(old: HolomapStats, new: HolomapStats) -> dict[str, Any]:
    """Compare two holomap statistics."""
    return {
        "nodes_delta": new.nodes.total - old.nodes.total,
        "flows_delta": new.flows.total - old.flows.total,
        "metrics_delta": new.metrics.total - old.metrics.total,
        "complexity_delta": new.complexity_score - old.complexity_score,
        "new_types": [
            t for t in new.nodes.by_type
            if t not in old.nodes.by_type
        ],
        "removed_types": [
            t for t in old.nodes.by_type
            if t not in new.nodes.by_type
        ],
    }
