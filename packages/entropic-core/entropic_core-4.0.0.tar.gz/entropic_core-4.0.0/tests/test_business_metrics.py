"""
Tests for Business Metrics module
"""

from unittest.mock import Mock

from entropic_core.business.metrics import (
    BusinessMetrics,
    BusinessMetricsConfig,
    create_metrics,
)


def test_metrics_initialization():
    """Test basic initialization"""
    metrics = BusinessMetrics()
    assert metrics is not None


def test_metrics_with_config():
    """Test metrics with custom config"""
    config = BusinessMetricsConfig()
    metrics = BusinessMetrics(config)
    assert metrics.config == config


def test_create_metrics_factory():
    """Test create_metrics factory function"""
    brain = Mock(current_entropy=0.5)
    metrics = create_metrics(brain)
    assert metrics is not None


def test_track_tokens():
    """Test tracking token usage"""
    metrics = BusinessMetrics()
    metrics.track_tokens("gpt-4", 100, 50)
    assert metrics.total_tokens > 0


def test_track_intervention():
    """Test tracking interventions"""
    metrics = BusinessMetrics()
    metrics.track_intervention("STABILIZATION")
    assert metrics.total_interventions > 0


def test_generate_roi_report():
    """Test generating ROI report"""
    metrics = BusinessMetrics()
    metrics.track_tokens("gpt-4", 1000, 500)
    report = metrics.generate_roi_report()
    assert isinstance(report, dict)
