"""
ARIA Holomap - Diff

Compare holomap snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aria.core.snapshot import WorldSnapshot


@dataclass
class NodeChange:
    """A change to a node."""
    node_id: str
    change_type: str  # added, removed, modified
    old_value: Any | None = None
    new_value: Any | None = None
    fields: list[str] | None = None


@dataclass
class FlowChange:
    """A change to a flow."""
    flow_id: str
    change_type: str  # added, removed, modified
    source: str | None = None
    target: str | None = None


@dataclass
class MetricChange:
    """A change to a metric."""
    metric_id: str
    change_type: str  # added, removed, modified
    old_value: float | None = None
    new_value: float | None = None
    delta: float = 0


@dataclass
class HolomapDiff:
    """Difference between two holomap snapshots."""
    nodes_added: list[NodeChange]
    nodes_removed: list[NodeChange]
    nodes_modified: list[NodeChange]
    flows_added: list[FlowChange]
    flows_removed: list[FlowChange]
    flows_modified: list[FlowChange]
    metrics_changed: list[MetricChange]
    
    @property
    def is_empty(self) -> bool:
        """Check if there are no changes."""
        return (
            not self.nodes_added
            and not self.nodes_removed
            and not self.nodes_modified
            and not self.flows_added
            and not self.flows_removed
            and not self.flows_modified
            and not self.metrics_changed
        )
    
    @property
    def summary(self) -> str:
        """Get a summary of changes."""
        parts = []
        if self.nodes_added:
            parts.append(f"+{len(self.nodes_added)} nodes")
        if self.nodes_removed:
            parts.append(f"-{len(self.nodes_removed)} nodes")
        if self.nodes_modified:
            parts.append(f"~{len(self.nodes_modified)} nodes")
        if self.flows_added:
            parts.append(f"+{len(self.flows_added)} flows")
        if self.flows_removed:
            parts.append(f"-{len(self.flows_removed)} flows")
        if self.metrics_changed:
            parts.append(f"~{len(self.metrics_changed)} metrics")
        return ", ".join(parts) if parts else "no changes"


def diff_snapshots(
    old: WorldSnapshot,
    new: WorldSnapshot,
) -> HolomapDiff:
    """Compare two holomap snapshots."""
    
    # Build node maps
    old_nodes = {n.id: n for n in old.nodes}
    new_nodes = {n.id: n for n in new.nodes}
    
    nodes_added = []
    nodes_removed = []
    nodes_modified = []
    
    # Find added and modified nodes
    for node_id, node in new_nodes.items():
        if node_id not in old_nodes:
            nodes_added.append(NodeChange(
                node_id=node_id,
                change_type="added",
                new_value=node,
            ))
        else:
            old_node = old_nodes[node_id]
            # Check for modifications
            modified_fields = []
            if node.type != old_node.type:
                modified_fields.append("type")
            if node.label != old_node.label:
                modified_fields.append("label")
            if node.metadata != old_node.metadata:
                modified_fields.append("metadata")
            
            if modified_fields:
                nodes_modified.append(NodeChange(
                    node_id=node_id,
                    change_type="modified",
                    old_value=old_node,
                    new_value=node,
                    fields=modified_fields,
                ))
    
    # Find removed nodes
    for node_id, node in old_nodes.items():
        if node_id not in new_nodes:
            nodes_removed.append(NodeChange(
                node_id=node_id,
                change_type="removed",
                old_value=node,
            ))
    
    # Build flow maps
    def flow_key(f):
        return (f.source_id, f.target_id)
    
    old_flows = {flow_key(f): f for f in old.flows}
    new_flows = {flow_key(f): f for f in new.flows}
    
    flows_added = []
    flows_removed = []
    flows_modified = []
    
    for key, flow in new_flows.items():
        if key not in old_flows:
            flows_added.append(FlowChange(
                flow_id=f"{flow.source_id}->{flow.target_id}",
                change_type="added",
                source=flow.source_id,
                target=flow.target_id,
            ))
    
    for key, flow in old_flows.items():
        if key not in new_flows:
            flows_removed.append(FlowChange(
                flow_id=f"{flow.source_id}->{flow.target_id}",
                change_type="removed",
                source=flow.source_id,
                target=flow.target_id,
            ))
    
    # Compare metrics from nodes
    metrics_changed: list[MetricChange] = []
    
    # Collect metrics from old and new snapshots
    def collect_node_metrics(snapshot: WorldSnapshot) -> dict[str, float]:
        result = {}
        for node in snapshot.nodes:
            for metric in node.metrics:
                key = f"{node.id}.{metric.name}"
                result[key] = metric.value
        return result
    
    old_metrics = collect_node_metrics(old)
    new_metrics = collect_node_metrics(new)
    all_metric_keys = set(old_metrics.keys()) | set(new_metrics.keys())
    
    for key in all_metric_keys:
        old_val = old_metrics.get(key)
        new_val = new_metrics.get(key)
        
        if old_val is None and new_val is not None:
            metrics_changed.append(MetricChange(
                metric_id=key,
                change_type="added",
                new_value=new_val,
            ))
        elif old_val is not None and new_val is None:
            metrics_changed.append(MetricChange(
                metric_id=key,
                change_type="removed",
                old_value=old_val,
            ))
        elif old_val != new_val:
            metrics_changed.append(MetricChange(
                metric_id=key,
                change_type="modified",
                old_value=old_val,
                new_value=new_val,
                delta=new_val - old_val if old_val is not None and new_val is not None else 0,
            ))
    
    return HolomapDiff(
        nodes_added=nodes_added,
        nodes_removed=nodes_removed,
        nodes_modified=nodes_modified,
        flows_added=flows_added,
        flows_removed=flows_removed,
        flows_modified=flows_modified,
        metrics_changed=metrics_changed,
    )
