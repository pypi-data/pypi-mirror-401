"""
Telemetry Reporter - Generates reports from collected telemetry data
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional
from entropic_core.telemetry.collector import TelemetryCollector


class TelemetryReporter:
    """
    Generates human-readable reports from telemetry data.
    """

    def __init__(self, collector: "TelemetryCollector"):
        """
        Initialize the reporter with a telemetry collector.

        Args:
            collector: TelemetryCollector instance to read data from
        """
        self.collector = collector

    def generate_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Generate a summary report of telemetry data.

        Args:
            days: Number of days to include in the report

        Returns:
            Dictionary containing summary statistics
        """
        events = self.collector.get_events(days=days)

        if not events:
            return {
                "period": f"Last {days} days",
                "total_events": 0,
                "message": "No telemetry data available",
            }

        # Count events by type
        event_counts = {}
        for event in events:
            event_type = event.get("event_type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Calculate metrics
        total_events = len(events)
        start_date = min(e.get("timestamp", datetime.now().isoformat()) for e in events)
        end_date = max(e.get("timestamp", datetime.now().isoformat()) for e in events)

        return {
            "period": f"Last {days} days",
            "start_date": start_date,
            "end_date": end_date,
            "total_events": total_events,
            "events_by_type": event_counts,
            "avg_events_per_day": total_events / days if days > 0 else 0,
        }

    def generate_detailed_report(self, days: int = 30) -> str:
        """
        Generate a detailed text report.

        Args:
            days: Number of days to include in the report

        Returns:
            Formatted text report
        """
        summary = self.generate_summary(days)

        report = []
        report.append("=" * 60)
        report.append("ENTROPIC CORE TELEMETRY REPORT")
        report.append("=" * 60)
        report.append(f"\nPeriod: {summary['period']}")
        report.append(f"Total Events: {summary['total_events']}")

        if summary["total_events"] > 0:
            report.append(f"Start Date: {summary['start_date']}")
            report.append(f"End Date: {summary['end_date']}")
            report.append(f"Average Events/Day: {summary['avg_events_per_day']:.2f}")

            report.append("\n" + "-" * 60)
            report.append("Events by Type:")
            report.append("-" * 60)

            for event_type, count in sorted(summary["events_by_type"].items()):
                percentage = (count / summary["total_events"]) * 100
                report.append(f"  {event_type}: {count} ({percentage:.1f}%)")
        else:
            report.append(f"\n{summary['message']}")

        report.append("\n" + "=" * 60)

        return "\n".join(report)

    def export_json(self, days: int = 30, output_file: Optional[str] = None) -> str:
        """
        Export telemetry data as JSON.

        Args:
            days: Number of days to include
            output_file: Optional file path to write JSON to

        Returns:
            JSON string of telemetry data
        """
        data = {
            "generated_at": datetime.now().isoformat(),
            "period_days": days,
            "summary": self.generate_summary(days),
            "events": self.collector.get_events(days=days),
        }

        json_str = json.dumps(data, indent=2)

        if output_file:
            with open(output_file, "w") as f:
                f.write(json_str)

        return json_str
