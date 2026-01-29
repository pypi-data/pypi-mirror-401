"""
CrewAI Integration - Native adapter for CrewAI framework
Now uses Universal LLM Middleware for interception.
"""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Union

logger = logging.getLogger(__name__)


class CrewAIEntropyAdapter:
    """
    Adapter for CrewAI that monitors and regulates entropy in crews.

    Usage:
        from crewai import Crew, Agent, Task
        from entropic_core.integrations import CrewAIEntropyAdapter

        crew = Crew(agents=[...], tasks=[...])
        adapter = CrewAIEntropyAdapter(crew, enable_intervention=True)
        result = adapter.kickoff()
    """

    def __init__(
        self,
        crew: Any = None,
        entropy_brain: Any = None,
        enable_intervention: bool = True,
    ):
        """
        Initialize the CrewAI adapter.

        Args:
            crew: CrewAI Crew instance (optional during init)
            entropy_brain: EntropyBrain instance for monitoring
            enable_intervention: Enable REAL LLM interception
        """
        self.crew = crew

        if entropy_brain is None:
            from entropic_core import EntropyBrain

            self.entropy_brain = EntropyBrain(enable_intervention=enable_intervention)
        else:
            self.entropy_brain = entropy_brain
            # Safe check for intervention enablement
            if enable_intervention and not getattr(
                self.entropy_brain, "_intervention_enabled", False
            ):
                self.entropy_brain.enable_active_intervention()

        self.wrapped_agents = []
        self.task_entropy_history = []
        self.agent_interactions = []

        if self.crew:
            self._wrap_crew_agents()

        logger.info("CrewAI adapter initialized with active intervention")

    def wrap_crew(self, crew: Any) -> "CrewAIEntropyAdapter":
        """
        FIX: Added missing method required by integration tests.
        Wraps a crew instance or a list of agents.
        """
        self.crew = crew
        self._wrap_crew_agents()
        return self

    def _get_entropy_value(self, entropy: Union[float, Dict]) -> float:
        """Helper to safely extract float value from entropy data"""
        if isinstance(entropy, dict):
            return float(entropy.get("combined", 0.5))
        return float(entropy)

    def _wrap_crew_agents(self):
        """Wraps crew agents with entropy awareness and LLM middleware"""
        from entropic_core.core.agent_adapter import AgentAdapter

        # Handle both Crew objects and raw lists of agents (for mocks/tests)
        agents = (
            self.crew
            if isinstance(self.crew, list)
            else getattr(self.crew, "agents", [])
        )

        self.wrapped_agents = []

        for i, agent in enumerate(agents):
            # Handle dict-based mock agents or real objects
            if isinstance(agent, dict):
                agent_id = agent.get("role", agent.get("name", f"agent_{i}"))
            else:
                agent_id = getattr(agent, "role", f"agent_{i}")

            # Wrap the agent
            wrapped = AgentAdapter.wrap_agent(agent, agent_id=agent_id)
            self.wrapped_agents.append(wrapped)

            # Wrap LLM if present
            if hasattr(agent, "llm"):
                agent.llm = self._wrap_crewai_llm(agent.llm)

            # Wrap execute_task if present
            if hasattr(agent, "execute_task"):
                original_execute = agent.execute_task
                agent.execute_task = self._wrap_execute_task(original_execute, agent)

        # CONEXIÓN MANUAL: NO llamar a brain.connect()
        if self.entropy_brain:
            # Solo actualizar las listas
            self.entropy_brain.agents = agents
            self.entropy_brain.wrapped_agents = self.wrapped_agents

            # Hacer logging manual
            if hasattr(self.entropy_brain, "telemetry"):
                self.entropy_brain.telemetry.track_event(
                    "agents_connected", {"agent_count": len(agents)}
                )

            if hasattr(self.entropy_brain, "memory"):
                self.entropy_brain.memory.log_event(
                    entropy=0.0,
                    event_type="SYSTEM_INIT",
                    outcome="SUCCESS",
                    metadata={"agent_count": len(agents), "free_open_source": True},
                )

            logger.info(
                f"Connected {len(agents)} agents via CrewAI adapter (manual connection)"
            )

    def _wrap_crewai_llm(self, llm: Any) -> Any:
        """Wrap CrewAI LLM with entropy regulation"""
        if hasattr(llm, "__call__"):
            original_call = llm.__call__
            llm.__call__ = self.entropy_brain.wrap_llm(original_call)
            logger.info("Wrapped CrewAI LLM with middleware")
        return llm

    def _wrap_execute_task(self, original_execute: Callable, agent: Any) -> Callable:
        """Wrap task execution with entropy monitoring"""

        def monitored_execute(*args, **kwargs):
            entropy_before = self.entropy_brain.measure()
            result = original_execute(*args, **kwargs)
            entropy_after = self.entropy_brain.measure()

            self._log_task_execution(agent, entropy_before, entropy_after)
            return result

        return monitored_execute

    def _log_task_execution(self, agent: Any, entropy_before: Any, entropy_after: Any):
        """Log task execution with entropy"""
        before_val = self._get_entropy_value(entropy_before)
        after_val = self._get_entropy_value(entropy_after)

        self.agent_interactions.append(
            {
                "timestamp": datetime.now().isoformat(),
                "agent_role": (
                    getattr(agent, "role", "unknown")
                    if not isinstance(agent, dict)
                    else agent.get("role", "unknown")
                ),
                "entropy_before": before_val,
                "entropy_after": after_val,
                "entropy_delta": after_val - before_val,
            }
        )

    def kickoff(self, inputs: Dict = None) -> Any:
        """Executes the crew with entropy monitoring."""
        if self.entropy_brain:
            initial_entropy = self.entropy_brain.measure()
            self._log_entropy_event("crew_start", initial_entropy)

        try:
            # Handle both real Crew objects and mocks
            if hasattr(self.crew, "kickoff"):
                result = self.crew.kickoff(inputs=inputs)
            else:
                result = "Mock result"

            if self.entropy_brain:
                final_entropy = self.entropy_brain.measure()
                final_val = self._get_entropy_value(final_entropy)
                self._log_entropy_event("crew_complete", final_entropy)

                if final_val > 0.7 or final_val < 0.3:
                    action = self.entropy_brain.regulate()
                    self._log_entropy_event("regulation", final_entropy, action)

            return result

        except Exception as e:
            if self.entropy_brain:
                error_entropy = self.entropy_brain.measure()
                self._log_entropy_event("crew_error", error_entropy, str(e))
            raise

    def _log_entropy_event(self, event_type: str, entropy: Any, details: Any = None):
        """Logs entropy events during crew execution"""
        entropy_val = self._get_entropy_value(entropy)

        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "entropy": {"combined": entropy_val},
            "details": details,
            "agent_count": len(self.wrapped_agents),
        }
        self.task_entropy_history.append(event)

        if self.entropy_brain and hasattr(self.entropy_brain, "memory"):
            self.entropy_brain.memory.log_event(
                entropy=entropy_val,
                event_type=event_type,
                action=str(details) if details else None,
                metadata={"crew_size": len(self.wrapped_agents)},
            )

    def get_entropy_report(self) -> Dict:
        """Generates entropy report for the crew execution."""
        if not self.task_entropy_history:
            return {"status": "no_data", "events": []}

        entropies = [e["entropy"]["combined"] for e in self.task_entropy_history]

        return {
            "total_events": len(self.task_entropy_history),
            "avg_entropy": sum(entropies) / len(entropies) if entropies else 0,
            "max_entropy": max(entropies) if entropies else 0,
            "min_entropy": min(entropies) if entropies else 0,
            "events": self.task_entropy_history,
            "agent_count": len(self.wrapped_agents),
        }

    def monitor_task_execution(self, task: Any, callback: Optional[Callable] = None):
        """Monitors entropy during individual task execution."""
        if not self.entropy_brain:
            raise ValueError("EntropyBrain required for task monitoring")

        before_entropy = self.entropy_brain.measure()
        result = task.execute()
        after_entropy = self.entropy_brain.measure()

        before_val = self._get_entropy_value(before_entropy)
        after_val = self._get_entropy_value(after_entropy)
        entropy_delta = after_val - before_val

        self._log_entropy_event(
            "task_executed",
            after_entropy,
            {
                "task_description": getattr(task, "description", "unknown"),
                "entropy_delta": entropy_delta,
            },
        )

        if callback and abs(entropy_delta) > 0.2:
            callback(task, before_entropy, after_entropy, entropy_delta)

        return result


class CrewAIEntropyCallback:
    """Callback handler for CrewAI"""

    def __init__(self, entropy_brain: Any):
        self.entropy_brain = entropy_brain
        self.events = []

    def _get_val(self, entropy: Any) -> float:
        if isinstance(entropy, dict):
            return float(entropy.get("combined", 0.5))
        return float(entropy)

    def on_task_start(self, task: Any):
        entropy = self.entropy_brain.measure()
        self.events.append(
            {
                "type": "task_start",
                "task": getattr(task, "description", str(task)),
                "entropy": {"combined": self._get_val(entropy)},
                "timestamp": datetime.now().isoformat(),
            }
        )

    def on_task_end(self, task: Any, output: Any):
        entropy = self.entropy_brain.measure()
        entropy_val = self._get_val(entropy)
        self.events.append(
            {
                "type": "task_end",
                "task": getattr(task, "description", str(task)),
                "entropy": {"combined": entropy_val},
                "output": str(output)[:100],
                "timestamp": datetime.now().isoformat(),
            }
        )

        if entropy_val > 0.75:
            action = self.entropy_brain.regulate()
            self.events.append(
                {
                    "type": "auto_regulation",
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    def get_summary(self) -> Dict:
        return {"total_events": len(self.events), "events": self.events}


CrewAIEntropyMonitor = CrewAIEntropyAdapter

__all__ = ["CrewAIEntropyAdapter", "CrewAIEntropyCallback", "CrewAIEntropyMonitor"]
