"""
Basic tests for core modules
"""

import sys

import pytest

sys.path.insert(0, "scripts")

from entropic_core.core.agent_adapter import AgentAdapter
from entropic_core.core.entropy_monitor import EntropyMonitor
from entropic_core.core.entropy_regulator import EntropyRegulator


def test_entropy_monitor():
    """Test entropy monitoring"""
    monitor = EntropyMonitor()

    # Create mock agents
    agents = [
        AgentAdapter.create_mock_agent(f"agent_{i}", behavior="balanced")
        for i in range(5)
    ]

    # Wrap agents
    wrapped = [AgentAdapter.wrap_agent(a) for a in agents]

    # Measure entropy
    metrics = monitor.measure_system_entropy(wrapped)

    assert "combined" in metrics
    assert "decision" in metrics
    assert "dispersion" in metrics
    assert "communication" in metrics
    assert 0 <= metrics["combined"] <= 1


def test_entropy_regulator():
    """Test entropy regulation"""
    regulator = EntropyRegulator()

    agents = [AgentAdapter.create_mock_agent(f"agent_{i}") for i in range(3)]

    # Test high entropy regulation
    decision = regulator.regulate(0.9, agents)
    assert decision["action"] == "REDUCE_CHAOS"
    assert "commands" in decision

    # Test low entropy regulation
    decision = regulator.regulate(0.1, agents)
    assert decision["action"] == "INCREASE_CHAOS"

    # Test optimal entropy
    decision = regulator.regulate(0.5, agents)
    assert decision["action"] == "MAINTAIN"


def test_agent_adapter():
    """Test agent adapter"""
    mock_agent = AgentAdapter.create_mock_agent("test", behavior="balanced")

    # Test wrapping
    wrapped = AgentAdapter.wrap_agent(mock_agent)

    # Test entropy context
    wrapped.set_entropy_context({"chaos_level": 0.8})
    assert wrapped.homeostasis_score < 1.0

    # Test action
    result = wrapped.act("test observation")
    assert result is not None
    assert wrapped.last_decision is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
