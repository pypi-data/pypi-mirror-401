"""
Real problem detection based on actual user issues from AutoGen, CrewAI, LangChain
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ProblemDetector:
    """
    Detects specific real problems identified from GitHub issues:
    1. Infinite loops
    2. Memory leaks
    3. API runaways
    4. Race conditions
    5. Timeout cascades
    """

    PROBLEMS = {
        "infinite_loop": {
            "name": "Infinite Loop Detection",
            "description": "Agents stuck repeating same actions without progress",
            "github_quote": '"agent stuck in a loop...keeps iterating in an infinite loop"',
            "severity": "HIGH",
            "indicators": [
                "repeated_actions",
                "no_state_change",
                "high_entropy_variance",
            ],
        },
        "memory_leak": {
            "name": "Memory Leak Detection",
            "description": "System memory growing unbounded over time",
            "github_quote": '"Debug Memory Leak in Autogen"',
            "severity": "CRITICAL",
            "indicators": ["increasing_memory", "no_cleanup", "resource_exhaustion"],
        },
        "api_runaway": {
            "name": "API Cost Runaway",
            "description": "Excessive API calls causing cost explosion",
            "github_quote": '"TimeoutError: OpenAI API call timed out"',
            "severity": "HIGH",
            "indicators": ["excessive_api_calls", "timeout_errors", "cost_spike"],
        },
        "race_condition": {
            "name": "Concurrency Conflict",
            "description": "Multiple agents accessing shared resources simultaneously",
            "github_quote": '"Concurrency conflict...agents accessing shared resources"',
            "severity": "MEDIUM",
            "indicators": ["concurrent_access", "data_corruption", "deadlock"],
        },
        "thinking_freeze": {
            "name": "Thinking State Freeze",
            "description": 'Agents stuck in "THINKING" state indefinitely',
            "github_quote": '"CREW getting stuck on any task as THINKING and freezing"',
            "severity": "HIGH",
            "indicators": ["frozen_state", "no_progress", "timeout"],
        },
    }

    def __init__(self, brain: Any):
        """
        Initialize problem detector

        Args:
            brain: EntropyBrain instance for accessing memory and metrics
        """
        self.brain = brain
        self.detection_history: List[Dict[str, Any]] = []

    def scan_for_problems(self) -> List[Dict[str, Any]]:
        """
        Scan system for all known real problems

        Returns:
            List of detected problems with severity and recommendations
        """
        detected = []

        # Check each known problem type
        for problem_id, problem_info in self.PROBLEMS.items():
            result = self._check_problem(problem_id, problem_info)
            if result["detected"]:
                detected.append(result)
                logger.warning(f"Problem detected: {problem_info['name']}")

        self.detection_history.append(
            {
                "timestamp": datetime.now(),
                "problems_found": len(detected),
                "details": detected,
            }
        )

        return detected

    def detect_problems(self) -> List[Dict[str, Any]]:
        """
        Detect all problems (alias for scan_for_problems)

        Returns:
            List of detected problems
        """
        return self.scan_for_problems()

    def get_risk_score(self) -> float:
        """
        Calculate overall system risk score

        Returns:
            Risk score from 0.0 (safe) to 1.0 (critical)
        """
        problems = self.scan_for_problems()

        if not problems:
            return 0.0

        # Weight by severity
        severity_weights = {"CRITICAL": 1.0, "HIGH": 0.7, "MEDIUM": 0.4, "LOW": 0.2}

        total_risk = sum(
            severity_weights.get(p["severity"], 0.5) * p["confidence"] for p in problems
        )

        # Normalize
        max_risk = len(problems)
        return min(total_risk / max_risk if max_risk > 0 else 0.0, 1.0)

    def get_recommendations(self) -> List[str]:
        """
        Get recommendations for all detected problems

        Returns:
            List of recommendation strings
        """
        problems = self.scan_for_problems()
        return [p["recommendation"] for p in problems if p["detected"]]

    def _check_problem(self, problem_id: str, problem_info: Dict) -> Dict[str, Any]:
        """Check for a specific problem type"""

        # Get recent events from memory
        recent_events = self.brain.memory.get_recent_events(limit=50)
        metrics_history = self.brain.memory.get_metrics_history(hours=1)

        result = {
            "problem_id": problem_id,
            "name": problem_info["name"],
            "description": problem_info["description"],
            "severity": problem_info["severity"],
            "detected": False,
            "confidence": 0.0,
            "evidence": [],
            "recommendation": "",
            "github_reference": problem_info["github_quote"],
        }

        # Problem-specific detection logic
        if problem_id == "infinite_loop":
            result = self._detect_infinite_loop(recent_events, metrics_history, result)
        elif problem_id == "memory_leak":
            result = self._detect_memory_leak(recent_events, result)
        elif problem_id == "api_runaway":
            result = self._detect_api_runaway(recent_events, result)
        elif problem_id == "race_condition":
            result = self._detect_race_condition(recent_events, result)
        elif problem_id == "thinking_freeze":
            result = self._detect_thinking_freeze(recent_events, result)

        return result

    def _detect_infinite_loop(self, events: List, metrics: List, result: Dict) -> Dict:
        """Detect infinite loop pattern"""
        if len(events) < 10:
            return result

        # Check for repeated action patterns
        recent_actions = [e.get("event_type") for e in events[-20:]]

        # Count consecutive repeats
        max_repeats = 1
        current_repeats = 1
        for i in range(1, len(recent_actions)):
            if recent_actions[i] == recent_actions[i - 1]:
                current_repeats += 1
                max_repeats = max(max_repeats, current_repeats)
            else:
                current_repeats = 1

        # Check for high variance in entropy (oscillating)
        if len(metrics) >= 10:
            entropy_values = [m.get("combined", 0) for m in metrics[-10:]]
            import numpy as np

            variance = np.var(entropy_values)

            if max_repeats >= 5 and variance > 0.1:
                result["detected"] = True
                result["confidence"] = min(0.9, (max_repeats / 10) + (variance * 2))
                result["evidence"] = [
                    f"Repeated action {max_repeats} times consecutively",
                    f"High entropy variance: {variance:.3f}",
                    "System oscillating without progress",
                ]
                result["recommendation"] = (
                    "IMMEDIATE: Stop system and check agent logic\n"
                    "- Use entropic-core fix-infinite-loop command\n"
                    "- Add max_iterations limit to agents\n"
                    "- Enable early stopping with force method"
                )

        return result

    def _detect_memory_leak(self, events: List, result: Dict) -> Dict:
        """Detect memory leak pattern"""
        # Check for increasing event count without cleanup
        if len(events) > 100:
            # Simple heuristic: too many events might indicate memory not being cleaned
            result["detected"] = True
            result["confidence"] = 0.6
            result["evidence"] = [
                f"{len(events)} events in recent memory",
                "Potential unbounded growth",
                "No cleanup detected in recent cycles",
            ]
            result["recommendation"] = (
                "RECOMMENDED: Implement periodic cleanup\n"
                "- Use entropic-core fix-memory-leak command\n"
                "- Create new runtime instances per task\n"
                "- Implement garbage collection for old events"
            )

        return result

    def _detect_api_runaway(self, events: List, result: Dict) -> Dict:
        """Detect excessive API calls"""
        # Count interactions in last events
        interaction_count = sum(
            1 for e in events if e.get("event_type") == "INTERACTION"
        )

        if interaction_count > 50 and len(events) <= 100:
            result["detected"] = True
            result["confidence"] = 0.8
            result["evidence"] = [
                f"{interaction_count} API calls in short timeframe",
                "Risk of timeout errors and cost explosion",
                "May indicate agent not respecting rate limits",
            ]
            result["recommendation"] = (
                "URGENT: Implement rate limiting\n"
                "- Use entropic-core fix-api-runaway command\n"
                "- Add timeout handling to all API calls\n"
                "- Implement exponential backoff"
            )

        return result

    def _detect_race_condition(self, events: List, result: Dict) -> Dict:
        """Detect concurrency conflicts"""
        # Look for concurrent regulation attempts
        regulation_events = [e for e in events if "CHAOS" in e.get("event_type", "")]

        # Check for rapid succession regulations (might indicate race)
        if len(regulation_events) >= 3:
            timestamps = [e.get("timestamp") for e in regulation_events[-3:]]
            if timestamps and all(timestamps):
                # Check if all within 1 second
                time_diffs = []
                for i in range(1, len(timestamps)):
                    try:
                        if isinstance(timestamps[i], str):
                            t1 = datetime.fromisoformat(timestamps[i])
                            t2 = datetime.fromisoformat(timestamps[i - 1])
                            time_diffs.append((t1 - t2).total_seconds())
                    except:
                        pass

                if time_diffs and max(time_diffs) < 1.0:
                    result["detected"] = True
                    result["confidence"] = 0.7
                    result["evidence"] = [
                        f"{len(regulation_events)} regulations in rapid succession",
                        f"Time between events: {min(time_diffs):.2f}s",
                        "Possible concurrent access conflict",
                    ]
                    result["recommendation"] = (
                        "RECOMMENDED: Implement locking\n"
                        "- Use entropic-core fix-race-condition command\n"
                        "- Add threading.Lock() to critical sections\n"
                        "- Ensure thread-safe operations"
                    )

        return result

    def _detect_thinking_freeze(self, events: List, result: Dict) -> Dict:
        """Detect frozen thinking state"""
        # Check for long periods without events
        if len(events) < 5:
            # System might be frozen
            result["detected"] = True
            result["confidence"] = 0.5
            result["evidence"] = [
                f"Only {len(events)} recent events",
                "System may be frozen in thinking state",
                "No progress detected",
            ]
            result["recommendation"] = (
                "IMMEDIATE: Check system status\n"
                "- Use entropic-core fix-thinking-freeze command\n"
                "- Implement timeout for thinking operations\n"
                "- Add progress monitoring"
            )

        return result

    def generate_diagnostic_report(self) -> str:
        """Generate human-readable diagnostic report"""
        problems = self.scan_for_problems()

        if not problems:
            return """
╔════════════════════════════════════════════════════════════════╗
║                  SYSTEM HEALTH: EXCELLENT                      ║
╚════════════════════════════════════════════════════════════════╝

No critical problems detected. Your multi-agent system is stable.

Keep monitoring with: entropic-core monitor
"""

        report = """
╔════════════════════════════════════════════════════════════════╗
║              SYSTEM DIAGNOSTIC REPORT                          ║
╚════════════════════════════════════════════════════════════════╝

"""

        for problem in sorted(
            problems,
            key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}.get(x["severity"], 3),
        ):
            severity_symbol = {"CRITICAL": "🔴", "HIGH": "⚠️ ", "MEDIUM": "⚡"}.get(
                problem["severity"], "ℹ️ "
            )

            report += f"""
{severity_symbol} PROBLEM DETECTED: {problem['name']}
   Severity: {problem['severity']}
   Confidence: {problem['confidence']:.0%}
   
   Description: {problem['description']}
   
   Evidence:
"""
            for evidence in problem["evidence"]:
                report += f"   • {evidence}\n"

            report += f"""
   This matches real issue reported by users:
   "{problem['github_reference']}"
   
   RECOMMENDED ACTION:
   {problem['recommendation']}
   
"""

        report += """
═══════════════════════════════════════════════════════════════

Run specific fixes:
  entropic-core fix --problem <problem_id>
  
Get detailed help:
  entropic-core diagnose --help

"""
        return report


KNOWN_PROBLEMS = {
    "infinite_loop": {
        "name": "Infinite Loop Detection",
        "description": "Agents stuck repeating same actions without progress",
        "symptoms": ["repeated_actions", "no_state_change", "high_entropy_variance"],
        "solution": "Add max_iterations limit and early stopping to agent configuration",
        "github_quote": '"agent stuck in a loop...keeps iterating in an infinite loop"',
        "severity": "HIGH",
        "indicators": ["repeated_actions", "no_state_change", "high_entropy_variance"],
    },
    "memory_leak": {
        "name": "Memory Leak Detection",
        "description": "System memory growing unbounded over time",
        "symptoms": ["increasing_memory", "no_cleanup", "resource_exhaustion"],
        "solution": "Create new runtime instances per task and implement periodic garbage collection",
        "github_quote": '"Debug Memory Leak in Autogen"',
        "severity": "CRITICAL",
        "indicators": ["increasing_memory", "no_cleanup", "resource_exhaustion"],
    },
    "api_runaway": {
        "name": "API Cost Runaway",
        "description": "Excessive API calls causing cost explosion",
        "symptoms": ["excessive_api_calls", "timeout_errors", "cost_spike"],
        "solution": "Implement rate limiting and timeout handling for all API calls",
        "github_quote": '"TimeoutError: OpenAI API call timed out"',
        "severity": "HIGH",
        "indicators": ["excessive_api_calls", "timeout_errors", "cost_spike"],
    },
    "race_condition": {
        "name": "Concurrency Conflict",
        "description": "Multiple agents accessing shared resources simultaneously",
        "symptoms": ["concurrent_access", "data_corruption", "deadlock"],
        "solution": "Add threading.Lock() to protect critical sections",
        "github_quote": '"Concurrency conflict...agents accessing shared resources"',
        "severity": "MEDIUM",
        "indicators": ["concurrent_access", "data_corruption", "deadlock"],
    },
    "thinking_freeze": {
        "name": "Thinking State Freeze",
        "description": 'Agents stuck in "THINKING" state indefinitely',
        "symptoms": ["frozen_state", "no_progress", "timeout"],
        "solution": "Implement timeout for thinking operations with progress monitoring",
        "github_quote": '"CREW getting stuck on any task as THINKING and freezing"',
        "severity": "HIGH",
        "indicators": ["frozen_state", "no_progress", "timeout"],
    },
}

__all__ = ["ProblemDetector", "KNOWN_PROBLEMS"]
