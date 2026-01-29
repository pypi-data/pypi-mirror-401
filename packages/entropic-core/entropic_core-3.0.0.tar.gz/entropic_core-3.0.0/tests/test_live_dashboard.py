"""
Tests for Live Dashboard module
"""

from unittest.mock import Mock

from entropic_core.realtime.live_dashboard import (
    DashboardConfig,
    LiveDashboard,
    create_dashboard,
)


def test_dashboard_initialization():
    """Test basic initialization"""
    config = DashboardConfig(port=8765)
    brain = Mock(current_entropy=0.5)
    dashboard = LiveDashboard(config, brain)

    assert dashboard is not None
    assert dashboard.config.port == 8765


def test_create_dashboard_factory():
    """Test factory function"""
    brain = Mock()
    dashboard = create_dashboard(brain, port=9000)
    assert dashboard is not None


def test_get_current_state():
    """Test getting current dashboard state"""
    brain = Mock(current_entropy=0.6)
    dashboard = LiveDashboard(DashboardConfig(), brain)

    state = dashboard.get_current_state()
    assert "entropy" in state
