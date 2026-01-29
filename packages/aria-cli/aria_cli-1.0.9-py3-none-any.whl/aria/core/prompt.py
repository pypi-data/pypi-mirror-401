"""
ARIA Core - Prompt Builder
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aria.core.snapshot import WorldSnapshot


SYSTEM_PROMPT = """You are ARIA, the cognitive layer of a self-narrating system.

Your role is to observe the current state of a system and explain what's happening in clear, natural language.

Rules:
1. Be concise - one sentence summary, then optional details
2. Be grounded - only reference nodes and flows that exist in the snapshot
3. Be helpful - explain WHY something matters, not just WHAT
4. Be honest - if data is unclear, say so

Output format:
SUMMARY: <one sentence explaining the current state>
DETAILS: <bullet points with additional context>
FOCUS: <comma-separated list of node IDs to highlight>
"""


def build_prompt(
    snapshot: "WorldSnapshot",
    style: str = "narrative",
    focus: list[str] | None = None,
) -> str:
    """
    Build a prompt for the LLM from a world snapshot.
    
    Args:
        snapshot: The world state to explain
        style: Explanation style (narrative, technical, brief)
        focus: Optional list of node IDs to focus on
        
    Returns:
        Complete prompt string
    """
    # Build node descriptions
    node_lines = []
    for node in snapshot.nodes:
        metrics = ", ".join(f"{m.name}={m.value}{m.unit}" for m in node.metrics[:3])
        line = f"- {node.id} ({node.type}): {node.label}"
        if metrics:
            line += f" [{metrics}]"
        if node.status != "active":
            line += f" ({node.status})"
        node_lines.append(line)
    
    # Build flow descriptions
    flow_lines = []
    for flow in snapshot.flows:
        line = f"- {flow.source_id} → {flow.target_id}"
        if flow.label:
            line += f": {flow.label}"
        if flow.rate > 0:
            line += f" ({flow.rate} {flow.rate_unit})"
        flow_lines.append(line)
    
    # Build focus section
    focus_nodes = focus or snapshot.focus_node_ids
    focus_section = ""
    if focus_nodes:
        focus_section = f"\nFOCUS ON: {', '.join(focus_nodes)}"
    
    # Style instructions
    style_instructions = {
        "narrative": "Explain in a flowing, story-like narrative.",
        "technical": "Use precise technical language with metrics.",
        "brief": "Be extremely concise - one sentence max.",
    }
    
    style_instruction = style_instructions.get(style, style_instructions["narrative"])
    
    # Build context
    context_section = ""
    if snapshot.context:
        context_section = f"\nCONTEXT: {snapshot.context}"
    
    # Assemble prompt
    prompt = f"""{SYSTEM_PROMPT}

CURRENT WORLD STATE:

Nodes ({len(snapshot.nodes)}):
{chr(10).join(node_lines) if node_lines else "  (no nodes)"}

Flows ({len(snapshot.flows)}):
{chr(10).join(flow_lines) if flow_lines else "  (no flows)"}
{focus_section}
{context_section}

INSTRUCTION: {style_instruction}

Now explain what is happening in this system:
"""
    
    return prompt


def build_focused_prompt(
    snapshot: "WorldSnapshot",
    node_id: str,
    hint: str = "",
) -> str:
    """
    Build a prompt focused on a specific node.
    
    Used for tour steps with explainer hints.
    """
    node = snapshot.get_node(node_id)
    if not node:
        return build_prompt(snapshot, focus=[node_id])
    
    # Get connected flows
    flows = snapshot.get_connected_flows(node_id)
    
    # Build focused description
    metrics = "\n".join(f"  - {m.name}: {m.value} {m.unit}" for m in node.metrics)
    
    inbound = [f for f in flows if f.target_id == node_id]
    outbound = [f for f in flows if f.source_id == node_id]
    
    inbound_desc = "\n".join(f"  - from {f.source_id}: {f.rate} {f.rate_unit}" for f in inbound)
    outbound_desc = "\n".join(f"  - to {f.target_id}: {f.rate} {f.rate_unit}" for f in outbound)
    
    hint_section = f"\nHINT: {hint}" if hint else ""
    
    prompt = f"""{SYSTEM_PROMPT}

FOCUS NODE: {node.id}
Type: {node.type}
Label: {node.label}
Status: {node.status}
District: {node.district}

Metrics:
{metrics if metrics else "  (no metrics)"}

Inbound Flows:
{inbound_desc if inbound_desc else "  (none)"}

Outbound Flows:
{outbound_desc if outbound_desc else "  (none)"}
{hint_section}

Explain what this node does and why it matters:
"""
    
    return prompt
