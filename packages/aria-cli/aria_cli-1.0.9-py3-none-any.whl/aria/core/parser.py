"""
ARIA Core - Response Parser
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from aria.core.response import ExplainerResponse

if TYPE_CHECKING:
    from aria.core.snapshot import WorldSnapshot


def parse_response(
    raw_response: str,
    snapshot: "WorldSnapshot",
) -> ExplainerResponse:
    """
    Parse the raw LLM response into an ExplainerResponse.
    
    Handles various output formats and validates against the snapshot.
    """
    # Extract sections
    summary = extract_section(raw_response, "SUMMARY")
    details = extract_list_section(raw_response, "DETAILS")
    focus = extract_list_section(raw_response, "FOCUS", separator=",")
    
    # If no structured output, use the whole response as summary
    if not summary:
        summary = raw_response.strip()
        # Truncate if too long
        if len(summary) > 500:
            summary = summary[:497] + "..."
    
    # Validate focus nodes exist in snapshot
    valid_node_ids = {node.id for node in snapshot.nodes}
    validated_focus = [f for f in focus if f in valid_node_ids]
    
    # Validate details don't reference non-existent nodes
    validated_details = []
    for detail in details:
        # Basic sanity check - detail shouldn't be too long
        if len(detail) > 200:
            detail = detail[:197] + "..."
        validated_details.append(detail)
    
    # Calculate confidence based on validation
    confidence = 1.0
    if not summary:
        confidence = 0.5
    if focus and not validated_focus:
        confidence -= 0.2  # Penalize for invalid focus
    
    return ExplainerResponse(
        summary=summary,
        details=validated_details,
        focus_nodes=validated_focus,
        confidence=max(0.0, confidence),
    )


def extract_section(text: str, section_name: str) -> str:
    """Extract a named section from the response."""
    # Try "SECTION:" format
    pattern = rf"{section_name}:\s*(.+?)(?=\n[A-Z]+:|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try "**Section**" markdown format
    pattern = rf"\*\*{section_name}\*\*[:\s]*(.+?)(?=\*\*[A-Z]+\*\*|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    
    return ""


def extract_list_section(
    text: str,
    section_name: str,
    separator: str = "\n",
) -> list[str]:
    """Extract a list section from the response."""
    raw = extract_section(text, section_name)
    if not raw:
        return []
    
    if separator == ",":
        items = [item.strip() for item in raw.split(",")]
    else:
        # Handle bullet points
        lines = raw.split("\n")
        items = []
        for line in lines:
            line = line.strip()
            # Remove bullet prefixes
            line = re.sub(r"^[-•*]\s*", "", line)
            if line:
                items.append(line)
    
    return items


def sanitize_response(response: ExplainerResponse) -> ExplainerResponse:
    """
    Sanitize a response for safety and quality.
    """
    # Remove any potential prompt injection
    summary = response.summary
    summary = re.sub(r"<[^>]+>", "", summary)  # Remove HTML-like tags
    summary = re.sub(r"\[INST\].*?\[/INST\]", "", summary, flags=re.DOTALL)  # Remove instruction markers
    
    # Truncate if needed
    if len(summary) > 500:
        summary = summary[:497] + "..."
    
    return ExplainerResponse(
        summary=summary,
        details=response.details[:10],  # Max 10 details
        focus_nodes=response.focus_nodes[:5],  # Max 5 focus nodes
        confidence=response.confidence,
        metadata=response.metadata,
    )
