"""
Tests for ConsensusEngine module
"""

from entropic_core.core.consensus_engine import (
    ConsensusEngine,
    ConsensusMethod,
    create_consensus_engine,
)


class MockAgent:
    """Mock agent for testing"""

    def __init__(self, name, stability=0.5):
        self.name = name
        self.stability = stability
        self.entropy = 1.0 - stability

    def respond(self, prompt):
        return f"Response from {self.name}"


def test_consensus_engine_initialization():
    """Test basic initialization"""
    engine = ConsensusEngine()
    assert engine is not None


def test_create_consensus_engine_factory():
    """Test factory function"""
    engine = create_consensus_engine()
    assert engine is not None


def test_consensus_method_enum():
    """Test ConsensusMethod enum values"""
    assert ConsensusMethod.MAJORITY.value == "majority"
    assert ConsensusMethod.WEIGHTED.value == "weighted"


def test_reach_consensus():
    """Test reaching consensus"""
    engine = ConsensusEngine()
    agents = [MockAgent("agent1"), MockAgent("agent2")]

    result = engine.reach_consensus(agents, "Test question", options=["A", "B"])

    assert "decision" in result
    assert "confidence" in result
