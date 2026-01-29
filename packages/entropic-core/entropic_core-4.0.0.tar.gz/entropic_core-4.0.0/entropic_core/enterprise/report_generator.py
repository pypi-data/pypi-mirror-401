"""
Generate compliance and audit reports for Entropic Core
"""

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generate reports for enterprise compliance and auditing.
    Supports markdown, HTML, and PDF formats.
    """

    def __init__(self, brain=None):
        """
        Initialize report generator

        Args:
            brain: EntropyBrain instance for pulling metrics
        """
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
        if format == "html":
            report = self._generate_html_content(**kwargs)
        elif format == "pdf":
            report = self._generate_pdf_content(**kwargs)
        else:
            report = self._generate_markdown_content(**kwargs)

        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            Path(output_file).write_text(report, encoding="utf-8")

        return report

    def _generate_markdown_content(self, **kwargs) -> str:
        """Generate markdown formatted report content"""
        lines = [
            "# Entropic Core Report",
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## System Health\n",
        ]

        if self.brain:
            try:
                entropy = self.brain.measure()
                lines.append(f"- Current Entropy: {entropy:.4f}")
                agent_count = (
                    len(self.brain.agents) if hasattr(self.brain, "agents") else 0
                )
                lines.append(f"- Active Agents: {agent_count}")
            except Exception as e:
                lines.append(f"- Error: {str(e)}")
        else:
            lines.append("- No brain instance connected")

        lines.append("\n## Summary\n")
        lines.append("System operating normally.")

        return "\n".join(lines)

    def _generate_html_content(self, **kwargs) -> str:
        """Generate HTML formatted report content"""
        markdown = self._generate_markdown_content(**kwargs)
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Entropic Core Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        pre {{ background: #f5f5f5; padding: 20px; }}
    </style>
</head>
<body>
<pre>{markdown}</pre>
</body>
</html>"""

    def _generate_pdf_content(self, **kwargs) -> str:
        """Generate PDF content (returns markdown as placeholder)"""
        return self._generate_markdown_content(**kwargs)

    def generate_daily_report(self, **kwargs) -> str:
        """Alias for backward compatibility"""
        return self._generate_markdown_content(**kwargs)

    def generate_html_report(self, **kwargs) -> str:
        """Alias for backward compatibility"""
        return self._generate_html_content(**kwargs)

    def generate_pdf_report(self, **kwargs) -> str:
        """Alias for backward compatibility"""
        return self._generate_pdf_content(**kwargs)
