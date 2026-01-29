"""
Automatic LLM Discovery System
Detects available LLMs without requiring manual configuration
"""

import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class LLMProvider:
    """Represents an available LLM provider"""

    name: str
    type: str  # 'local', 'api', 'cloud'
    available: bool
    cost_per_1k_tokens: float
    setup_url: str
    api_key_required: bool
    endpoint: Optional[str] = None


class LLMDiscoverer:
    """
    Automatically discovers available LLM providers
    Prioritizes: Local > Free APIs > Paid APIs
    """

    def __init__(self):
        self.providers: List[LLMProvider] = []

    def discover_all(self) -> Dict:
        """
        Scan for all available LLM providers
        Returns recommendations based on cost and availability
        """
        logger.info("🔍 Discovering available LLM providers...")

        # Check local models first (zero cost)
        self._check_ollama()
        self._check_lm_studio()
        self._check_llamacpp()

        # Check API keys in environment
        self._check_openai()
        self._check_anthropic()
        self._check_groq()

        # Check free/cheap alternatives
        self._check_openrouter()
        self._check_together()

        available = [p for p in self.providers if p.available]

        return {
            "available": available,
            "recommended": self._get_recommendation(available),
            "total_providers": len(self.providers),
            "available_count": len(available),
            "estimated_monthly_cost": self._estimate_cost(available),
        }

    def _check_ollama(self):
        """Check if Ollama is running locally"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                self.providers.append(
                    LLMProvider(
                        name="Ollama",
                        type="local",
                        available=len(models) > 0,
                        cost_per_1k_tokens=0.0,
                        setup_url="https://ollama.ai/download",
                        api_key_required=False,
                        endpoint="http://localhost:11434",
                    )
                )
                logger.info(f"✅ Ollama found with {len(models)} models")
        except Exception as e:
            self.providers.append(
                LLMProvider(
                    name="Ollama",
                    type="local",
                    available=False,
                    cost_per_1k_tokens=0.0,
                    setup_url="https://ollama.ai/download",
                    api_key_required=False,
                )
            )
            logger.debug(f"Ollama not available: {e}")

    def _check_lm_studio(self):
        """Check if LM Studio is running"""
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=2)
            if response.status_code == 200:
                self.providers.append(
                    LLMProvider(
                        name="LM Studio",
                        type="local",
                        available=True,
                        cost_per_1k_tokens=0.0,
                        setup_url="https://lmstudio.ai",
                        api_key_required=False,
                        endpoint="http://localhost:1234",
                    )
                )
                logger.info("✅ LM Studio found")
        except Exception:
            self.providers.append(
                LLMProvider(
                    name="LM Studio",
                    type="local",
                    available=False,
                    cost_per_1k_tokens=0.0,
                    setup_url="https://lmstudio.ai",
                    api_key_required=False,
                )
            )

    def _check_llamacpp(self):
        """Check if llama.cpp server is running"""
        try:
            response = requests.get("http://localhost:8080/health", timeout=2)
            if response.status_code == 200:
                self.providers.append(
                    LLMProvider(
                        name="llama.cpp",
                        type="local",
                        available=True,
                        cost_per_1k_tokens=0.0,
                        setup_url="https://github.com/ggerganov/llama.cpp",
                        api_key_required=False,
                        endpoint="http://localhost:8080",
                    )
                )
                logger.info("✅ llama.cpp found")
        except Exception:
            self.providers.append(
                LLMProvider(
                    name="llama.cpp",
                    type="local",
                    available=False,
                    cost_per_1k_tokens=0.0,
                    setup_url="https://github.com/ggerganov/llama.cpp",
                    api_key_required=False,
                )
            )

    def _check_openai(self):
        """Check for OpenAI API key"""
        api_key = os.getenv("OPENAI_API_KEY")
        self.providers.append(
            LLMProvider(
                name="OpenAI",
                type="api",
                available=api_key is not None,
                cost_per_1k_tokens=0.002,  # GPT-4o-mini pricing
                setup_url="https://platform.openai.com/api-keys",
                api_key_required=True,
                endpoint="https://api.openai.com/v1",
            )
        )
        if api_key:
            logger.info("✅ OpenAI API key found")

    def _check_anthropic(self):
        """Check for Anthropic API key"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.providers.append(
            LLMProvider(
                name="Anthropic",
                type="api",
                available=api_key is not None,
                cost_per_1k_tokens=0.003,  # Claude pricing
                setup_url="https://console.anthropic.com",
                api_key_required=True,
                endpoint="https://api.anthropic.com/v1",
            )
        )
        if api_key:
            logger.info("✅ Anthropic API key found")

    def _check_groq(self):
        """Check for Groq API key"""
        api_key = os.getenv("GROQ_API_KEY")
        self.providers.append(
            LLMProvider(
                name="Groq",
                type="api",
                available=api_key is not None,
                cost_per_1k_tokens=0.0001,  # Very cheap
                setup_url="https://console.groq.com",
                api_key_required=True,
                endpoint="https://api.groq.com/openai/v1",
            )
        )
        if api_key:
            logger.info("✅ Groq API key found")

    def _check_openrouter(self):
        """Check for OpenRouter API key"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        self.providers.append(
            LLMProvider(
                name="OpenRouter",
                type="cloud",
                available=api_key is not None,
                cost_per_1k_tokens=0.0005,  # Aggregated pricing
                setup_url="https://openrouter.ai",
                api_key_required=True,
                endpoint="https://openrouter.ai/api/v1",
            )
        )
        if api_key:
            logger.info("✅ OpenRouter API key found")

    def _check_together(self):
        """Check for Together AI API key"""
        api_key = os.getenv("TOGETHER_API_KEY")
        self.providers.append(
            LLMProvider(
                name="Together AI",
                type="cloud",
                available=api_key is not None,
                cost_per_1k_tokens=0.0002,
                setup_url="https://together.ai",
                api_key_required=True,
                endpoint="https://api.together.xyz/v1",
            )
        )
        if api_key:
            logger.info("✅ Together AI API key found")

    def _get_recommendation(
        self, available: List[LLMProvider]
    ) -> Optional[LLMProvider]:
        """
        Recommend best provider based on:
        1. Local first (zero cost)
        2. Cheapest API second
        3. Most reliable third
        """
        if not available:
            return None

        # Prefer local models
        local = [p for p in available if p.type == "local"]
        if local:
            return local[0]

        # Then cheapest API
        apis = sorted(available, key=lambda p: p.cost_per_1k_tokens)
        return apis[0] if apis else None

    def _estimate_cost(self, available: List[LLMProvider]) -> Dict:
        """
        Estimate monthly cost based on typical usage
        Assumes: 10k tokens/day for entropy monitoring
        """
        recommended = self._get_recommendation(available)
        if not recommended:
            return {"monthly": 0, "currency": "USD", "note": "No providers available"}

        daily_tokens = 10000  # Conservative estimate
        monthly_tokens = daily_tokens * 30
        monthly_cost = (monthly_tokens / 1000) * recommended.cost_per_1k_tokens

        return {
            "provider": recommended.name,
            "daily_tokens": daily_tokens,
            "monthly_tokens": monthly_tokens,
            "monthly_cost": round(monthly_cost, 2),
            "currency": "USD",
            "note": "Estimated cost for typical entropy monitoring",
        }
