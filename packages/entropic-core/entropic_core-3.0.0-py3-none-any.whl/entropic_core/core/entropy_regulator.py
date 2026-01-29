"""
Entropy Regulator - Takes action based on entropy measurements
"""

from typing import Any, Dict, List


class EntropyRegulator:
    """Regulates system behavior based on entropy levels"""

    def __init__(self, config: Dict[str, float] = None):
        self.thresholds = config or {
            "max_entropy": 0.8,  # Too much chaos
            "min_entropy": 0.2,  # Too much order
            "optimal_min": 0.4,  # Lower bound of optimal range
            "optimal_max": 0.6,  # Upper bound of optimal range
        }
        self.regulation_history = []

    def regulate(self, current_entropy: float, agents: List[Any]) -> Dict[str, Any]:
        """
        Determines action based on current entropy level
        Returns regulation command with detailed instructions
        """

        action_result = None

        if current_entropy > self.thresholds["max_entropy"]:
            # System is too chaotic - stabilize
            action_result = {
                "action": "REDUCE_CHAOS",
                "severity": "high" if current_entropy > 0.9 else "medium",
                "commands": [
                    "merge_similar_agents",
                    "increase_validation_steps",
                    "enforce_stricter_protocols",
                    "reduce_exploration_rate",
                ],
                "message": f"System too chaotic (entropy: {current_entropy:.2f}). Stabilizing...",
                "parameters": {
                    "validation_threshold": 0.9,
                    "merge_similarity_threshold": 0.8,
                    "exploration_rate": 0.1,
                },
            }

        elif current_entropy < self.thresholds["min_entropy"]:
            # System is too ordered - innovate
            action_result = {
                "action": "INCREASE_CHAOS",
                "severity": "high" if current_entropy < 0.1 else "medium",
                "commands": [
                    "create_explorer_agent",
                    "inject_random_perturbation",
                    "relax_constraints",
                    "increase_diversity",
                ],
                "message": f"System stagnant (entropy: {current_entropy:.2f}). Injecting innovation...",
                "parameters": {
                    "explorer_count": 1,
                    "perturbation_strength": 0.3,
                    "exploration_rate": 0.5,
                },
            }

        else:
            # System in optimal range - maintain
            action_result = {
                "action": "MAINTAIN",
                "severity": "low",
                "commands": ["fine_tune_parameters"],
                "message": f"System in homeostasis (entropy: {current_entropy:.2f}). Maintaining...",
                "parameters": {"adjustment_factor": 0.05},
            }

        # Add metadata
        action_result["entropy_value"] = current_entropy
        action_result["agent_count"] = len(agents)
        action_result["thresholds"] = self.thresholds

        self.regulation_history.append(action_result)

        return action_result

    def apply_regulation(self, agents: List[Any], regulation: Dict[str, Any]) -> None:
        """
        Applies regulation commands to agents
        This is a hook for actual implementation
        """
        action = regulation["action"]

        if action == "REDUCE_CHAOS":
            self._reduce_chaos(agents, regulation["parameters"])
        elif action == "INCREASE_CHAOS":
            self._increase_chaos(agents, regulation["parameters"])
        elif action == "MAINTAIN":
            self._maintain_homeostasis(agents, regulation["parameters"])

    def _reduce_chaos(self, agents: List[Any], params: Dict[str, Any]) -> None:
        """Reduces system chaos"""
        for agent in agents:
            if hasattr(agent, "exploration_rate"):
                agent.exploration_rate = params.get("exploration_rate", 0.1)
            if hasattr(agent, "validation_threshold"):
                agent.validation_threshold = params.get("validation_threshold", 0.9)

    def _increase_chaos(self, agents: List[Any], params: Dict[str, Any]) -> None:
        """Increases system exploration"""
        for agent in agents:
            if hasattr(agent, "exploration_rate"):
                agent.exploration_rate = params.get("exploration_rate", 0.5)
            if hasattr(agent, "creativity_factor"):
                agent.creativity_factor = params.get("perturbation_strength", 0.3)

    def _maintain_homeostasis(self, agents: List[Any], params: Dict[str, Any]) -> None:
        """Fine-tunes system in optimal range"""
        adjustment = params.get("adjustment_factor", 0.05)
        for agent in agents:
            if hasattr(agent, "learning_rate"):
                agent.learning_rate *= 1 + adjustment

    def get_regulation_history(self, last_n: int = None) -> List[Dict[str, Any]]:
        """Returns regulation history"""
        if last_n:
            return self.regulation_history[-last_n:]
        return self.regulation_history

    def update_thresholds(self, new_thresholds: Dict[str, float]) -> None:
        """Updates regulation thresholds"""
        self.thresholds.update(new_thresholds)
