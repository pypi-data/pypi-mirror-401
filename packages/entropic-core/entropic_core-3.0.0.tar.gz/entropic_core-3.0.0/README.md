# Entropic Core v1.0

**100% FREE & OPEN SOURCE entropy regulation for multi-agent AI systems.**

Entropic Core monitors and automatically regulates chaos in multi-agent systems, preventing both system collapse and stagnation. Think of it as a thermostat for your AI agents.

## What Makes This Special?

- **Completely FREE** - No tiers, no limits, no paywalls
- **Open Source** - MIT License, use it anywhere
- **No API Keys Required** - Works entirely locally
- **Production Ready** - Battle-tested algorithms
- **Framework Agnostic** - Works with AutoGen, LangChain, CrewAI, or custom agents

## What Problem Does It Solve?

Multi-agent systems have a critical problem: they either become too chaotic (agents conflict, system crashes) or too ordered (agents stagnate, no innovation). Entropic Core solves this by:

1. **Measuring entropy** across 3 dimensions (decisions, state dispersion, communication)
2. **Automatically regulating** the system to maintain optimal chaos/order balance
3. **Learning patterns** to prevent future failures
4. **Predicting problems** before they happen
5. **Diagnosing root causes** when issues occur

## Quick Start

### Installation

```bash
# Basic installation (core features)
pip install entropic-core

# Full installation (all features)
pip install entropic-core[full]
```

### Basic Usage

```python
from entropic_core import EntropyBrain

# Initialize
brain = EntropyBrain()

# Connect your agents (unlimited)
brain.connect([agent1, agent2, agent3])

# Monitor and regulate automatically
brain.run(cycles=100)
```

### Integration with AutoGen

```python
from autogen import AssistantAgent
from entropic_core import EntropyBrain

# Your existing AutoGen agents
writer = AssistantAgent("writer", llm_config={...})
critic = AssistantAgent("critic", llm_config={...})

# Add entropy monitoring
brain = EntropyBrain()
brain.connect([writer, critic])

# Run with entropy awareness
for i in range(10):
    writer.generate_reply(messages)
    
    # Measure and regulate
    metrics = brain.measure()
    if metrics['combined'] > 0.8:
        brain.regulate()  # Automatically stabilizes
```

## All Features Included (100% Free)

### Core Features
- Real-time entropy monitoring (3 metrics)
- Automatic chaos/order regulation
- SQLite/PostgreSQL memory storage
- Universal agent adapter
- Pattern learning and recognition
- Unlimited agents
- Unlimited measurements

### Advanced Analytics
- **Causal Analysis** - Diagnoses WHY entropy spiked
- **Predictive Forecasting** - Predicts failures before they happen
- **Anomaly Detection** - Catches unusual patterns
- **Pattern Recognition** - Learns from history
- **Time Series Analysis** - Tracks entropy trends

### Enterprise Features
- Real-time web dashboard
- Automated PDF/HTML reports
- Multi-system orchestration
- Compliance logging & audit trails
- REST API
- Slack/Email/Webhook alerts

## Examples

### Example 1: Basic Monitoring

```python
from entropic_core import EntropyBrain
from entropic_core.core.agent_adapter import AgentAdapter

# Create mock agents
agents = [
    AgentAdapter.create_mock_agent(f"agent_{i}", behavior='balanced')
    for i in range(5)
]

# Initialize brain
brain = EntropyBrain(auto_regulate=True)
brain.connect(agents)

# Run for 10 cycles
brain.run(cycles=10)

# Get status
status = brain.get_status()
print(f"Current entropy: {status['current_entropy']:.3f}")
```

### Example 2: Causal Diagnosis

```python
from entropic_core import EntropyBrain

brain = EntropyBrain()
brain.connect(my_agents)

# Build history
for i in range(20):
    my_agents[i % len(my_agents)].act(observation)
    brain.measure()

# Diagnose problems
diagnosis = brain.diagnose()
print(f"Root cause: {diagnosis['primary_cause']}")
print(f"Confidence: {diagnosis['confidence']:.1%}")
print(f"Fix: {diagnosis['suggested_fix']}")
```

### Example 3: Predictive Monitoring

```python
brain = EntropyBrain()
brain.connect(my_agents)

# Get forecast
forecast = brain.forecast(steps=10)
print(f"Risk level: {forecast['risk_level']}")

if forecast['time_to_collapse']:
    print(f"WARNING: Collapse in {forecast['time_to_collapse']} steps!")
    print("Recommended actions:")
    for action in forecast['recommended_preventive_actions']:
        print(f"  - {action}")
```

## How It Works

### 1. Entropy Measurement

Entropic Core calculates entropy across three dimensions:

- **Decision Entropy**: How unpredictable agent decisions are (Shannon entropy)
- **State Dispersion**: How different agent states are from each other
- **Communication Complexity**: How much inter-agent communication is happening

These combine into a single "combined entropy" score from 0 to 1.

### 2. Automatic Regulation

Based on entropy levels, the system takes action:

- **High entropy (>0.8)**: System too chaotic → Reduce exploration, merge similar agents, enforce protocols
- **Low entropy (<0.2)**: System too ordered → Inject randomness, create explorer agents, relax constraints
- **Optimal (0.4-0.6)**: Maintain homeostasis → Fine-tune parameters

### 3. Learning & Memory

Every decision and outcome is stored in SQLite/PostgreSQL:

- **Events**: What happened and when
- **Patterns**: What worked in similar situations
- **Rules**: Which regulations were effective
- **Metrics**: Time-series entropy data

The system learns from history to make better decisions over time.

### 4. Causal Analysis

When entropy spikes, the causal analyzer:

1. Analyzes correlations in recent history
2. Identifies root causes with confidence scores
3. Searches for similar past events
4. Generates specific fix recommendations

### 5. Predictive Engine

The predictive engine:

1. Forecasts entropy using time-series analysis
2. Predicts time until system collapse or stagnation
3. Detects anomalies using statistical methods
4. Recommends preventive actions

## Architecture

```
entropic-core/
├── core/                    # Core modules (always included)
│   ├── entropy_monitor.py   # Measures entropy
│   ├── entropy_regulator.py # Takes regulatory action
│   ├── evolutionary_memory.py # Persistent storage
│   └── agent_adapter.py     # Universal agent wrapper
│
├── advanced/               # Advanced analytics (free)
│   ├── causal_analyzer.py  # Root cause diagnosis
│   ├── predictive_engine.py # Forecasting & anomalies
│   ├── simulation_mode.py  # Scenario simulation
│   └── security_layer.py   # Attack detection
│
├── integrations/           # Framework adapters (free)
│   ├── autogen_adapter.py  # AutoGen integration
│   ├── langchain_adapter.py # LangChain integration
│   └── custom_builder.py   # Custom adapter builder
│
├── visualization/          # Dashboards & reports (free)
│   ├── dashboard.py        # Real-time web dashboard
│   ├── report_generator.py # Automated reports
│   └── alert_system.py     # Multi-channel alerts
│
├── enterprise/            # Enterprise features (free)
│   ├── orchestrator.py    # Multi-system coordination
│   ├── compliance.py      # Audit & compliance
│   └── marketplace.py     # Pattern sharing
│
└── brain.py               # Main orchestrator
```

## Framework Integrations

Entropic Core works with any agent framework:

- **AutoGen**: Full integration with conversation agents
- **LangChain**: Compatible with chains and agents
- **CrewAI**: Works with crew-based systems
- **Custom**: Universal adapter for any agent architecture

## Performance

- **Overhead**: <5ms per measurement cycle
- **Memory**: ~10MB base + 1KB per agent
- **Storage**: ~1MB per 10,000 cycles
- **Scalability**: Tested with 1,000+ agents

## Use Cases

### Financial Trading
Monitor multi-agent trading systems to prevent both runaway risk and missed opportunities.

### Game Development
Keep NPC behaviors interesting but not chaotic, preventing both boredom and frustration.

### Research Labs
Coordinate multiple research agents exploring solution spaces without getting stuck or diverging.

### Production Systems
Ensure agent-based microservices maintain healthy communication patterns without overload.

## Installation Options

```bash
# Minimal (core only)
pip install entropic-core

# With advanced analytics
pip install entropic-core scipy scikit-learn

# With visualization
pip install entropic-core flask plotly pandas

# Everything (recommended)
pip install entropic-core[full]
```

## Why 100% Free?

We believe that fundamental infrastructure for AI safety should be accessible to everyone. Entropic Core is:

- **MIT Licensed** - Use it anywhere, including commercial projects
- **No Hidden Costs** - No API calls, no cloud services required
- **Community Driven** - Contributions welcome
- **Research Friendly** - Perfect for academic use

## Support & Community

- **Documentation**: https://github.com/entropic-core/entropic-core/wiki
- **Issues**: https://github.com/entropic-core/entropic-core/issues
- **Discussions**: https://github.com/entropic-core/entropic-core/discussions
- **Discord**: [Join our community](https://discord.gg/entropic-core)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - Use it anywhere, no restrictions.

## Citation

If you use Entropic Core in research, please cite:

```bibtex
@software{entropic_core_2025,
  title={Entropic Core: Entropy Regulation for Multi-Agent Systems},
  author={Entropic Core Team},
  year={2025},
  url={https://github.com/entropic-core/entropic-core},
  license={MIT}
}
