"""
Tests for aria.tour
"""

import pytest
import json
from pathlib import Path
from aria.tour import Tour, TourStep, load_tour, validate_tour


class TestTour:
    """Tests for Tour and TourStep."""
    
    def test_load_tour(self, tmp_path, sample_tour_data):
        """Test loading a tour from file."""
        tour_file = tmp_path / "test.json"
        with open(tour_file, "w") as f:
            json.dump(sample_tour_data, f)
        
        tour = load_tour(tour_file)
        
        assert tour.id == "test-tour"
        assert tour.name == "Test Tour"
        assert len(tour.steps) == 2
    
    def test_tour_step_defaults(self):
        """Test TourStep default values."""
        step = TourStep(
            id="test",
            title="Test",
            description="A test step",
        )
        
        assert step.auto_advance is False
        assert step.delay_ms == 0
        assert step.trigger_explainer is False
        assert step.explainer_style == "narrative"


class TestTourValidation:
    """Tests for tour validation."""
    
    def test_valid_tour(self, sample_tour_data):
        """Test validating a valid tour."""
        tour = Tour(
            id=sample_tour_data["id"],
            name=sample_tour_data["name"],
            description=sample_tour_data["description"],
            steps=[
                TourStep(**step) for step in sample_tour_data["steps"]
            ],
        )
        
        result = validate_tour(tour)
        
        assert result.valid is True
        assert len(result.errors) == 0
    
    def test_missing_id(self):
        """Test validation catches missing ID."""
        tour = Tour(
            id="",
            name="Test",
            description="",
            steps=[TourStep(id="s1", title="Step", description="")],
        )
        
        result = validate_tour(tour)
        
        assert result.valid is False
        assert any("ID" in e.message for e in result.errors)
    
    def test_empty_steps(self):
        """Test validation catches empty steps."""
        tour = Tour(
            id="test",
            name="Test",
            description="",
            steps=[],
        )
        
        result = validate_tour(tour)
        
        assert result.valid is False
