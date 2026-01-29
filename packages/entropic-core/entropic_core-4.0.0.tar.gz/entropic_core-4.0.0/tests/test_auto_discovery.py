"""
Tests for Auto-Discovery module
"""

from unittest.mock import Mock, patch

from entropic_core.discovery.auto_discover import (
    AutoDiscovery,
    get_discovery,
    get_protection_stats,
    protect,
    unprotect,
)


def test_auto_discovery_initialization():
    """Test basic initialization"""
    discovery = AutoDiscovery()
    assert discovery is not None


def test_protect_function():
    """Test protect() convenience function"""
    with patch("entropic_core.discovery.auto_discover.AutoDiscovery") as MockDiscovery:
        mock_instance = Mock()
        MockDiscovery.return_value = mock_instance

        protect()

        MockDiscovery.assert_called_once()


def test_unprotect_function():
    """Test unprotect() function"""
    # Should not raise
    unprotect()
    assert True


def test_get_discovery():
    """Test get_discovery() function"""
    discovery = get_discovery()
    # May return None if not initialized
    assert discovery is None or isinstance(discovery, AutoDiscovery)


def test_get_protection_stats():
    """Test get_protection_stats() function"""
    stats = get_protection_stats()
    assert isinstance(stats, dict)
