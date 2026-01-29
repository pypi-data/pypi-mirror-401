"""
Hallucination Detector - Detect and prevent LLM hallucinations in real-time

Key Features:
1. Semantic consistency checking
2. Factual grounding verification
3. Self-contradiction detection
4. Confidence scoring
5. Source attribution tracking
"""

import hashlib
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class HallucinationReport:
    """Report of hallucination analysis"""

    is_hallucination: bool
    confidence: float
    hallucination_type: str
    evidence: List[str]
    suggested_fix: str
    flagged_segments: List[Dict[str, Any]]


@dataclass
class FactualClaim:
    """A factual claim extracted from text"""

    text: str
    claim_type: str  # 'number', 'date', 'name', 'fact', 'opinion'
    confidence: float
    source_segment: str
    verifiable: bool


class HallucinationDetector:
    """
    Detects hallucinations in LLM outputs using multiple strategies

    Detection Methods:
    1. Self-consistency: Compare multiple outputs for same input
    2. Semantic drift: Detect deviation from conversation context
    3. Factual anomaly: Flag suspicious factual claims
    4. Confidence analysis: Detect hedging language patterns
    5. Source grounding: Check claims against provided context
    """

    def __init__(self, brain=None):
        self.brain = brain
        self.conversation_context: List[Dict] = []
        self.established_facts: Dict[str, str] = {}  # fact_hash -> fact_text
        self.response_history: List[str] = []

        # Detection thresholds
        self.consistency_threshold = 0.7
        self.drift_threshold = 0.5
        self.confidence_threshold = 0.6

        # Patterns that indicate uncertainty/hedging
        self.hedging_patterns = [
            r"\bi think\b",
            r"\bprobably\b",
            r"\bmaybe\b",
            r"\bperhaps\b",
            r"\bmight be\b",
            r"\bcould be\b",
            r"\bpossibly\b",
            r"\bi believe\b",
            r"\bit seems\b",
            r"\bapparently\b",
            r"\bas far as i know\b",
            r"\bto my knowledge\b",
            r"\bi\'m not sure\b",
            r"\bi\'m uncertain\b",
        ]

        # Patterns that indicate confident but potentially hallucinated claims
        self.overconfidence_patterns = [
            r"\bdefinitely\b",
            r"\babsolutely\b",
            r"\bcertainly\b",
            r"\bwithout a doubt\b",
            r"\b100%\b",
            r"\balways\b",
            r"\bnever\b",
            r"\beveryone knows\b",
            r"\bit\'s a fact\b",
            r"\bundoubtedly\b",
        ]

        # Number pattern for factual claims
        self.number_pattern = (
            r"\b\d+(?:\.\d+)?(?:\s*(?:million|billion|thousand|percent|%))?\b"
        )
        self.date_pattern = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}|\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b\s+\d{1,2}(?:,?\s+\d{4})?)\b"

    # --- AÑADIDO: Método requerido por el sistema de eventos del Brain ---
    def update_entropy(self, entropy: float):
        """Update internal sensitivity based on system entropy"""
        # A mayor entropía, somos más estrictos con la detección
        if entropy > 0.8:
            self.confidence_threshold = 0.4  # Más paranoico
        elif entropy < 0.2:
            self.confidence_threshold = 0.8  # Más relajado

    # --- AÑADIDO: Wrapper requerido por Brain.py y Tests ---
    def detect(self, text: str, context: List[str] = None) -> Dict[str, Any]:
        """
        Wrapper compatible con Brain.py que devuelve un diccionario.
        Convierte la lista de strings (contexto simple) a lista de dicts para 'analyze'.
        """
        # Normalizar contexto: los tests pasan listas de strings, analyze quiere dicts
        formatted_context = []
        if context:
            for item in context:
                if isinstance(item, str):
                    formatted_context.append({"role": "user", "content": item})
                elif isinstance(item, dict):
                    formatted_context.append(item)

        # Llamar a la lógica original completa
        report = self.analyze(text, formatted_context)

        # Convertir Report a Diccionario (lo que esperan los tests)
        return {
            "is_hallucination": report.is_hallucination,
            "confidence": report.confidence,
            "score": report.confidence,  # Alias para compatibilidad
            "reason": report.hallucination_type,
            "evidence": report.evidence,
            "details": {
                "type": report.hallucination_type,
                "fix": report.suggested_fix,
                "flagged": report.flagged_segments,
            },
        }

    def analyze(self, response: str, context: List[Dict] = None) -> HallucinationReport:
        """
        Analyze a response for potential hallucinations

        Args:
            response: The LLM response text to analyze
            context: The conversation context (messages history)

        Returns:
            HallucinationReport with analysis results
        """
        if context:
            self.conversation_context = context

        flagged_segments = []
        evidence = []

        # 1. Check for semantic drift from context
        drift_score, drift_evidence = self._check_semantic_drift(response)
        if drift_score > self.drift_threshold:
            evidence.extend(drift_evidence)

        # 2. Check for self-contradictions
        contradiction_score, contra_evidence = self._check_self_contradiction(response)
        if contradiction_score > 0.5:
            evidence.extend(contra_evidence)

        # 3. Extract and verify factual claims
        claims = self._extract_factual_claims(response)
        suspicious_claims = self._verify_claims(claims)
        for claim in suspicious_claims:
            flagged_segments.append(
                {
                    "text": claim.text,
                    "type": claim.claim_type,
                    "reason": "unverifiable_claim",
                    "confidence": claim.confidence,
                }
            )
            evidence.append(f"Suspicious claim: '{claim.text}'")

        # 4. Analyze confidence patterns
        confidence_analysis = self._analyze_confidence_patterns(response)
        if confidence_analysis["overconfidence_score"] > 0.7:
            evidence.append("High overconfidence language detected")

        # 5. Check consistency with established facts
        inconsistencies = self._check_fact_consistency(response)
        for inconsistency in inconsistencies:
            flagged_segments.append(inconsistency)
            evidence.append(
                f"Inconsistent with established fact: {inconsistency['established']}"
            )

        # Calculate overall hallucination probability
        hallucination_score = self._calculate_hallucination_score(
            drift_score,
            contradiction_score,
            len(suspicious_claims),
            confidence_analysis,
            len(inconsistencies),
        )

        # Determine hallucination type
        hallucination_type = self._determine_hallucination_type(
            drift_score, contradiction_score, suspicious_claims, inconsistencies
        )

        # Generate fix suggestion
        suggested_fix = self._generate_fix_suggestion(
            hallucination_type, flagged_segments
        )

        # Update history
        self.response_history.append(response)
        self._update_established_facts(response)

        return HallucinationReport(
            is_hallucination=hallucination_score > self.confidence_threshold,
            confidence=hallucination_score,
            hallucination_type=hallucination_type,
            evidence=evidence,
            suggested_fix=suggested_fix,
            flagged_segments=flagged_segments,
        )

    def _check_semantic_drift(self, response: str) -> Tuple[float, List[str]]:
        """Check if response drifts from conversation context"""
        if not self.conversation_context:
            return 0.0, []

        evidence = []

        # Extract key terms from context
        context_text = " ".join(
            msg.get("content", "") for msg in self.conversation_context
        )
        context_terms = set(self._extract_key_terms(context_text))
        response_terms = set(self._extract_key_terms(response))

        if not context_terms:
            return 0.0, []

        # Calculate overlap
        overlap = len(context_terms & response_terms)
        drift_score = 1.0 - (overlap / len(context_terms))

        if drift_score > self.drift_threshold:
            new_terms = response_terms - context_terms
            if new_terms:
                evidence.append(f"New terms not in context: {list(new_terms)[:5]}")

        return drift_score, evidence

    def _check_self_contradiction(self, response: str) -> Tuple[float, List[str]]:
        """Check for self-contradictions within the response"""
        evidence = []

        # Split into sentences
        sentences = re.split(r"[.!?]+", response)
        sentences = [s.strip() for s in sentences if s.strip()]

        contradiction_score = 0.0

        # Check for negation patterns
        for i, sent in enumerate(sentences):
            for j, other_sent in enumerate(sentences[i + 1 :], i + 1):
                # Simple negation check
                if self._are_contradictory(sent, other_sent):
                    contradiction_score = max(contradiction_score, 0.8)
                    evidence.append(
                        f"Potential contradiction: '{sent[:50]}...' vs '{other_sent[:50]}...'"
                    )

        return contradiction_score, evidence

    def _are_contradictory(self, sent1: str, sent2: str) -> bool:
        """Simple check for contradictory statements"""
        sent1_lower = sent1.lower()
        sent2_lower = sent2.lower()

        # Check for explicit negations
        negation_pairs = [
            ("is", "is not"),
            ("are", "are not"),
            ("was", "was not"),
            ("can", "cannot"),
            ("will", "will not"),
            ("do", "do not"),
            ("should", "should not"),
            ("must", "must not"),
            ("true", "false"),
            ("yes", "no"),
            ("always", "never"),
        ]

        for pos, neg in negation_pairs:
            if pos in sent1_lower and neg in sent2_lower:
                # Check if they're about the same subject
                sent1_words = set(sent1_lower.split())
                sent2_words = set(sent2_lower.split())
                overlap = len(sent1_words & sent2_words)
                if overlap > 3:  # Significant overlap suggests same topic
                    return True
            if neg in sent1_lower and pos in sent2_lower:
                sent1_words = set(sent1_lower.split())
                sent2_words = set(sent2_lower.split())
                overlap = len(sent1_words & sent2_words)
                if overlap > 3:
                    return True

        return False

    def _extract_factual_claims(self, response: str) -> List[FactualClaim]:
        """Extract factual claims from response"""
        claims = []

        # Extract numeric claims
        for match in re.finditer(self.number_pattern, response, re.IGNORECASE):
            # Get surrounding context
            start = max(0, match.start() - 50)
            end = min(len(response), match.end() + 50)
            context = response[start:end]

            claims.append(
                FactualClaim(
                    text=match.group(),
                    claim_type="number",
                    confidence=0.5,  # Numbers need verification
                    source_segment=context,
                    verifiable=True,
                )
            )

        # Extract date claims
        for match in re.finditer(self.date_pattern, response, re.IGNORECASE):
            start = max(0, match.start() - 50)
            end = min(len(response), match.end() + 50)
            context = response[start:end]

            claims.append(
                FactualClaim(
                    text=match.group(),
                    claim_type="date",
                    confidence=0.5,
                    source_segment=context,
                    verifiable=True,
                )
            )

        return claims

    def _verify_claims(self, claims: List[FactualClaim]) -> List[FactualClaim]:
        """Verify claims against context and flag suspicious ones"""
        suspicious = []

        context_text = " ".join(
            msg.get("content", "") for msg in self.conversation_context
        )

        for claim in claims:
            # Check if claim appears in original context
            if claim.text not in context_text:
                # Check if it's a reasonable inference
                claim.confidence = 0.7  # Higher suspicion if not in context
                suspicious.append(claim)

        return suspicious

    def _analyze_confidence_patterns(self, response: str) -> Dict[str, Any]:
        """Analyze hedging and overconfidence patterns"""
        response_lower = response.lower()

        hedging_count = sum(
            len(re.findall(pattern, response_lower))
            for pattern in self.hedging_patterns
        )

        overconfidence_count = sum(
            len(re.findall(pattern, response_lower))
            for pattern in self.overconfidence_patterns
        )

        word_count = len(response.split())

        return {
            "hedging_score": hedging_count / max(1, word_count / 100),
            "overconfidence_score": overconfidence_count / max(1, word_count / 100),
            "hedging_count": hedging_count,
            "overconfidence_count": overconfidence_count,
        }

    def _check_fact_consistency(self, response: str) -> List[Dict]:
        """Check response against established facts from conversation"""
        inconsistencies = []

        response.lower()

        for fact_hash, fact_text in self.established_facts.items():
            # Simple check: if we mention the same entities, are we consistent?
            fact_terms = set(self._extract_key_terms(fact_text))
            response_terms = set(self._extract_key_terms(response))

            common_terms = fact_terms & response_terms

            if len(common_terms) >= 2:  # Talking about same thing
                # Check for contradictory statements
                if self._are_contradictory(fact_text, response):
                    inconsistencies.append(
                        {
                            "type": "fact_inconsistency",
                            "established": fact_text[:100],
                            "new_statement": response[:100],
                            "common_terms": list(common_terms),
                        }
                    )

        return inconsistencies

    def _calculate_hallucination_score(
        self,
        drift_score: float,
        contradiction_score: float,
        suspicious_claims_count: int,
        confidence_analysis: Dict,
        inconsistency_count: int,
    ) -> float:
        """Calculate overall hallucination probability"""

        # Weighted combination
        score = (
            drift_score * 0.2
            + contradiction_score * 0.3
            + min(1.0, suspicious_claims_count * 0.15) * 0.2
            + confidence_analysis["overconfidence_score"] * 0.15
            + min(1.0, inconsistency_count * 0.25) * 0.15
        )

        return min(1.0, score)

    def _determine_hallucination_type(
        self,
        drift_score: float,
        contradiction_score: float,
        suspicious_claims: List,
        inconsistencies: List,
    ) -> str:
        """Determine the primary type of hallucination"""

        if contradiction_score > 0.7:
            return "self_contradiction"
        elif len(inconsistencies) > 0:
            return "fact_inconsistency"
        elif len(suspicious_claims) > 2:
            return "fabricated_facts"
        elif drift_score > 0.7:
            return "context_drift"
        else:
            return "none"

    def _generate_fix_suggestion(
        self, hallucination_type: str, flagged_segments: List[Dict]
    ) -> str:
        """Generate suggestion for fixing the hallucination"""

        suggestions = {
            "self_contradiction": "The response contains self-contradictory statements. Regenerate with clearer logic flow.",
            "fact_inconsistency": "The response contradicts previously established facts. Ground the response in the original context.",
            "fabricated_facts": "The response contains unverifiable factual claims. Add source attribution or remove specific claims.",
            "context_drift": "The response drifts from the conversation topic. Refocus on the original query.",
            "none": "No significant hallucination detected.",
        }

        base_suggestion = suggestions.get(
            hallucination_type, "Review response for accuracy."
        )

        if flagged_segments:
            base_suggestion += f"\n\nFlagged segments ({len(flagged_segments)}):"
            for seg in flagged_segments[:3]:
                base_suggestion += f"\n- {seg.get('text', '')[:50]}..."

        return base_suggestion

    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text for comparison"""
        # Simple tokenization and filtering
        words = re.findall(r"\b[a-z]+\b", text.lower())

        # Remove common stop words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "between",
            "under",
            "again",
            "further",
            "then",
            "once",
            "here",
            "there",
            "when",
            "where",
            "why",
            "how",
            "all",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "just",
            "and",
            "but",
            "or",
            "if",
            "because",
            "until",
            "while",
            "it",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "we",
            "they",
        }

        return [w for w in words if w not in stop_words and len(w) > 2]

    def _update_established_facts(self, response: str):
        """Update established facts from response"""
        # Extract factual statements and store them
        sentences = re.split(r"[.!?]+", response)

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Only meaningful sentences
                # Check if it's a factual statement (not a question or opinion)
                if not sentence.endswith("?") and not any(
                    pattern in sentence.lower()
                    for pattern in ["i think", "i believe", "maybe", "perhaps"]
                ):
                    fact_hash = hashlib.md5(sentence.lower().encode()).hexdigest()[:16]
                    self.established_facts[fact_hash] = sentence

        # Keep only last 100 facts
        if len(self.established_facts) > 100:
            items = list(self.established_facts.items())
            self.established_facts = dict(items[-100:])

    def get_trust_score(self, response: str) -> float:
        """Quick trust score without full analysis"""
        report = self.analyze(response)
        return 1.0 - report.confidence


def create_detector() -> HallucinationDetector:
    """Factory function to create hallucination detector"""
    return HallucinationDetector()


# Module validation
__module_version__ = "3.0.0"
__module_name__ = "hallucination_detector"
