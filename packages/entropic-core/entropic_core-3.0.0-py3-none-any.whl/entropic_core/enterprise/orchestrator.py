"""
Multi-System Orchestrator
Coordinates multiple Entropic Core instances for global homeostasis
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

import numpy as np


class EntropyOrchestrator:
    """
    Coordinates multiple multi-agent systems
    Manages cross-system entropy resonance and load balancing
    """

    def __init__(self):
        self.subsystems: Dict[str, Any] = {}
        self.global_entropy_history = []
        self.resonance_detector = ResonanceDetector()
        self.load_balancer = EntropyLoadBalancer()
        self.logger = logging.getLogger(__name__)

    def register_subsystem(self, name: str, brain):
        """Register a subsystem for orchestration"""
        self.subsystems[name] = {
            "brain": brain,
            "registered_at": datetime.now(),
            "last_sync": None,
            "health_score": 1.0,
        }
        self.logger.info(f"Registered subsystem: {name}")

    def unregister_subsystem(self, name: str):
        """Remove a subsystem from orchestration"""
        if name in self.subsystems:
            del self.subsystems[name]
            self.logger.info(f"Unregistered subsystem: {name}")

    def coordinate_cross_system(self) -> Dict[str, Any]:
        """
        Main coordination loop
        Detects resonances, balances load, and maintains global homeostasis
        """
        # Measure global entropy
        global_entropy = self._calculate_global_entropy()
        self.global_entropy_history.append(
            {"timestamp": datetime.now().isoformat(), "entropy": global_entropy}
        )

        # Detect dangerous resonances
        resonances = self.resonance_detector.detect(self.subsystems)

        # Balance entropy load if needed
        balancing_actions = []
        if global_entropy > 0.75:
            balancing_actions = self.load_balancer.redistribute_entropy(self.subsystems)

        # Desynchronize if dangerous resonance detected
        if resonances["dangerous_sync"]:
            self._desynchronize_systems(resonances["affected_systems"])

        # Generate coordination plan
        coordination_plan = self._generate_coordination_plan(
            global_entropy, resonances, balancing_actions
        )

        return {
            "global_entropy": global_entropy,
            "subsystem_count": len(self.subsystems),
            "resonances": resonances,
            "balancing_actions": balancing_actions,
            "coordination_plan": coordination_plan,
            "health_status": self._assess_global_health(),
        }

    def _calculate_global_entropy(self) -> float:
        """Calculate entropy across all subsystems"""
        if not self.subsystems:
            return 0.0

        entropies = []
        for name, subsys in self.subsystems.items():
            brain = subsys["brain"]
            metrics = brain.monitor.measure_system_entropy(brain.agents)
            entropies.append(metrics["combined"])

        # Weighted average (could be more sophisticated)
        return sum(entropies) / len(entropies)

    def _desynchronize_systems(self, affected_systems: List[str]):
        """Desynchronize systems to prevent destructive resonance"""
        for i, system_name in enumerate(affected_systems):
            if system_name in self.subsystems:
                self.subsystems[system_name]["brain"]
                # Inject random delay or parameter adjustment
                phase_shift = i * 0.1  # Stagger by 100ms
                self.logger.info(
                    f"Desynchronizing {system_name} with phase shift {phase_shift}"
                )
                # Implementation would adjust regulation timing

    def _generate_coordination_plan(
        self, global_entropy: float, resonances: Dict, balancing_actions: List[Dict]
    ) -> Dict:
        """Generate plan for coordinating subsystems"""
        plan = {
            "timestamp": datetime.now().isoformat(),
            "global_status": (
                "optimal" if 0.4 <= global_entropy <= 0.6 else "suboptimal"
            ),
            "actions": [],
        }

        if global_entropy > 0.8:
            plan["actions"].append(
                {
                    "type": "global_stabilization",
                    "description": "Reduce chaos across all subsystems",
                    "priority": "high",
                }
            )
        elif global_entropy < 0.2:
            plan["actions"].append(
                {
                    "type": "global_innovation",
                    "description": "Inject exploration across subsystems",
                    "priority": "medium",
                }
            )

        if resonances["dangerous_sync"]:
            plan["actions"].append(
                {
                    "type": "desynchronization",
                    "description": "Break destructive resonance patterns",
                    "priority": "critical",
                }
            )

        return plan

    def _assess_global_health(self) -> Dict[str, Any]:
        """Assess overall health of orchestrated systems"""
        health_scores = []
        for subsys in self.subsystems.values():
            health_scores.append(subsys["health_score"])

        if not health_scores:
            return {"status": "no_systems", "score": 0.0}

        avg_health = sum(health_scores) / len(health_scores)

        return {
            "status": "healthy" if avg_health > 0.7 else "degraded",
            "score": avg_health,
            "subsystems_healthy": sum(1 for s in health_scores if s > 0.7),
            "subsystems_total": len(health_scores),
        }

    def get_subsystem_status(self, name: str) -> Dict[str, Any]:
        """Get detailed status of a specific subsystem"""
        if name not in self.subsystems:
            return {"error": "Subsystem not found"}

        subsys = self.subsystems[name]
        brain = subsys["brain"]
        metrics = brain.monitor.measure_system_entropy(brain.agents)

        return {
            "name": name,
            "entropy": metrics["combined"],
            "agent_count": len(brain.agents),
            "health_score": subsys["health_score"],
            "registered_at": subsys["registered_at"].isoformat(),
            "last_sync": (
                subsys["last_sync"].isoformat() if subsys["last_sync"] else None
            ),
        }


class ResonanceDetector:
    """Detects dangerous entropy resonances between systems"""

    def detect(self, subsystems: Dict) -> Dict[str, Any]:
        """Detect resonance patterns"""
        if len(subsystems) < 2:
            return {"dangerous_sync": False, "affected_systems": []}

        # Extract entropy values
        entropies = {}
        for name, subsys in subsystems.items():
            brain = subsys["brain"]
            metrics = brain.monitor.measure_system_entropy(brain.agents)
            entropies[name] = metrics["combined"]

        # Check for synchronization (all systems in same phase)
        values = list(entropies.values())
        if len(values) > 1:
            std_dev = np.std(values)
            # If all systems have very similar entropy, they might be resonating
            dangerous_sync = std_dev < 0.05 and (
                np.mean(values) > 0.8 or np.mean(values) < 0.2
            )
        else:
            dangerous_sync = False

        return {
            "dangerous_sync": dangerous_sync,
            "affected_systems": list(entropies.keys()) if dangerous_sync else [],
            "sync_coefficient": 1.0 - std_dev if len(values) > 1 else 0.0,
            "insights": self._generate_insights(entropies, dangerous_sync),
        }

    def _generate_insights(self, entropies: Dict, dangerous: bool) -> List[str]:
        """Generate human-readable insights"""
        insights = []

        if dangerous:
            insights.append("Dangerous synchronization detected across subsystems")
            insights.append("Systems may amplify each other's instabilities")

        high_entropy_systems = [name for name, e in entropies.items() if e > 0.8]
        if high_entropy_systems:
            insights.append(f"High entropy in: {', '.join(high_entropy_systems)}")

        return insights


class EntropyLoadBalancer:
    """Balances entropy load across subsystems"""

    def redistribute_entropy(self, subsystems: Dict) -> List[Dict]:
        """Redistribute entropy load to prevent overload"""
        actions = []

        # Find high-load and low-load systems
        load_map = {}
        for name, subsys in subsystems.items():
            brain = subsys["brain"]
            metrics = brain.monitor.measure_system_entropy(brain.agents)
            load_map[name] = metrics["combined"]

        # Identify candidates for load transfer
        high_load = [name for name, load in load_map.items() if load > 0.75]
        low_load = [name for name, load in load_map.items() if load < 0.4]

        # Generate transfer actions
        for high_sys in high_load:
            for low_sys in low_load:
                actions.append(
                    {
                        "type": "entropy_transfer",
                        "from": high_sys,
                        "to": low_sys,
                        "description": f"Transfer tasks from {high_sys} to {low_sys}",
                    }
                )
                break  # One transfer per high-load system

        return actions
