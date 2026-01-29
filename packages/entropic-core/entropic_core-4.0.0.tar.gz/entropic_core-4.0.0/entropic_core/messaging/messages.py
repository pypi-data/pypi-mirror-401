"""
User-friendly messaging system
Transforms technical concepts into business value
"""

from typing import Dict, Optional


class MessageBuilder:
    """
    Builds user-friendly messages that emphasize value over technical details

    Transforms:
    - "Entropy" → "System health"
    - "Regulation" → "Automatic healing"
    - "Homeostasis" → "Optimal balance"
    """

    @staticmethod
    def entropy_status(entropy_value: float, context: Optional[Dict] = None) -> str:
        """
        Convert entropy value to business-friendly status

        Args:
            entropy_value: Raw entropy value (0-1)
            context: Additional context (agent count, time, etc.)

        Returns:
            User-friendly status message
        """
        if entropy_value > 0.8:
            return (
                f"🔴 System Health: CRITICAL\n"
                f"   Your AI agents are becoming unpredictable.\n"
                f"   Entropic Core is stabilizing the system..."
            )
        elif entropy_value > 0.6:
            return (
                f"⚠️  System Health: WARNING\n"
                f"   Detecting increased chaos in agent behavior.\n"
                f"   Monitoring closely for stability issues."
            )
        elif entropy_value < 0.2:
            return (
                f"🔵 System Health: STAGNANT\n"
                f"   Your AI agents are becoming too rigid.\n"
                f"   Injecting creativity to maintain innovation..."
            )
        elif entropy_value < 0.4:
            return (
                f"💡 System Health: LOW INNOVATION\n"
                f"   System is stable but could be more creative.\n"
                f"   Gradually increasing exploration."
            )
        else:
            return (
                f"✅ System Health: OPTIMAL\n"
                f"   Perfect balance between stability and innovation.\n"
                f"   Your agents are performing at peak efficiency."
            )

    @staticmethod
    def regulation_action(action: str, impact: Optional[Dict] = None) -> str:
        """
        Explain regulation action in business terms

        Args:
            action: Technical action taken
            impact: Estimated impact (cost saved, downtime avoided, etc.)

        Returns:
            User-friendly explanation
        """
        messages = {
            "REDUCE_CHAOS": (
                "🛡️  AUTOMATIC HEALING: Stabilizing System\n"
                "   Action: Reducing agent autonomy temporarily\n"
                "   Goal: Prevent system collapse\n"
                "   {impact}"
            ),
            "INCREASE_CHAOS": (
                "💡 AUTOMATIC HEALING: Boosting Innovation\n"
                "   Action: Increasing agent exploration\n"
                "   Goal: Prevent stagnation and missed opportunities\n"
                "   {impact}"
            ),
            "MAINTAIN": (
                "✅ AUTOMATIC HEALING: Maintaining Balance\n"
                "   Action: Fine-tuning parameters\n"
                "   Goal: Keep system in optimal state\n"
                "   {impact}"
            ),
        }

        message = messages.get(action, "System adjusting...")

        if impact:
            impact_text = MessageBuilder._format_impact(impact)
            message = message.format(impact=impact_text)
        else:
            message = message.format(impact="")

        return message

    @staticmethod
    def _format_impact(impact: Dict) -> str:
        """Format impact metrics"""
        parts = []

        if "cost_saved" in impact:
            parts.append(f"💰 Estimated savings: ${impact['cost_saved']}")

        if "downtime_avoided" in impact:
            parts.append(f"⏱️  Downtime avoided: {impact['downtime_avoided']} minutes")

        if "decisions_improved" in impact:
            parts.append(f"📊 Decisions improved: {impact['decisions_improved']}")

        return "\n   ".join(parts) if parts else ""

    @staticmethod
    def value_proposition(scenario: str) -> str:
        """
        Show value proposition for different scenarios

        Args:
            scenario: User scenario (first_use, chaos_detected, etc.)

        Returns:
            Compelling value message
        """
        messages = {
            "first_use": (
                "\n" + "=" * 60 + "\n"
                "🧠 Welcome to Entropic Core\n"
                "   Your AI System's Immune System\n"
                "=" * 60 + "\n\n"
                "What Entropic Core does for you:\n"
                "• Prevents system crashes before they happen\n"
                "• Maintains optimal balance automatically\n"
                "• Saves hours of manual monitoring\n"
                "• 100% FREE and open source\n\n"
                "Think of it as:\n"
                "• Netflix's chaos engineering... for your AI agents\n"
                "• A thermostat... but for system stability\n"
                "• Your AI team's health insurance\n"
            ),
            "chaos_detected": (
                "\n💡 Entropic Core just saved you from a system crash!\n\n"
                "What happened:\n"
                "• Your agents were diverging dangerously\n"
                "• System collapse was ~5 minutes away\n"
                "• Automatic stabilization prevented downtime\n\n"
                "Without Entropic Core:\n"
                "❌ You'd be debugging right now\n"
                "❌ Users would see errors\n"
                "❌ You'd lose revenue/trust\n\n"
                "With Entropic Core:\n"
                "✅ System self-healed automatically\n"
                "✅ Users never noticed anything\n"
                "✅ You stayed focused on building\n"
            ),
            "stagnation_detected": (
                "\n💡 Entropic Core is boosting your system's creativity!\n\n"
                "What we detected:\n"
                "• Your agents were becoming too predictable\n"
                "• Innovation was declining\n"
                "• Users might notice repetitive behavior\n\n"
                "What we're doing:\n"
                "✅ Injecting controlled exploration\n"
                "✅ Maintaining stability while innovating\n"
                "✅ Finding new solutions automatically\n\n"
                "Result: Better outcomes without manual tuning\n"
            ),
            "optimal": (
                "\n✅ Your system is performing perfectly!\n\n"
                "Current state:\n"
                "• Optimal balance between stability and innovation\n"
                "• Agents are coordinating efficiently\n"
                "• Peak performance achieved\n\n"
                "Entropic Core is monitoring 24/7 to keep it this way.\n"
            ),
        }

        return messages.get(scenario, "")
