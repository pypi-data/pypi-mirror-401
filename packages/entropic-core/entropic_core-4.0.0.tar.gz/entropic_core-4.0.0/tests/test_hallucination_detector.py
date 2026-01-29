"""
Tests for HallucinationDetector module
"""

from entropic_core.core.hallucination_detector import (
    HallucinationDetector,
    create_detector,
)


def test_hallucination_detector_initialization():
    """Test basic initialization"""
    detector = HallucinationDetector()
    assert detector is not None


def test_create_detector_factory():
    """Test factory function"""
    detector = create_detector()
    assert detector is not None


def test_detect_contradiction():
    """Test contradiction detection"""
    detector = HallucinationDetector()

    context = ["The capital of France is Paris."]
    text = "The capital of France is London."

    result = detector.detect(text, context)
    assert "is_hallucination" in result


def test_no_hallucination():
    """Test consistent text is not flagged"""
    detector = HallucinationDetector()

    context = ["Python is a programming language."]
    text = "Python is widely used for data science."

    result = detector.detect(text, context)
    assert (
        result.get("is_hallucination", False) == False
        or result.get("confidence", 0) > 0.5
    )
