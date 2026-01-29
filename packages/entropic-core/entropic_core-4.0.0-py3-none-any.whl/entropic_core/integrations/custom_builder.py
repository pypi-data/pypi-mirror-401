"""
Custom Adapter Builder - Create adapters for any framework

Provides a builder pattern for creating custom entropy adapters.
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)


class CustomAdapterBuilder:
    """
    Builder for creating custom entropy monitoring adapters

    Example:
        builder = CustomAdapterBuilder()

        adapter = (builder
            .set_brain(my_brain)
            .add_hook('before_action', lambda agent: print(f"Acting: {agent}"))
            .add_hook('after_action', lambda agent, result: log_result(result))
            .add_metric('custom_metric', lambda state: calculate_metric(state))
            .build())

        # Use adapter
        adapter.wrap_agent(my_custom_agent)
    """

    def __init__(self):
        """Initialize builder"""
        self.brain = None
        self.hooks = {
            "before_action": [],
            "after_action": [],
            "on_communicate": [],
            "on_error": [],
        }
        self.custom_metrics = {}
        self.config = {}
        self.state_extractor = None
        self.decision_extractor = None
        self.message_counter = None

        logger.info("Custom adapter builder initialized")

    def set_brain(self, brain):
        """Set the EntropyBrain instance"""
        self.brain = brain
        return self

    def add_hook(self, hook_name: str, callback: Callable) -> "CustomAdapterBuilder":
        """
        Add a callback hook

        Args:
            hook_name: Name of hook (before_action, after_action, etc.)
            callback: Function to call at hook point

        Returns:
            Self for chaining
        """
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []

        self.hooks[hook_name].append(callback)
        logger.debug(f"Added hook: {hook_name}")
        return self

    def add_metric(
        self, metric_name: str, calculator: Callable
    ) -> "CustomAdapterBuilder":
        """
        Add custom entropy metric

        Args:
            metric_name: Name of the metric
            calculator: Function that calculates the metric

        Returns:
            Self for chaining
        """
        self.custom_metrics[metric_name] = calculator
        logger.debug(f"Added custom metric: {metric_name}")
        return self

    def set_config(self, key: str, value: Any) -> "CustomAdapterBuilder":
        """
        Set configuration option

        Args:
            key: Configuration key
            value: Configuration value

        Returns:
            Self for chaining
        """
        self.config[key] = value
        return self

    def register_state_extractor(self, extractor: Callable) -> "CustomAdapterBuilder":
        """
        Register custom state extractor

        Args:
            extractor: Function that extracts state from agent

        Returns:
            Self for chaining
        """
        self.state_extractor = extractor
        return self

    def register_decision_extractor(
        self, extractor: Callable
    ) -> "CustomAdapterBuilder":
        """Register custom decision extractor"""
        self.decision_extractor = extractor
        return self

    def register_message_counter(self, counter: Callable) -> "CustomAdapterBuilder":
        """Register custom message counter"""
        self.message_counter = counter
        return self

    def extract_state(self, agent: Any) -> Any:
        """Extract state using registered extractor"""
        if hasattr(self, "state_extractor"):
            return self.state_extractor(agent)
        return {}

    def extract_decision(self, agent: Any) -> Any:
        """Extract decision using registered extractor"""
        if hasattr(self, "decision_extractor"):
            return self.decision_extractor(agent)
        return "unknown"

    def count_messages(self, agent: Any) -> int:
        """Count messages using registered counter"""
        if hasattr(self, "message_counter"):
            return self.message_counter(agent)
        return 0

    def build(self) -> "CustomAdapter":
        """
        Build the custom adapter

        Returns:
            CustomAdapter instance
        """
        if self.brain is None:
            from entropic_core import EntropyBrain

            self.brain = EntropyBrain()

        adapter = CustomAdapter(
            brain=self.brain,
            hooks=self.hooks,
            custom_metrics=self.custom_metrics,
            config=self.config,
            state_extractor=self.state_extractor,
            decision_extractor=self.decision_extractor,
            message_counter=self.message_counter,
        )

        logger.info("Custom adapter built successfully")
        return adapter


class CustomAdapter:
    """
    Custom entropy monitoring adapter

    Created by CustomAdapterBuilder
    """

    def __init__(
        self,
        brain,
        hooks,
        custom_metrics,
        config,
        state_extractor=None,
        decision_extractor=None,
        message_counter=None,
    ):
        """Initialize custom adapter"""
        self.brain = brain
        self.hooks = hooks
        self.custom_metrics = custom_metrics
        self.config = config
        self.wrapped_agents = []
        self.event_log = []
        self.state_extractor = state_extractor
        self.decision_extractor = decision_extractor
        self.message_counter = message_counter

        logger.info("Custom adapter initialized")

    def wrap_agent(self, agent: Any) -> Any:
        """
        Wrap an agent with entropy monitoring

        Args:
            agent: Agent instance to wrap

        Returns:
            Wrapped agent
        """
        original_methods = {}

        # Find methods to wrap
        method_names = self.config.get("methods_to_wrap", ["act", "step", "run"])

        for method_name in method_names:
            if hasattr(agent, method_name):
                original_methods[method_name] = getattr(agent, method_name)

                # Create wrapped version
                wrapped_method = self._create_wrapped_method(
                    agent, method_name, original_methods[method_name]
                )

                setattr(agent, method_name, wrapped_method)
                logger.debug(f"Wrapped method: {method_name}")

        self.wrapped_agents.append(agent)
        self.brain.connect([agent])

        return agent

    def _create_wrapped_method(
        self, agent: Any, method_name: str, original_method: Callable
    ) -> Callable:
        """Create a wrapped version of a method"""

        def wrapped(*args, **kwargs):
            # Execute before hooks
            for hook in self.hooks["before_action"]:
                try:
                    hook(agent)
                except Exception as e:
                    logger.error(f"Before hook error: {e}")

            # Measure entropy before
            entropy_before = self.brain.measure()

            # Calculate custom metrics before
            metrics_before = {}
            for metric_name, calculator in self.custom_metrics.items():
                try:
                    metrics_before[metric_name] = calculator(agent)
                except Exception as e:
                    logger.error(f"Metric calculation error ({metric_name}): {e}")

            # Extract state before
            state_before = self.extract_state(agent)

            # Extract decision before
            decision_before = self.extract_decision(agent)

            # Count messages before
            messages_before = self.count_messages(agent)

            # Execute original method
            try:
                result = original_method(*args, **kwargs)
                error = None
            except Exception as e:
                result = None
                error = e

                # Execute error hooks
                for hook in self.hooks["on_error"]:
                    try:
                        hook(agent, e)
                    except Exception as hook_error:
                        logger.error(f"Error hook error: {hook_error}")

                raise e

            # Measure entropy after
            entropy_after = self.brain.measure()

            # Calculate custom metrics after
            metrics_after = {}
            for metric_name, calculator in self.custom_metrics.items():
                try:
                    metrics_after[metric_name] = calculator(agent)
                except Exception as e:
                    logger.error(f"Metric calculation error ({metric_name}): {e}")

            # Extract state after
            state_after = self.extract_state(agent)

            # Extract decision after
            decision_after = self.extract_decision(agent)

            # Count messages after
            messages_after = self.count_messages(agent)

            # Log event
            event = {
                "timestamp": datetime.now().isoformat(),
                "agent": str(agent),
                "method": method_name,
                "entropy_before": entropy_before,
                "entropy_after": entropy_after,
                "entropy_change": entropy_after - entropy_before,
                "metrics_before": metrics_before,
                "metrics_after": metrics_after,
                "state_before": state_before,
                "state_after": state_after,
                "decision_before": decision_before,
                "decision_after": decision_after,
                "messages_before": messages_before,
                "messages_after": messages_after,
                "error": str(error) if error else None,
            }
            self.event_log.append(event)

            # Execute after hooks
            for hook in self.hooks["after_action"]:
                try:
                    hook(agent, result)
                except Exception as e:
                    logger.error(f"After hook error: {e}")

            return result

        return wrapped

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics from wrapped agents"""

        if not self.event_log:
            return {"error": "No event data"}

        import numpy as np

        entropy_values = [e["entropy_after"] for e in self.event_log]
        entropy_changes = [e["entropy_change"] for e in self.event_log]

        analytics = {
            "total_events": len(self.event_log),
            "wrapped_agents": len(self.wrapped_agents),
            "avg_entropy": float(np.mean(entropy_values)),
            "max_entropy": float(np.max(entropy_values)),
            "min_entropy": float(np.min(entropy_values)),
            "avg_entropy_change": float(np.mean(np.abs(entropy_changes))),
            "errors": sum(1 for e in self.event_log if e["error"] is not None),
        }

        # Add custom metric analytics
        for metric_name in self.custom_metrics.keys():
            metric_values = []
            for event in self.event_log:
                if metric_name in event["metrics_after"]:
                    metric_values.append(event["metrics_after"][metric_name])

            if metric_values:
                analytics[f"{metric_name}_avg"] = float(np.mean(metric_values))
                analytics[f"{metric_name}_max"] = float(np.max(metric_values))

        # Add state analytics
        if self.state_extractor:
            state_changes = []
            for event in self.event_log:
                if event["state_before"] != event["state_after"]:
                    state_changes.append(1)
                else:
                    state_changes.append(0)

            analytics["state_changes"] = sum(state_changes)

        # Add decision analytics
        if self.decision_extractor:
            decision_changes = []
            for event in self.event_log:
                if event["decision_before"] != event["decision_after"]:
                    decision_changes.append(1)
                else:
                    decision_changes.append(0)

            analytics["decision_changes"] = sum(decision_changes)

        # Add message analytics
        if self.message_counter:
            message_deltas = []
            for event in self.event_log:
                message_deltas.append(
                    event["messages_after"] - event["messages_before"]
                )

            analytics["avg_message_delta"] = float(np.mean(message_deltas))
            analytics["max_message_delta"] = float(np.max(message_deltas))

        return analytics

    def extract_state(self, agent: Any) -> Any:
        """Extract state from agent using registered extractor."""
        if self.state_extractor:
            return self.state_extractor(agent)
        return {}

    def extract_decision(self, agent: Any) -> Any:
        """Extract decision from agent using registered extractor."""
        if self.decision_extractor:
            return self.decision_extractor(agent)
        return "unknown"

    def count_messages(self, agent: Any) -> int:
        """Count messages from agent using registered counter."""
        if self.message_counter:
            return self.message_counter(agent)
        return 0
