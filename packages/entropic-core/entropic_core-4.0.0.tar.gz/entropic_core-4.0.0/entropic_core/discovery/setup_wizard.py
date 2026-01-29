"""
Interactive Setup Wizard
Guides users through initial configuration
"""

import os
import sys
from typing import Dict

from .llm_discoverer import LLMDiscoverer


class SetupWizard:
    """Interactive configuration wizard for first-time users"""

    def __init__(self):
        self.discoverer = LLMDiscoverer()
        self.config = {}

    def run(self) -> Dict:
        """
        Run interactive setup wizard
        Returns configuration dictionary
        """
        print("\n" + "=" * 60)
        print("🧠 ENTROPIC CORE - Setup Wizard")
        print("   Your AI System's Immune System")
        print("=" * 60 + "\n")

        # Step 1: Discover LLMs
        print("Step 1/3: Discovering available LLM providers...")
        discovery = self.discoverer.discover_all()

        if not discovery["available"]:
            return self._handle_no_llms()

        # Step 2: Select provider
        print(f"\nStep 2/3: Found {discovery['available_count']} provider(s)")
        selected = self._select_provider(
            discovery["available"], discovery["recommended"]
        )

        # Step 3: Configure
        print("\nStep 3/3: Configuring Entropic Core...")
        config = self._configure_system(selected)

        print("\n" + "=" * 60)
        print("✅ Setup complete! Your system is ready.")
        print(
            f"💰 Estimated monthly cost: ${discovery['estimated_monthly_cost']['monthly_cost']}"
        )
        print("=" * 60 + "\n")

        return config

    def _handle_no_llms(self) -> Dict:
        """Handle case where no LLMs are available"""
        print("\n⚠️  No LLM providers found!")
        print("\nTo use Entropic Core, you need at least one LLM provider.")
        print("\n🆓 FREE OPTIONS (Recommended):")
        print("   1. Ollama (local, zero cost)")
        print("      Install: curl -fsSL https://ollama.ai/install.sh | sh")
        print("      Then: ollama pull llama2")
        print("\n   2. LM Studio (local, zero cost)")
        print("      Download: https://lmstudio.ai")
        print("\n💳 PAID OPTIONS:")
        print("   3. Groq (very cheap, ~$0.10/month)")
        print("      Sign up: https://console.groq.com")
        print("      Set: export GROQ_API_KEY=your_key")
        print("\n   4. OpenRouter (flexible pricing)")
        print("      Sign up: https://openrouter.ai")
        print("      Set: export OPENROUTER_API_KEY=your_key")
        print("\n   5. OpenAI/Anthropic (premium)")
        print("      OpenAI: https://platform.openai.com")
        print("      Anthropic: https://console.anthropic.com")

        print("\n💡 TIP: Run this wizard again after installing a provider")
        print("   Command: entropic-setup\n")

        sys.exit(1)

    def _select_provider(self, available, recommended) -> Dict:
        """Let user select from available providers"""
        print("\nAvailable providers:\n")

        for i, provider in enumerate(available, 1):
            cost_info = (
                "FREE"
                if provider.cost_per_1k_tokens == 0
                else f"${provider.cost_per_1k_tokens}/1k tokens"
            )
            marker = "⭐" if provider == recommended else "  "
            print(f"{marker} {i}. {provider.name} ({provider.type}) - {cost_info}")

        if recommended:
            print(f"\n⭐ Recommended: {recommended.name} (best value)")

        # Auto-select recommended in non-interactive mode
        if not sys.stdin.isatty():
            return recommended

        while True:
            try:
                choice = input(
                    f"\nSelect provider [1-{len(available)}] or press Enter for recommended: "
                ).strip()
                if not choice and recommended:
                    return recommended
                idx = int(choice) - 1
                if 0 <= idx < len(available):
                    return available[idx]
                print("❌ Invalid selection. Try again.")
            except (ValueError, KeyboardInterrupt):
                if recommended:
                    return recommended
                print("\n❌ Selection cancelled.")
                sys.exit(1)

    def _configure_system(self, provider: Dict) -> Dict:
        """Configure Entropic Core with selected provider"""
        config = {
            "provider": provider.name,
            "endpoint": provider.endpoint,
            "type": provider.type,
            "cost_per_1k_tokens": provider.cost_per_1k_tokens,
        }

        # Save to config file
        config_path = os.path.expanduser("~/.entropic/config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        import json

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Configuration saved to {config_path}")

        return config

    @staticmethod
    def quick_check() -> bool:
        """Quick check if system is configured"""
        config_path = os.path.expanduser("~/.entropic/config.json")
        return os.path.exists(config_path)
