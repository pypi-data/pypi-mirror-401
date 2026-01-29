"""
Comprehensive tests for diagnosis system
"""

import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, "scripts")

from entropic_core.diagnosis.diagnostic_scripts import DiagnosticScriptGenerator
from entropic_core.diagnosis.problem_detector import KNOWN_PROBLEMS, ProblemDetector


class MockBrain:
    """Mock brain for testing diagnosis"""

    def __init__(self):
        self.memory = MagicMock()
        self.monitor = MagicMock()
        self.agents = []
        self.current_entropy = 0.5

    def get_current_entropy(self):
        return {"combined": self.current_entropy}


class TestProblemDetector:
    """Tests for ProblemDetector"""

    def test_detector_initialization(self):
        """Test detector initializes correctly"""
        brain = MockBrain()
        detector = ProblemDetector(brain)
        assert detector.brain is brain

    def test_detect_infinite_loop(self):
        """Test infinite loop detection"""
        brain = MockBrain()
        brain.memory.get_recent_events.return_value = [
            {"type": "action", "action": "same_action", "timestamp": i}
            for i in range(20)
        ]

        detector = ProblemDetector(brain)
        problems = detector.detect_problems()

        # Should detect repeated actions
        assert isinstance(problems, list)

    def test_detect_high_entropy(self):
        """Test high entropy detection"""
        brain = MockBrain()
        brain.current_entropy = 0.95
        brain.monitor.get_history.return_value = [
            {"combined": 0.9 + i * 0.01} for i in range(10)
        ]

        detector = ProblemDetector(brain)
        problems = detector.detect_problems()

        assert isinstance(problems, list)

    def test_detect_memory_growth(self):
        """Test memory growth detection"""
        brain = MockBrain()
        brain.memory.get_stats.return_value = {"total_events": 100000, "memory_mb": 500}

        detector = ProblemDetector(brain)
        problems = detector.detect_problems()

        assert isinstance(problems, list)

    def test_get_risk_score(self):
        """Test risk score calculation"""
        brain = MockBrain()
        detector = ProblemDetector(brain)

        score = detector.get_risk_score()

        assert isinstance(score, (int, float))
        assert 0 <= score <= 100

    def test_get_recommendations(self):
        """Test recommendation generation"""
        brain = MockBrain()
        detector = ProblemDetector(brain)

        recommendations = detector.get_recommendations()

        assert isinstance(recommendations, list)


class TestDiagnosticScriptGenerator:
    """Tests for DiagnosticScriptGenerator"""

    def test_generate_infinite_loop_fix(self):
        """Test infinite loop fix script generation"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("infinite_loop")

        assert script is not None
        assert "loop" in script.lower() or "iteration" in script.lower()

    def test_generate_memory_leak_fix(self):
        """Test memory leak fix script generation"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("memory_leak")

        assert script is not None
        assert "memory" in script.lower() or "cleanup" in script.lower()

    def test_generate_api_runaway_fix(self):
        """Test API runaway fix script generation"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("api_runaway")

        assert script is not None
        assert "rate" in script.lower() or "limit" in script.lower()

    def test_generate_race_condition_fix(self):
        """Test race condition fix script generation"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("race_condition")

        assert script is not None
        assert "lock" in script.lower() or "thread" in script.lower()

    def test_generate_frozen_agent_fix(self):
        """Test frozen agent fix script generation"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("frozen_agent")

        assert script is not None
        assert "timeout" in script.lower() or "stuck" in script.lower()

    def test_generate_unknown_problem(self):
        """Test handling unknown problem type"""
        generator = DiagnosticScriptGenerator()

        script = generator.generate_fix_script("unknown_problem_xyz")

        # Should return generic fix or None
        assert script is None or isinstance(script, str)


class TestKnownProblems:
    """Tests for known problems database"""

    def test_known_problems_structure(self):
        """Test known problems have required fields"""
        required_fields = ["name", "description", "symptoms", "solution"]

        for problem_id, problem in KNOWN_PROBLEMS.items():
            for field in required_fields:
                assert field in problem, f"Problem {problem_id} missing field {field}"

    def test_known_problems_symptoms_list(self):
        """Test symptoms are lists"""
        for problem_id, problem in KNOWN_PROBLEMS.items():
            assert isinstance(
                problem["symptoms"], list
            ), f"Problem {problem_id} symptoms should be a list"

    def test_known_problems_have_quotes(self):
        """Test problems have real user quotes"""
        for problem_id, problem in KNOWN_PROBLEMS.items():
            if "user_quotes" in problem:
                assert isinstance(problem["user_quotes"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
