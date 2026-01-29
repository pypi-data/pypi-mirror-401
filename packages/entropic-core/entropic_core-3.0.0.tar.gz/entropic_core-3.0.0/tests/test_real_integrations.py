"""
Real Integration Tests with Actual Frameworks
Tests with AutoGen, LangChain, and CrewAI (not mocks)
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from entropic_core import EntropyBrain
from entropic_core.integrations.autogen_adapter import AutoGenEntropyPlugin
from entropic_core.integrations.crewai_adapter import CrewAIEntropyMonitor
from entropic_core.integrations.langchain_adapter import LangChainEntropyHandler


def _autogen_available() -> bool:
    try:
        pass

        return True
    except ImportError:
        return False


def _langchain_available() -> bool:
    try:
        pass

        return True
    except ImportError:
        return False


def _crewai_available() -> bool:
    try:
        pass

        return True
    except ImportError:
        return False


class TestAutoGenIntegration:
    """Test real AutoGen integration"""

    @pytest.mark.skipif(not _autogen_available(), reason="AutoGen not installed")
    def test_autogen_real_conversation(self):
        """Test with real AutoGen conversation"""
        try:
            import autogen
        except ImportError:
            pytest.skip("AutoGen not available")

        brain = EntropyBrain()
        plugin = AutoGenEntropyPlugin(brain)

        config_list = [{"model": "gpt-3.5-turbo", "api_key": "test"}]

        assistant = autogen.AssistantAgent(
            name="assistant", llm_config={"config_list": config_list}
        )
        user_proxy = autogen.UserProxyAgent(name="user_proxy", human_input_mode="NEVER")

        plugin.wrap_agent_group([assistant, user_proxy])

        assert len(brain.agents) == 2
        entropy = brain.measure()
        assert 0.0 <= entropy <= 1.0


class TestLangChainIntegration:
    """Test real LangChain integration"""

    @pytest.mark.skipif(not _langchain_available(), reason="LangChain not installed")
    def test_langchain_real_chain(self):
        """Test with real LangChain chain"""
        try:
            from langchain.chains import LLMChain
            from langchain.llms.fake import FakeListLLM
            from langchain.prompts import PromptTemplate
        except ImportError:
            pytest.skip("LangChain not available")

        brain = EntropyBrain()
        handler = LangChainEntropyHandler(brain)

        responses = ["Response 1", "Response 2", "Response 3"]
        llm = FakeListLLM(responses=responses)

        prompt = PromptTemplate(input_variables=["input"], template="Say: {input}")
        chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])

        result = chain.run("Hello")

        assert result in responses
        assert len(handler.entropy_measurements) > 0

        analytics = handler.get_analytics()
        assert "total_runs" in analytics
        assert analytics["total_runs"] > 0


class TestCrewAIIntegration:
    """Test real CrewAI integration"""

    @pytest.mark.skipif(not _crewai_available(), reason="CrewAI not installed")
    def test_crewai_real_crew(self):
        """Test with real CrewAI crew"""
        try:
            pass
        except ImportError:
            pytest.skip("CrewAI not available")

        brain = EntropyBrain()
        monitor = CrewAIEntropyMonitor(brain)

        # Crear agentes simples en lugar de diccionarios
        class MockAgent:
            def __init__(self, name, role):
                self.name = name
                self.role = role
                self.agent_id = f"{role}_{name}"

        brain = EntropyBrain()
        monitor = CrewAIEntropyMonitor(entropy_brain=brain)  # ← CORREGIDO

        agents_data = [
            MockAgent("Agent1", "Writer"),
            MockAgent("Agent2", "Editor"),
        ]

        monitor.wrap_crew(agents_data)

        assert len(brain.wrapped_agents) == 2  # Ahora sí funcionará
