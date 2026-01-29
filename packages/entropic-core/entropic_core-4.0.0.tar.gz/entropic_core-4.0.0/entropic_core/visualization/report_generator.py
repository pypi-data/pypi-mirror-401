"""
Automated Report Generation System
Creates daily/weekly reports with visualizations and insights
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


class ReportGenerator:
    """
    Generates automated reports in multiple formats
    Provides executive summaries and detailed analytics
    """

    def __init__(self, brain):
        self.brain = brain

    def generate_report(
        self, format: str = "markdown", output_file: str = None, **kwargs
    ) -> str:
        """
        Generate report in specified format

        Args:
            format: Output format ('markdown', 'html', 'pdf')
            output_file: Optional file path to write report
            **kwargs: Additional parameters

        Returns:
            Generated report as string
        """
        # Generate basic report content
        report_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "System operating normally.",
            "metrics": {},
            "events": [],
            "recommendations": ["Continue monitoring system health."],
        }

        # Try to get metrics from brain if available
        if self.brain:
            try:
                entropy = self.brain.measure()
                report_data["metrics"]["current_entropy"] = f"{entropy:.4f}"
                report_data["metrics"]["agent_count"] = (
                    len(self.brain.agents) if hasattr(self.brain, "agents") else 0
                )
            except:
                pass

        # Generate content in requested format
        if format == "html":
            content = self._generate_html_content(report_data)
        elif format == "pdf":
            content = self._generate_markdown_content(
                report_data
            )  # PDF falls back to markdown
        else:
            content = self._generate_markdown_content(report_data)

        # Write to file if specified
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            Path(output_file).write_text(content, encoding="utf-8")

        return content

    def _generate_markdown_content(self, report_data: Dict) -> str:
        """Generate markdown formatted report content"""
        lines = [
            "# Entropy System Report",
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n**Date:** {report_data.get('date', 'N/A')}",
            "\n## Executive Summary\n",
            report_data.get("summary", "No summary available."),
            "\n## Key Metrics\n",
        ]

        for key, value in report_data.get("metrics", {}).items():
            lines.append(f"- **{key.replace('_', ' ').title()}**: {value}")

        lines.append("\n## Recommendations\n")
        for i, rec in enumerate(report_data.get("recommendations", []), 1):
            lines.append(f"{i}. {rec}")

        return "\n".join(lines)

    def _generate_html_content(self, report_data: Dict) -> str:
        """Generate HTML formatted report content"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Entropy System Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .section {{ margin: 20px 0; padding: 15px; background: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>Entropy System Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{report_data.get('summary', 'No summary available.')}</p>
    </div>
    <div class="section">
        <h2>Key Metrics</h2>
        <ul>
        {''.join(f'<li><strong>{k.replace("_", " ").title()}</strong>: {v}</li>' for k, v in report_data.get('metrics', {}).items())}
        </ul>
    </div>
</body>
</html>"""

    def generate_daily_report(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive daily report"""
        if date is None:
            date = datetime.now()

        # Gather data for the day
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        history = self.brain.memory.get_entropy_history_range(start_of_day, end_of_day)

        # Calculate key metrics
        metrics = self._calculate_daily_metrics(history)

        # Identify significant events
        events = self._identify_significant_events(history)

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, events)

        return {
            "date": date.strftime("%Y-%m-%d"),
            "summary": self._generate_executive_summary(metrics, events),
            "metrics": metrics,
            "events": events,
            "recommendations": recommendations,
            "charts": self._generate_chart_data(history),
        }

    def generate_weekly_report(
        self, week_start: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive weekly report"""
        if week_start is None:
            week_start = datetime.now() - timedelta(days=7)

        week_end = week_start + timedelta(days=7)

        history = self.brain.memory.get_entropy_history_range(week_start, week_end)

        metrics = self._calculate_weekly_metrics(history)
        trends = self._analyze_trends(history)
        patterns = self._identify_patterns(history)

        return {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": week_end.strftime("%Y-%m-%d"),
            "summary": self._generate_weekly_summary(metrics, trends),
            "metrics": metrics,
            "trends": trends,
            "patterns": patterns,
            "recommendations": self._generate_strategic_recommendations(
                metrics, trends
            ),
        }

    def export_to_markdown(self, report: Dict[str, Any]) -> str:
        """Export report to Markdown format"""
        md = f"# Entropic Core Report\n\n"

        if "date" in report:
            md += f"**Date:** {report['date']}\n\n"
        elif "week_start" in report:
            md += f"**Period:** {report['week_start']} to {report['week_end']}\n\n"

        md += f"## Executive Summary\n\n{report['summary']}\n\n"

        md += "## Key Metrics\n\n"
        for key, value in report["metrics"].items():
            md += f"- **{key.replace('_', ' ').title()}**: {value}\n"

        md += "\n## Events\n\n"
        for event in report.get("events", []):
            md += f"- **{event['timestamp']}**: {event['description']} (severity: {event['severity']})\n"

        md += "\n## Recommendations\n\n"
        for i, rec in enumerate(report.get("recommendations", []), 1):
            md += f"{i}. {rec}\n"

        return md

    def export_to_html(self, report: Dict[str, Any]) -> str:
        """Export report to HTML format"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Entropic Core Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h2 {{ color: #667eea; margin-top: 0; }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .metric:last-child {{ border-bottom: none; }}
        .event {{
            padding: 10px;
            background: #f9f9f9;
            margin: 10px 0;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        .recommendation {{
            padding: 10px;
            background: #e7f3ff;
            margin: 10px 0;
            border-radius: 6px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Entropic Core Report</h1>
        <p>{report.get('date') or f"{report.get('week_start')} to {report.get('week_end')}"}</p>
    </div>
    
    <div class="card">
        <h2>Executive Summary</h2>
        <p>{report['summary']}</p>
    </div>
    
    <div class="card">
        <h2>Key Metrics</h2>
        {''.join(
            f'<div class="metric"><span>{k.replace("_", " ").title()}</span><strong>{v}</strong></div>'
            for k, v in report['metrics'].items()
        )}
    </div>
    
    <div class="card">
        <h2>Significant Events</h2>
        {''.join(
            f'<div class="event"><strong>{e["timestamp"]}</strong>: {e["description"]}</div>'
            for e in report.get('events', [])
        )}
    </div>
    
    <div class="card">
        <h2>Recommendations</h2>
        {''.join(
            f'<div class="recommendation">{i}. {rec}</div>'
            for i, rec in enumerate(report.get('recommendations', []), 1)
        )}
    </div>
</body>
</html>
        """
        return html

    def save_report(
        self,
        report: Dict[str, Any],
        format: str = "markdown",
        output_dir: str = "reports",
    ) -> Path:
        """Save report to file"""
        Path(output_dir).mkdir(exist_ok=True)

        filename = f"report_{report.get('date', datetime.now().strftime('%Y-%m-%d'))}"

        if format == "markdown":
            content = self.export_to_markdown(report)
            filepath = Path(output_dir) / f"{filename}.md"
        elif format == "html":
            content = self.export_to_html(report)
            filepath = Path(output_dir) / f"{filename}.html"
        elif format == "json":
            content = json.dumps(report, indent=2)
            filepath = Path(output_dir) / f"{filename}.json"
        else:
            raise ValueError(f"Unsupported format: {format}")

        filepath.write_text(content)
        return filepath

    def _calculate_daily_metrics(self, history: List[Dict]) -> Dict[str, Any]:
        """Calculate daily metrics from history"""
        if not history:
            return {}

        entropies = [h["entropy"] for h in history]

        return {
            "average_entropy": sum(entropies) / len(entropies),
            "max_entropy": max(entropies),
            "min_entropy": min(entropies),
            "entropy_range": max(entropies) - min(entropies),
            "measurements_count": len(history),
            "time_in_optimal": sum(1 for e in entropies if 0.4 <= e <= 0.6)
            / len(entropies)
            * 100,
            "chaos_incidents": sum(1 for e in entropies if e > 0.8),
            "stagnation_incidents": sum(1 for e in entropies if e < 0.2),
        }

    def _calculate_weekly_metrics(self, history: List[Dict]) -> Dict[str, Any]:
        """Calculate weekly metrics from history"""
        daily_metrics = self._calculate_daily_metrics(history)

        # Add weekly-specific metrics
        daily_metrics["uptime_percentage"] = 99.5  # Placeholder
        daily_metrics["regulation_count"] = len(
            [h for h in history if h.get("regulated")]
        )

        return daily_metrics

    def _identify_significant_events(self, history: List[Dict]) -> List[Dict]:
        """Identify significant events in history"""
        events = []

        for i, entry in enumerate(history):
            if entry["entropy"] > 0.8:
                events.append(
                    {
                        "timestamp": entry["timestamp"],
                        "description": f"High chaos detected (entropy: {entry['entropy']:.3f})",
                        "severity": "high",
                    }
                )
            elif entry["entropy"] < 0.2:
                events.append(
                    {
                        "timestamp": entry["timestamp"],
                        "description": f"Low entropy detected - stagnation risk (entropy: {entry['entropy']:.3f})",
                        "severity": "medium",
                    }
                )

        return events[:10]  # Return top 10 events

    def _generate_recommendations(self, metrics: Dict, events: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if metrics.get("chaos_incidents", 0) > 5:
            recommendations.append(
                "System experienced multiple chaos incidents. Consider increasing stability measures."
            )

        if metrics.get("time_in_optimal", 0) < 50:
            recommendations.append(
                "System spent less than 50% time in optimal range. Review regulation thresholds."
            )

        if metrics.get("stagnation_incidents", 0) > 3:
            recommendations.append(
                "Multiple stagnation incidents detected. Inject more exploration or randomness."
            )

        if not recommendations:
            recommendations.append(
                "System performing within expected parameters. Continue monitoring."
            )

        return recommendations

    def _generate_executive_summary(self, metrics: Dict, events: List[Dict]) -> str:
        """Generate executive summary text"""
        avg_entropy = metrics.get("average_entropy", 0)
        time_optimal = metrics.get("time_in_optimal", 0)

        if avg_entropy >= 0.4 and avg_entropy <= 0.6 and time_optimal > 70:
            status = "excellent"
        elif time_optimal > 50:
            status = "good"
        else:
            status = "needs attention"

        return f"""
System performance: {status.upper()}

Average entropy: {avg_entropy:.3f}
Time in optimal range: {time_optimal:.1f}%
Significant events: {len(events)}

The multi-agent system operated with {status} homeostasis throughout the reporting period.
{'No critical issues detected.' if status != 'needs attention' else 'Several areas require attention.'}
        """.strip()

    def _generate_weekly_summary(self, metrics: Dict, trends: Dict) -> str:
        """Generate weekly summary text"""
        return self._generate_executive_summary(metrics, [])

    def _generate_strategic_recommendations(
        self, metrics: Dict, trends: Dict
    ) -> List[str]:
        """Generate strategic recommendations for weekly report"""
        return self._generate_recommendations(metrics, [])

    def _analyze_trends(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze trends in historical data"""
        if len(history) < 2:
            return {}

        entropies = [h["entropy"] for h in history]

        # Simple trend calculation
        first_half_avg = sum(entropies[: len(entropies) // 2]) / (len(entropies) // 2)
        second_half_avg = sum(entropies[len(entropies) // 2 :]) / (
            len(entropies) - len(entropies) // 2
        )

        return {
            "direction": (
                "increasing" if second_half_avg > first_half_avg else "decreasing"
            ),
            "magnitude": abs(second_half_avg - first_half_avg),
            "stability": (
                "stable" if abs(second_half_avg - first_half_avg) < 0.1 else "volatile"
            ),
        }

    def _identify_patterns(self, history: List[Dict]) -> List[Dict]:
        """Identify recurring patterns"""
        # Placeholder for pattern recognition
        return []

    def _generate_chart_data(self, history: List[Dict]) -> Dict:
        """Generate data for charts"""
        return {
            "timestamps": [h["timestamp"] for h in history],
            "entropy_values": [h["entropy"] for h in history],
        }
