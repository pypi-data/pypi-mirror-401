"""
Track usage patterns to identify conversion opportunities
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class UsageTracker:
    """
    Tracks Entropic Core usage to identify when to show value propositions

    Privacy-first: All data stored locally, no external transmission
    """

    def __init__(self):
        self.storage_dir = self._get_storage_dir()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.usage_file = self.storage_dir / "usage_stats.json"

        self.stats = self._load_stats()

    @staticmethod
    def _get_storage_dir() -> Path:
        """Get the storage directory for usage stats"""
        return Path.home() / ".entropic"

    def _load_stats(self) -> Dict[str, Any]:
        """Load usage stats from disk"""
        default_stats = {
            "first_use": datetime.now().isoformat(),
            "total_cycles": 0,
            "total_regulations": 0,
            "regulations_by_type": {},  # Track types of regulations
            "chaos_prevented": 0,
            "stagnation_prevented": 0,
            "preventions": 0,  # Total preventions
            "preventions_by_type": {},
            "api_calls_saved": 0,
            "last_conversion_prompt": None,
            "conversion_prompts_shown": 0,
            "user_opted_in": False,
            "milestones_reached": [],
        }

        if self.usage_file.exists():
            try:
                with open(self.usage_file, "r") as f:
                    loaded_stats = json.load(f)

                for key, value in default_stats.items():
                    if key not in loaded_stats:
                        loaded_stats[key] = value

                return loaded_stats
            except Exception as e:
                logger.warning(f"Could not load usage stats: {e}")

        return default_stats

    def _save_stats(self):
        """Save usage stats to disk"""
        try:
            with open(self.usage_file, "w") as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save usage stats: {e}")

    def track_cycle(self):
        """Track a monitoring cycle"""
        self.stats["total_cycles"] += 1
        self._save_stats()

    def track_regulation(self, action: str):
        """Track a regulation action"""
        self.stats["total_regulations"] += 1

        if "regulations_by_type" not in self.stats:
            self.stats["regulations_by_type"] = {}

        if action not in self.stats["regulations_by_type"]:
            self.stats["regulations_by_type"][action] = 0
        self.stats["regulations_by_type"][action] += 1

        if "REDUCE" in action or "CHAOS" in action:
            self.stats["chaos_prevented"] += 1
        elif "INCREASE" in action or "STAGNATION" in action:
            self.stats["stagnation_prevented"] += 1

        self._save_stats()

    def track_prevention(self, incident_type: str):
        """Track a prevented incident"""
        self.stats["preventions"] += 1

        # Track specific incident types
        if incident_type not in self.stats["preventions_by_type"]:
            self.stats["preventions_by_type"][incident_type] = 0
        self.stats["preventions_by_type"][incident_type] += 1

        self._save_stats()

    def track_api_save(self, count: int = 1):
        """Track API calls saved by prevention"""
        self.stats["api_calls_saved"] += count
        self._save_stats()

    def should_show_conversion(self) -> bool:
        """Alias for should_show_conversion_message"""
        return self.should_show_conversion_message()

    def should_show_conversion_message(self) -> bool:
        """
        Determine if we should show a conversion message

        Shows message when:
        - First regulation performed, OR
        - User has had 3+ successful interventions
        - Haven't shown message in last 7 days
        - User hasn't opted in
        """
        if self.stats["user_opted_in"]:
            return False

        if self.stats["total_regulations"] == 1:
            # Check if we already showed it
            if self.stats.get("last_conversion_prompt"):
                return False
            return True

        # Check if we've prevented enough problems
        total_prevented = (
            self.stats["chaos_prevented"] + self.stats["stagnation_prevented"]
        )

        if total_prevented < 3:
            return False

        # Check time since last prompt
        last_prompt = self.stats.get("last_conversion_prompt")
        if last_prompt:
            last_prompt_dt = datetime.fromisoformat(last_prompt)
            if datetime.now() - last_prompt_dt < timedelta(days=7):
                return False

        return True

    def mark_conversion_shown(self):
        """Mark that we showed a conversion message"""
        self.stats["last_conversion_prompt"] = datetime.now().isoformat()
        self.stats["conversion_prompts_shown"] += 1
        self._save_stats()

    def mark_milestone(self, milestone: str):
        """Mark a usage milestone"""
        if milestone not in self.stats["milestones_reached"]:
            self.stats["milestones_reached"].append(milestone)
            self._save_stats()
            return True
        return False

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get summary of usage statistics"""
        first_use = datetime.fromisoformat(self.stats["first_use"])
        days_using = (datetime.now() - first_use).days

        return {
            "days_using": days_using,
            "total_cycles": self.stats["total_cycles"],
            "total_regulations": self.stats["total_regulations"],
            "problems_prevented": (
                self.stats["chaos_prevented"] + self.stats["stagnation_prevented"]
            ),
            "api_calls_saved": self.stats["api_calls_saved"],
            "milestones": self.stats["milestones_reached"],
        }

    def calculate_value(self) -> Dict[str, Any]:
        """Calculate total value delivered to user"""
        # Estimate cost per incident
        avg_incident_cost = 1000  # $1000 per chaos incident
        avg_api_cost_per_call = 0.002  # $0.002 per API call

        total_preventions = self.stats.get("preventions", 0)

        # Also calculate from chaos/stagnation if preventions not set
        if total_preventions == 0:
            total_preventions = (
                self.stats["chaos_prevented"] + self.stats["stagnation_prevented"]
            )

        chaos_value = self.stats["chaos_prevented"] * avg_incident_cost
        stagnation_value = self.stats["stagnation_prevented"] * (
            avg_incident_cost * 0.5
        )
        api_value = self.stats["api_calls_saved"] * avg_api_cost_per_call

        total_value = chaos_value + stagnation_value + api_value

        return {
            "total_value_usd": total_value,
            "chaos_value": chaos_value,
            "stagnation_value": stagnation_value,
            "api_value": api_value,
            "incidents_prevented": total_preventions,
            "api_calls_saved": self.stats["api_calls_saved"],
            "estimated_savings": total_value,  # Added estimated_savings field
            "breakdown": {
                "chaos_incidents_prevented": self.stats["chaos_prevented"],
                "stagnation_incidents_prevented": self.stats["stagnation_prevented"],
                "api_calls_saved": self.stats["api_calls_saved"],
            },
        }
