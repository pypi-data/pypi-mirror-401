"""
Integration Adapters Test Suite
Tests for AutoGen, LangChain, and custom adapter integrations
"""

import os
import sys
import unittest

# CORRECCIÓN: Importar correctamente langchain para la detección
try:
    import langchain

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entropic_core.integrations.autogen_adapter import AutoGenEntropyPlugin
from entropic_core.integrations.custom_builder import CustomAdapterBuilder
from entropic_core.integrations.langchain_adapter import LangChainEntropyCallback


class TestAutoGenAdapter(unittest.TestCase):
    """Test AutoGen integration"""

    def test_plugin_initialization(self):
        """Test plugin can be initialized"""
        plugin = AutoGenEntropyPlugin()
        self.assertIsNotNone(plugin)
        self.assertIsNotNone(plugin.brain)

    def test_message_wrapping(self):
        """Test message interception and wrapping"""
        plugin = AutoGenEntropyPlugin()

        test_message = {"role": "assistant", "content": "Test message"}

        wrapped = plugin.wrap_message(test_message, agent_name="test_agent")

        self.assertIn("role", wrapped)
        self.assertIn("content", wrapped)
        # Should have added entropy context
        self.assertTrue(hasattr(plugin, "last_entropy"))


class TestLangChainAdapter(unittest.TestCase):
    """Test LangChain integration"""

    def test_callback_initialization(self):
        """Test callback handler initialization"""
        callback = LangChainEntropyCallback()
        self.assertIsNotNone(callback)
        self.assertIsNotNone(callback.brain)

    @pytest.mark.skipif(not LANGCHAIN_AVAILABLE, reason="langchain not installed")
    def test_llm_start_callback(self):
        """Test LLM start callback"""
        callback = LangChainEntropyCallback()

        # Simulate LangChain callback
        callback.on_llm_start(
            serialized={"name": "test_llm"}, prompts=["test prompt"], run_id="test_run"
        )

        # Should register the call
        self.assertTrue(hasattr(callback, "active_runs"))

    @pytest.mark.skipif(not LANGCHAIN_AVAILABLE, reason="langchain not installed")
    def test_llm_end_callback(self):
        """Test LLM end callback and entropy measurement"""
        callback = LangChainEntropyCallback()

        # Start a run
        callback.on_llm_start(
            serialized={"name": "test_llm"}, prompts=["test prompt"], run_id="test_run"
        )

        # CORRECCIÓN: Importar dentro del test y manejar caso de que LangChain no esté instalado
        if LANGCHAIN_AVAILABLE:
            # Solo importar si LangChain está disponible
            try:
                from langchain.schema import Generation, LLMResult

                result = LLMResult(generations=[[Generation(text="test response")]])
                callback.on_llm_end(result, run_id="test_run")

                # Should have measured entropy
                self.assertTrue(len(callback.brain.monitor.get_history()) > 0)
            except ImportError:
                # Si hay un error de importación, saltar el test
                self.skipTest("langchain.schema not available")
        else:
            self.skipTest("LangChain not installed")


class TestCustomBuilder(unittest.TestCase):
    """Test custom adapter builder"""

    def test_builder_initialization(self):
        """Test builder can be initialized"""
        builder = CustomAdapterBuilder()
        self.assertIsNotNone(builder)

    def test_method_registration(self):
        """Test registering custom methods"""
        builder = CustomAdapterBuilder()

        def custom_state_extractor(agent):
            return {"custom": "state"}

        builder.register_state_extractor(custom_state_extractor)

        # Test extraction
        class MockAgent:
            pass

        state = builder.extract_state(MockAgent())
        self.assertEqual(state, {"custom": "state"})

    def test_complete_adapter_build(self):
        """Test building a complete custom adapter"""
        builder = CustomAdapterBuilder()

        # Register all required methods
        builder.register_state_extractor(lambda agent: {"state": "test"})
        builder.register_decision_extractor(lambda agent: "decision")
        builder.register_message_counter(lambda agent: 5)

        adapter = builder.build()

        self.assertIsNotNone(adapter)
        self.assertTrue(callable(adapter.extract_state))
        self.assertTrue(callable(adapter.extract_decision))
        self.assertTrue(callable(adapter.count_messages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
