"""
Tests for aria.core.engine
"""

import pytest
from aria.core.engine import CognitiveEngine, EngineConfig
from aria.core.snapshot import WorldSnapshot, NodeSnapshot


class TestEngineConfig:
    """Tests for EngineConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = EngineConfig()
        
        assert config.brain == "tinyllama"
        assert config.context_size == 2048
        assert config.temperature == 0.7
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = EngineConfig(
            brain="phi2",
            context_size=4096,
            temperature=0.5,
        )
        
        assert config.brain == "phi2"
        assert config.context_size == 4096
        assert config.temperature == 0.5


class TestCognitiveEngine:
    """Tests for CognitiveEngine."""
    
    def test_mock_mode(self):
        """Test engine in mock mode."""
        # Create engine directly with brain name
        engine = CognitiveEngine(brain="mock")
        
        snapshot = WorldSnapshot(
            nodes=[NodeSnapshot(id="core", type="processor", label="Core")],
            flows=[],
        )
        response = engine.explain(snapshot)
        
        assert response.summary is not None
        assert response.confidence > 0
    
    def test_graceful_degradation(self):
        """Test graceful degradation when brain not available."""
        config = EngineConfig(brain="nonexistent", graceful_degradation=True)
        engine = CognitiveEngine(config=config)
        
        snapshot = WorldSnapshot(
            nodes=[NodeSnapshot(id="core", type="processor", label="Core")],
            flows=[],
        )
        response = engine.explain(snapshot)
        
        assert response.is_degraded is True
