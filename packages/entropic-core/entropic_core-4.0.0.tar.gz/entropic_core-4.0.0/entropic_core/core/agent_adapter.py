"""
Agent Adapter - Universal wrapper for any agent architecture
"""

from typing import Any, Dict


class AgentAdapter:
    """Adapts any agent to work with Entropic Core"""

    @staticmethod
    def wrap_agent(base_agent: Any, agent_id: str = None):
        """
        Wraps any agent with entropy awareness
        Returns an enhanced version of the agent
        """

        class EntropicAgent:
            def __init__(self, wrapped_agent: Any, agent_id: str = None):
                self.wrapped = wrapped_agent
                self.agent_id = agent_id or f"agent_{id(wrapped_agent)}"
                self.entropy_context = None
                self.homeostasis_score = 1.0
                self.last_decision = None
                self.last_action = None
                self.current_state = 0
                self.messages = []

            def act(self, observation: Any, **kwargs) -> Any:
                """Enhanced act method with entropy awareness"""

                # Modify behavior based on entropy context
                if self.entropy_context:
                    observation = self._adjust_for_entropy(observation)

                # Call original act method if it exists
                if hasattr(self.wrapped, "act"):
                    result = self.wrapped.act(observation, **kwargs)
                elif hasattr(self.wrapped, "__call__"):
                    result = self.wrapped(observation, **kwargs)
                else:
                    result = observation

                # Store decision
                self.last_decision = result
                self.last_action = result

                return result

            def _adjust_for_entropy(self, observation: Any) -> Any:
                """Adjusts observation based on current entropy level"""
                chaos_level = self.entropy_context.get("chaos_level", 0.5)

                # High chaos - be more conservative
                if chaos_level > 0.7:
                    if hasattr(observation, "confidence_threshold"):
                        observation.confidence_threshold = 0.9
                    if hasattr(self.wrapped, "exploration_rate"):
                        self.wrapped.exploration_rate = 0.1

                # Low chaos - be more creative
                elif chaos_level < 0.3:
                    if hasattr(observation, "creativity_boost"):
                        observation.creativity_boost = 1.5
                    if hasattr(self.wrapped, "exploration_rate"):
                        self.wrapped.exploration_rate = 0.7

                return observation

            def set_entropy_context(self, context: Dict[str, Any]) -> None:
                """Updates entropy context"""
                self.entropy_context = context
                self.homeostasis_score = (
                    1.0 - abs(context.get("chaos_level", 0.5) - 0.5) * 2
                )

            def get_state(self) -> Dict[str, Any]:
                """Returns current agent state"""
                return {
                    "agent_id": self.agent_id,
                    "last_decision": self.last_decision,
                    "last_action": self.last_action,
                    "current_state": self.current_state,
                    "homeostasis_score": self.homeostasis_score,
                    "messages": self.messages,
                }

            def __getattr__(self, name: str) -> Any:
                """Delegates unknown attributes to wrapped agent"""
                return getattr(self.wrapped, name)

        return EntropicAgent(base_agent, agent_id)

    @staticmethod
    def create_mock_agent(agent_id: str = None, behavior: str = "balanced"):
        """Creates a mock agent for testing"""

        class MockAgent:
            def __init__(self, agent_id: str, behavior: str):
                self.agent_id = agent_id or f"mock_{id(self)}"
                self.behavior = behavior
                self.last_decision = None
                self.current_state = 0.5
                self.messages = []
                self.exploration_rate = 0.3

            def act(self, observation: Any) -> str:
                """Simple mock action"""
                import random

                if self.behavior == "chaotic":
                    decision = random.choice(["A", "B", "C", "D", "E"])
                elif self.behavior == "ordered":
                    decision = "A"  # Always same decision
                else:  # balanced
                    decision = random.choice(["A", "B", "C"])

                self.last_decision = decision
                self.messages.append(f"Decision: {decision}")

                return decision

        return MockAgent(agent_id, behavior)


class BaseAgent:
    """Base agent class for testing"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.last_decision = None
        self.last_action = None
        self.current_state = 0.5
        self.messages = []
        self.exploration_rate = 0.3

    def act(self, observation: Any) -> Any:
        """Basic act method"""
        import random

        decision = random.choice(["A", "B", "C"])
        self.last_decision = decision
        self.last_action = decision
        self.messages.append(f"Decision: {decision}")
        return decision

    def get_state(self) -> Dict[str, Any]:
        """Returns agent state"""
        return {
            "agent_id": self.agent_id,
            "last_decision": self.last_decision,
            "current_state": self.current_state,
            "messages": self.messages,
        }
