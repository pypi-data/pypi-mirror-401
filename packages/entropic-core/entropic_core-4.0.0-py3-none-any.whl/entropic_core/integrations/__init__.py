"""
Entropic Core - Framework Integrations
Plug-and-play adapters for popular multi-agent frameworks
"""

from .autogen_adapter import AutoGenEntropyPlugin
from .crewai_adapter import CrewAIEntropyAdapter, CrewAIEntropyCallback
from .custom_builder import CustomAdapterBuilder
from .langchain_adapter import LangChainEntropyHandler
from .vercel_ai_adapter import VercelAIEntropyWrapper

__all__ = [
    "AutoGenEntropyPlugin",
    "LangChainEntropyHandler",
    "CustomAdapterBuilder",
    "CrewAIEntropyAdapter",
    "CrewAIEntropyCallback",
    "VercelAIEntropyWrapper",
]
