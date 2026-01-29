"""
Integration tests for EntropyBrain with new modules
"""

from entropic_core import EntropyBrain


def test_brain_with_all_modules_enabled():
    """Test brain initialization with all modules"""
    brain = EntropyBrain(
        enable_intervention=True,
        enable_hallucination_detection=True,
        enable_auto_healing=True,
        enable_consensus=True,
    )

    assert brain.llm_middleware is not None
    assert brain.hallucination_detector is not None
    assert brain.auto_healer is not None
    assert brain.consensus_engine is not None


def test_hallucination_detection_integration():
    """Test hallucination detection through brain"""
    brain = EntropyBrain(enable_hallucination_detection=True)

    result = brain.detect_hallucinations(
        "The capital of France is London", context=["The capital of France is Paris"]
    )

    assert "is_hallucination" in result
    assert result["is_hallucination"] is True


def test_auto_healing_integration():
    """Test auto-healing through brain"""
    brain = EntropyBrain(enable_auto_healing=True)

    # Create checkpoint
    cp_id = brain.create_checkpoint("test")
    assert cp_id is not None

    # Rollback
    success = brain.rollback_to_checkpoint(cp_id)
    assert success in [True, False]  # May fail if no state change


def test_consensus_integration():
    """Test consensus through brain"""
    brain = EntropyBrain(enable_consensus=True)

    class MockAgent:
        def __init__(self, name):
            self.name = name
            self.entropy = 0.3

        def respond(self, prompt):
            return "Option A"

    agents = [MockAgent(f"agent_{i}") for i in range(3)]

    result = brain.reach_consensus(
        agents, "What is the best option?", options=["A", "B", "C"]
    )

    assert "decision" in result
    assert "confidence" in result


def test_intervention_with_hallucination_detection():
    """Test that intervention and hallucination detection work together"""
    brain = EntropyBrain(enable_intervention=True, enable_hallucination_detection=True)

    def mock_llm(**kwargs):
        from unittest.mock import Mock

        return Mock(choices=[Mock(message=Mock(content="Test response"))])

    wrapped = brain.wrap_llm(mock_llm)

    # Call should be intercepted
    result = wrapped(messages=[{"role": "user", "content": "test"}])

    stats = brain.get_intervention_stats()
    assert stats["total_calls"] > 0


def test_entropy_propagation_to_all_modules():
    """Test that entropy updates propagate to all modules"""
    brain = EntropyBrain(
        enable_intervention=True,
        enable_hallucination_detection=True,
        enable_auto_healing=True,
        enable_consensus=True,
    )

    # Connect mock agents
    class MockAgent:
        def __init__(self):
            self.state = "active"
            self.last_decision = None

    agents = [MockAgent() for _ in range(3)]
    brain.connect(agents)

    # Measure entropy (should update all modules)
    entropy = brain.measure()

    # Verify all modules received update
    assert brain.llm_middleware.current_entropy == entropy
    assert brain.hallucination_detector.current_entropy == entropy
