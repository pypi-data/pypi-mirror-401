"""
Comprehensive tests for streaming system
"""

import sys

import pytest

sys.path.insert(0, "scripts")

from entropic_core.streaming.event_emitter import EventEmitter


class MockBrain:
    """Mock brain for testing streaming"""

    def __init__(self):
        self.current_entropy = 0.5

    def get_current_entropy(self):
        return {"combined": self.current_entropy}


def test_event_emitter_subscribe():
    """Test event subscription"""
    emitter = EventEmitter()

    received = []

    def handler(data):
        received.append(data)

    emitter.on("test_event", handler)
    emitter.emit("test_event", {"value": 42})

    assert len(received) == 1
    assert received[0]["value"] == 42


def test_event_emitter_unsubscribe():
    """Test event unsubscription"""
    emitter = EventEmitter()

    received = []

    def handler(data):
        received.append(data)

    emitter.on("test_event", handler)
    emitter.off("test_event", handler)
    emitter.emit("test_event", {"value": 42})

    assert len(received) == 0


def test_event_emitter_multiple_handlers():
    """Test multiple handlers for same event"""
    emitter = EventEmitter()

    results = {"handler1": 0, "handler2": 0}

    def handler1(data):
        results["handler1"] += 1

    def handler2(data):
        results["handler2"] += 1

    emitter.on("test_event", handler1)
    emitter.on("test_event", handler2)
    emitter.emit("test_event", {})

    assert results["handler1"] == 1
    assert results["handler2"] == 1


def test_event_emitter_once():
    """Test one-time event handler"""
    emitter = EventEmitter()

    received = []

    def handler(data):
        received.append(data)

    emitter.once("test_event", handler)
    emitter.emit("test_event", {"first": True})
    emitter.emit("test_event", {"second": True})

    assert len(received) == 1
    assert received[0]["first"] == True


def test_event_emitter_wildcard():
    """Test wildcard event subscription"""
    emitter = EventEmitter()

    received = []

    def handler(data):
        received.append(data)

    emitter.on("*", handler)
    emitter.emit("event1", {"type": 1})
    emitter.emit("event2", {"type": 2})

    # Wildcard should receive all events
    assert len(received) >= 2


def test_event_emitter_error_handling():
    """Test error handling in event handlers"""
    emitter = EventEmitter()

    def bad_handler(data):
        raise ValueError("Intentional error")

    good_results = []

    def good_handler(data):
        good_results.append(data)

    emitter.on("test_event", bad_handler)
    emitter.on("test_event", good_handler)

    # Should not crash, good handler should still run
    emitter.emit("test_event", {"value": 1})

    # Good handler should have received the event
    assert len(good_results) == 1


def test_event_emitter_entropy_events():
    """Test entropy-specific events"""
    emitter = EventEmitter()

    entropy_events = []
    regulation_events = []
    alert_events = []

    emitter.on("entropy_update", lambda d: entropy_events.append(d))
    emitter.on("regulation", lambda d: regulation_events.append(d))
    emitter.on("alert", lambda d: alert_events.append(d))

    # Emit entropy update
    emitter.emit(
        "entropy_update", {"combined": 0.75, "decision": 0.8, "dispersion": 0.7}
    )

    # Emit regulation
    emitter.emit(
        "regulation", {"action": "REDUCE_CHAOS", "reason": "High entropy detected"}
    )

    # Emit alert
    emitter.emit(
        "alert", {"level": "warning", "message": "Entropy approaching critical"}
    )

    assert len(entropy_events) == 1
    assert len(regulation_events) == 1
    assert len(alert_events) == 1


def test_event_emitter_listener_count():
    """Test getting listener count"""
    emitter = EventEmitter()

    emitter.on("event1", lambda d: None)
    emitter.on("event1", lambda d: None)
    emitter.on("event2", lambda d: None)

    count1 = emitter.listener_count("event1")
    count2 = emitter.listener_count("event2")

    assert count1 == 2
    assert count2 == 1


def test_event_emitter_remove_all():
    """Test removing all listeners"""
    emitter = EventEmitter()

    emitter.on("event1", lambda d: None)
    emitter.on("event2", lambda d: None)

    emitter.remove_all_listeners("event1")

    assert emitter.listener_count("event1") == 0
    assert emitter.listener_count("event2") == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
