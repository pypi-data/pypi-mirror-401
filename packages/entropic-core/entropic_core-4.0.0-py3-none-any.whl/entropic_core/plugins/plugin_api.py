"""Plugin API for extending Entropic Core functionality."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class PluginContext:
    """Context passed to plugins during execution."""

    entropy_value: float
    agents_state: List[Any]
    system_metrics: Dict[str, Any]
    timestamp: float
    brain_instance: Any


class EntropyPlugin(ABC):
    """Base class for all Entropic Core plugins."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = True
        self.logger = logging.getLogger(f"plugin.{self.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin name."""

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""

    @property
    def description(self) -> str:
        """Plugin description."""
        return "No description provided"

    @property
    def author(self) -> str:
        """Plugin author."""
        return "Unknown"

    def initialize(self) -> bool:
        """Initialize plugin. Called once on load."""
        self.logger.info(f"Initializing plugin: {self.name} v{self.version}")
        return True

    def shutdown(self) -> None:
        """Cleanup plugin resources."""
        self.logger.info(f"Shutting down plugin: {self.name}")

    @abstractmethod
    def on_entropy_measured(self, context: PluginContext) -> None:
        """Called after entropy is measured."""

    def on_regulation_decision(self, context: PluginContext, decision: Dict) -> Dict:
        """Called before regulation decision is applied. Can modify decision."""
        return decision

    def on_regulation_complete(self, context: PluginContext, result: Dict) -> None:
        """Called after regulation is complete."""

    def on_agent_added(self, agent: Any) -> None:
        """Called when a new agent is added."""

    def on_agent_removed(self, agent: Any) -> None:
        """Called when an agent is removed."""

    def on_error(self, error: Exception, context: PluginContext) -> bool:
        """Called when an error occurs. Return True to suppress error."""
        return False


class PluginAPI:
    """API for plugins to interact with Entropic Core."""

    def __init__(self, brain_instance):
        self.brain = brain_instance
        self.logger = logging.getLogger("plugin.api")

    def get_current_entropy(self) -> float:
        """Get current system entropy."""
        return self.brain.current_entropy

    def get_entropy_history(self, limit: int = 100) -> List[Dict]:
        """Get historical entropy measurements."""
        return self.brain.monitor.metrics_history[-limit:]

    def get_agents_state(self) -> List[Any]:
        """Get current state of all agents."""
        return self.brain.agents

    def get_agents(self) -> List[Any]:
        """Get agents (alias for get_agents_state for backward compatibility)."""
        return self.get_agents_state()

    def force_regulation(self, action: str) -> Dict:
        """Force a specific regulation action."""
        self.logger.warning(f"Plugin forcing regulation action: {action}")
        return self.brain.regulator.regulate(
            self.brain.current_entropy, self.brain.agents
        )

    def log_event(self, event_type: str, data: Dict) -> None:
        """Log a custom event to memory."""
        self.brain.memory.log_decision(
            entropy=self.brain.current_entropy, action=event_type, result=str(data)
        )

    def send_alert(self, message: str, severity: str = "info") -> None:
        """Send an alert through the alert system."""
        if hasattr(self.brain, "alert_system"):
            self.brain.alert_system.send_alert(message, severity)

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.brain.config.get(key, default)

    def set_metric(self, name: str, value: Any) -> None:
        """Set a custom metric."""
        if not hasattr(self.brain, "custom_metrics"):
            self.brain.custom_metrics = {}
        self.brain.custom_metrics[name] = value
