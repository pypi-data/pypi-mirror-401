"""
ARIA Brain - Model Loader

Loads LLM models for inference.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aria.core.engine import EngineConfig


class BaseLLM(ABC):
    """Abstract base class for LLM backends."""
    
    @abstractmethod
    def complete(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        stop: list[str] | None = None,
    ) -> str:
        """Generate a completion for the given prompt."""
        ...
    
    @abstractmethod
    def close(self) -> None:
        """Release resources."""
        ...


class LlamaCppLLM(BaseLLM):
    """LLM backend using llama-cpp-python."""
    
    def __init__(
        self,
        model_path: Path,
        context_size: int = 2048,
        n_threads: int = 4,
    ) -> None:
        try:
            from llama_cpp import Llama
        except ImportError:
            raise RuntimeError(
                "llama-cpp-python is required for local inference. "
                "Install it with: pip install aria-cli[llm]"
            )
        
        self._llm = Llama(
            model_path=str(model_path),
            n_ctx=context_size,
            n_threads=n_threads,
            verbose=False,
        )
    
    def complete(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        stop: list[str] | None = None,
    ) -> str:
        """Generate a completion."""
        output = self._llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop or [],
            echo=False,
        )
        
        return output["choices"][0]["text"]
    
    def close(self) -> None:
        """Release resources."""
        del self._llm
        self._llm = None


class MockLLM(BaseLLM):
    """Mock LLM for testing without a real model."""
    
    def complete(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        stop: list[str] | None = None,
    ) -> str:
        """Return a mock response."""
        return """SUMMARY: The system is operating normally with all nodes active.
DETAILS:
- Trinity Core is cycling at standard frequency
- Waterwheel is processing incoming data
- ARIA is monitoring and predicting system behavior
FOCUS: LenixTrinityEngine, WaterwheelHub"""
    
    def close(self) -> None:
        """No resources to release."""
        pass


def load_brain(name: str, config: "EngineConfig") -> BaseLLM:
    """
    Load a brain for inference.
    
    Args:
        name: Brain name (from registry) or path to GGUF file
        config: Engine configuration
        
    Returns:
        Loaded LLM instance
    """
    from aria.brain.manager import BrainManager
    
    # Check for mock mode
    if name == "mock":
        return MockLLM()
    
    # Get model path
    if Path(name).exists():
        model_path = Path(name)
    elif config.model_path and config.model_path.exists():
        model_path = config.model_path
    else:
        manager = BrainManager()
        if not manager.is_installed(name):
            # Try to download
            try:
                model_path = manager.download(name)
            except Exception as e:
                raise RuntimeError(f"Brain '{name}' not found and download failed: {e}")
        else:
            model_path = manager.get_path(name)
    
    # Load the model
    return LlamaCppLLM(
        model_path=model_path,
        context_size=config.context_size,
    )
