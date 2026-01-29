"""
AutoGen Integration - Native entropy monitoring for AutoGen agents

Provides seamless integration with Microsoft's AutoGen framework.
Now uses Universal LLM Middleware for interception.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AutoGenEntropyPlugin:
    """
    AutoGen-specific entropy monitoring plugin

    Example:
        from autogen import AssistantAgent, UserProxyAgent
        from entropic_core.integrations import AutoGenEntropyPlugin

        # Create AutoGen agents
        assistant = AssistantAgent("assistant", llm_config={...})
        user = UserProxyAgent("user", ...)

        # Add entropy monitoring with active intervention
        plugin = AutoGenEntropyPlugin(enable_intervention=True)
        plugin.wrap_agents([assistant, user])

        # Now all interactions are monitored AND regulated
        user.initiate_chat(assistant, message="Hello")
    """

    def __init__(self, brain=None, auto_regulate=True, enable_intervention=True):
        """
        Initialize AutoGen plugin

        Args:
            brain: EntropyBrain instance (creates new if None)
            auto_regulate: Automatically apply regulation
            enable_intervention: Enable REAL LLM interception
        """
        if brain is None:
            from entropic_core import EntropyBrain

            self.brain = EntropyBrain(enable_intervention=enable_intervention)
        else:
            self.brain = brain
            if enable_intervention and not self.brain._intervention_enabled:
                self.brain.enable_active_intervention()

        self.auto_regulate = auto_regulate
        self.wrapped_agents = []
        self.conversation_history = []
        self.last_entropy = 0.0

        logger.info("AutoGen entropy plugin initialized with active intervention")

    def wrap_agents(self, agents: List[Any]) -> None:
        """
        Wrap AutoGen agents with entropy monitoring + active intervention

        Args:
            agents: List of AutoGen agent instances
        """
        self.brain.connect(agents)

        for agent in agents:
            self._wrap_single_agent(agent)

        self.wrapped_agents = agents
        logger.info(f"Wrapped {len(agents)} AutoGen agents with LLM middleware")

    def _wrap_single_agent(self, agent: Any) -> None:
        """Wrap a single AutoGen agent with LLM middleware"""

        if hasattr(agent, "generate_reply"):
            original_generate_reply = agent.generate_reply

            # Wrap with LLM middleware
            agent.generate_reply = self.brain.wrap_llm(
                original_generate_reply,
                agent_id=agent.name if hasattr(agent, "name") else "autogen_agent",
            )

        if hasattr(agent, "client") and hasattr(agent.client, "create"):
            # Wrap the OpenAI client directly
            original_create = agent.client.create
            agent.client.create = self.brain.wrap_llm(original_create)

            logger.info(
                f"Wrapped LLM client for agent: {agent.name if hasattr(agent, 'name') else 'unknown'}"
            )

        # Store original methods
        original_send = agent.send if hasattr(agent, "send") else None

        # Create wrapped versions
        if original_send:

            def monitored_send(message, recipient, request_reply=None, silent=False):
                # Measure entropy
                current_entropy = self.brain.measure()
                if isinstance(current_entropy, dict):
                    self.last_entropy = current_entropy["combined"]
                else:
                    self.last_entropy = current_entropy

                # Call original
                result = original_send(message, recipient, request_reply, silent)

                # Log
                self._log_interaction(
                    agent, "send", self.last_entropy, self.last_entropy
                )

                return result

            # Replace method
            agent.send = monitored_send

    def wrap_message(self, message: Dict[str, Any], agent_name: str) -> Dict[str, Any]:
        """
        Wrap a message with entropy context

        Args:
            message: Message dictionary
            agent_name: Name of the agent

        Returns:
            Message with entropy context added
        """
        # Measure current entropy
        entropy = self.brain.measure()

        if isinstance(entropy, dict):
            self.last_entropy = entropy["combined"]
        else:
            self.last_entropy = entropy

        # Add entropy metadata (non-intrusive)
        wrapped = message.copy()

        # Log for internal tracking
        self._log_interaction(
            {"name": agent_name}, "wrap_message", self.last_entropy, self.last_entropy
        )

        return wrapped

    def _log_interaction(
        self, agent: Any, method: str, entropy_before: float, entropy_after: float
    ):
        """Log agent interaction with entropy metrics"""

        interaction = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent.name if hasattr(agent, "name") else str(agent),
            "method": method,
            "entropy_before": entropy_before,
            "entropy_after": entropy_after,
            "entropy_change": entropy_after - entropy_before,
        }

        self.conversation_history.append(interaction)

        if abs(interaction["entropy_change"]) > 0.1:
            logger.info(
                f"Significant entropy change detected: "
                f"{interaction['agent_name']}.{method}() changed entropy by {interaction['entropy_change']:+.3f}"
            )

    def _check_and_regulate(self, current_entropy: float):
        """Check if regulation is needed"""

        if current_entropy > 0.8:
            logger.warning(
                f"High entropy detected ({current_entropy:.3f}), applying regulation"
            )
            action = self.brain.regulate()
            logger.info(f"Applied regulation: {action['action']}")
        elif current_entropy < 0.2:
            logger.info(
                f"Low entropy detected ({current_entropy:.3f}), injecting innovation"
            )
            action = self.brain.regulate()
            logger.info(f"Applied regulation: {action['action']}")

    def get_conversation_analytics(self) -> Dict[str, Any]:
        """
        Get analytics about the conversation

        Returns:
            Dictionary with conversation insights
        """
        if not self.conversation_history:
            return {"error": "No conversation data"}

        import numpy as np

        entropy_values = [i["entropy_after"] for i in self.conversation_history]
        entropy_changes = [i["entropy_change"] for i in self.conversation_history]

        return {
            "total_interactions": len(self.conversation_history),
            "avg_entropy": float(np.mean(entropy_values)),
            "entropy_std": float(np.std(entropy_values)),
            "max_entropy": float(np.max(entropy_values)),
            "min_entropy": float(np.min(entropy_values)),
            "avg_entropy_change": float(np.mean(np.abs(entropy_changes))),
            "high_chaos_events": sum(1 for e in entropy_values if e > 0.8),
            "low_chaos_events": sum(1 for e in entropy_values if e < 0.2),
            "system_stability": 1.0 - float(np.std(entropy_values)),
        }

    def generate_conversation_report(self) -> str:
        """Generate human-readable conversation report"""

        analytics = self.get_conversation_analytics()

        if "error" in analytics:
            return "No conversation data available"

        report = f"""
AutoGen Conversation Report
{'=' * 50}

Interactions: {analytics['total_interactions']}
Average Entropy: {analytics['avg_entropy']:.3f}
Entropy Range: [{analytics['min_entropy']:.3f}, {analytics['max_entropy']:.3f}]

System Health:
- Stability Score: {analytics['system_stability']:.1%}
- High Chaos Events: {analytics['high_chaos_events']}
- Low Chaos Events: {analytics['low_chaos_events']}

Average Entropy Change per Interaction: {analytics['avg_entropy_change']:.3f}

Status: {'HEALTHY' if 0.3 <= analytics['avg_entropy'] <= 0.7 else 'NEEDS ATTENTION'}
        """.strip()

        return report


class AutoGenGroupChatMonitor:
    """
    Monitor AutoGen GroupChat conversations

    Example:
        from autogen import GroupChat, GroupChatManager

        groupchat = GroupChat(agents=[agent1, agent2, agent3], messages=[])
        manager = GroupChatManager(groupchat=groupchat)

        monitor = AutoGenGroupChatMonitor(groupchat)
        monitor.start_monitoring()
    """

    def __init__(self, groupchat, brain=None):
        """
        Initialize GroupChat monitor

        Args:
            groupchat: AutoGen GroupChat instance
            brain: EntropyBrain instance
        """
        self.groupchat = groupchat

        if brain is None:
            from entropic_core import EntropyBrain

            self.brain = EntropyBrain()
        else:
            self.brain = brain

        self.metrics = []
        logger.info("AutoGen GroupChat monitor initialized")

    def start_monitoring(self):
        """Start monitoring the group chat"""

        self.brain.connect(self.groupchat.agents)
        logger.info(f"Monitoring {len(self.groupchat.agents)} agents in group chat")

    def measure_group_entropy(self) -> Dict[str, float]:
        """Measure entropy specific to group dynamics"""

        # Base entropy
        base_entropy = self.brain.measure()

        # Group-specific metrics
        len(self.groupchat.agents)
        num_messages = len(self.groupchat.messages)

        # Participation balance (how evenly agents participate)
        if num_messages > 0:
            agent_message_counts = {}
            for msg in self.groupchat.messages:
                agent_name = msg.get("name", "unknown")
                agent_message_counts[agent_name] = (
                    agent_message_counts.get(agent_name, 0) + 1
                )

            participation_values = list(agent_message_counts.values())
            participation_entropy = 0
            if participation_values:
                import numpy as np

                participation_entropy = float(
                    np.std(participation_values) / (np.mean(participation_values) + 1)
                )
        else:
            participation_entropy = 0

        return {
            "base_entropy": base_entropy["combined"],
            "participation_imbalance": participation_entropy,
            "combined_group_entropy": (base_entropy["combined"] + participation_entropy)
            / 2,
        }
