"""
Tests for AutoHealer module
"""

import time

from entropic_core.core.auto_healer import AgentState, Checkpoint, create_healer


class MockBrain:
    """Mock brain for testing"""

    def __init__(self):
        self.current_entropy = 0.5
        self.agents = []


def test_auto_healer_initialization():
    """Test basic initialization"""
    healer = create_healer()
    assert healer is not None


def test_agent_state_enum():
    """Test AgentState enum values"""
    assert AgentState.HEALTHY.value == "healthy"
    assert AgentState.DEGRADED.value == "degraded"
    assert AgentState.CRITICAL.value == "critical"
    assert AgentState.QUARANTINED.value == "quarantined"


def test_checkpoint_creation():
    """Test checkpoint dataclass"""
    checkpoint = Checkpoint(
        checkpoint_id="test-123",
        agent_id="agent-1",
        timestamp=time.time(),
        state_snapshot={"key": "value"},
        entropy_at_checkpoint=0.3,
    )
    assert checkpoint.checkpoint_id == "test-123"
    assert checkpoint.agent_id == "agent-1"
