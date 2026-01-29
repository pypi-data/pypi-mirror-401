"""
Anonymous Telemetry Collection
Opt-in only, helps improve the product
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class TelemetryCollector:
    """
    Collects anonymous usage data to improve Entropic Core

    Privacy First:
    - Opt-in only (disabled by default)
    - No personal information
    - No agent data or decisions
    - Only aggregate metrics
    """

    def __init__(self):
        self.enabled = self._check_opt_in()
        self.session_id = str(uuid.uuid4())
        self.installation_id = self._get_installation_id()
        self.data_path = Path.home() / ".entropic" / "telemetry"
        self.data_path.mkdir(parents=True, exist_ok=True)

    def _check_opt_in(self) -> bool:
        """Check if user has opted in to telemetry"""
        # Check environment variable
        env_opt_in = os.getenv("ENTROPIC_TELEMETRY", "").lower()
        if env_opt_in in ("1", "true", "yes"):
            return True

        # Check config file
        config_path = Path.home() / ".entropic" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    return config.get("telemetry_enabled", False)
            except Exception:
                pass

        return False

    def _get_installation_id(self) -> str:
        """Get or create anonymous installation ID"""
        id_file = Path.home() / ".entropic" / "installation_id"

        if id_file.exists():
            return id_file.read_text().strip()

        # Create new ID
        installation_id = str(uuid.uuid4())
        id_file.parent.mkdir(parents=True, exist_ok=True)
        id_file.write_text(installation_id)

        return installation_id

    def track_event(self, event_type: str, properties: Optional[Dict] = None):
        """
        Track an anonymous event

        Args:
            event_type: Type of event (e.g., 'quickstart_run', 'entropy_spike')
            properties: Anonymous properties (no PII, no sensitive data)
        """
        if not self.enabled:
            return

        event = {
            "installation_id": self.installation_id,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "properties": self._sanitize_properties(properties or {}),
        }

        # Save locally (will be sent in batches)
        self._save_event(event)

    def _sanitize_properties(self, properties: Dict) -> Dict:
        """Remove any potentially sensitive information"""
        safe_keys = {
            "agent_count",
            "entropy_value",
            "regulation_action",
            "duration_seconds",
            "success",
            "error_type",
            "provider_type",
            "has_llm",
            "python_version",
            "os_type",
            "entropic_version",
        }

        return {
            k: v
            for k, v in properties.items()
            if k in safe_keys and not self._contains_pii(str(v))
        }

    def _contains_pii(self, value: str) -> bool:
        """Basic check for potential PII"""
        # Check for email-like patterns
        if "@" in value and "." in value:
            return True

        # Check for API key-like patterns
        if any(x in value.lower() for x in ["key", "token", "secret", "password"]):
            return True

        return False

    def _save_event(self, event: Dict):
        """Save event to local buffer"""
        events_file = (
            self.data_path / f'events_{datetime.now().strftime("%Y%m%d")}.jsonl'
        )

        with open(events_file, "a") as f:
            f.write(json.dumps(event) + "\n")

    def get_stats(self) -> Dict:
        """Get local usage statistics"""
        stats = {
            "enabled": self.enabled,
            "installation_id": self.installation_id[:8] + "...",  # Partial for privacy
            "events_collected": 0,
            "last_event": None,
        }

        if not self.enabled:
            return stats

        # Count events
        for events_file in self.data_path.glob("events_*.jsonl"):
            with open(events_file) as f:
                events = [line for line in f if line.strip()]
                stats["events_collected"] += len(events)

                if events:
                    last_event = json.loads(events[-1])
                    stats["last_event"] = last_event["timestamp"]

        return stats

    @staticmethod
    def enable():
        """Enable telemetry"""
        config_path = Path.home() / ".entropic" / "config.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config = {}
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)

        config["telemetry_enabled"] = True

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print("\n✅ Telemetry enabled!")
        print("   This helps us improve Entropic Core for everyone.")
        print("   No personal data is collected. Thank you! 🙏\n")

    @staticmethod
    def disable():
        """Disable telemetry"""
        config_path = Path.home() / ".entropic" / "config.json"

        config = {}
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)

        config["telemetry_enabled"] = False

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print("\n✅ Telemetry disabled.")
        print("   Your privacy is respected.\n")
