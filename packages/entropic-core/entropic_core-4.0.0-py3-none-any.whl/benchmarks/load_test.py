"""Load testing for Entropic Core."""

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

sys.path.insert(0, "../")

from entropic_core import EntropyBrain


class MockAgent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.state = 0.5
        self.last_decision = f"decision_{agent_id}"


def worker_thread(brain: EntropyBrain, duration: int, worker_id: int) -> Dict[str, Any]:
    """Worker thread that continuously measures entropy."""
    start_time = time.time()
    operations = 0
    errors = 0

    while time.time() - start_time < duration:
        try:
            brain.measure()
            operations += 1
        except Exception:
            errors += 1

    elapsed = time.time() - start_time

    return {
        "worker_id": worker_id,
        "operations": operations,
        "errors": errors,
        "duration": elapsed,
        "ops_per_sec": operations / elapsed,
    }


def run_load_test(
    agent_count: int = 10, concurrent_workers: int = 10, duration_seconds: int = 30
) -> Dict[str, Any]:
    """Run load test with multiple concurrent workers."""

    print(f"\n{'='*60}")
    print(f"ENTROPIC CORE LOAD TEST")
    print(f"{'='*60}\n")
    print(f"Configuration:")
    print(f"  Agents: {agent_count}")
    print(f"  Concurrent workers: {concurrent_workers}")
    print(f"  Duration: {duration_seconds}s")
    print(f"{'='*60}\n")

    # Setup
    agents = [MockAgent(i) for i in range(agent_count)]
    brain = EntropyBrain()
    brain.connect(agents)

    # Run load test
    print("Starting load test...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        futures = [
            executor.submit(worker_thread, brain, duration_seconds, i)
            for i in range(concurrent_workers)
        ]

        results = [future.result() for future in as_completed(futures)]

    end_time = time.time()

    # Calculate statistics
    total_operations = sum(r["operations"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    actual_duration = end_time - start_time

    overall_throughput = total_operations / actual_duration
    error_rate = (total_errors / total_operations * 100) if total_operations > 0 else 0

    # Print results
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    print(f"Total operations: {total_operations}")
    print(f"Total errors: {total_errors}")
    print(f"Error rate: {error_rate:.2f}%")
    print(f"Overall throughput: {overall_throughput:.2f} ops/sec")
    print(f"Actual duration: {actual_duration:.2f}s")

    print(f"\nPer-worker breakdown:")
    for result in results:
        print(f"  Worker {result['worker_id']}: {result['ops_per_sec']:.2f} ops/sec")

    print(f"{'='*60}\n")

    return {
        "total_operations": total_operations,
        "total_errors": total_errors,
        "error_rate": error_rate,
        "throughput": overall_throughput,
        "duration": actual_duration,
        "workers": results,
    }


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    agent_count = int(args[0]) if len(args) > 0 else 10
    workers = int(args[1]) if len(args) > 1 else 10
    duration = int(args[2]) if len(args) > 2 else 30

    run_load_test(agent_count, workers, duration)
