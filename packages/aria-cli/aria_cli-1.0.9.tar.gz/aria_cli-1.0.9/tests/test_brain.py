"""
Tests for aria.brain
"""

import pytest
from aria.brain import BrainManager, BrainInfo


class TestBrainManager:
    """Tests for BrainManager."""
    
    def test_list_brains(self, tmp_path):
        """Test listing available brains."""
        manager = BrainManager(model_dir=tmp_path)
        brains = manager.list_brains()
        
        # Should list registry brains
        assert len(brains) >= 4
        brain_names = [b.name for b in brains]
        assert "tinyllama" in brain_names
        assert "phi2" in brain_names
    
    def test_get_info(self, tmp_path):
        """Test getting brain info."""
        manager = BrainManager(model_dir=tmp_path)
        info = manager.get_info("tinyllama")
        
        assert info.name == "tinyllama"
        assert info.model == "TinyLlama 1.1B Chat"
        assert info.license == "Apache 2.0"
    
    def test_is_installed(self, tmp_path):
        """Test checking if brain is installed."""
        manager = BrainManager(model_dir=tmp_path)
        
        # Should not be installed in empty dir
        assert manager.is_installed("tinyllama") is False
    
    def test_unknown_brain(self, tmp_path):
        """Test handling unknown brain."""
        manager = BrainManager(model_dir=tmp_path)
        
        with pytest.raises(ValueError):
            manager.get_info("unknown_brain")
