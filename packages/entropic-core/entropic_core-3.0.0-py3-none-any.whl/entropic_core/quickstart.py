"""
Magical Quickstart Command
Gets users from zero to value in 30 seconds
"""

import time
from typing import List

from .core.entropy_monitor import EntropyMonitor
from .core.entropy_regulator import EntropyRegulator
from .discovery import SetupWizard


class DemoAgent:
    """Simplified agent for quickstart demo"""

    def __init__(self, name: str, behavior: str = "normal"):
        self.name = name
        self.behavior = behavior
        self.decision_count = 0
        self.state = 0.5

    def make_decision(self):
        """Simulate agent decision-making"""
        import random

        if self.behavior == "chaotic":
            self.state = random.random()  # High entropy
        elif self.behavior == "rigid":
            self.state = 0.5  # Low entropy
        else:
            self.state += random.gauss(0, 0.1)  # Normal
            self.state = max(0, min(1, self.state))

        self.decision_count += 1
        return self.state


class QuickstartDemo:
    """
    30-second demo that shows immediate value
    No configuration required (uses toy mode if needed)
    """

    def __init__(self):
        self.agents: List[DemoAgent] = []
        self.monitor = None
        self.regulator = None

    def run(self, duration_seconds: int = 30):
        """Run the magical quickstart demo"""
        print("\n" + "=" * 60)
        print("🚀 ENTROPIC CORE - 30 Second Demo")
        print("   Watch your AI system self-regulate in real-time")
        print("=" * 60 + "\n")

        # Check if configured
        if not SetupWizard.quick_check():
            print("First time setup required...")
            wizard = SetupWizard()
            wizard.run()

        # Create demo scenario
        print("Creating 3 AI agents...")
        self.agents = [
            DemoAgent("Analyst", "normal"),
            DemoAgent("Creative", "chaotic"),
            DemoAgent("Validator", "rigid"),
        ]
        print("✅ Agents created\n")

        # Initialize monitoring
        print("Initializing entropy monitoring...")
        self.monitor = EntropyMonitor()
        self.regulator = EntropyRegulator()
        print("✅ Monitoring active\n")

        # Run simulation
        print(f"Running {duration_seconds}s simulation...\n")
        print("TIME  | ENTROPY | STATUS        | ACTION")
        print("-" * 60)

        start_time = time.time()
        tick = 0

        while time.time() - start_time < duration_seconds:
            # Agents make decisions
            for agent in self.agents:
                agent.make_decision()

            # Measure entropy
            agent_states = [
                {"current_state": a.state, "last_decision": a.decision_count}
                for a in self.agents
            ]
            entropy = self.monitor.measure_system_entropy(agent_states)

            # Regulate
            regulation = self.regulator.regulate(entropy["combined"], self.agents)

            # Display
            status_emoji = self._get_status_emoji(entropy["combined"])
            print(
                f"{tick:4d}s | {entropy['combined']:.3f}   | {status_emoji:13s} | {regulation['action']}"
            )

            tick += 1
            time.sleep(1)

        # Summary
        print("\n" + "=" * 60)
        print("✅ Demo Complete!")
        print("\nWhat just happened?")
        print("• Your agents were making decisions (some chaotic, some rigid)")
        print("• Entropic Core measured system entropy in real-time")
        print("• When entropy got too high → system stabilized")
        print("• When entropy got too low → system injected creativity")
        print("• Result: Optimal balance between chaos and order")
        print("\n💡 This is homeostasis in action!")
        print("=" * 60 + "\n")

        self._show_next_steps()

    def _get_status_emoji(self, entropy: float) -> str:
        """Get status indicator"""
        if entropy > 0.8:
            return "🔴 TOO CHAOTIC"
        elif entropy < 0.2:
            return "🔵 TOO RIGID"
        elif 0.4 <= entropy <= 0.6:
            return "✅ OPTIMAL"
        else:
            return "⚠️  ADJUSTING"

    def _show_next_steps(self):
        """Show what to do next"""
        print("📚 Next Steps:\n")
        print("1. Try with your own agents:")
        print("   from entropic_core import EntropyBrain")
        print("   brain = EntropyBrain()")
        print("   brain.connect(your_agents)")
        print("\n2. View the dashboard:")
        print("   entropic-dashboard")
        print("\n3. Read the docs:")
        print("   https://entropic-core.readthedocs.io")
        print("\n4. Join the community:")
        print("   https://discord.gg/entropic-core")
        print()


def main():
    """Entry point for quickstart command"""
    demo = QuickstartDemo()
    demo.run(duration_seconds=30)


if __name__ == "__main__":
    main()
