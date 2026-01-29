"""Plugin loader for discovering and loading plugins."""

import importlib
import importlib.util
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .plugin_api import EntropyPlugin

logger = logging.getLogger(__name__)


@dataclass
class PluginMetadata:
    """Metadata about a loaded plugin."""

    name: str
    version: str
    description: str
    author: str
    file_path: str
    class_name: str
    enabled: bool = True


class PluginLoader:
    """Loads and manages plugins from directories."""

    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        self.plugin_dirs = plugin_dirs or self._default_plugin_dirs()
        self.plugins: Dict[str, EntropyPlugin] = {}
        self.metadata: Dict[str, PluginMetadata] = {}
        self.logger = logging.getLogger("plugin.loader")

    def _default_plugin_dirs(self) -> List[str]:
        """Get default plugin directories."""
        return [
            os.path.expanduser("~/.entropic/plugins"),
            os.path.join(os.path.dirname(__file__), "builtin"),
            "./plugins",
        ]

    def discover_plugins(self) -> List[PluginMetadata]:
        """Discover all available plugins."""
        discovered = []

        for plugin_dir in self.plugin_dirs:
            if not os.path.exists(plugin_dir):
                continue

            self.logger.info(f"Scanning for plugins in: {plugin_dir}")

            for file in Path(plugin_dir).glob("*.py"):
                if file.name.startswith("_"):
                    continue

                try:
                    metadata = self._load_plugin_metadata(str(file))
                    if metadata:
                        discovered.append(metadata)
                        self.logger.info(
                            f"Discovered plugin: {metadata.name} v{metadata.version}"
                        )
                except Exception as e:
                    self.logger.error(f"Error discovering plugin {file}: {e}")

        return discovered

    def _load_plugin_metadata(self, file_path: str) -> Optional[PluginMetadata]:
        """Load metadata from a plugin file without instantiating it."""
        spec = importlib.util.spec_from_file_location("temp_plugin", file_path)
        if not spec or not spec.loader:
            return None

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find EntropyPlugin subclass
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, EntropyPlugin)
                and attr is not EntropyPlugin
            ):

                # Create temporary instance to get metadata
                temp_instance = attr()

                return PluginMetadata(
                    name=temp_instance.name,
                    version=temp_instance.version,
                    description=temp_instance.description,
                    author=temp_instance.author,
                    file_path=file_path,
                    class_name=attr_name,
                )

        return None

    def load_plugin(self, name: str, config: Optional[Dict] = None) -> bool:
        """Load and initialize a specific plugin."""
        metadata = self.metadata.get(name)
        if not metadata:
            # Try to discover it
            discovered = self.discover_plugins()
            metadata = next((m for m in discovered if m.name == name), None)
            if not metadata:
                self.logger.error(f"Plugin not found: {name}")
                return False

        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(name, metadata.file_path)
            if not spec or not spec.loader:
                return False

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the plugin class
            plugin_class = getattr(module, metadata.class_name)

            # Instantiate and initialize
            plugin_instance = plugin_class(config)
            if plugin_instance.initialize():
                self.plugins[name] = plugin_instance
                self.metadata[name] = metadata
                self.logger.info(f"Loaded plugin: {name} v{metadata.version}")
                return True
            else:
                self.logger.error(f"Plugin initialization failed: {name}")
                return False

        except Exception as e:
            self.logger.error(f"Error loading plugin {name}: {e}")
            return False

    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin."""
        if name not in self.plugins:
            return False

        try:
            self.plugins[name].shutdown()
            del self.plugins[name]
            self.logger.info(f"Unloaded plugin: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Error unloading plugin {name}: {e}")
            return False

    def load_all_plugins(self, auto_enable: bool = True) -> int:
        """Load all discovered plugins."""
        discovered = self.discover_plugins()
        loaded_count = 0

        for metadata in discovered:
            if auto_enable or metadata.enabled:
                if self.load_plugin(metadata.name):
                    loaded_count += 1

        return loaded_count

    def get_loaded_plugins(self) -> List[PluginMetadata]:
        """Get list of currently loaded plugins."""
        return [self.metadata[name] for name in self.plugins.keys()]
