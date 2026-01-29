"""
Tests for Universal LLM Middleware
"""

from entropic_core.core.llm_middleware import (
    LLMMiddleware,
    LLMProvider,
    MiddlewareConfig,
)


def test_middleware_initialization():
    """Test basic middleware initialization"""
    middleware = LLMMiddleware()
    assert middleware is not None


def test_middleware_with_config():
    """Test middleware with custom config"""
    config = MiddlewareConfig(
        high_entropy_threshold=0.7, enable_temperature_control=True
    )
    middleware = LLMMiddleware(config)
    assert middleware.config == config


def test_wrap_function():
    """Test wrapping an LLM function"""
    middleware = LLMMiddleware()

    def mock_llm_call(messages=None, temperature=0.7):
        return {"content": "Hello"}

    wrapped = middleware.wrap(mock_llm_call)
    assert wrapped is not None
    assert callable(wrapped)


def test_middleware_provider_enum():
    """Test LLMProvider enum values"""
    assert LLMProvider.OPENAI.value == "openai"
    assert LLMProvider.ANTHROPIC.value == "anthropic"
