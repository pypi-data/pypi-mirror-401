"""Memory profiling for Entropic Core."""

import gc
import sys
import tracemalloc

sys.path.insert(0, "../")

from entropic_core import EntropyBrain


class MockAgent:
    def __init__(self, agent_id: int):
        self.id = agent_id
        self.state = 0.5
        self.last_decision = f"decision_{agent_id}"


def run_memory_profile(agent_count: int = 100, iterations: int = 1000):
    """Profile memory usage of Entropic Core."""

    print(f"\n{'='*60}")
    print(f"ENTROPIC CORE MEMORY PROFILE")
    print(f"{'='*60}\n")

    # Start memory tracking
    tracemalloc.start()
    gc.collect()

    snapshot_before = tracemalloc.take_snapshot()

    # Create brain and agents
    print(f"Creating {agent_count} agents...")
    agents = [MockAgent(i) for i in range(agent_count)]
    brain = EntropyBrain()
    brain.connect(agents)

    snapshot_after_init = tracemalloc.take_snapshot()

    # Run operations
    print(f"Running {iterations} iterations...")
    for i in range(iterations):
        brain.measure()
        if i % 100 == 0:
            brain.regulate()
            brain.log()

    snapshot_after_ops = tracemalloc.take_snapshot()

    # Calculate memory differences
    stats_init = snapshot_after_init.compare_to(snapshot_before, "lineno")
    stats_ops = snapshot_after_ops.compare_to(snapshot_after_init, "lineno")

    # Print results
    print(f"\n{'='*60}")
    print("INITIALIZATION MEMORY USAGE")
    print(f"{'='*60}")

    total_init = sum(stat.size_diff for stat in stats_init)
    print(f"Total memory increase: {total_init / 1024 / 1024:.2f} MB")

    print(f"\nTop 5 memory allocations:")
    for stat in stats_init[:5]:
        print(f"  {stat.size_diff / 1024:.1f} KB - {stat.traceback.format()[0]}")

    print(f"\n{'='*60}")
    print("OPERATIONS MEMORY USAGE")
    print(f"{'='*60}")

    total_ops = sum(stat.size_diff for stat in stats_ops)
    print(f"Total memory increase: {total_ops / 1024 / 1024:.2f} MB")
    print(f"Memory per iteration: {total_ops / iterations / 1024:.2f} KB")

    print(f"\nTop 5 memory allocations:")
    for stat in stats_ops[:5]:
        print(f"  {stat.size_diff / 1024:.1f} KB - {stat.traceback.format()[0]}")

    # Current memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"\n{'='*60}")
    print("OVERALL MEMORY USAGE")
    print(f"{'='*60}")
    print(f"Current: {current / 1024 / 1024:.2f} MB")
    print(f"Peak: {peak / 1024 / 1024:.2f} MB")
    print(f"{'='*60}\n")

    tracemalloc.stop()


if __name__ == "__main__":
    import sys

    agent_count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

    run_memory_profile(agent_count, iterations)
