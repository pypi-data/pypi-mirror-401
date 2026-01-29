"""
Enhanced CLI with quickstart and setup commands
"""

import sys

import click


@click.group()
def cli():
    """Entropic Core - 100% FREE entropy regulation for multi-agent systems"""


@cli.command()
def quickstart():
    """
    🚀 Magical 30-second demo

    Experience Entropic Core's value immediately with zero configuration.
    Perfect for first-time users!
    """
    from entropic_core.quickstart import QuickstartDemo

    demo = QuickstartDemo()
    demo.run(duration_seconds=30)


@cli.command()
@click.option("--non-interactive", is_flag=True, help="Run without prompts")
def setup(non_interactive):
    """
    🛠️  Interactive setup wizard

    Automatically discovers available LLM providers and configures Entropic Core.
    Runs automatically on first use if needed.
    """
    from entropic_core.discovery import SetupWizard

    if non_interactive:
        import os

        os.environ["ENTROPIC_NON_INTERACTIVE"] = "1"

    wizard = SetupWizard()
    config = wizard.run()

    click.echo("\n✅ Setup complete!")
    click.echo(f"Provider: {config['provider']}")
    click.echo(f"Type: {config['type']}")

    if config["cost_per_1k_tokens"] == 0:
        cost_str = "FREE"
    else:
        cost_str = f"${config['cost_per_1k_tokens']}/1k tokens"

    click.echo(f"Cost: {cost_str}")


@cli.command()
def discover():
    """
    🔍 Discover available LLM providers

    Scans for local and cloud LLM providers and shows cost estimates.
    """
    from entropic_core.discovery import LLMDiscoverer

    discoverer = LLMDiscoverer()
    result = discoverer.discover_all()

    click.echo("\n" + "=" * 60)
    click.echo("🔍 LLM Provider Discovery")
    click.echo("=" * 60 + "\n")

    if not result["available"]:
        click.echo("❌ No providers found!")
        click.echo("\n💡 Install a provider:")
        click.echo("   • Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        click.echo("   • LM Studio: https://lmstudio.ai")
        click.echo("   • Get API key: https://groq.com (cheapest)")
        return

    click.echo(f"Found {result['available_count']} provider(s):\n")

    for provider in result["available"]:
        cost = (
            "FREE"
            if provider.cost_per_1k_tokens == 0
            else f"${provider.cost_per_1k_tokens}/1k"
        )
        marker = "⭐" if provider == result["recommended"] else "  "
        click.echo(f"{marker} {provider.name} ({provider.type}) - {cost}")
        if provider.endpoint:
            click.echo(f"   Endpoint: {provider.endpoint}")

    if result["recommended"]:
        click.echo(f"\n⭐ Recommended: {result['recommended'].name}")

    cost_info = result["estimated_monthly_cost"]
    click.echo(f"\n💰 Estimated monthly cost: ${cost_info['monthly_cost']}")
    click.echo(f"   Based on {cost_info['daily_tokens']:,} tokens/day")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=5000, help="Port to bind to")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def dashboard(host, port, debug):
    """
    📊 Launch the web dashboard

    Opens a browser-based dashboard with real-time entropy visualization.
    100% FREE - All features included.
    """
    try:
        from entropic_core.visualization.dashboard import EntropyDashboard

        click.echo(f"\n🚀 Starting Entropic Core Dashboard...")
        click.echo(f"   URL: http://{host}:{port}")
        click.echo("   Press Ctrl+C to stop\n")

        dashboard_instance = EntropyDashboard()
        dashboard_instance.run(host=host, port=port, debug=debug)

    except ImportError:
        click.echo("❌ Dashboard dependencies not installed!")
        click.echo("\n💡 Install with:")
        click.echo("   pip install entropic-core[visualization]")
        click.echo("\nThis includes: flask, plotly, pandas")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error starting dashboard: {e}")
        sys.exit(1)


@cli.command()
@click.argument("agents", type=int, default=3)
@click.option("--duration", default=60, help="Duration in seconds")
def monitor(agents, duration):
    """
    👁️  Monitor a simulated multi-agent system

    Creates N agents and monitors their entropy in real-time.
    """
    from entropic_core import EntropyBrain
    from entropic_core.core.agent_adapter import AgentAdapter

    click.echo(f"\n📡 Monitoring {agents} agents for {duration}s...")

    # Create mock agents
    agent_list = [
        AgentAdapter.create_mock_agent(
            agent_id=f"agent_{i}",
            behavior=(
                "balanced" if i % 3 == 0 else ("chaotic" if i % 3 == 1 else "ordered")
            ),
        )
        for i in range(agents)
    ]

    # Create brain
    brain = EntropyBrain(auto_regulate=True)
    brain.connect(agent_list)

    # Run monitoring
    try:
        brain.run(duration=float(duration))
    except KeyboardInterrupt:
        click.echo("\n👋 Monitoring stopped")
    finally:
        brain.close()


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["text", "json"]),
    default="text",
    help="Output format",
)
def diagnose(format):
    """
    🔍 Diagnose problems in your multi-agent system

    Scans for real problems reported by users:
    - Infinite loops
    - Memory leaks
    - API cost runaways
    - Race conditions
    - Thinking state freezes
    """
    try:
        import os

        from entropic_core import EntropyBrain
        from entropic_core.diagnosis import ProblemDetector

        if not os.path.exists("entropy_memory.db"):
            click.echo("\n⚠️  No active Entropic Core system found!")
            click.echo("\nStart monitoring first:")
            click.echo("  entropic-quickstart")
            click.echo("or")
            click.echo("  entropic-core monitor --agents 5 --duration 60")
            return

        # Create brain and detector
        brain = EntropyBrain()
        detector = ProblemDetector(brain)

        if format == "json":
            import json

            problems = detector.scan_for_problems()
            click.echo(json.dumps(problems, indent=2, default=str))
        else:
            report = detector.generate_diagnostic_report()
            click.echo(report)

    except ImportError as e:
        click.echo(f"❌ Missing dependencies: {e}")
        click.echo("\nInstall with:")
        click.echo("  pip install entropic-core[full]")
        sys.exit(1)


@cli.command()
@click.option(
    "--problem",
    type=click.Choice(
        [
            "infinite_loop",
            "memory_leak",
            "api_runaway",
            "race_condition",
            "thinking_freeze",
        ]
    ),
    required=True,
    help="Problem to fix",
)
@click.option("--output", type=click.Path(), help="Save fix script to file")
def fix(problem, output):
    """
    🔧 Get fix script for a specific problem

    Generates code to fix common multi-agent problems.
    Based on real solutions from GitHub issues.
    """
    from entropic_core.diagnosis import DiagnosticScripts

    fix_script = DiagnosticScripts.generate_fix_script(problem)

    if output:
        with open(output, "w") as f:
            f.write(fix_script)
        click.echo(f"✅ Fix script saved to {output}")
    else:
        click.echo("\n" + "=" * 60)
        click.echo(f"FIX SCRIPT: {problem.replace('_', ' ').title()}")
        click.echo("=" * 60)
        click.echo(fix_script)
        click.echo("=" * 60)
        click.echo("\nCopy this code into your project to fix the issue.")


@cli.command()
@click.argument("action", type=click.Choice(["enable", "disable", "status"]))
def telemetry(action):
    """
    📊 Manage anonymous telemetry

    Help improve Entropic Core by sharing anonymous usage data.
    We NEVER collect personal information, agent data, or API keys.
    """
    from entropic_core.telemetry import TelemetryCollector

    if action == "enable":
        TelemetryCollector.enable()
        click.echo("✅ Telemetry enabled")
        click.echo("\nThank you for helping improve Entropic Core!")
        click.echo("We collect only:")
        click.echo("  • Feature usage counts")
        click.echo("  • System performance metrics")
        click.echo("  • Error types (no sensitive data)")

    elif action == "disable":
        TelemetryCollector.disable()
        click.echo("✅ Telemetry disabled")

    elif action == "status":
        status = TelemetryCollector.get_status()
        click.echo(f"\nTelemetry: {'Enabled' if status['enabled'] else 'Disabled'}")
        if status["enabled"]:
            click.echo(f"Events collected: {status.get('event_count', 0)}")
            click.echo(f"Last sync: {status.get('last_sync', 'Never')}")


@cli.command()
def value():
    """
    💰 Calculate value generated by Entropic Core

    Shows estimated savings from prevented downtime and API waste.
    """
    import os

    from entropic_core import EntropyBrain

    if not os.path.exists("entropy_memory.db"):
        click.echo("\n⚠️  No usage data found. Start using Entropic Core first!")
        return

    brain = EntropyBrain()

    # Get metrics
    insights = brain.get_insights()
    recent_events = insights.get("recent_events", [])

    # Count interventions
    chaos_interventions = sum(
        1 for e in recent_events if e.get("event_type") == "REDUCE_CHAOS"
    )
    stagnation_interventions = sum(
        1 for e in recent_events if e.get("event_type") == "INCREASE_CHAOS"
    )
    total_cycles = len(recent_events)

    # Calculate value (conservative estimates)
    downtime_per_incident = 45  # minutes
    cost_per_hour_downtime = 5000  # dollars
    api_waste_per_incident = 500  # dollars

    prevented_downtime_hours = (chaos_interventions * downtime_per_incident) / 60
    saved_downtime = prevented_downtime_hours * cost_per_hour_downtime
    saved_api = chaos_interventions * api_waste_per_incident
    saved_stagnation = stagnation_interventions * 1000  # productivity loss

    total_saved = saved_downtime + saved_api + saved_stagnation

    click.echo("\n" + "=" * 60)
    click.echo("💰 VALUE CALCULATOR")
    click.echo("=" * 60)
    click.echo(f"\nTotal monitoring cycles: {total_cycles}")
    click.echo(f"Chaos interventions: {chaos_interventions}")
    click.echo(f"Stagnation interventions: {stagnation_interventions}")
    click.echo("\n" + "-" * 60)
    click.echo("ESTIMATED SAVINGS:")
    click.echo(f"  Prevented downtime: ${saved_downtime:,.0f}")
    click.echo(f"  Saved API costs: ${saved_api:,.0f}")
    click.echo(f"  Avoided stagnation: ${saved_stagnation:,.0f}")
    click.echo("-" * 60)
    click.echo(f"  TOTAL VALUE: ${total_saved:,.0f}")
    click.echo("=" * 60)
    click.echo("\n💡 These are conservative estimates based on industry averages.")
    click.echo("   Your actual savings may be higher.\n")

    brain.close()


@cli.command()
@click.option(
    "--output", type=click.Path(), default="diagnostic.py", help="Output file path"
)
def export_diagnostic(output):
    """
    📦 Export standalone diagnostic script

    Creates a single-file diagnostic script that can be shared or curl'd.
    """
    from entropic_core.diagnosis import DiagnosticScripts

    script = DiagnosticScripts.generate_curl_script()

    with open(output, "w") as f:
        f.write(script)

    click.echo(f"✅ Diagnostic script exported to {output}")
    click.echo("\nShare with others:")
    click.echo(f"  python {output}")
    click.echo("\nOr host and share as curl command:")
    click.echo(f"  curl -s https://your-domain.com/{output} | python3 -")


def main():
    """Main CLI entry point"""
    cli()


if __name__ == "__main__":
    main()
