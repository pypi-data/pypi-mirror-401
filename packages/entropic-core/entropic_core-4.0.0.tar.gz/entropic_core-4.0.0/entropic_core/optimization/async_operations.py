"""Async operations for improved I/O performance."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from entropic_core import EntropyBrain  # Import EntropyBrain for optional creation

logger = logging.getLogger(__name__)


class AsyncEntropyBrain:
    """Async version of EntropyBrain for non-blocking operations."""

    def __init__(self, brain=None):
        """
        Wrap existing EntropyBrain with async capabilities.

        Args:
            brain: Optional EntropyBrain instance. If not provided, creates new one.
        """
        if brain is None:
            brain = EntropyBrain()

        self.brain = brain
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.agents = []

    def connect(self, agents: List[Any]) -> None:
        """
        Connect agents to async brain.

        Args:
            agents: List of agents to connect
        """
        self.agents = agents
        if hasattr(self.brain, "connect"):
            self.brain.connect(agents)

    async def async_measure(self) -> float:
        """
        Measure entropy asynchronously.

        Returns:
            Float value of combined entropy
        """
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, self.brain.measure)
        return result

    async def measure_async(self) -> float:
        """Measure entropy asynchronously (alias)."""
        return await self.async_measure()

    async def regulate_async(self) -> Dict[str, Any]:
        """Regulate system asynchronously."""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, self.brain.regulate)
        return result

    async def analyze_async(self) -> Dict[str, Any]:
        """Run causal analysis asynchronously."""
        loop = asyncio.get_event_loop()

        if hasattr(self.brain, "causal_analyzer"):
            result = await loop.run_in_executor(
                self.executor,
                self.brain.causal_analyzer.find_root_cause,
                self.brain.current_entropy,
            )
            return result

        return {"error": "Causal analyzer not available"}

    async def predict_async(self, time_horizon: str = "1h") -> Dict[str, Any]:
        """Run prediction asynchronously."""
        loop = asyncio.get_event_loop()

        if hasattr(self.brain, "predictive_engine"):
            result = await loop.run_in_executor(
                self.executor,
                self.brain.predictive_engine.forecast_system_health,
                time_horizon,
            )
            return result

        return {"error": "Predictive engine not available"}

    async def full_cycle_async(self) -> Dict[str, Any]:
        """Run full monitoring cycle asynchronously."""
        # Run measure, regulate, and log in parallel where possible
        entropy_task = self.measure_async()

        entropy = await entropy_task

        # Regulate based on measurement
        regulation = await self.regulate_async()

        # Log asynchronously
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self.executor, self.brain.log)

        return {
            "entropy": entropy,
            "regulation": regulation,
            "timestamp": asyncio.get_event_loop().time(),
        }

    async def batch_measure_agents(self, agents: List[Any]) -> List[Dict[str, float]]:
        """Measure entropy for multiple agents in parallel."""
        tasks = []

        for agent in agents:
            task = asyncio.create_task(self._measure_single_agent(agent))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def _measure_single_agent(self, agent) -> Dict[str, float]:
        """Measure entropy for a single agent."""
        asyncio.get_event_loop()
        # Simulate measurement (replace with actual implementation)
        await asyncio.sleep(0.01)  # Non-blocking I/O simulation
        return {"agent_id": id(agent), "entropy": 0.5}

    def close(self):
        """Cleanup executor."""
        self.executor.shutdown(wait=True)


async def async_measure(brain) -> Dict[str, float]:
    """Standalone async measure function."""
    async_brain = AsyncEntropyBrain(brain)
    result = await async_brain.measure_async()
    async_brain.close()
    return result


async def async_regulate(brain) -> Dict[str, Any]:
    """Standalone async regulate function."""
    async_brain = AsyncEntropyBrain(brain)
    result = await async_brain.regulate_async()
    async_brain.close()
    return result


async def async_monitor_loop(
    brain, interval: float = 1.0, duration: Optional[float] = None
):
    """Run monitoring loop asynchronously."""
    async_brain = AsyncEntropyBrain(brain)
    start_time = asyncio.get_event_loop().time()

    try:
        while True:
            # Check duration limit
            if duration and (asyncio.get_event_loop().time() - start_time) >= duration:
                break

            # Run full cycle
            result = await async_brain.full_cycle_async()
            logger.info(f"Async cycle completed: {result}")

            # Wait for next interval
            await asyncio.sleep(interval)

    finally:
        async_brain.close()
