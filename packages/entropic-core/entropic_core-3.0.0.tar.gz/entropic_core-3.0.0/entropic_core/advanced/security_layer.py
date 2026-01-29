"""
Security Layer - Entropy-based attack detection and mitigation

Detects three types of entropy attacks:
1. Flood Attack: Overwhelming system with chaos
2. Drain Attack: Paralyzing system with excessive order
3. Resonance Attack: Creating destructive oscillations
"""

import logging
from collections import deque
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class EntropySecurity:
    """
    Detects and mitigates entropy-based attacks on multi-agent systems

    Example:
        security = EntropySecurity(brain)
        threat = security.detect_threats()
        if threat['detected']:
            security.apply_mitigation(threat['attack_type'])
    """

    def __init__(self, brain_instance, lookback_window: int = 100):
        """
        Initialize security layer

        Args:
            brain_instance: EntropyBrain instance to protect
            lookback_window: Number of historical measurements to analyze
        """
        self.brain = brain_instance
        self.lookback_window = lookback_window
        self.entropy_buffer = deque(maxlen=lookback_window)
        self.alert_history = []
        self.mitigation_actions = []

        # Attack detection thresholds
        self.thresholds = {
            "flood_rate": 0.15,  # Entropy increase rate
            "drain_rate": -0.15,  # Entropy decrease rate
            "resonance_amplitude": 0.3,  # Oscillation amplitude
            "resonance_frequency": 5.0,  # Cycles per 100 steps
            "anomaly_std_multiplier": 3.0,  # Standard deviations for anomaly
        }

        logger.info("Security layer initialized")

    def update(self, current_entropy: float) -> None:
        """
        Update security state with new entropy measurement

        Args:
            current_entropy: Current system entropy value
        """
        self.entropy_buffer.append(
            {"entropy": current_entropy, "timestamp": datetime.now()}
        )

    def detect_threats(self) -> Dict[str, Any]:
        """
        Detect all types of entropy attacks

        Returns:
            Dictionary with threat analysis
        """
        if len(self.entropy_buffer) < 10:
            return {
                "detected": False,
                "reason": "Insufficient data for threat analysis",
            }

        # Check for each attack type
        flood = self._detect_flood_attack()
        drain = self._detect_drain_attack()
        resonance = self._detect_resonance_attack()
        anomaly = self._detect_anomaly()

        threats = []
        if flood["detected"]:
            threats.append(flood)
        if drain["detected"]:
            threats.append(drain)
        if resonance["detected"]:
            threats.append(resonance)
        if anomaly["detected"]:
            threats.append(anomaly)

        if threats:
            # Return highest confidence threat
            primary_threat = max(threats, key=lambda t: t["confidence"])

            self._log_threat(primary_threat)

            return {
                "detected": True,
                "primary_threat": primary_threat,
                "all_threats": threats,
                "severity": self._calculate_severity(threats),
                "recommended_action": self._get_mitigation_strategy(
                    primary_threat["attack_type"]
                ),
            }

        return {
            "detected": False,
            "system_status": "SECURE",
            "entropy_health": self._calculate_health_score(),
        }

    def detect_entropy_attack(self) -> Dict[str, Any]:
        """
        Detect entropy attacks (alias for detect_threats for backward compatibility)

        Returns:
            Dictionary with attack detection results
        """
        return self.detect_threats()

    def _detect_flood_attack(self) -> Dict[str, Any]:
        """
        Detect entropy flood attack (rapid chaos increase)

        Characteristics:
        - Rapid entropy increase
        - Sustained high entropy
        - Unusual spike patterns
        """
        if len(self.entropy_buffer) < 20:
            return {"detected": False}

        recent = [e["entropy"] for e in list(self.entropy_buffer)[-20:]]

        # Calculate rate of change
        rates = np.diff(recent)
        avg_rate = np.mean(rates)

        # Check for rapid increase
        flood_detected = avg_rate > self.thresholds["flood_rate"]

        # Check for sustained high entropy
        high_entropy_count = sum(1 for e in recent if e > 0.8)
        sustained_high = high_entropy_count > len(recent) * 0.7

        if flood_detected or sustained_high:
            confidence = min(0.99, avg_rate * 3 + (high_entropy_count / len(recent)))

            return {
                "detected": True,
                "attack_type": "ENTROPY_FLOOD",
                "confidence": confidence,
                "description": "System under rapid chaos injection attack",
                "indicators": {
                    "rate_of_increase": avg_rate,
                    "high_entropy_ratio": high_entropy_count / len(recent),
                    "peak_entropy": max(recent),
                },
                "impact": "HIGH" if confidence > 0.8 else "MEDIUM",
            }

        return {"detected": False}

    def _detect_drain_attack(self) -> Dict[str, Any]:
        """
        Detect entropy drain attack (forced paralysis through excessive order)

        Characteristics:
        - Rapid entropy decrease
        - Sustained low entropy
        - System becoming too predictable
        """
        if len(self.entropy_buffer) < 20:
            return {"detected": False}

        recent = [e["entropy"] for e in list(self.entropy_buffer)[-20:]]

        # Calculate rate of change
        rates = np.diff(recent)
        avg_rate = np.mean(rates)

        # Check for rapid decrease
        drain_detected = avg_rate < self.thresholds["drain_rate"]

        # Check for sustained low entropy
        low_entropy_count = sum(1 for e in recent if e < 0.15)
        sustained_low = low_entropy_count > len(recent) * 0.7

        if drain_detected or sustained_low:
            confidence = min(
                0.99, abs(avg_rate) * 3 + (low_entropy_count / len(recent))
            )

            return {
                "detected": True,
                "attack_type": "ENTROPY_DRAIN",
                "confidence": confidence,
                "description": "System under order-forcing paralysis attack",
                "indicators": {
                    "rate_of_decrease": avg_rate,
                    "low_entropy_ratio": low_entropy_count / len(recent),
                    "minimum_entropy": min(recent),
                },
                "impact": "HIGH" if confidence > 0.8 else "MEDIUM",
            }

        return {"detected": False}

    def _detect_resonance_attack(self) -> Dict[str, Any]:
        """
        Detect resonance attack (destructive oscillations)

        Characteristics:
        - Regular oscillations in entropy
        - Increasing amplitude over time
        - Frequency matching system natural frequency
        """
        if len(self.entropy_buffer) < 50:
            return {"detected": False}

        recent = np.array([e["entropy"] for e in list(self.entropy_buffer)[-50:]])

        # Use FFT to detect oscillations
        fft = np.fft.fft(recent - np.mean(recent))
        frequencies = np.fft.fftfreq(len(recent))
        magnitude = np.abs(fft)

        # Find dominant frequency
        dominant_freq_idx = np.argmax(magnitude[1 : len(magnitude) // 2]) + 1
        dominant_freq = (
            abs(frequencies[dominant_freq_idx]) * 100
        )  # Scale to cycles per 100 steps
        dominant_magnitude = magnitude[dominant_freq_idx] / len(recent)

        # Check for oscillation characteristics
        oscillation_detected = (
            dominant_magnitude > self.thresholds["resonance_amplitude"]
            and dominant_freq > 0.5  # At least one cycle every 200 steps
        )

        if oscillation_detected:
            # Check if amplitude is increasing (destructive resonance)
            first_half = recent[:25]
            second_half = recent[25:]
            amplitude_increasing = np.std(second_half) > np.std(first_half) * 1.2

            confidence = min(0.99, dominant_magnitude * 2)
            if amplitude_increasing:
                confidence = min(0.99, confidence * 1.5)

            return {
                "detected": True,
                "attack_type": "ENTROPY_RESONANCE",
                "confidence": confidence,
                "description": "System under destructive oscillation attack",
                "indicators": {
                    "oscillation_frequency": dominant_freq,
                    "oscillation_amplitude": dominant_magnitude,
                    "amplitude_increasing": amplitude_increasing,
                },
                "impact": "CRITICAL" if amplitude_increasing else "HIGH",
            }

        return {"detected": False}

    def _detect_anomaly(self) -> Dict[str, Any]:
        """
        Detect general anomalies using statistical methods

        Characteristics:
        - Values outside normal distribution
        - Sudden pattern changes
        - Unusual entropy patterns
        """
        if len(self.entropy_buffer) < 30:
            return {"detected": False}

        values = np.array([e["entropy"] for e in self.entropy_buffer])

        # Calculate statistical baseline
        mean = np.mean(values[:-5])  # Exclude recent values
        std = np.std(values[:-5])

        # Check recent values against baseline
        recent = values[-5:]
        anomalies = [
            v
            for v in recent
            if abs(v - mean) > self.thresholds["anomaly_std_multiplier"] * std
        ]

        if anomalies:
            confidence = min(0.99, len(anomalies) / len(recent))

            return {
                "detected": True,
                "attack_type": "ANOMALY",
                "confidence": confidence,
                "description": "Unusual entropy pattern detected",
                "indicators": {
                    "anomaly_count": len(anomalies),
                    "deviation_from_mean": max(abs(v - mean) for v in anomalies),
                    "baseline_mean": mean,
                    "baseline_std": std,
                },
                "impact": "MEDIUM",
            }

        return {"detected": False}

    def apply_mitigation(self, attack_type: str) -> Dict[str, Any]:
        """
        Apply mitigation strategy for detected attack

        Args:
            attack_type: Type of attack to mitigate

        Returns:
            Dictionary with mitigation actions taken
        """
        strategy = self._get_mitigation_strategy(attack_type)

        logger.warning(
            f"Applying mitigation for {attack_type}: {strategy['primary_action']}"
        )

        # Log mitigation
        mitigation_record = {
            "timestamp": datetime.now().isoformat(),
            "attack_type": attack_type,
            "strategy": strategy,
            "actions_taken": [],
        }

        # Apply actions
        for action in strategy["actions"]:
            result = self._execute_mitigation_action(action)
            mitigation_record["actions_taken"].append(result)

        self.mitigation_actions.append(mitigation_record)

        return mitigation_record

    def _get_mitigation_strategy(self, attack_type: str) -> Dict[str, Any]:
        """Get appropriate mitigation strategy for attack type"""

        strategies = {
            "ENTROPY_FLOOD": {
                "primary_action": "STABILIZE_SYSTEM",
                "actions": [
                    "increase_validation_steps",
                    "reduce_agent_autonomy",
                    "enforce_strict_protocols",
                    "quarantine_chaotic_agents",
                ],
                "priority": "CRITICAL",
                "estimated_recovery_time": "2-5 minutes",
            },
            "ENTROPY_DRAIN": {
                "primary_action": "INJECT_CONTROLLED_CHAOS",
                "actions": [
                    "create_explorer_agents",
                    "relax_constraints",
                    "inject_random_events",
                    "encourage_agent_creativity",
                ],
                "priority": "HIGH",
                "estimated_recovery_time": "5-10 minutes",
            },
            "ENTROPY_RESONANCE": {
                "primary_action": "BREAK_OSCILLATION_PATTERN",
                "actions": [
                    "desynchronize_agents",
                    "inject_phase_shift",
                    "modify_communication_timing",
                    "apply_damping_factor",
                ],
                "priority": "CRITICAL",
                "estimated_recovery_time": "1-3 minutes",
            },
            "ANOMALY": {
                "primary_action": "INVESTIGATE_AND_ISOLATE",
                "actions": [
                    "enable_detailed_logging",
                    "isolate_suspicious_agents",
                    "snapshot_current_state",
                    "increase_monitoring_frequency",
                ],
                "priority": "MEDIUM",
                "estimated_recovery_time": "10-15 minutes",
            },
        }

        return strategies.get(attack_type, strategies["ANOMALY"])

    def _execute_mitigation_action(self, action: str) -> Dict[str, Any]:
        """Execute a specific mitigation action"""

        logger.info(f"Executing mitigation action: {action}")

        # In a real implementation, this would actually modify the system
        # For now, we simulate the action

        return {
            "action": action,
            "status": "EXECUTED",
            "timestamp": datetime.now().isoformat(),
            "effect": "SIMULATED",  # Would be 'APPLIED' in production
        }

    def _log_threat(self, threat: Dict[str, Any]) -> None:
        """Log detected threat to alert history"""

        alert = {
            "timestamp": datetime.now().isoformat(),
            "threat": threat,
            "system_state": {
                "current_entropy": (
                    self.entropy_buffer[-1]["entropy"] if self.entropy_buffer else None
                ),
                "buffer_size": len(self.entropy_buffer),
            },
        }

        self.alert_history.append(alert)
        logger.warning(
            f"SECURITY ALERT: {threat['attack_type']} detected (confidence: {threat['confidence']:.2%})"
        )

    def _calculate_severity(self, threats: List[Dict[str, Any]]) -> str:
        """Calculate overall threat severity"""

        max_confidence = max(t["confidence"] for t in threats)
        threat_count = len(threats)

        if max_confidence > 0.9 or threat_count > 2:
            return "CRITICAL"
        elif max_confidence > 0.7 or threat_count > 1:
            return "HIGH"
        elif max_confidence > 0.5:
            return "MEDIUM"
        else:
            return "LOW"

    def _calculate_health_score(self) -> float:
        """Calculate system security health score (0-1)"""

        if len(self.entropy_buffer) < 10:
            return 0.5  # Unknown

        recent = [e["entropy"] for e in list(self.entropy_buffer)[-20:]]

        # Good health = stable entropy in optimal range
        in_optimal = sum(1 for e in recent if 0.3 <= e <= 0.7)
        stability = 1.0 - np.std(recent)

        health = (in_optimal / len(recent)) * 0.6 + stability * 0.4

        return health

    def generate_forensic_log(self) -> Dict[str, Any]:
        """
        Generate detailed forensic log for security analysis

        Returns:
            Comprehensive security report
        """
        return {
            "report_timestamp": datetime.now().isoformat(),
            "monitoring_duration": len(self.entropy_buffer),
            "total_alerts": len(self.alert_history),
            "alerts_by_type": self._count_alerts_by_type(),
            "mitigation_actions": len(self.mitigation_actions),
            "current_health_score": self._calculate_health_score(),
            "recent_alerts": self.alert_history[-10:] if self.alert_history else [],
            "entropy_statistics": self._calculate_entropy_statistics(),
            "threat_timeline": self._create_threat_timeline(),
        }

    def _count_alerts_by_type(self) -> Dict[str, int]:
        """Count alerts by attack type"""

        counts = {}
        for alert in self.alert_history:
            attack_type = alert["threat"]["attack_type"]
            counts[attack_type] = counts.get(attack_type, 0) + 1

        return counts

    def _calculate_entropy_statistics(self) -> Dict[str, float]:
        """Calculate statistical summary of entropy values"""

        if not self.entropy_buffer:
            return {}

        values = [e["entropy"] for e in self.entropy_buffer]

        return {
            "mean": float(np.mean(values)),
            "std": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "median": float(np.median(values)),
        }

    def _create_threat_timeline(self) -> List[Dict[str, Any]]:
        """Create timeline of security events"""

        timeline = []

        for alert in self.alert_history[-20:]:
            timeline.append(
                {
                    "timestamp": alert["timestamp"],
                    "event_type": "THREAT_DETECTED",
                    "attack_type": alert["threat"]["attack_type"],
                    "severity": alert["threat"].get("impact", "UNKNOWN"),
                }
            )

        for mitigation in self.mitigation_actions[-20:]:
            timeline.append(
                {
                    "timestamp": mitigation["timestamp"],
                    "event_type": "MITIGATION_APPLIED",
                    "attack_type": mitigation["attack_type"],
                    "actions_count": len(mitigation["actions_taken"]),
                }
            )

        # Sort by timestamp
        timeline.sort(key=lambda x: x["timestamp"])

        return timeline


SecurityLayer = EntropySecurity  # Alias for backward compatibility

__all__ = ["EntropySecurity", "SecurityLayer"]
