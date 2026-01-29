"""Example plugin: Slack notifications for entropy events."""

import requests

from ..plugin_api import EntropyPlugin, PluginContext


class SlackNotifierPlugin(EntropyPlugin):
    """Send Slack notifications when entropy exceeds thresholds."""

    @property
    def name(self) -> str:
        return "slack_notifier"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Sends Slack notifications for critical entropy events"

    @property
    def author(self) -> str:
        return "Entropic Core Team"

    def initialize(self) -> bool:
        """Initialize Slack webhook."""
        self.webhook_url = self.config.get("webhook_url")
        self.threshold = self.config.get("threshold", 0.8)
        self.channel = self.config.get("channel", "#entropy-alerts")

        if not self.webhook_url:
            self.logger.error("Slack webhook URL not configured")
            return False

        return super().initialize()

    def on_entropy_measured(self, context: PluginContext) -> None:
        """Check entropy and send alert if needed."""
        if context.entropy_value > self.threshold:
            message = self._format_alert_message(context)
            self._send_slack_message(message)

    def _format_alert_message(self, context: PluginContext) -> str:
        """Format alert message."""
        return f"""
🚨 *High Entropy Alert*
Current Entropy: `{context.entropy_value:.3f}`
Threshold: `{self.threshold}`
Agents Affected: `{len(context.agents_state)}`
Timestamp: `{context.timestamp}`
        """.strip()

    def _send_slack_message(self, message: str) -> None:
        """Send message to Slack."""
        try:
            response = requests.post(
                self.webhook_url,
                json={
                    "channel": self.channel,
                    "text": message,
                    "username": "Entropic Core Bot",
                    "icon_emoji": ":robot_face:",
                },
                timeout=5,
            )
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Failed to send Slack message: {e}")
