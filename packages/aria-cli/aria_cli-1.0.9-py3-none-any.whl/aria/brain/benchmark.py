"""
ARIA Brain - Benchmark

Benchmark LLM brains for performance comparison.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from aria.brain.manager import BrainManager


@dataclass
class BenchmarkResult:
    """Result from benchmarking a brain."""
    name: str
    tokens_per_sec: float
    latency_ms: float
    quality: str


TEST_PROMPT = """You are a helpful assistant. Explain in one sentence what a "cognitive runtime" is.

Answer:"""


def benchmark_brain(name: str, iterations: int = 3) -> BenchmarkResult:
    """Benchmark a single brain."""
    from aria.brain.loader import load_brain
    from aria.core.engine import EngineConfig
    
    manager = BrainManager()
    
    if not manager.is_installed(name):
        return BenchmarkResult(
            name=name,
            tokens_per_sec=0,
            latency_ms=0,
            quality="not installed",
        )
    
    config = EngineConfig(brain=name, max_tokens=100)
    llm = load_brain(name, config)
    
    latencies = []
    token_counts = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        response = llm.complete(TEST_PROMPT, max_tokens=100)
        elapsed = time.perf_counter() - start
        
        latencies.append(elapsed * 1000)  # Convert to ms
        # Approximate token count (rough estimate)
        token_counts.append(len(response.split()))
    
    llm.close()
    
    avg_latency = sum(latencies) / len(latencies)
    avg_tokens = sum(token_counts) / len(token_counts)
    tokens_per_sec = (avg_tokens / (avg_latency / 1000)) if avg_latency > 0 else 0
    
    # Quality rating based on response coherence (simplified)
    quality = "good" if avg_tokens > 20 else "fair"
    
    return BenchmarkResult(
        name=name,
        tokens_per_sec=tokens_per_sec,
        latency_ms=avg_latency,
        quality=quality,
    )


def run_benchmark(iterations: int = 3) -> list[BenchmarkResult]:
    """Benchmark all installed brains."""
    manager = BrainManager()
    brains = manager.list_brains()
    
    results = []
    for brain in brains:
        if brain.status == "installed":
            result = benchmark_brain(brain.name, iterations)
            results.append(result)
    
    return sorted(results, key=lambda r: r.tokens_per_sec, reverse=True)
