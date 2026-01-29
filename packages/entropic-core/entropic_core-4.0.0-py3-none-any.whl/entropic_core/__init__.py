"""
Entropic Core - Sistema de monitoreo y regulación de entropía para sistemas multiagente
Version: 3.0.0

100% Free and Open Source - All features available to everyone.

NEW IN 3.0: GAME-CHANGER FEATURES
- Universal LLM Middleware - Works with ANY provider (OpenAI, Anthropic, LangChain, etc.)
- Hallucination Detection - Real-time hallucination prevention
- Auto-Healing - Self-recovering agents with checkpoints and rollback
- Multi-Agent Consensus - Entropy-weighted voting for agent decisions

NEW IN 3.0: UNICORN FEATURES
- Auto-Discovery - Zero-config protection with just protect()
- Live Dashboard - Real-time WebSocket metrics streaming
- Business Metrics - ROI tracking and cost optimization
"""

from .brain import EntropyBrain, create_entropic_brain

# Business Metrics (ROI tracking)
from .business.metrics import (
    BusinessMetrics,
    BusinessMetricsConfig,
    ROISummary,
    create_metrics,
)
from .config import Config, Tier

# Active Intervention
from .core.active_intervention import (
    ActiveInterventionEngine,
    InterventionBridge,
    InterventionConfig,
    InterventionType,
    create_intervention_engine,
    wrap_openai_client,
)
from .core.agent_adapter import AgentAdapter

# Auto-Healing
from .core.auto_healer import AgentState, AutoHealer, Checkpoint, create_healer

# Multi-Agent Consensus
from .core.consensus_engine import (
    ConsensusEngine,
    ConsensusMethod,
    ConsensusResult,
    Vote,
    create_consensus_engine,
)

# Core modules (always available)
from .core.entropy_monitor import EntropyMonitor
from .core.entropy_regulator import EntropyRegulator
from .core.evolutionary_memory import EvolutionaryMemory

# Hallucination Detection
from .core.hallucination_detector import (
    HallucinationDetector,
    HallucinationReport,
    create_detector,
)

# Universal LLM Middleware
from .core.llm_middleware import (
    LLMMiddleware,
    LLMProvider,
    MiddlewareConfig,
    create_middleware,
    wrap_anthropic,
    wrap_openai,
)

# Auto-Discovery (Zero-config protection)
from .discovery.auto_discover import (
    AutoDiscovery,
    get_discovery,
    get_protection_stats,
    protect,
    unprotect,
)

# Live Dashboard (Real-time WebSocket)
from .realtime.live_dashboard import DashboardConfig, LiveDashboard, create_dashboard

__version__ = "3.0.0"
__all__ = [
    # Main brain
    "EntropyBrain",
    "create_entropic_brain",
    # Core modules
    "EntropyMonitor",
    "EntropyRegulator",
    "EvolutionaryMemory",
    "AgentAdapter",
    # Active Intervention
    "ActiveInterventionEngine",
    "InterventionConfig",
    "InterventionType",
    "InterventionBridge",
    "create_intervention_engine",
    "wrap_openai_client",
    # Universal LLM Middleware
    "LLMMiddleware",
    "LLMProvider",
    "MiddlewareConfig",
    "create_middleware",
    "wrap_openai",
    "wrap_anthropic",
    # Hallucination Detection
    "HallucinationDetector",
    "HallucinationReport",
    "create_detector",
    # Auto-Healing
    "AutoHealer",
    "AgentState",
    "Checkpoint",
    "create_healer",
    # Multi-Agent Consensus
    "ConsensusEngine",
    "ConsensusMethod",
    "ConsensusResult",
    "Vote",
    "create_consensus_engine",
    # Auto-Discovery
    "AutoDiscovery",
    "protect",
    "unprotect",
    "get_discovery",
    "get_protection_stats",
    # Live Dashboard
    "LiveDashboard",
    "DashboardConfig",
    "create_dashboard",
    # Business Metrics
    "BusinessMetrics",
    "BusinessMetricsConfig",
    "ROISummary",
    "create_metrics",
    # Config
    "Config",
    "Tier",
]

# Advanced modules (always available - 100% free)
try:
    pass

    __all__.extend(["CausalAnalyzer", "PredictiveEngine", "EntropySecurity"])
except ImportError:
    pass
