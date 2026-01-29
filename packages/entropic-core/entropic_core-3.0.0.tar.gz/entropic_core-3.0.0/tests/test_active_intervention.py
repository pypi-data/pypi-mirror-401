"""
Tests for Active Intervention module
"""

from entropic_core.core.active_intervention import (
    ActiveInterventionEngine,
    InterventionType,
    create_intervention_engine,
)


def test_intervention_engine_initialization():
    """Test basic initialization"""
    engine = ActiveInterventionEngine()
    assert engine is not None


def test_create_intervention_engine_factory():
    """Test factory function"""
    engine = create_intervention_engine()
    assert engine is not None


def test_intervention_type_enum():
    """Test InterventionType enum values"""
    assert InterventionType.TEMPERATURE_REDUCTION is not None
    assert InterventionType.PROMPT_INJECTION is not None


def test_create_llm_wrapper():
    """Test LLM function wrapping"""
    engine = ActiveInterventionEngine()

    def mock_llm(messages=None, temperature=0.7):
        return {"content": "response"}

    wrapped = engine.create_llm_wrapper(mock_llm, "test_agent")
    assert wrapped is not None
    assert callable(wrapped)
