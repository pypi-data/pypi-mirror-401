"""
Integration tests for Entropic Core
Tests complete workflows from monitoring to regulation
"""

import time

import numpy as np
import pytest

from entropic_core import EntropyBrain
from entropic_core.advanced import CausalAnalyzer, PredictiveEngine, SimulationEngine


class MockAgent:
    """Mock agent for testing"""

    def __init__(self, name, initial_state=0.5):
        self.name = name
        self.state = initial_state
        self.last_decision = None
        self.current_state = initial_state
        self.messages_sent = 0

    def act(self, observation=None):
        """Make a random decision"""
        import random

        self.last_decision = random.choice(["A", "B", "C"])
        self.state += random.uniform(-0.1, 0.1)
        self.state = max(0, min(1, self.state))
        self.current_state = self.state
        self.messages_sent += 1
        return self.last_decision


class TestFullWorkflow:
    """Test complete entropy monitoring workflow"""

    def test_basic_monitoring_cycle(self):
        """Test basic measure -> regulate -> log cycle"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(5)]

        brain.connect(agents)

        # Run monitoring cycle
        for _ in range(10):
            for agent in agents:
                agent.act()

            entropy = brain.measure()
            assert 0.0 <= entropy <= 1.0, "Entropy out of range"

            action = brain.regulate()
            assert action["action"] in ["REDUCE_CHAOS", "INCREASE_CHAOS", "MAINTAIN"]

            brain.log()

        # Verify memory was recorded
        assert len(brain.monitor.metrics_history) > 0

    def test_high_entropy_regulation(self):
        """Test system responds to high entropy"""
        brain = EntropyBrain()

        # Create agents with very different states (high entropy)
        agents = [MockAgent(f"Agent-{i}", initial_state=i * 0.2) for i in range(5)]
        brain.connect(agents)

        # Force different decisions
        for i, agent in enumerate(agents):
            agent.last_decision = chr(65 + i)  # A, B, C, D, E

        entropy = brain.measure()
        action = brain.regulate()

        if entropy > 0.7:
            assert action["action"] == "REDUCE_CHAOS"
            assert (
                "merge_similar_agents" in action["commands"]
                or "increase_validation_steps" in action["commands"]
            )

    def test_low_entropy_regulation(self):
        """Test system responds to low entropy"""
        brain = EntropyBrain()

        # Create agents with identical states (low entropy)
        agents = [MockAgent(f"Agent-{i}", initial_state=0.5) for i in range(5)]
        brain.connect(agents)

        # Force identical decisions
        for agent in agents:
            agent.last_decision = "A"

        entropy = brain.measure()
        action = brain.regulate()

        if entropy < 0.3:
            assert action["action"] == "INCREASE_CHAOS"
            assert (
                "create_explorer_agent" in action["commands"]
                or "inject_random_event" in action["commands"]
            )


class TestAdvancedFeatures:
    """Test advanced features integration"""

    def test_causal_analysis_integration(self):
        """Test causal analyzer with real system"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(5)]
        brain.connect(agents)

        # Generate some history
        for _ in range(20):
            for agent in agents:
                agent.act()
            brain.measure()
            brain.log()

        # Analyze causes
        analyzer = CausalAnalyzer(brain)

        # Force high entropy
        for i, agent in enumerate(agents):
            agent.state = i * 0.25
            agent.last_decision = chr(65 + i)

        entropy = brain.measure()

        if entropy > 0.7:
            diagnosis = analyzer.find_root_cause()
            assert "primary_cause" in diagnosis
            assert "confidence" in diagnosis
            assert 0 <= diagnosis["confidence"] <= 1

    def test_predictive_engine_integration(self):
        """Test predictive engine forecasting"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(5)]
        brain.connect(agents)

        # Generate history for prediction
        for _ in range(30):
            for agent in agents:
                agent.act()
            brain.measure()
            brain.log()

        predictor = PredictiveEngine(brain)
        forecast = predictor.forecast(steps_ahead=10)

        assert "next_value" in forecast
        assert "confidence_interval" in forecast
        assert "trend" in forecast
        assert forecast["trend"] in ["increasing", "decreasing", "stable"]

    def test_simulation_integration(self):
        """Test simulation engine"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(3)]
        brain.connect(agents)

        simulator = SimulationEngine(brain)

        # Simulate adding more agents
        result = simulator.simulate_scenario(
            scenario={"action": "add_agents", "count": 5}, steps=50
        )

        assert "system_stable" in result
        assert "max_agents_supported" in result or "system_collapses_at_step" in result


class TestMemoryAndLearning:
    """Test memory and learning capabilities"""

    def test_pattern_recognition(self):
        """Test system learns from patterns"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(5)]
        brain.connect(agents)

        # Create repeated pattern: high chaos -> regulation -> stable
        for cycle in range(5):
            # High chaos phase
            for agent in agents:
                agent.state = np.random.random()
                agent.last_decision = np.random.choice(["A", "B", "C"])

            brain.measure()
            brain.regulate()
            brain.log()

            # Stable phase
            for agent in agents:
                agent.state = 0.5
                agent.last_decision = "A"

            brain.measure()
            brain.regulate()
            brain.log()

        # Query patterns
        memory = brain.memory
        patterns = memory.query_patterns(min_success_rate=0.5)

        assert len(patterns) > 0, "Should have learned some patterns"

    def test_memory_persistence(self):
        """Test memory persists across sessions"""
        db_path = "test_memory.db"

        # Session 1: Create and log
        brain1 = EntropyBrain(db_path=db_path)
        agents = [MockAgent(f"Agent-{i}") for i in range(3)]
        brain1.connect(agents)

        for _ in range(10):
            for agent in agents:
                agent.act()
            brain1.measure()
            brain1.log()

        event_count_1 = len(brain1.memory.query_events())

        # Session 2: Load existing memory
        brain2 = EntropyBrain(db_path=db_path)
        event_count_2 = len(brain2.memory.query_events())

        assert event_count_2 == event_count_1, "Memory should persist"

        # Cleanup
        import os

        if os.path.exists(db_path):
            os.remove(db_path)


class TestPerformance:
    """Performance and stress tests"""

    def test_large_scale_monitoring(self):
        """Test with many agents"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(100)]
        brain.connect(agents)

        start_time = time.time()

        for _ in range(10):
            for agent in agents:
                agent.act()
            brain.measure()

        elapsed = time.time() - start_time

        # Should handle 100 agents x 10 cycles in reasonable time
        assert elapsed < 5.0, f"Performance too slow: {elapsed:.2f}s"

    def test_memory_efficiency(self):
        """Test memory doesn't grow unbounded"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(10)]
        brain.connect(agents)

        # Run many cycles
        for _ in range(1000):
            for agent in agents:
                agent.act()
            brain.measure()
            brain.log()

        # Check history doesn't grow infinitely
        assert len(brain.monitor.metrics_history) <= 100, "History should be bounded"


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_empty_agents(self):
        """Test with no agents"""
        brain = EntropyBrain()
        brain.connect([])

        entropy = brain.measure()
        assert entropy == 0.0, "Empty system should have zero entropy"

    def test_single_agent(self):
        """Test with single agent"""
        brain = EntropyBrain()
        agent = MockAgent("Solo")
        brain.connect([agent])

        agent.act()
        entropy = brain.measure()

        # Single agent should have low entropy
        assert entropy < 0.3

    def test_invalid_agent_state(self):
        """Test handles invalid agent states gracefully"""
        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(3)]

        # Corrupt an agent's state
        agents[1].last_decision = None
        agents[2].current_state = None

        brain.connect(agents)

        # Should not crash
        try:
            entropy = brain.measure()
            assert entropy >= 0.0
        except Exception as e:
            pytest.fail(f"Should handle invalid state gracefully: {e}")


class TestConcurrency:
    """Test concurrent operations"""

    def test_thread_safety(self):
        """Test thread-safe operations"""
        import threading

        brain = EntropyBrain()
        agents = [MockAgent(f"Agent-{i}") for i in range(10)]
        brain.connect(agents)

        results = []

        def measure_entropy():
            for _ in range(10):
                for agent in agents:
                    agent.act()
                entropy = brain.measure()
                results.append(entropy)

        # Run multiple threads
        threads = [threading.Thread(target=measure_entropy) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All measurements should be valid
        assert all(0.0 <= e <= 1.0 for e in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
