"""Event emitter for streaming events."""

import logging
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class StreamingEvent:
    """Event for streaming."""

    name: str
    data: Dict[str, Any]
    priority: int = 0


class EventEmitter:
    """Simple event emitter for streaming."""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("streaming.emitter")

    def on(self, event: str, callback: Callable) -> None:
        """Register event listener."""
        if event not in self.listeners:
            self.listeners[event] = []

        self.listeners[event].append(callback)
        self.logger.debug(f"Registered listener for event: {event}")

    def off(self, event: str, callback: Callable) -> None:
        """Unregister event listener."""
        if event in self.listeners:
            self.listeners[event] = [
                cb for cb in self.listeners[event] if cb != callback
            ]

    def emit(self, event: str, data: Dict[str, Any]) -> None:
        """Emit event to all listeners including wildcard"""
        # Emit to specific event listeners
        if event in self.listeners:
            for callback in self.listeners[event]:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"Error in event listener for {event}: {e}")

        # Emit to wildcard listeners
        if "*" in self.listeners:
            for callback in self.listeners["*"]:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"Error in wildcard listener: {e}")

    def once(self, event: str, callback: Callable) -> None:
        """Register one-time event listener."""

        def wrapper(data):
            callback(data)
            self.off(event, wrapper)

        self.on(event, wrapper)

    def listener_count(self, event: str) -> int:
        """Get count of listeners for an event"""
        return len(self.listeners.get(event, []))

    def remove_all_listeners(self, event: str = None) -> None:
        """Remove all listeners for an event or all events"""
        if event is None:
            self.listeners.clear()
        elif event in self.listeners:
            self.listeners[event].clear()
