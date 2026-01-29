"""
Alert System for Critical Events
Sends notifications via multiple channels
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Callable, Dict, List


class AlertLevel(Enum):
    """Alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertSystem:
    """
    Multi-channel alert system
    Monitors entropy and triggers notifications
    """

    def __init__(self, brain):
        self.brain = brain
        self.handlers: List[Callable] = []
        self.alert_history: List[Dict] = []
        self.thresholds = {
            "critical_high": 0.85,
            "critical_low": 0.15,
            "warning_high": 0.75,
            "warning_low": 0.25,
        }
        self.logger = logging.getLogger(__name__)

    def add_handler(self, handler: Callable[[Dict], None]):
        """Add alert handler (email, slack, webhook, etc.)"""
        self.handlers.append(handler)

    def check_and_alert(self) -> List[Dict]:
        """Check system state and send alerts if needed"""
        alerts = []

        current_metrics = self.brain.monitor.measure_system_entropy(self.brain.agents)
        entropy = current_metrics["combined"]

        # Check critical thresholds
        if entropy > self.thresholds["critical_high"]:
            alert = self._create_alert(
                AlertLevel.CRITICAL,
                f"Critical entropy level: {entropy:.3f}",
                {
                    "entropy": entropy,
                    "metrics": current_metrics,
                    "recommendation": "Immediate stabilization required",
                },
            )
            alerts.append(alert)

        elif entropy < self.thresholds["critical_low"]:
            alert = self._create_alert(
                AlertLevel.CRITICAL,
                f"Critical stagnation: entropy {entropy:.3f}",
                {
                    "entropy": entropy,
                    "metrics": current_metrics,
                    "recommendation": "Inject innovation immediately",
                },
            )
            alerts.append(alert)

        # Check warning thresholds
        elif entropy > self.thresholds["warning_high"]:
            alert = self._create_alert(
                AlertLevel.WARNING,
                f"High entropy warning: {entropy:.3f}",
                {
                    "entropy": entropy,
                    "metrics": current_metrics,
                    "recommendation": "Monitor closely, prepare to stabilize",
                },
            )
            alerts.append(alert)

        elif entropy < self.thresholds["warning_low"]:
            alert = self._create_alert(
                AlertLevel.WARNING,
                f"Low entropy warning: {entropy:.3f}",
                {
                    "entropy": entropy,
                    "metrics": current_metrics,
                    "recommendation": "Consider increasing exploration",
                },
            )
            alerts.append(alert)

        # Check for prediction-based alerts
        if hasattr(self.brain, "predictor"):
            forecast = self.brain.predictor.forecast_system_health()
            if (
                forecast.get("time_to_collapse") and forecast["time_to_collapse"] < 600
            ):  # 10 minutes
                alert = self._create_alert(
                    AlertLevel.EMERGENCY,
                    f"System collapse predicted in {forecast['time_to_collapse']}s",
                    {
                        "forecast": forecast,
                        "recommendation": "Take preventive action now",
                    },
                )
                alerts.append(alert)

        # Send all alerts through handlers
        for alert in alerts:
            self._dispatch_alert(alert)

        return alerts

    def _create_alert(self, level: AlertLevel, message: str, details: Dict) -> Dict:
        """Create alert object"""
        alert = {
            "id": len(self.alert_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "level": level.value,
            "message": message,
            "details": details,
        }

        self.alert_history.append(alert)
        return alert

    def _dispatch_alert(self, alert: Dict):
        """Send alert through all registered handlers"""
        for handler in self.handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.error(f"Error dispatching alert: {e}")

    def get_alert_history(self, hours: int = 24) -> List[Dict]:
        """Get alert history for specified hours"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        return [
            alert
            for alert in self.alert_history
            if datetime.fromisoformat(alert["timestamp"]).timestamp() > cutoff
        ]

    # Built-in handlers
    @staticmethod
    def console_handler(alert: Dict):
        """Simple console logger handler"""
        level_emoji = {"info": "ℹ️", "warning": "⚠️", "critical": "🚨", "emergency": "🆘"}
        emoji = level_emoji.get(alert["level"], "📢")
        print(f"\n{emoji} [{alert['level'].upper()}] {alert['timestamp']}")
        print(f"   {alert['message']}")
        if "recommendation" in alert["details"]:
            print(f"   → {alert['details']['recommendation']}")

    @staticmethod
    def log_handler(alert: Dict):
        """Logging handler"""
        logger = logging.getLogger("entropic_core.alerts")
        level_map = {
            "info": logging.INFO,
            "warning": logging.WARNING,
            "critical": logging.CRITICAL,
            "emergency": logging.CRITICAL,
        }
        logger.log(
            level_map.get(alert["level"], logging.INFO),
            f"{alert['message']} | {alert['details']}",
        )
