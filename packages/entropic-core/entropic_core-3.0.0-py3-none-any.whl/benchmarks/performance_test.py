"""Performance benchmarking for Entropic Core."""

import statistics
import sys
import time
from typing import Any, Dict

sys.path.insert(0, "../")

from entropic_core import EntropyBrain
from entropic_core.optimization import CacheManager


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, agent_id: int):
        self.id = agent_id
        self.state = 0.5
        self.last_decision = f"decision_{agent_id}"

    def act(self):
        """Simulate action."""
        self.state += 0.01
        return f"action_{self.id}"


def benchmark_entropy_measurement(
    brain: EntropyBrain, iterations: int = 1000
) -> Dict[str, Any]:
    """Benchmark entropy measurement performance."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        brain.measure()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms

    return {
        "operation": "entropy_measurement",
        "iterations": iterations,
        "mean_ms": round(statistics.mean(times), 3),
        "median_ms": round(statistics.median(times), 3),
        "stdev_ms": round(statistics.stdev(times), 3),
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3),
        "p95_ms": round(statistics.quantiles(times, n=20)[18], 3),
        "p99_ms": round(statistics.quantiles(times, n=100)[98], 3),
    }


def benchmark_regulation(brain: EntropyBrain, iterations: int = 100) -> Dict[str, Any]:
    """Benchmark regulation performance."""
    times = []

    for _ in range(iterations):
        # Set varying entropy levels
        brain.current_entropy = 0.3 + (_ % 10) / 10

        start = time.perf_counter()
        brain.regulate()
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return {
        "operation": "regulation",
        "iterations": iterations,
        "mean_ms": round(statistics.mean(times), 3),
        "median_ms": round(statistics.median(times), 3),
        "stdev_ms": round(statistics.stdev(times), 3),
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3),
    }


def benchmark_caching(cache: CacheManager, iterations: int = 10000) -> Dict[str, Any]:
    """Benchmark cache performance."""
    # Warm up cache
    for i in range(100):
        cache.set(f"key_{i}", f"value_{i}")

    hit_times = []
    miss_times = []

    for i in range(iterations):
        key = f"key_{i % 100}"  # Will hit cache for many

        start = time.perf_counter()
        value = cache.get(key)
        end = time.perf_counter()

        if value is not None:
            hit_times.append((end - start) * 1000000)  # microseconds
        else:
            miss_times.append((end - start) * 1000000)

    return {
        "operation": "caching",
        "total_operations": iterations,
        "cache_hits": len(hit_times),
        "cache_misses": len(miss_times),
        "hit_rate": round(len(hit_times) / iterations * 100, 2),
        "mean_hit_us": round(statistics.mean(hit_times), 3) if hit_times else 0,
        "mean_miss_us": round(statistics.mean(miss_times), 3) if miss_times else 0,
    }


def benchmark_full_cycle(brain: EntropyBrain, iterations: int = 100) -> Dict[str, Any]:
    """Benchmark full measure-regulate-log cycle."""
    times = []

    for _ in range(iterations):
        start = time.perf_counter()

        # Full cycle
        brain.measure()
        brain.regulate()
        brain.log()

        end = time.perf_counter()
        times.append((end - start) * 1000)

    return {
        "operation": "full_cycle",
        "iterations": iterations,
        "mean_ms": round(statistics.mean(times), 3),
        "median_ms": round(statistics.median(times), 3),
        "throughput_ops_sec": round(1000 / statistics.mean(times), 2),
    }


def run_performance_benchmark(agent_count: int = 10) -> Dict[str, Any]:
    """Run complete performance benchmark suite."""
    print(f"\n{'='*60}")
    print(f"ENTROPIC CORE PERFORMANCE BENCHMARK")
    print(f"{'='*60}\n")

    # Setup
    print(f"Setting up with {agent_count} agents...")
    agents = [MockAgent(i) for i in range(agent_count)]
    brain = EntropyBrain()
    brain.connect(agents)
    cache = CacheManager(backend="memory")

    results = {}

    # Run benchmarks
    print("\n1. Benchmarking entropy measurement...")
    results["measurement"] = benchmark_entropy_measurement(brain, iterations=1000)
    print(f"   Mean: {results['measurement']['mean_ms']}ms")
    print(f"   P95: {results['measurement']['p95_ms']}ms")

    print("\n2. Benchmarking regulation...")
    results["regulation"] = benchmark_regulation(brain, iterations=100)
    print(f"   Mean: {results['regulation']['mean_ms']}ms")

    print("\n3. Benchmarking caching...")
    results["caching"] = benchmark_caching(cache, iterations=10000)
    print(f"   Hit rate: {results['caching']['hit_rate']}%")
    print(f"   Mean hit: {results['caching']['mean_hit_us']}μs")

    print("\n4. Benchmarking full cycle...")
    results["full_cycle"] = benchmark_full_cycle(brain, iterations=100)
    print(f"   Mean: {results['full_cycle']['mean_ms']}ms")
    print(f"   Throughput: {results['full_cycle']['throughput_ops_sec']} ops/sec")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Agent count: {agent_count}")
    print(f"Measurement latency (P95): {results['measurement']['p95_ms']}ms")
    print(
        f"Full cycle throughput: {results['full_cycle']['throughput_ops_sec']} ops/sec"
    )
    print(f"Cache hit rate: {results['caching']['hit_rate']}%")
    print(f"{'='*60}\n")

    return results


if __name__ == "__main__":
    import sys

    agent_count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    run_performance_benchmark(agent_count)
