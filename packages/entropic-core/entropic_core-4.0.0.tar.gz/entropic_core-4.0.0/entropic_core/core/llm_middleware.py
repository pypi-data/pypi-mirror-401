"""
Universal LLM Middleware - Works with ANY LLM provider
This is the CORE innovation - intercept ALL LLM calls regardless of framework

Supports:
- OpenAI (GPT-4, GPT-3.5, etc.)
- Anthropic (Claude)
- Google (Gemini)
- Local models (Ollama, LMStudio)
- LangChain chains
- CrewAI crews
- AutoGen agents
- Vercel AI SDK
"""

import functools
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    LANGCHAIN = "langchain"
    CREWAI = "crewai"
    AUTOGEN = "autogen"
    VERCEL_AI = "vercel_ai"
    CUSTOM = "custom"


@dataclass
class InterceptionResult:
    """Result of an LLM call interception"""

    original_request: Dict[str, Any]
    modified_request: Dict[str, Any]
    response: Any
    entropy_before: float
    entropy_after: float
    interventions_applied: List[str]
    latency_ms: float
    tokens_saved: int = 0
    cost_saved: float = 0.0


@dataclass
class MiddlewareConfig:
    """Configuration for the middleware"""

    # Intervention triggers
    high_entropy_threshold: float = 0.7
    low_entropy_threshold: float = 0.2
    hallucination_threshold: float = 0.6

    # Feature toggles
    enable_prompt_injection: bool = True
    enable_temperature_control: bool = True
    enable_context_pruning: bool = True
    enable_hallucination_detection: bool = True
    enable_cost_optimization: bool = True
    enable_retry_logic: bool = True

    # Cost optimization
    max_context_tokens: int = 4000
    target_cost_reduction: float = 0.3

    # Retry settings
    max_retries: int = 3
    retry_temperature_decay: float = 0.8


class LLMMiddleware:
    """
    Universal middleware that intercepts ALL LLM calls

    Usage:
        middleware = LLMMiddleware()

        # OpenAI
        openai.chat.completions.create = middleware.wrap(openai.chat.completions.create)

        # Anthropic
        anthropic.messages.create = middleware.wrap(anthropic.messages.create)

        # LangChain
        chain.invoke = middleware.wrap(chain.invoke)
    """

    def __init__(self, config: MiddlewareConfig = None, brain=None):
        self.config = config or MiddlewareConfig()
        self.brain = brain
        self.current_entropy = 0.5
        self.call_history: List[InterceptionResult] = []
        self.total_tokens_saved = 0
        self.total_cost_saved = 0.0
        self._call_count = 0

        # Provider-specific adapters
        self._adapters: Dict[LLMProvider, "ProviderAdapter"] = {}
        self._register_default_adapters()

    def _register_default_adapters(self):
        """Register adapters for common providers"""
        self._adapters[LLMProvider.OPENAI] = OpenAIAdapter()
        self._adapters[LLMProvider.ANTHROPIC] = AnthropicAdapter()
        self._adapters[LLMProvider.LANGCHAIN] = LangChainAdapter()
        self._adapters[LLMProvider.VERCEL_AI] = VercelAIAdapter()

    def wrap(self, func: Callable, provider: LLMProvider = None) -> Callable:
        """
        Wrap any LLM function with entropic middleware
        Auto-detects provider if not specified
        """
        detected_provider = provider or self._detect_provider(func)
        adapter = self._adapters.get(detected_provider, GenericAdapter())

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return self._intercept_call(func, adapter, args, kwargs)

        return wrapped

    def _intercept_call(
        self, func: Callable, adapter: "ProviderAdapter", args: tuple, kwargs: dict
    ) -> Any:
        """Core interception logic"""
        self._call_count += 1
        start_time = time.time()

        # Extract request info
        original_request = adapter.extract_request(args, kwargs)
        entropy_before = self.current_entropy

        # PHASE 1: Pre-call modifications
        modified_request = self._apply_pre_call_interventions(original_request, adapter)

        # PHASE 2: Execute the actual call
        modified_args, modified_kwargs = adapter.rebuild_request(
            args, kwargs, modified_request
        )
        response = func(*modified_args, **modified_kwargs)

        # PHASE 3: Post-call analysis and potential retry
        response, retry_count = self._apply_post_call_interventions(
            func, adapter, modified_args, modified_kwargs, response
        )

        # Update entropy based on response
        response_entropy = self._analyze_response_entropy(response, adapter)
        self.current_entropy = response_entropy

        # Record result
        latency_ms = (time.time() - start_time) * 1000
        result = InterceptionResult(
            original_request=original_request,
            modified_request=modified_request,
            response=response,
            entropy_before=entropy_before,
            entropy_after=response_entropy,
            interventions_applied=modified_request.get("_interventions", []),
            latency_ms=latency_ms,
            tokens_saved=modified_request.get("_tokens_saved", 0),
            cost_saved=modified_request.get("_cost_saved", 0.0),
        )
        self.call_history.append(result)

        return response

    def _apply_pre_call_interventions(
        self, request: Dict, adapter: "ProviderAdapter"
    ) -> Dict:
        """Apply all pre-call interventions"""
        modified = request.copy()
        interventions = []

        # 1. TEMPERATURE CONTROL based on entropy
        if self.config.enable_temperature_control:
            modified, applied = self._control_temperature(modified)
            if applied:
                interventions.append("temperature_adjusted")

        # 2. PROMPT INJECTION for stability
        if (
            self.config.enable_prompt_injection
            and self.current_entropy > self.config.high_entropy_threshold
        ):
            modified = self._inject_stability_prompt(modified, adapter)
            interventions.append("stability_prompt_injected")

        # 3. CONTEXT PRUNING for cost optimization
        if self.config.enable_context_pruning:
            modified, tokens_saved = self._prune_context(modified, adapter)
            if tokens_saved > 0:
                interventions.append(f"context_pruned_{tokens_saved}_tokens")
                modified["_tokens_saved"] = tokens_saved

        # 4. HALLUCINATION PREVENTION
        if (
            self.config.enable_hallucination_detection
            and self.current_entropy > self.config.hallucination_threshold
        ):
            modified = self._add_grounding_instructions(modified, adapter)
            interventions.append("grounding_added")

        modified["_interventions"] = interventions
        return modified

    def _apply_post_call_interventions(
        self,
        func: Callable,
        adapter: "ProviderAdapter",
        args: tuple,
        kwargs: dict,
        response: Any,
    ) -> Tuple[Any, int]:
        """Apply post-call interventions, including retry logic"""
        retry_count = 0

        if not self.config.enable_retry_logic:
            return response, retry_count

        # Check if response needs retry
        response_text = adapter.extract_response_text(response)
        response_quality = self._assess_response_quality(response_text)

        current_temp = kwargs.get("temperature", 0.7)

        while response_quality < 0.5 and retry_count < self.config.max_retries:
            retry_count += 1

            # Reduce temperature and retry
            new_temp = current_temp * self.config.retry_temperature_decay
            kwargs["temperature"] = new_temp

            response = func(*args, **kwargs)
            response_text = adapter.extract_response_text(response)
            response_quality = self._assess_response_quality(response_text)
            current_temp = new_temp

        return response, retry_count

    def _control_temperature(self, request: Dict) -> Tuple[Dict, bool]:
        """Dynamically adjust temperature based on entropy"""
        current_temp = request.get("temperature", 0.7)
        applied = False

        if self.current_entropy > self.config.high_entropy_threshold:
            # High entropy -> reduce temperature for stability
            new_temp = max(0.1, current_temp * 0.6)
            request["temperature"] = new_temp
            applied = True
        elif self.current_entropy < self.config.low_entropy_threshold:
            # Low entropy -> increase temperature for creativity
            new_temp = min(1.0, current_temp * 1.4)
            request["temperature"] = new_temp
            applied = True

        return request, applied

    def _inject_stability_prompt(
        self, request: Dict, adapter: "ProviderAdapter"
    ) -> Dict:
        """Inject stability instructions into the prompt"""
        stability_instruction = """
[SYSTEM STABILITY PROTOCOL ACTIVE]
The conversation is showing signs of entropy drift. Please:
1. Stay focused on the specific task at hand
2. Reference and maintain consistency with prior context
3. Avoid speculative or tangential responses
4. If uncertain, acknowledge limitations rather than hallucinating
5. Provide structured, clear responses
"""
        return adapter.inject_system_message(request, stability_instruction)

    def _prune_context(
        self, request: Dict, adapter: "ProviderAdapter"
    ) -> Tuple[Dict, int]:
        """Prune context to reduce tokens while preserving essential information"""
        messages = adapter.extract_messages(request)
        if not messages:
            return request, 0

        original_tokens = self._estimate_tokens(messages)

        if original_tokens <= self.config.max_context_tokens:
            return request, 0

        # Smart pruning strategy
        pruned_messages = self._smart_prune(messages, self.config.max_context_tokens)
        pruned_tokens = self._estimate_tokens(pruned_messages)

        tokens_saved = original_tokens - pruned_tokens
        self.total_tokens_saved += tokens_saved

        # Estimate cost saved (rough approximation)
        cost_saved = tokens_saved * 0.00002  # Approximate cost per token
        self.total_cost_saved += cost_saved

        return adapter.set_messages(request, pruned_messages), tokens_saved

    def _smart_prune(self, messages: List[Dict], target_tokens: int) -> List[Dict]:
        """Intelligently prune messages while preserving important context"""
        if not messages:
            return messages

        # Always keep system message and last few exchanges
        system_msgs = [m for m in messages if m.get("role") == "system"]
        other_msgs = [m for m in messages if m.get("role") != "system"]

        # Keep last 4 exchanges (8 messages) minimum
        essential_msgs = other_msgs[-8:] if len(other_msgs) > 8 else other_msgs

        # Calculate tokens
        current_tokens = self._estimate_tokens(system_msgs + essential_msgs)

        if current_tokens <= target_tokens:
            # We have room for more context
            remaining_budget = target_tokens - current_tokens
            middle_msgs = other_msgs[:-8] if len(other_msgs) > 8 else []

            # Add middle messages that fit, prioritizing recent ones
            for msg in reversed(middle_msgs):
                msg_tokens = self._estimate_tokens([msg])
                if msg_tokens <= remaining_budget:
                    essential_msgs.insert(0, msg)
                    remaining_budget -= msg_tokens

        return system_msgs + essential_msgs

    def _add_grounding_instructions(
        self, request: Dict, adapter: "ProviderAdapter"
    ) -> Dict:
        """Add grounding instructions to reduce hallucination"""
        grounding_instruction = """
[FACTUAL GROUNDING REQUIRED]
High entropy detected - please ground your response in:
1. Explicitly stated information from the conversation
2. Verifiable facts you are confident about
3. If making inferences, clearly label them as such
4. Avoid speculation - say "I don't know" when uncertain
"""
        return adapter.inject_system_message(request, grounding_instruction)

    def _analyze_response_entropy(
        self, response: Any, adapter: "ProviderAdapter"
    ) -> float:
        """Analyze entropy of the response"""
        text = adapter.extract_response_text(response)
        if not text:
            return 0.5

        # Calculate word-level Shannon entropy
        import math
        from collections import Counter

        words = text.lower().split()
        if not words:
            return 0.5

        word_counts = Counter(words)
        total = len(words)

        entropy = 0.0
        for count in word_counts.values():
            prob = count / total
            entropy -= prob * math.log2(prob)

        # Normalize
        max_entropy = math.log2(len(word_counts)) if word_counts else 1
        normalized = entropy / max_entropy if max_entropy > 0 else 0.5

        return normalized

    def _assess_response_quality(self, text: str) -> float:
        """Assess quality of response (0-1)"""
        if not text:
            return 0.0

        quality = 1.0

        # Penalize very short responses
        if len(text) < 50:
            quality -= 0.3

        # Penalize repetitive content
        words = text.split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        if unique_ratio < 0.5:
            quality -= 0.3

        # Penalize uncertainty markers (might indicate hallucination avoidance)
        uncertainty_markers = ["i think", "maybe", "possibly", "not sure", "might be"]
        for marker in uncertainty_markers:
            if marker in text.lower():
                quality -= 0.1

        return max(0.0, min(1.0, quality))

    def _estimate_tokens(self, messages: List[Dict]) -> int:
        """Estimate token count (rough approximation)"""
        total_chars = sum(len(str(m.get("content", ""))) for m in messages)
        return total_chars // 4  # Rough estimate: 4 chars per token

    def _detect_provider(self, func: Callable) -> LLMProvider:
        """Auto-detect the LLM provider from function"""
        func_module = getattr(func, "__module__", "")
        getattr(func, "__qualname__", "")

        if "openai" in func_module.lower():
            return LLMProvider.OPENAI
        elif "anthropic" in func_module.lower():
            return LLMProvider.ANTHROPIC
        elif "langchain" in func_module.lower():
            return LLMProvider.LANGCHAIN
        elif "crewai" in func_module.lower():
            return LLMProvider.CREWAI
        elif "autogen" in func_module.lower():
            return LLMProvider.AUTOGEN
        else:
            return LLMProvider.CUSTOM

    def update_entropy(self, entropy: float):
        """Update current entropy from external source"""
        self.current_entropy = entropy

    def get_stats(self) -> Dict[str, Any]:
        """Get middleware statistics"""
        return {
            "total_calls": self._call_count,
            "total_tokens_saved": self.total_tokens_saved,
            "total_cost_saved": self.total_cost_saved,
            "average_entropy": (
                sum(r.entropy_after for r in self.call_history) / len(self.call_history)
                if self.call_history
                else 0.5
            ),
            "intervention_rate": sum(
                1 for r in self.call_history if r.interventions_applied
            )
            / max(1, len(self.call_history)),
        }


# =============================================================================
# PROVIDER ADAPTERS - Handle provider-specific formats
# =============================================================================


class ProviderAdapter(ABC):
    """Base adapter for LLM providers"""

    @abstractmethod
    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        """Extract request info from function arguments"""

    @abstractmethod
    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        """Rebuild function arguments from modified request"""

    @abstractmethod
    def extract_messages(self, request: Dict) -> List[Dict]:
        """Extract messages from request"""

    @abstractmethod
    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        """Set messages in request"""

    @abstractmethod
    def inject_system_message(self, request: Dict, content: str) -> Dict:
        """Inject a system message"""

    @abstractmethod
    def extract_response_text(self, response: Any) -> str:
        """Extract text from response"""


class OpenAIAdapter(ProviderAdapter):
    """Adapter for OpenAI API"""

    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        return {
            "messages": kwargs.get("messages", []),
            "model": kwargs.get("model", "gpt-4"),
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens"),
        }

    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        new_kwargs = kwargs.copy()
        new_kwargs["messages"] = modified.get("messages", kwargs.get("messages", []))
        new_kwargs["temperature"] = modified.get(
            "temperature", kwargs.get("temperature", 0.7)
        )
        return args, new_kwargs

    def extract_messages(self, request: Dict) -> List[Dict]:
        return request.get("messages", [])

    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        request["messages"] = messages
        return request

    def inject_system_message(self, request: Dict, content: str) -> Dict:
        messages = request.get("messages", [])
        # Insert after existing system messages
        insert_idx = 0
        for i, msg in enumerate(messages):
            if msg.get("role") == "system":
                insert_idx = i + 1
            else:
                break

        messages.insert(insert_idx, {"role": "system", "content": content})
        request["messages"] = messages
        return request

    def extract_response_text(self, response: Any) -> str:
        if hasattr(response, "choices") and response.choices:
            if hasattr(response.choices[0], "message"):
                return response.choices[0].message.content or ""
        return str(response)


class AnthropicAdapter(ProviderAdapter):
    """Adapter for Anthropic API"""

    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        return {
            "messages": kwargs.get("messages", []),
            "model": kwargs.get("model", "claude-3-sonnet"),
            "system": kwargs.get("system", ""),
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1024),
        }

    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        new_kwargs = kwargs.copy()
        new_kwargs["messages"] = modified.get("messages", kwargs.get("messages", []))
        new_kwargs["system"] = modified.get("system", kwargs.get("system", ""))
        new_kwargs["temperature"] = modified.get(
            "temperature", kwargs.get("temperature", 0.7)
        )
        return args, new_kwargs

    def extract_messages(self, request: Dict) -> List[Dict]:
        return request.get("messages", [])

    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        request["messages"] = messages
        return request

    def inject_system_message(self, request: Dict, content: str) -> Dict:
        existing_system = request.get("system", "")
        request["system"] = (
            existing_system + "\n\n" + content if existing_system else content
        )
        return request

    def extract_response_text(self, response: Any) -> str:
        if hasattr(response, "content") and response.content:
            if isinstance(response.content, list):
                return " ".join(c.text for c in response.content if hasattr(c, "text"))
            return str(response.content)
        return str(response)


class LangChainAdapter(ProviderAdapter):
    """Adapter for LangChain"""

    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        # LangChain can have various input formats
        input_data = args[0] if args else kwargs.get("input", {})
        return {
            "input": input_data,
            "config": kwargs.get("config", {}),
        }

    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        new_args = (modified.get("input", args[0] if args else {}),) + args[1:]
        return new_args, kwargs

    def extract_messages(self, request: Dict) -> List[Dict]:
        input_data = request.get("input", {})
        if isinstance(input_data, dict) and "messages" in input_data:
            return input_data["messages"]
        return []

    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        if isinstance(request.get("input"), dict):
            request["input"]["messages"] = messages
        return request

    def inject_system_message(self, request: Dict, content: str) -> Dict:
        input_data = request.get("input", {})
        if isinstance(input_data, dict):
            if "system" in input_data:
                input_data["system"] = input_data["system"] + "\n\n" + content
            else:
                input_data["system"] = content
            request["input"] = input_data
        return request

    def extract_response_text(self, response: Any) -> str:
        if hasattr(response, "content"):
            return str(response.content)
        if isinstance(response, dict):
            return response.get("output", response.get("text", str(response)))
        return str(response)


class VercelAIAdapter(ProviderAdapter):
    """Adapter for Vercel AI SDK"""

    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        return {
            "messages": kwargs.get("messages", []),
            "model": kwargs.get("model", ""),
            "temperature": kwargs.get("temperature", 0.7),
        }

    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        new_kwargs = kwargs.copy()
        new_kwargs["messages"] = modified.get("messages", kwargs.get("messages", []))
        new_kwargs["temperature"] = modified.get(
            "temperature", kwargs.get("temperature", 0.7)
        )
        return args, new_kwargs

    def extract_messages(self, request: Dict) -> List[Dict]:
        return request.get("messages", [])

    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        request["messages"] = messages
        return request

    def inject_system_message(self, request: Dict, content: str) -> Dict:
        messages = request.get("messages", [])
        messages.insert(0, {"role": "system", "content": content})
        request["messages"] = messages
        return request

    def extract_response_text(self, response: Any) -> str:
        if hasattr(response, "text"):
            return response.text
        return str(response)


class GenericAdapter(ProviderAdapter):
    """Generic adapter for unknown providers"""

    def extract_request(self, args: tuple, kwargs: dict) -> Dict[str, Any]:
        return dict(kwargs)

    def rebuild_request(
        self, args: tuple, kwargs: dict, modified: Dict
    ) -> Tuple[tuple, dict]:
        return args, modified

    def extract_messages(self, request: Dict) -> List[Dict]:
        return request.get("messages", [])

    def set_messages(self, request: Dict, messages: List[Dict]) -> Dict:
        request["messages"] = messages
        return request

    def inject_system_message(self, request: Dict, content: str) -> Dict:
        messages = request.get("messages", [])
        messages.insert(0, {"role": "system", "content": content})
        request["messages"] = messages
        return request

    def extract_response_text(self, response: Any) -> str:
        if isinstance(response, str):
            return response
        if hasattr(response, "content"):
            return str(response.content)
        return str(response)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def create_middleware(config: Optional[MiddlewareConfig] = None) -> LLMMiddleware:
    """Factory function to create LLM middleware"""
    return LLMMiddleware(config)


def wrap_openai(client, middleware: LLMMiddleware = None):
    """Convenience function to wrap OpenAI client"""
    if middleware is None:
        middleware = create_middleware()

    client.chat.completions.create = middleware.wrap(
        client.chat.completions.create, provider=LLMProvider.OPENAI
    )
    return client


def wrap_anthropic(client, middleware: LLMMiddleware = None):
    """Convenience function to wrap Anthropic client"""
    if middleware is None:
        middleware = create_middleware()

    client.messages.create = middleware.wrap(
        client.messages.create, provider=LLMProvider.ANTHROPIC
    )
    return client
