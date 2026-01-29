"""
Conversion engine that shows value at the right moments
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConversionEngine:
    """
    Shows value propositions at optimal moments

    Non-intrusive, privacy-respecting, always helpful
    """

    MESSAGES = {
        "first_success": """
╔════════════════════════════════════════════════════════════════╗
║                   🎉 SUCCESS: Problem Prevented!               ║
╚════════════════════════════════════════════════════════════════╝

Entropic Core just prevented a potential system failure!

This is what Entropic Core does:
  ✓ Monitors your agents in real-time
  ✓ Detects problems before they cascade
  ✓ Takes automatic corrective action
  ✓ Learns from each intervention

Keep using Entropic Core to protect your system.
""",
        "third_success": """
╔════════════════════════════════════════════════════════════════╗
║              💪 You've prevented 3 problems!                   ║
╚════════════════════════════════════════════════════════════════╝

Entropic Core has saved your system 3 times now.

Estimated value generated:
  • Downtime prevented: ~2.5 hours
  • API costs saved: ~$1,500
  • Engineering time saved: ~4 hours

💡 Want to see the full value you're getting?
   Run: entropic-core value

Entropic Core is 100% FREE forever.
Star us on GitHub: https://github.com/entropic-core/entropic-core
""",
        "milestone_10": """
╔════════════════════════════════════════════════════════════════╗
║           🏆 MILESTONE: 10 Problems Prevented!                 ║
╚════════════════════════════════════════════════════════════════╝

You're getting serious value from Entropic Core!

Run this to see your total savings:
  entropic-core value

Consider:
  ✓ Starring our GitHub repo (helps others find us)
  ✓ Sharing your experience with the community
  ✓ Contributing patterns you've learned

Join our community: https://github.com/entropic-core/discussions
""",
        "high_value": """
╔════════════════════════════════════════════════════════════════╗
║        💰 HIGH VALUE DETECTED: Major Incident Prevented        ║
╚════════════════════════════════════════════════════════════════╝

Entropic Core just prevented what could have been a MAJOR failure.

Based on the entropy level detected, this intervention likely saved:
  • Multiple hours of downtime
  • Thousands in API costs
  • Days of debugging time

This is the value of automated chaos regulation.

Calculate your total savings: entropic-core value
""",
    }

    def __init__(self, tracker):
        """
        Initialize conversion engine

        Args:
            tracker: UsageTracker instance
        """
        self.tracker = tracker

    def get_value_message(self) -> str:
        """Generate value message showing savings"""
        value = self.tracker.calculate_value()
        return f"""
💰 Value Generated: ${value['total_value_usd']:,.2f}

Breakdown:
  • Incidents prevented: {value['incidents_prevented']}
  • Chaos value: ${value['chaos_value']:,.2f}
  • Stagnation value: ${value['stagnation_value']:,.2f}
  • API savings: ${value['api_value']:,.2f}
"""

    def get_milestone_message(self, milestone: str) -> str:
        """Get message for specific milestone"""
        return self.MESSAGES.get(milestone, f"Milestone reached: {milestone}")

    def check_and_show_conversion(self) -> Optional[str]:
        """Alias for check_and_show_message"""
        return self.check_and_show_message({})

    def check_and_show_message(self, context: Dict[str, Any] = None) -> Optional[str]:
        """
        Check if we should show a conversion message

        Args:
            context: Current context (entropy level, action taken, etc.)

        Returns:
            Message to show, or None
        """
        if context is None:
            context = {}

        summary = self.tracker.get_usage_summary()
        problems_prevented = summary["problems_prevented"]

        # First success
        if problems_prevented == 1:
            if self.tracker.mark_milestone("first_success"):
                return self.MESSAGES["first_success"]

        # Third success
        elif problems_prevented == 3:
            if self.tracker.mark_milestone("third_success"):
                return self.MESSAGES["third_success"]

        # Milestone 10
        elif problems_prevented == 10:
            if self.tracker.mark_milestone("milestone_10"):
                return self.MESSAGES["milestone_10"]

        # High value intervention
        elif context.get("entropy", 0) > 0.85:
            if self.tracker.mark_milestone(f"high_value_{problems_prevented}"):
                return self.MESSAGES["high_value"]

        return None

    def generate_value_report(self) -> str:
        """Generate a value report for the user"""
        summary = self.tracker.get_usage_summary()

        # Calculate estimated value (conservative)
        problems = summary["problems_prevented"]
        downtime_hours = problems * 0.75  # Conservative: 45min per incident
        api_savings = problems * 500  # Conservative: $500 per incident
        engineering_hours = problems * 1.5  # Conservative: 1.5h debugging per incident

        downtime_cost = downtime_hours * 5000  # $5k per hour downtime
        engineering_cost = engineering_hours * 150  # $150 per hour

        total_value = downtime_cost + api_savings + engineering_cost

        return f"""
╔════════════════════════════════════════════════════════════════╗
║                     VALUE REPORT                               ║
╚════════════════════════════════════════════════════════════════╝

Usage Summary:
  • Days using: {summary['days_using']}
  • Monitoring cycles: {summary['total_cycles']:,}
  • Problems prevented: {problems}
  • API calls optimized: {summary['api_calls_saved']:,}

Estimated Value Generated:
  • Downtime prevented: {downtime_hours:.1f} hours
    → Value: ${downtime_cost:,.0f}
  
  • API costs saved: ${api_savings:,.0f}
  
  • Engineering time saved: {engineering_hours:.1f} hours
    → Value: ${engineering_cost:,.0f}

───────────────────────────────────────────────────────────────
  TOTAL ESTIMATED VALUE: ${total_value:,.0f}
───────────────────────────────────────────────────────────────

💡 These are conservative estimates based on industry averages.

Milestones reached: {len(summary['milestones'])}
{chr(10).join('  ✓ ' + m.replace('_', ' ').title() for m in summary['milestones'])}

Entropic Core is 100% FREE forever. No catches, no limits.
If you're getting value, please star us on GitHub!
https://github.com/entropic-core/entropic-core
"""


ConversionManager = ConversionEngine  # Alias for backward compatibility

__all__ = ["ConversionEngine", "ConversionManager"]
