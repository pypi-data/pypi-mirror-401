"""
Tests for Vercel AI SDK Adapter
"""

from unittest.mock import Mock

from entropic_core.integrations.vercel_ai_adapter import VercelAIAdapter


def test_vercel_ai_adapter_initialization():
    """Test basic initialization"""
    brain = Mock(current_entropy=0.5)
    adapter = VercelAIAdapter(brain)

    assert adapter is not None
    assert adapter.brain == brain


def test_wrap_generate_text():
    """Test wrapping generateText function"""
    brain = Mock(current_entropy=0.5)
    adapter = VercelAIAdapter(brain)

    def mock_generate_text(model, prompt, **kwargs):
        return {"text": "Generated response"}

    wrapped = adapter.wrap_generate_text(mock_generate_text)
    assert wrapped is not None
    assert callable(wrapped)
