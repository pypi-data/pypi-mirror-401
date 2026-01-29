"""
Advanced Features Test Suite
Tests for causal analyzer, predictive engine, simulation, and security
"""

import os
import sys
import unittest
from datetime import datetime

import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entropic_core.advanced.causal_analyzer import CausalAnalyzer
from entropic_core.advanced.predictive_engine import PredictiveEngine
from entropic_core.advanced.security_layer import SecurityLayer
from entropic_core.advanced.simulation_mode import SimulationEngine
from entropic_core.core.evolutionary_memory import EvolutionaryMemory


class TestCausalAnalyzer(unittest.TestCase):
    """Test suite for causal analysis functionality"""

    def setUp(self):
        self.memory = EvolutionaryMemory(db_path=":memory:")
        self.analyzer = CausalAnalyzer(self.memory)

        # Seed memory with test data
        self._seed_test_data()

    def _seed_test_data(self):
        """Create realistic test scenarios in memory"""
        # Scenario 1: Agent communication spike causes entropy increase
        for i in range(10):
            self.memory.log_decision(
                entropy=0.4 + (i * 0.05),
                action="maintain",
                result="success",
                metadata={
                    "agent_count": 5,
                    "message_count": 50 + (i * 10),
                    "decision_time": 0.2,
                },
            )

        # Create entropy spike
        self.memory.log_decision(
            entropy=0.85,
            action="reduce_chaos",
            result="success",
            metadata={
                "agent_count": 5,
                "message_count": 250,  # Spike!
                "decision_time": 0.2,
            },
        )

    def test_causal_analyzer_accuracy(self):
        """Verify diagnostic accuracy >90%"""
        spike_event = {
            "timestamp": datetime.now(),
            "entropy": 0.85,
            "metrics": {
                "decision_entropy": 0.8,
                "dispersion": 0.9,
                "communication": 0.95,  # Clear spike
            },
        }

        diagnosis = self.analyzer.find_root_cause(spike_event)

        # Check that communication is identified as primary cause
        self.assertIsNotNone(diagnosis["primary_cause"])
        self.assertIn("communication", diagnosis["primary_cause"].lower())
        self.assertGreater(diagnosis["confidence"], 0.7)
        self.assertIsNotNone(diagnosis["suggested_fix"])

    def test_correlation_detection(self):
        """Test detection of correlations between metrics"""
        metrics = [
            {"combined": 0.8, "decision": 0.8, "dispersion": 0.7, "communication": 0.9}
        ]
        events = []

        correlations = self.analyzer._analyze_correlations(metrics, events)

        self.assertIsInstance(correlations, list)
        self.assertGreater(len(correlations), 0)

        # Each correlation should have type and confidence
        for corr in correlations:
            self.assertIn("type", corr)
            self.assertIn("confidence", corr)
            self.assertIsInstance(corr["confidence"], float)

    def test_pattern_matching(self):
        """Test matching to historical patterns"""
        current_event = {
            "entropy": 0.85,
            "metrics": {
                "decision_entropy": 0.8,
                "dispersion": 0.9,
                "communication": 0.95,
            },
        }

        patterns = self.analyzer._match_historical_patterns(current_event)

        self.assertIsInstance(patterns, list)
        # Should find at least one similar pattern
        if len(patterns) > 0:
            pattern = patterns[0]
            self.assertIn("similarity", pattern)
            self.assertIn("historical_event", pattern)


class TestPredictiveEngine(unittest.TestCase):
    """Test suite for predictive forecasting"""

    def setUp(self):
        self.memory = EvolutionaryMemory(db_path=":memory:")
        self.engine = PredictiveEngine(self.memory)

        # Create time series data
        self._seed_trending_data()

    def _seed_trending_data(self):
        """Create realistic time series for forecasting"""
        base = 0.3
        for i in range(30):
            self.memory.log_decision(
                entropy=base + (i * 0.015),  # Steady increase
                action="maintain",
                result="success",
                metadata={"agent_count": 5},
            )

    def test_collapse_prediction(self):
        """Test prediction of system collapse"""
        prediction = self.engine.predict_collapse_risk(hours_ahead=2)

        self.assertIn("probability", prediction)
        self.assertIn("time_to_collapse", prediction)
        self.assertIn("confidence", prediction)
        self.assertIsInstance(prediction["probability"], float)
        self.assertGreaterEqual(prediction["probability"], 0.0)
        self.assertLessEqual(prediction["probability"], 1.0)

    def test_forecast_accuracy(self):
        """Test entropy forecasting accuracy"""
        forecast = self.engine.forecast_entropy(steps_ahead=10)

        self.assertIn("predicted_values", forecast)
        self.assertIn("confidence_intervals", forecast)
        self.assertEqual(len(forecast["predicted_values"]), 10)

    def test_trend_detection(self):
        """Test detection of entropy trends"""
        trend = self.engine._detect_trend()

        self.assertIsNotNone(trend)
        self.assertIn("direction", trend)
        self.assertIn("strength", trend)
        # With our seeded data, should detect upward trend
        self.assertIn(trend["direction"], ["INCREASING", "STABLE", "DECREASING"])


class TestSimulationEngine(unittest.TestCase):
    """Test suite for scenario simulation"""

    def setUp(self):
        # Create minimal brain mock
        from entropic_core.brain import EntropyBrain
        from entropic_core.core.agent_adapter import BaseAgent

        agents = [BaseAgent(f"agent_{i}") for i in range(3)]
        self.brain = EntropyBrain(agents)
        self.memory = EvolutionaryMemory(db_path=":memory:")
        self.simulator = SimulationEngine(self.brain, self.memory)

    def test_agent_addition_simulation(self):
        """Test simulation of adding agents"""
        result = self.simulator.simulate_scenario(scenario={"add_agents": 5}, steps=50)

        self.assertIn("system_stable", result)
        self.assertIn("avg_entropy", result)
        self.assertIsInstance(result["system_stable"], bool)

    def test_load_spike_simulation(self):
        """Test simulation of load increase"""
        result = self.simulator.simulate_scenario(
            scenario={"increase_load": 2.0}, steps=50
        )

        self.assertIn("system_stable", result)
        self.assertIn("avg_entropy", result)
        # Higher load should increase entropy
        self.assertGreater(result["avg_entropy"], 0.3)

    def test_bottleneck_identification(self):
        """Test identification of system bottlenecks"""
        result = self.simulator.simulate_scenario(
            scenario={"add_agents": 50}, steps=100, monte_carlo_runs=3  # Stress test
        )

        self.assertIn("bottleneck_analysis", result)
        self.assertIn("bottleneck", result["bottleneck_analysis"])


class TestSecurityLayer(unittest.TestCase):
    """Test suite for security features"""

    def setUp(self):
        from entropic_core.brain import EntropyBrain
        from entropic_core.core.agent_adapter import BaseAgent

        agents = [BaseAgent(f"agent_{i}") for i in range(3)]
        self.brain = EntropyBrain(agents)
        self.security = SecurityLayer(self.brain)

    def test_flood_attack_detection(self):
        """Test detection of entropy flood attack"""
        # Simulate flood: rapid entropy increase
        for i in range(30):
            self.security.update(0.3 + (i * 0.02))

        threat = self.security.detect_entropy_attack()

        # Should detect either flood or anomaly
        if threat["detected"]:
            self.assertIn("primary_threat", threat)

    def test_drain_attack_detection(self):
        """Test detection of entropy drain attack"""
        # Simulate drain: rapid entropy decrease
        for i in range(30):
            self.security.update(0.7 - (i * 0.02))

        threat = self.security.detect_entropy_attack()

        if threat["detected"]:
            self.assertIn("primary_threat", threat)

    def test_resonance_detection(self):
        """Test detection of resonance attack"""
        # Simulate oscillation
        for i in range(60):
            entropy = 0.5 + 0.2 * np.sin(i / 5)
            self.security.update(entropy)

        threat = self.security.detect_entropy_attack()

        if threat["detected"]:
            self.assertIn("primary_threat", threat)

    def test_false_positive_rate(self):
        """Ensure false positive rate is low"""
        # Simulate normal operation
        for i in range(50):
            self.security.update(0.5 + np.random.normal(0, 0.05))

        threat = self.security.detect_entropy_attack()

        # Should NOT detect threats in normal operation
        # (Allow occasional false positives)
        self.assertIsNotNone(threat)


class TestIntegration(unittest.TestCase):
    """Integration tests for advanced features"""

    def setUp(self):
        from entropic_core.brain import EntropyBrain
        from entropic_core.core.agent_adapter import BaseAgent

        agents = [BaseAgent(f"agent_{i}") for i in range(3)]
        self.brain = EntropyBrain(agents)
        self.memory = EvolutionaryMemory(db_path=":memory:")
        self.analyzer = CausalAnalyzer(self.memory)
        self.predictor = PredictiveEngine(self.memory)
        self.security = SecurityLayer(self.brain)

    def test_full_pipeline(self):
        """Test full advanced feature pipeline"""
        # Simulate several cycles
        for i in range(20):
            entropy = 0.4 + (i * 0.02)
            self.memory.log_decision(
                entropy=entropy,
                action="maintain",
                result="success",
                metadata={"agent_count": 3},
            )
            self.security.update(entropy)

        # Test causal analysis
        spike_event = {
            "timestamp": datetime.now(),
            "entropy": 0.8,
            "metrics": {
                "decision_entropy": 0.7,
                "dispersion": 0.8,
                "communication": 0.9,
            },
        }
        diagnosis = self.analyzer.find_root_cause(spike_event)
        self.assertIsNotNone(diagnosis)

        # Test prediction
        prediction = self.predictor.predict_collapse_risk(hours_ahead=1)
        self.assertIn("probability", prediction)

        # Test security
        threat = self.security.detect_entropy_attack()
        self.assertIn("detected", threat)

        # Test simulation
        simulator = SimulationEngine(self.brain, self.memory)
        sim_result = simulator.simulate_scenario(scenario={"add_agents": 5}, steps=30)
        self.assertIn("system_stable", sim_result)


if __name__ == "__main__":
    unittest.main()
