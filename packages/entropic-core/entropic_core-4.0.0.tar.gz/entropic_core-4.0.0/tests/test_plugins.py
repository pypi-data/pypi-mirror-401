"""
Comprehensive tests for plugin system
"""

import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, "scripts")

from entropic_core.plugins.plugin_api import EntropyPlugin, PluginAPI
from entropic_core.plugins.plugin_loader import PluginLoader
from entropic_core.plugins.plugin_manager import PluginManager


class MockBrain:
    """Mock brain for testing plugins"""

    def __init__(self):
        self.agents = []
        self.current_entropy = 0.5
        self.regulations = []

    def get_current_entropy(self):
        return {"combined": self.current_entropy}

    def get_agents(self):
        return self.agents


class MockPlugin(EntropyPlugin):
    """Mock plugin implementation for unit tests"""

    name = "mock_plugin"
    version = "1.0.0"
    description = "Mock plugin for unit tests"

    def __init__(self, config=None):
        super().__init__(config)
        self.initialized = False
        self.activated = False
        self.deactivated = False
        self.cycles_processed = 0
        self.regulations_processed = 0

    def on_initialize(self, api: PluginAPI):
        self.initialized = True
        self.api = api

    def on_activate(self):
        self.activated = True

    def on_deactivate(self):
        self.deactivated = True

    def on_entropy_measured(self, entropy_value: float):
        """Called when entropy is measured"""

    def on_entropy_cycle(self, entropy_data: dict):
        self.cycles_processed += 1
        return entropy_data

    def on_regulation(self, decision: dict):
        self.regulations_processed += 1
        return decision


def test_plugin_lifecycle():
    """Test plugin lifecycle methods"""
    plugin = MockPlugin()
    brain = MockBrain()
    api = PluginAPI(brain)

    # Initialize
    plugin.on_initialize(api)
    assert plugin.initialized

    # Activate
    plugin.on_activate()
    assert plugin.activated

    # Process cycles
    plugin.on_entropy_cycle({"combined": 0.5})
    assert plugin.cycles_processed == 1

    # Process regulation
    plugin.on_regulation({"action": "MAINTAIN"})
    assert plugin.regulations_processed == 1

    # Deactivate
    plugin.on_deactivate()
    assert plugin.deactivated


def test_plugin_api():
    """Test PluginAPI functionality"""
    brain = MockBrain()
    brain.current_entropy = 0.75
    api = PluginAPI(brain)

    # Test get entropy
    entropy = api.get_current_entropy()
    if isinstance(entropy, dict):
        assert entropy["combined"] == 0.75
    else:
        assert entropy == 0.75

    # Test get agents
    agents = api.get_agents()
    assert isinstance(agents, list)


def test_plugin_loader_discovery():
    """Test plugin discovery from directories"""
    loader = PluginLoader()

    # Should not crash with default dirs
    plugins = loader.discover_plugins()
    assert isinstance(plugins, list)


def test_plugin_loader_with_custom_dir():
    """Test plugin loader with custom directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a test plugin file
        plugin_code = """
from entropic_core.plugins.plugin_api import EntropyPlugin

class CustomTestPlugin(EntropyPlugin):
    name = "custom_test"
    version = "1.0.0"
    description = "Custom test plugin"
    
    def on_initialize(self, api):
        pass
"""
        plugin_path = Path(tmpdir) / "custom_plugin.py"
        plugin_path.write_text(plugin_code)

        loader = PluginLoader(plugin_dirs=[tmpdir])
        # Discovery should work without errors
        plugins = loader.discover_plugins()
        assert isinstance(plugins, list)


def test_plugin_manager_register():
    """Test plugin registration"""
    brain = MockBrain()
    manager = PluginManager(brain)

    plugin = MockPlugin()
    manager.register_plugin(plugin)

    assert "mock_plugin" in manager.plugins
    assert plugin.initialized


def test_plugin_manager_unregister():
    """Test plugin unregistration"""
    brain = MockBrain()
    manager = PluginManager(brain)

    plugin = MockPlugin()
    manager.register_plugin(plugin)
    manager.unregister_plugin("mock_plugin")

    assert "mock_plugin" not in manager.plugins
    assert plugin.deactivated


def test_plugin_manager_broadcast():
    """Test broadcasting events to plugins"""
    brain = MockBrain()
    manager = PluginManager(brain)

    plugin = MockPlugin()
    manager.register_plugin(plugin)

    # Broadcast entropy cycle
    manager.broadcast_entropy_cycle({"combined": 0.6})
    assert plugin.cycles_processed == 1

    # Broadcast regulation
    manager.broadcast_regulation({"action": "REDUCE_CHAOS"})
    assert plugin.regulations_processed == 1


def test_plugin_config():
    """Test plugin configuration"""
    config = {"threshold": 0.8, "enabled": True}
    plugin = MockPlugin(config)

    assert plugin.config["threshold"] == 0.8
    assert plugin.config["enabled"] == True


def test_plugin_error_handling():
    """Test plugin error handling"""

    class BrokenPlugin(EntropyPlugin):
        name = "broken_plugin"
        version = "1.0.0"
        description = "Plugin that throws errors"

        def on_entropy_measured(self, entropy_value: float):
            pass

        def on_entropy_cycle(self, entropy_data):
            raise ValueError("Intentional error")

    brain = MockBrain()
    manager = PluginManager(brain)

    broken = BrokenPlugin()
    manager.register_plugin(broken)

    # Should not crash, should handle error gracefully
    try:
        manager.broadcast_entropy_cycle({"combined": 0.5})
    except Exception:
        pytest.fail("Plugin manager should handle plugin errors gracefully")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
