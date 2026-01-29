"""
Simulation Engine - "What if?" scenarios for entropy-based systems

Allows testing system configurations before deployment:
- Add/remove agents
- Change thresholds
- Test load scenarios
- Find breaking points
"""

import copy
import logging
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class SimulationEngine:
    """
    Monte Carlo simulation engine for entropy systems

    Example:
        simulator = SimulationEngine(brain)
        result = simulator.simulate_scenario(
            scenario={'add_agents': 10},
            steps=100
        )
        if result['system_stable']:
            print(f"System can handle {result['max_agents_supported']} agents")
    """

    def __init__(self, brain_instance, memory_instance=None):
        """
        Initialize simulator with reference brain

        Args:
            brain_instance: EntropyBrain instance to simulate from
            memory_instance: Optional EvolutionaryMemory instance (for backward compatibility)
        """
        self.brain = brain_instance
        self.memory = memory_instance  # Store but not required
        self.simulation_history = []
        logger.info("Simulation engine initialized")

    def simulate_scenario(
        self, scenario: Dict[str, Any], steps: int = 100, monte_carlo_runs: int = 1
    ) -> Dict[str, Any]:
        """
        Simulate a scenario for N steps

        Args:
            scenario: Dictionary describing the scenario
                - 'add_agents': int - Number of agents to add
                - 'remove_agents': int - Number of agents to remove
                - 'change_threshold': float - New entropy threshold
                - 'inject_chaos': float - Amount of chaos to inject (0-1)
                - 'increase_load': float - Multiplier for system load
            steps: Number of simulation steps
            monte_carlo_runs: Number of times to run simulation (for averaging)

        Returns:
            Dictionary with simulation results
        """
        logger.info(f"Simulating scenario: {scenario} for {steps} steps")

        all_runs = []

        for run in range(monte_carlo_runs):
            run_result = self._run_single_simulation(scenario, steps)
            all_runs.append(run_result)

        # Aggregate results
        avg_entropy = np.mean([r["avg_entropy"] for r in all_runs])
        max_entropy = np.max([r["max_entropy"] for r in all_runs])
        collapse_rate = sum(1 for r in all_runs if r["collapsed"]) / monte_carlo_runs

        result = {
            "scenario": scenario,
            "steps_simulated": steps,
            "monte_carlo_runs": monte_carlo_runs,
            "system_stable": collapse_rate < 0.1,
            "collapse_probability": collapse_rate,
            "avg_entropy": avg_entropy,
            "max_entropy": max_entropy,
            "recommended_configuration": self._generate_recommendation(all_runs),
            "performance_metrics": self._calculate_performance(all_runs),
            "bottleneck_analysis": self._identify_bottleneck(all_runs),
            "timestamp": datetime.now().isoformat(),
        }

        # Add collapse/capacity information
        if collapse_rate > 0:
            # Find earliest collapse step across all runs
            collapse_steps = [
                r["collapse_step"]
                for r in all_runs
                if r["collapsed"] and r["collapse_step"]
            ]
            if collapse_steps:
                result["system_collapses_at_step"] = int(np.min(collapse_steps))
        else:
            # If adding agents, estimate max capacity
            if "add_agents" in scenario or "action" in scenario:
                current_agents = (
                    len(self.brain.agents) if hasattr(self.brain, "agents") else 3
                )
                added_agents = scenario.get("count", scenario.get("add_agents", 0))
                total_agents = current_agents + added_agents

                # Estimate max based on stability
                if result["system_stable"]:
                    # System is stable, could likely handle more
                    estimated_max = int(total_agents * 1.5)
                    result["max_agents_supported"] = estimated_max

        self.simulation_history.append(result)
        logger.info(f"Simulation complete. Stable: {result['system_stable']}")

        return result

    def _run_single_simulation(
        self, scenario: Dict[str, Any], steps: int
    ) -> Dict[str, Any]:
        """Run a single simulation iteration"""

        # Create simulated state
        simulated_state = self._create_simulated_state(scenario)

        entropy_history = []
        collapsed = False
        collapse_step = None

        for step in range(steps):
            # Calculate entropy for current state
            entropy = self._calculate_simulated_entropy(simulated_state, step)
            entropy_history.append(entropy)

            # Check for collapse
            if entropy > 0.95:
                collapsed = True
                collapse_step = step
                break

            # Update state for next step
            simulated_state = self._update_simulated_state(simulated_state, entropy)

        return {
            "entropy_history": entropy_history,
            "avg_entropy": np.mean(entropy_history),
            "max_entropy": np.max(entropy_history),
            "collapsed": collapsed,
            "collapse_step": collapse_step,
            "final_state": simulated_state,
        }

    def _create_simulated_state(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Create initial simulated state from scenario"""

        # Start with current brain state
        base_agents = len(self.brain.agents) if hasattr(self.brain, "agents") else 3

        state = {
            "num_agents": base_agents,
            "entropy_threshold": self.brain.regulator.thresholds["max_entropy"],
            "chaos_level": 0.5,
            "load_multiplier": 1.0,
            "communication_complexity": 0.5,
        }

        # Apply scenario modifications
        if "add_agents" in scenario:
            state["num_agents"] += scenario["add_agents"]

        if "remove_agents" in scenario:
            state["num_agents"] = max(
                1, state["num_agents"] - scenario["remove_agents"]
            )

        if "change_threshold" in scenario:
            state["entropy_threshold"] = scenario["change_threshold"]

        if "inject_chaos" in scenario:
            state["chaos_level"] = min(
                1.0, state["chaos_level"] + scenario["inject_chaos"]
            )

        if "increase_load" in scenario:
            state["load_multiplier"] = scenario["increase_load"]

        return state

    def _calculate_simulated_entropy(self, state: Dict[str, Any], step: int) -> float:
        """Calculate entropy for simulated state"""

        # Base entropy from agent count (more agents = more potential entropy)
        agent_entropy = min(0.5, state["num_agents"] / 100)

        # Add chaos level
        chaos_component = state["chaos_level"] * 0.3

        # Communication complexity scales with agents
        comm_complexity = min(0.3, (state["num_agents"] ** 1.5) / 1000)

        # Load multiplier effect
        load_effect = (state["load_multiplier"] - 1.0) * 0.2

        # Add some randomness to simulate real-world variation
        noise = np.random.normal(0, 0.05)

        # Add temporal dynamics (oscillations)
        temporal = 0.1 * np.sin(step / 10)

        total_entropy = (
            agent_entropy
            + chaos_component
            + comm_complexity
            + load_effect
            + noise
            + temporal
        )

        return np.clip(total_entropy, 0.0, 1.0)

    def _update_simulated_state(
        self, state: Dict[str, Any], current_entropy: float
    ) -> Dict[str, Any]:
        """Update state based on current entropy (homeostasis simulation)"""

        new_state = copy.deepcopy(state)

        # Simulate regulatory response
        if current_entropy > state["entropy_threshold"]:
            # System would reduce chaos
            new_state["chaos_level"] *= 0.95
            new_state["communication_complexity"] *= 0.98
        elif current_entropy < 0.3:
            # System would increase chaos
            new_state["chaos_level"] *= 1.02

        return new_state

    def _generate_recommendation(self, runs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate configuration recommendations based on simulation results"""

        stable_runs = [r for r in runs if not r["collapsed"]]

        if not stable_runs:
            return {
                "recommendation": "REDUCE_SCALE",
                "reason": "System collapses in all scenarios",
                "suggested_actions": [
                    "Reduce number of agents",
                    "Increase entropy thresholds",
                    "Add more regulatory controls",
                ],
            }

        avg_entropy = np.mean([r["avg_entropy"] for r in stable_runs])

        if avg_entropy < 0.3:
            return {
                "recommendation": "INCREASE_INNOVATION",
                "reason": "System too stable, may stagnate",
                "suggested_actions": [
                    "Add explorer agents",
                    "Relax constraints",
                    "Inject controlled chaos",
                ],
            }
        elif avg_entropy > 0.7:
            return {
                "recommendation": "INCREASE_STABILITY",
                "reason": "System operates at high entropy",
                "suggested_actions": [
                    "Strengthen protocols",
                    "Reduce agent autonomy",
                    "Increase validation steps",
                ],
            }
        else:
            return {
                "recommendation": "OPTIMAL",
                "reason": "System operates in optimal range",
                "suggested_actions": ["Maintain current configuration"],
            }

    def _calculate_performance(self, runs: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate performance metrics from simulation runs"""

        return {
            "stability_score": sum(1 for r in runs if not r["collapsed"]) / len(runs),
            "avg_entropy": np.mean([r["avg_entropy"] for r in runs]),
            "entropy_variance": np.var([r["avg_entropy"] for r in runs]),
            "efficiency": 1.0 - np.mean([r["max_entropy"] for r in runs]),
        }

    def _identify_bottleneck(self, runs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify system bottlenecks from simulation"""

        collapsed_runs = [r for r in runs if r["collapsed"]]

        if not collapsed_runs:
            return {"bottleneck": "NONE", "description": "No bottlenecks detected"}

        collapse_steps = [
            r["collapse_step"] for r in collapsed_runs if r["collapse_step"] is not None
        ]

        if not collapse_steps:
            return {
                "bottleneck": "UNKNOWN",
                "description": "Collapse detected but step information missing",
            }

        avg_collapse_step = np.mean(collapse_steps)

        if avg_collapse_step < 20:
            return {
                "bottleneck": "IMMEDIATE_OVERLOAD",
                "description": "System collapses immediately under load",
                "recommendation": "Critical: Reduce agent count or increase resources",
            }
        elif avg_collapse_step < 50:
            return {
                "bottleneck": "COMMUNICATION_BREAKDOWN",
                "description": "System fails as communication complexity increases",
                "recommendation": "Optimize agent communication protocols",
            }
        else:
            return {
                "bottleneck": "GRADUAL_ENTROPY_ACCUMULATION",
                "description": "System slowly accumulates entropy over time",
                "recommendation": "Implement periodic system resets or cleanup",
            }

    def find_max_agents(self, max_attempts: int = 20) -> Dict[str, Any]:
        """
        Binary search to find maximum number of agents system can support

        Args:
            max_attempts: Maximum number of binary search iterations

        Returns:
            Dictionary with max agents and related metrics
        """
        logger.info("Finding maximum agent capacity...")

        low, high = 1, 1000
        max_stable = 0

        for attempt in range(max_attempts):
            mid = (low + high) // 2

            result = self.simulate_scenario(
                scenario={"add_agents": mid - len(self.brain.agents)},
                steps=100,
                monte_carlo_runs=3,
            )

            if result["system_stable"]:
                max_stable = mid
                low = mid + 1
            else:
                high = mid - 1

        return {
            "max_agents_supported": max_stable,
            "confidence": "high" if max_attempts > 15 else "medium",
            "recommendation": f"Safe operating range: up to {int(max_stable * 0.8)} agents",
        }

    def compare_scenarios(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple scenarios side-by-side

        Args:
            scenarios: List of scenario dictionaries

        Returns:
            Comparison results with rankings
        """
        results = []

        for scenario in scenarios:
            result = self.simulate_scenario(scenario, steps=100, monte_carlo_runs=5)
            results.append(result)

        # Rank by stability and efficiency
        ranked = sorted(
            results, key=lambda r: (r["system_stable"], -r["avg_entropy"]), reverse=True
        )

        return {
            "scenarios_compared": len(scenarios),
            "rankings": ranked,
            "best_scenario": ranked[0]["scenario"] if ranked else None,
            "comparison_summary": self._create_comparison_summary(ranked),
        }

    def _create_comparison_summary(self, ranked_results: List[Dict[str, Any]]) -> str:
        """Create human-readable comparison summary"""

        if not ranked_results:
            return "No scenarios to compare"

        best = ranked_results[0]
        worst = ranked_results[-1]

        summary = f"""
Scenario Comparison Results:
        
Best Scenario: {best['scenario']}
- Stability: {'STABLE' if best['system_stable'] else 'UNSTABLE'}
- Avg Entropy: {best['avg_entropy']:.3f}
- Collapse Probability: {best['collapse_probability']:.1%}

Worst Scenario: {worst['scenario']}
- Stability: {'STABLE' if worst['system_stable'] else 'UNSTABLE'}
- Avg Entropy: {worst['avg_entropy']:.3f}
- Collapse Probability: {worst['collapse_probability']:.1%}

Improvement Margin: {((worst['avg_entropy'] - best['avg_entropy']) / worst['avg_entropy'] * 100):.1f}%
        """.strip()

        return summary
