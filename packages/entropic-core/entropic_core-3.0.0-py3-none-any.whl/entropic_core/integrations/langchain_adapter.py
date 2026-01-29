"""
LangChain Integration - Entropy monitoring for LangChain agents

Provides callback handlers for LangChain agent monitoring.
Now uses Universal LLM Middleware for interception.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Union

logger = logging.getLogger(__name__)


class LangChainEntropyHandler:
    """
    LangChain callback handler with entropy monitoring + active intervention

    Example:
        from langchain.agents import AgentExecutor
        from entropic_core.integrations import LangChainEntropyHandler

        handler = LangChainEntropyHandler(enable_intervention=True)

        agent = AgentExecutor(
            agent=agent_chain,
            tools=tools,
            callbacks=[handler]
        )

        # Entropy is monitored AND regulated automatically
        result = agent.run("Your query here")

        # Get analytics
        print(handler.get_analytics())
    """

    def __init__(self, brain=None, enable_intervention=True):
        """
        Initialize LangChain handler

        Args:
            brain: EntropyBrain instance
            enable_intervention: Enable REAL LLM interception
        """
        if brain is None:
            from entropic_core import EntropyBrain

            self.brain = EntropyBrain(enable_intervention=enable_intervention)
        else:
            self.brain = brain
            # Verificar si existe el atributo antes de acceder
            intervention_enabled = getattr(self.brain, "_intervention_enabled", False)
            if enable_intervention and not intervention_enabled:
                self.brain.enable_active_intervention()

        self.chain_runs = []
        self.tool_calls = []
        self.llm_calls = []
        self.active_runs = {}

        logger.info("LangChain entropy handler initialized with active intervention")

    def _extract_entropy_value(
        self, entropy_data: Union[float, Dict[str, Any]]
    ) -> float:
        """
        Helper para extraer el valor de entropía sin importar el formato.
        Evita el TypeError si el cerebro devuelve un float directamente.
        """
        if isinstance(entropy_data, dict):
            return float(entropy_data.get("combined", 0.0))
        return float(entropy_data)

    def wrap_llm(self, llm: Any) -> Any:
        """
        Wrap a LangChain LLM with entropy regulation

        Args:
            llm: LangChain LLM instance

        Returns:
            Wrapped LLM with active intervention
        """
        if hasattr(llm, "_generate"):
            original_generate = llm._generate
            llm._generate = self.brain.wrap_llm(original_generate)
            logger.info("Wrapped LangChain LLM with middleware")

        if hasattr(llm, "client"):
            # Wrap OpenAI/Anthropic client
            original_call = llm.client.create if hasattr(llm.client, "create") else None
            if original_call:
                llm.client.create = self.brain.wrap_llm(original_call)

        return llm

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs
    ) -> None:
        """Called when a chain starts running"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        run_id = kwargs.get("run_id", "unknown")

        run_info = {
            "type": "chain_start",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "chain_name": serialized.get("name", "unknown"),
            "inputs": inputs,
            "run_id": run_id,
        }

        self.chain_runs.append(run_info)
        self.active_runs[run_id] = run_info
        logger.debug(
            f"Chain started: {run_info['chain_name']}, entropy: {entropy_val:.3f}"
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when a chain ends"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        run_id = kwargs.get("run_id", "unknown")

        run_info = {
            "type": "chain_end",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "outputs": outputs,
            "run_id": run_id,
        }

        self.chain_runs.append(run_info)

        if run_id in self.active_runs:
            del self.active_runs[run_id]

        # Check for regulation
        if entropy_val > 0.8:
            logger.warning(f"High entropy after chain end: {entropy_val:.3f}")
            self.brain.regulate()

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs
    ) -> None:
        """Called when a tool starts"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        tool_info = {
            "type": "tool_start",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "tool_name": serialized.get("name", "unknown"),
            "input": input_str,
        }

        self.tool_calls.append(tool_info)

    def on_tool_end(self, output: str, **kwargs) -> None:
        """Called when a tool ends"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        tool_info = {
            "type": "tool_end",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "output": output,
        }

        self.tool_calls.append(tool_info)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs
    ) -> None:
        """Called when LLM starts"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        run_id = kwargs.get("run_id", "unknown")

        llm_info = {
            "type": "llm_start",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "num_prompts": len(prompts),
            "run_id": run_id,
        }

        self.llm_calls.append(llm_info)
        self.active_runs[run_id] = llm_info

    def on_llm_end(self, response: Any, **kwargs) -> None:
        """Called when LLM ends"""

        entropy_raw = self.brain.measure()
        entropy_val = self._extract_entropy_value(entropy_raw)

        run_id = kwargs.get("run_id", "unknown")

        llm_info = {
            "type": "llm_end",
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy_val,
            "run_id": run_id,
        }

        self.llm_calls.append(llm_info)

        if run_id in self.active_runs:
            del self.active_runs[run_id]

    def get_analytics(self) -> Dict[str, Any]:
        """Get entropy analytics for LangChain execution"""

        all_events = self.chain_runs + self.tool_calls + self.llm_calls

        if not all_events:
            return {"error": "No execution data"}

        import numpy as np

        entropy_values = [e["entropy"] for e in all_events]

        return {
            "total_events": len(all_events),
            "chain_runs": len(
                [e for e in self.chain_runs if e["type"] == "chain_start"]
            ),
            "tool_calls": len(
                [e for e in self.tool_calls if e["type"] == "tool_start"]
            ),
            "llm_calls": len([e for e in self.llm_calls if e["type"] == "llm_start"]),
            "avg_entropy": float(np.mean(entropy_values)),
            "max_entropy": float(np.max(entropy_values)),
            "min_entropy": float(np.min(entropy_values)),
            "entropy_trend": (
                "increasing" if entropy_values[-1] > entropy_values[0] else "decreasing"
            ),
            "system_stable": 0.3 <= np.mean(entropy_values) <= 0.7,
        }

    def generate_report(self) -> str:
        """Generate execution report"""

        analytics = self.get_analytics()

        if "error" in analytics:
            return "No execution data available"

        report = f"""
LangChain Execution Report
{'=' * 50}

Total Events: {analytics['total_events']}
- Chain Runs: {analytics['chain_runs']}
- Tool Calls: {analytics['tool_calls']}
- LLM Calls: {analytics['llm_calls']}

Entropy Metrics:
- Average: {analytics['avg_entropy']:.3f}
- Range: [{analytics['min_entropy']:.3f}, {analytics['max_entropy']:.3f}]
- Trend: {analytics['entropy_trend']}

System Status: {'STABLE' if analytics['system_stable'] else 'UNSTABLE'}
        """.strip()

        return report


LangChainEntropyCallback = LangChainEntropyHandler

__all__ = ["LangChainEntropyHandler", "LangChainEntropyCallback"]
