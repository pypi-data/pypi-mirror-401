"""
Entropic Core - Core Modules
Basic entropy monitoring and regulation for multi-agent systems.

NEW IN 2.0: Game-changing features for REAL agent control!
"""

from .active_intervention import ActiveInterventionSystem  # Add alias
from .active_intervention import (
    InterventionBridge,
)  # Added missing InterventionBridge class
from .active_intervention import create_intervention_system  # Add alias
from .active_intervention import (
    ActiveInterventionEngine,
    InterventionConfig,
    InterventionEvent,
    InterventionType,
    create_intervention_engine,
)
from .agent_adapter import AgentAdapter
from .auto_healer import (
    AgentState,
    AutoHealer,
    Checkpoint,
    HealingAction,
    create_healer,
)
from .consensus_engine import (
    ConsensusEngine,
    ConsensusMethod,
    ConsensusResult,
    Vote,
    create_consensus_engine,
)
from .entropy_monitor import EntropyMonitor
from .entropy_regulator import EntropyRegulator
from .evolutionary_memory import EvolutionaryMemory
from .hallucination_detector import (
    HallucinationDetector,
    HallucinationReport,
    create_detector,
)
from .llm_middleware import (
    LLMMiddleware,
    LLMProvider,
    MiddlewareConfig,
    create_middleware,
    wrap_anthropic,
    wrap_openai,
)

__all__ = [
    # Original core
    "EntropyMonitor",
    "EntropyRegulator",
    "EvolutionaryMemory",
    "AgentAdapter",
    # Active Intervention
    "ActiveInterventionEngine",
    "ActiveInterventionSystem",
    "InterventionConfig",
    "InterventionType",
    "InterventionEvent",
    "InterventionBridge",  # Added to exports
    "create_intervention_engine",
    "create_intervention_system",
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
    "HealingAction",
    "create_healer",
    # Multi-Agent Consensus
    "ConsensusEngine",
    "ConsensusMethod",
    "ConsensusResult",
    "Vote",
    "create_consensus_engine",
]
