"""
ARIA Tour - Tour Validator

Validate tour definition files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aria.tour.loader import Tour, load_tour


@dataclass
class ValidationError:
    """A validation error."""
    field: str
    message: str
    severity: str = "error"  # error, warning


@dataclass
class ValidationResult:
    """Result from validating a tour."""
    tour_id: str
    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]


def validate_tour(tour: Tour) -> ValidationResult:
    """Validate a tour definition."""
    errors = []
    warnings = []
    
    # Required fields
    if not tour.id:
        errors.append(ValidationError("id", "Tour ID is required"))
    
    if not tour.name:
        errors.append(ValidationError("name", "Tour name is required"))
    
    if not tour.steps:
        errors.append(ValidationError("steps", "Tour must have at least one step"))
    
    # Validate steps
    step_ids = set()
    for i, step in enumerate(tour.steps):
        prefix = f"steps[{i}]"
        
        if not step.id:
            errors.append(ValidationError(f"{prefix}.id", "Step ID is required"))
        elif step.id in step_ids:
            errors.append(ValidationError(f"{prefix}.id", f"Duplicate step ID: {step.id}"))
        else:
            step_ids.add(step.id)
        
        if not step.title:
            errors.append(ValidationError(f"{prefix}.title", "Step title is required"))
        
        if step.delay_ms < 0:
            errors.append(ValidationError(f"{prefix}.delay_ms", "Delay cannot be negative"))
        
        if step.delay_ms > 60000:
            warnings.append(ValidationError(
                f"{prefix}.delay_ms",
                "Delay is very long (>60 seconds)",
                severity="warning",
            ))
        
        if step.trigger_explainer and not step.focus_nodes:
            warnings.append(ValidationError(
                f"{prefix}.focus_nodes",
                "Explainer triggered but no focus nodes specified",
                severity="warning",
            ))
        
        if step.explainer_style not in ("narrative", "technical", "brief"):
            warnings.append(ValidationError(
                f"{prefix}.explainer_style",
                f"Unknown style: {step.explainer_style}",
                severity="warning",
            ))
    
    # Check for author
    if not tour.author:
        warnings.append(ValidationError(
            "author",
            "No author specified",
            severity="warning",
        ))
    
    return ValidationResult(
        tour_id=tour.id,
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def validate_tour_file(path: Path) -> ValidationResult:
    """Validate a tour file."""
    try:
        tour = load_tour(path)
        return validate_tour(tour)
    except Exception as e:
        return ValidationResult(
            tour_id=path.stem,
            valid=False,
            errors=[ValidationError("file", f"Failed to load: {e}")],
            warnings=[],
        )
