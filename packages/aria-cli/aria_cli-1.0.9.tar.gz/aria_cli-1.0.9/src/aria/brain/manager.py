"""
ARIA Brain - Model Manager

Manages downloading, loading, and benchmarking LLM brains.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class BrainInfo:
    """Information about an installed brain."""
    name: str
    model: str
    size: str
    path: str
    status: str
    context_size: int = 2048
    license: str = "Unknown"


# Registry of available brains
BRAIN_REGISTRY: dict[str, dict[str, Any]] = {
    "tinyllama": {
        "repo": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
        "file": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "model": "TinyLlama 1.1B Chat",
        "size": "638 MB",
        "context_size": 2048,
        "license": "Apache 2.0",
    },
    "phi2": {
        "repo": "TheBloke/phi-2-GGUF",
        "file": "phi-2.Q4_K_M.gguf",
        "model": "Microsoft Phi-2",
        "size": "1.7 GB",
        "context_size": 2048,
        "license": "MIT",
    },
    "qwen2": {
        "repo": "Qwen/Qwen2-1.5B-Instruct-GGUF",
        "file": "qwen2-1_5b-instruct-q4_k_m.gguf",
        "model": "Qwen2 1.5B Instruct",
        "size": "940 MB",
        "context_size": 2048,
        "license": "Apache 2.0",
    },
    "llama3": {
        "repo": "hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF",
        "file": "llama-3.2-1b-instruct-q4_k_m.gguf",
        "model": "Llama 3.2 1B Instruct",
        "size": "770 MB",
        "context_size": 2048,
        "license": "Meta Llama 3",
    },
}


class BrainManager:
    """Manages LLM brain models."""
    
    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = model_dir or Path.home() / ".aria" / "models"
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def list_brains(self) -> list[BrainInfo]:
        """List all available brains (installed and registry)."""
        brains = []
        
        for name, info in BRAIN_REGISTRY.items():
            path = self.model_dir / info["file"]
            status = "installed" if path.exists() else "available"
            
            brains.append(BrainInfo(
                name=name,
                model=info["model"],
                size=info["size"],
                path=str(path) if path.exists() else "",
                status=status,
                context_size=info["context_size"],
                license=info["license"],
            ))
        
        # Also check for any local GGUF files not in registry
        for path in self.model_dir.glob("*.gguf"):
            name = path.stem
            if not any(b.name == name for b in brains):
                size_mb = path.stat().st_size / (1024 * 1024)
                brains.append(BrainInfo(
                    name=name,
                    model="Local Model",
                    size=f"{size_mb:.0f} MB",
                    path=str(path),
                    status="installed",
                ))
        
        return brains
    
    def get_info(self, name: str) -> BrainInfo:
        """Get information about a specific brain."""
        if name in BRAIN_REGISTRY:
            info = BRAIN_REGISTRY[name]
            path = self.model_dir / info["file"]
            return BrainInfo(
                name=name,
                model=info["model"],
                size=info["size"],
                path=str(path) if path.exists() else "",
                status="installed" if path.exists() else "available",
                context_size=info["context_size"],
                license=info["license"],
            )
        
        # Check for local file
        path = self.model_dir / f"{name}.gguf"
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            return BrainInfo(
                name=name,
                model="Local Model",
                size=f"{size_mb:.0f} MB",
                path=str(path),
                status="installed",
            )
        
        raise ValueError(f"Unknown brain: {name}")
    
    def get_path(self, name: str) -> Path:
        """Get the path to a brain's model file."""
        if name in BRAIN_REGISTRY:
            return self.model_dir / BRAIN_REGISTRY[name]["file"]
        
        path = self.model_dir / f"{name}.gguf"
        if path.exists():
            return path
        
        raise ValueError(f"Brain not found: {name}")
    
    def is_installed(self, name: str) -> bool:
        """Check if a brain is installed."""
        try:
            path = self.get_path(name)
            return path.exists()
        except ValueError:
            return False
    
    def download(self, name: str, force: bool = False) -> Path:
        """Download a brain from HuggingFace."""
        if name not in BRAIN_REGISTRY:
            raise ValueError(f"Unknown brain: {name}. Available: {list(BRAIN_REGISTRY.keys())}")
        
        info = BRAIN_REGISTRY[name]
        path = self.model_dir / info["file"]
        
        if path.exists() and not force:
            return path
        
        # Download using huggingface_hub
        try:
            from huggingface_hub import hf_hub_download
        except ImportError:
            raise RuntimeError(
                "huggingface-hub is required for downloading models. "
                "Install it with: pip install huggingface-hub"
            )
        
        downloaded_path = hf_hub_download(
            repo_id=info["repo"],
            filename=info["file"],
            local_dir=self.model_dir,
            local_dir_use_symlinks=False,
        )
        
        return Path(downloaded_path)
    
    def delete(self, name: str) -> bool:
        """Delete an installed brain."""
        try:
            path = self.get_path(name)
            if path.exists():
                path.unlink()
                return True
        except ValueError:
            pass
        return False
