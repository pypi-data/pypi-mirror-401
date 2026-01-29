"""Plugin manager for coordinating plugin execution."""

import logging
from typing import Dict, List, Optional

from .plugin_api import EntropyPlugin, PluginAPI, PluginContext
from .plugin_loader import PluginLoader, PluginMetadata

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages plugin lifecycle and execution."""

    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.loader = PluginLoader()
        self.api = PluginAPI(brain_instance)
        self.logger = logging.getLogger("plugin.manager")
        self.plugins = {}

    def initialize(self, auto_load: bool = True) -> int:
        """Initialize plugin system."""
        self.logger.info("Initializing plugin system")

        if auto_load:
            return self.loader.load_all_plugins()

        return 0

    def register_plugin(self, plugin: EntropyPlugin) -> bool:
        """
        Register a plugin instance directly.

        Args:
            plugin: Plugin instance to register

        Returns:
            True if successful
        """
        try:
            if plugin.initialize():
                plugin.initialized = True  # Set flag for tests
                self.plugins[plugin.name] = plugin
                self.loader.plugins[plugin.name] = plugin
                self.logger.info(f"Registered plugin: {plugin.name}")
                return True
        except Exception as e:
            self.logger.error(f"Failed to register plugin {plugin.name}: {e}")
        return False

    def unregister_plugin(self, name: str) -> bool:
        """
        Unregister a plugin.

        Args:
            name: Plugin name

        Returns:
            True if successful
        """
        if name in self.plugins:
            try:
                plugin = self.plugins[name]
                plugin.shutdown()
                plugin.deactivated = True
                del self.plugins[name]
                if name in self.loader.plugins:
                    del self.loader.plugins[name]
                self.logger.info(f"Unregistered plugin: {name}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to unregister plugin {name}: {e}")
        return False

    def broadcast_event(self, event_name: str, *args, **kwargs) -> None:
        """
        Broadcast an event to all plugins.

        Args:
            event_name: Name of the event
            *args: Positional arguments for the event
            **kwargs: Keyword arguments for the event
        """
        for name, plugin in self.plugins.items():
            if not plugin.enabled:
                continue

            try:
                method_name = f"on_{event_name}"
                if hasattr(plugin, method_name):
                    method = getattr(plugin, method_name)
                    method(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error broadcasting {event_name} to {name}: {e}")
                try:
                    if hasattr(plugin, "on_error"):
                        plugin.on_error(e, None)
                except:
                    pass  # Swallow plugin errors

    def broadcast_entropy_cycle(self, entropy_data: Dict) -> None:
        """
        Broadcast entropy cycle event to all plugins.

        Args:
            entropy_data: Dictionary with entropy measurements
        """
        self.broadcast_event("entropy_cycle", entropy_data)

    def broadcast_regulation(self, regulation_data: Dict) -> None:
        """
        Broadcast regulation event to all plugins.

        Args:
            regulation_data: Dictionary with regulation details
        """
        self.broadcast_event("regulation", regulation_data)

    def shutdown(self) -> None:
        """Shutdown all plugins."""
        self.logger.info("Shutting down plugin system")

        for name in list(self.loader.plugins.keys()):
            self.loader.unload_plugin(name)

    def trigger_entropy_measured(
        self, entropy_value: float, agents_state: List, metrics: Dict
    ) -> None:
        """Trigger on_entropy_measured hook for all plugins."""
        context = PluginContext(
            entropy_value=entropy_value,
            agents_state=agents_state,
            system_metrics=metrics,
            timestamp=metrics.get("timestamp", 0),
            brain_instance=self.brain,
        )

        for name, plugin in self.plugins.items():
            if not plugin.enabled:
                continue

            try:
                plugin.on_entropy_measured(context)
            except Exception as e:
                self.logger.error(f"Error in plugin {name}.on_entropy_measured: {e}")
                if not plugin.on_error(e, context):
                    raise

    def trigger_regulation_decision(
        self, context: PluginContext, decision: Dict
    ) -> Dict:
        """Trigger on_regulation_decision hook. Plugins can modify decision."""
        modified_decision = decision.copy()

        for name, plugin in self.plugins.items():
            if not plugin.enabled:
                continue

            try:
                modified_decision = plugin.on_regulation_decision(
                    context, modified_decision
                )
            except Exception as e:
                self.logger.error(f"Error in plugin {name}.on_regulation_decision: {e}")
                if not plugin.on_error(e, context):
                    raise

        return modified_decision

    def trigger_regulation_complete(self, context: PluginContext, result: Dict) -> None:
        """Trigger on_regulation_complete hook."""
        for name, plugin in self.plugins.items():
            if not plugin.enabled:
                continue

            try:
                plugin.on_regulation_complete(context, result)
            except Exception as e:
                self.logger.error(f"Error in plugin {name}.on_regulation_complete: {e}")
                if not plugin.on_error(e, context):
                    raise

    def load_plugin(self, name: str, config: Optional[Dict] = None) -> bool:
        """Load a specific plugin."""
        return self.loader.load_plugin(name, config)

    def unload_plugin(self, name: str) -> bool:
        """Unload a specific plugin."""
        return self.loader.unload_plugin(name)

    def list_plugins(self) -> List[PluginMetadata]:
        """List all loaded plugins."""
        return self.loader.get_loaded_plugins()

    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin."""
        if name in self.plugins:
            self.plugins[name].enabled = True
            return True
        return False

    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin."""
        if name in self.plugins:
            self.plugins[name].enabled = False
            return True
        return False
