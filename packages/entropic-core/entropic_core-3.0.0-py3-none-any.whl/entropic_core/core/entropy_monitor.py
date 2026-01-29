"""
Entropy Monitor - Measures system entropy using multiple metrics
"""

from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

import numpy as np


class EntropyMonitor:
    """Monitors and measures entropy across multiple dimensions"""

    def __init__(self):
        self.metrics_history = []
        self.last_measurement = None
        self.max_history_size = 100

    def measure_system_entropy(self, agents_state: List[Any]) -> Dict[str, float]:
        """
        Calculates 3 core entropy metrics:
        1. Decision Entropy (Shannon)
        2. State Dispersion
        3. Communication Complexity
        """

        # Extract data from agents
        decisions = [self._extract_decision(agent) for agent in agents_state]
        states = [self._extract_state(agent) for agent in agents_state]
        messages = [self._extract_messages(agent) for agent in agents_state]

        # Calculate individual metrics
        decision_entropy = self._shannon_entropy(decisions)
        dispersion = self._calculate_dispersion(states)
        communication = self._communication_complexity(messages)

        # Combined entropy (weighted average)
        combined = decision_entropy * 0.4 + dispersion * 0.3 + communication * 0.3

        result = {
            "decision": decision_entropy,
            "dispersion": dispersion,
            "communication": communication,
            "combined": combined,
            "timestamp": datetime.now(),
        }

        self.metrics_history.append(result)
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size :]

        self.last_measurement = result

        return result

    def _shannon_entropy(self, decisions: List[Any]) -> float:
        """Calculates Shannon entropy of decisions"""
        if not decisions:
            return 0.0

        # Count occurrences
        counts = Counter(str(d) for d in decisions)
        total = len(decisions)

        # Calculate Shannon entropy
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)

        # Normalize to 0-1 range (assuming max entropy for uniform distribution)
        max_entropy = np.log2(len(counts)) if len(counts) > 1 else 1.0
        normalized = entropy / max_entropy if max_entropy > 0 else 0.0

        return min(normalized, 1.0)

    def _calculate_dispersion(self, states: List[Any]) -> float:
        """Calculates how dispersed agent states are"""
        if not states:
            return 0.0

        try:
            # Convert states to numeric values
            numeric_states = []
            for state in states:
                if isinstance(state, (int, float)):
                    numeric_states.append(float(state))
                elif hasattr(state, "__dict__"):
                    # Use hash of state dict as numeric representation
                    numeric_states.append(hash(str(state.__dict__)) % 1000 / 1000.0)
                else:
                    numeric_states.append(hash(str(state)) % 1000 / 1000.0)

            # Calculate standard deviation (normalized)
            if len(numeric_states) > 1:
                std_dev = np.std(numeric_states)
                # Normalize assuming states are in 0-1 range
                return min(std_dev * 2, 1.0)
            return 0.0

        except Exception:
            # Fallback to simple diversity measure
            unique_states = len(set(str(s) for s in states))
            return unique_states / len(states) if states else 0.0

    def _communication_complexity(self, messages: List[Any]) -> float:
        """Measures communication complexity/volume"""
        total_messages = sum(
            len(msg) if isinstance(msg, list) else 1 for msg in messages
        )

        # Normalize: 0 messages = 0 entropy, 100+ messages = 1.0 entropy
        normalized = min(total_messages / 100.0, 1.0)

        return normalized

    def _extract_decision(self, agent: Any) -> Any:
        """Extracts last decision from agent"""
        if hasattr(agent, "last_decision"):
            return agent.last_decision
        elif hasattr(agent, "last_action"):
            return agent.last_action
        return "unknown"

    def _extract_state(self, agent: Any) -> Any:
        """Extracts current state from agent"""
        if hasattr(agent, "current_state"):
            return agent.current_state
        elif hasattr(agent, "state"):
            return agent.state
        return 0

    def _extract_messages(self, agent: Any) -> List[Any]:
        """Extracts messages from agent"""
        if hasattr(agent, "messages"):
            return agent.messages
        elif hasattr(agent, "message_history"):
            return agent.message_history
        return []

    def get_history(self, last_n: int = None) -> List[Dict[str, float]]:
        """Returns entropy history"""
        if last_n:
            return self.metrics_history[-last_n:]
        return self.metrics_history

    def get_trend(self) -> str:
        """Analyzes recent trend in entropy"""
        if len(self.metrics_history) < 3:
            return "insufficient_data"

        recent = [m["combined"] for m in self.metrics_history[-5:]]

        if recent[-1] > recent[0] + 0.1:
            return "increasing"
        elif recent[-1] < recent[0] - 0.1:
            return "decreasing"
        else:
            return "stable"

    def measure_entropy(self, agents_state: List[Any]) -> float:
        """
        Measure entropy and return combined value as float (backward compatible)

        Args:
            agents_state: List of agent states

        Returns:
            Combined entropy value as float
        """
        metrics = self.measure_system_entropy(agents_state)
        return metrics["combined"]
