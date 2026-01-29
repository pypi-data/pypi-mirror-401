"""
End-to-end integration tests
"""

from unittest.mock import patch

from entropic_core import (
    EntropyBrain,
    create_dashboard,
    create_entropic_brain,
    create_metrics,
    protect,
)


def test_create_brain():
    """Test creating entropy brain"""
    brain = create_entropic_brain()
    assert brain is not None


def test_brain_measure():
    """Test brain entropy measurement"""
    brain = EntropyBrain()

    class MockAgent:
        def __init__(self):
            self.state = "active"
            self.last_decision = None

    agents = [MockAgent() for _ in range(3)]
    brain.connect(agents)

    entropy = brain.measure()
    assert 0 <= entropy <= 1


def test_protect_function():
    """Test protect() function exists and callable"""
    with patch("entropic_core.discovery.auto_discover.AutoDiscovery"):
        # Should not raise
        protect()
        assert True


def test_create_dashboard_integration():
    """Test creating dashboard with brain"""
    brain = EntropyBrain()
    dashboard = create_dashboard(brain, port=8766)
    assert dashboard.brain == brain


def test_create_metrics_integration():
    """Test creating metrics with brain"""
    brain = EntropyBrain()
    metrics = create_metrics(brain)
    assert metrics is not None
