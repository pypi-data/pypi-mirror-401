"""
Health Monitoring System for Entropic Core
Monitors the health of the monitoring system itself
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)


class HealthMonitor:
    """
    Monitors the health of Entropic Core itself

    Tracks:
    - System resource usage (CPU, memory)
    - API response times
    - Error rates
    - Service availability
    """

    def __init__(self, check_interval: int = 60):
        """
        Initialize health monitor

        Args:
            check_interval: Seconds between health checks
        """
        self.check_interval = check_interval
        self.health_history: List[Dict] = []
        self.error_count = 0
        self.total_requests = 0
        self.response_times: List[float] = []
        self.is_monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None

        logger.info("HealthMonitor initialized")

    def start_monitoring(self):
        """Start continuous health monitoring"""
        if self.is_monitoring:
            logger.warning("Health monitoring already running")
            return

        self.is_monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Health monitoring started")

    def stop_monitoring(self):
        """Stop health monitoring"""
        self.is_monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        logger.info("Health monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                health_status = self.check_system_health()
                self.health_history.append(
                    {"timestamp": datetime.now(), "status": health_status}
                )

                # Keep only last 1000 checks
                if len(self.health_history) > 1000:
                    self.health_history = self.health_history[-1000:]

                # Alert if unhealthy
                if health_status["status"] != "healthy":
                    logger.warning(f"System unhealthy: {health_status['issues']}")

            except Exception as e:
                logger.error(f"Error in health monitor loop: {e}")

            time.sleep(self.check_interval)

    def check_system_health(self) -> Dict:
        """
        Comprehensive system health check

        Returns:
            Dictionary with health metrics and status ('healthy' or 'unhealthy')
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "issues": [],
            "metrics": {},
        }

        # Check core services
        services = self._check_services()
        health["metrics"]["services"] = services
        if not services["all_running"]:
            health["status"] = "unhealthy"
            health["issues"].append("Some services not running")

        # Check memory usage
        memory = self._check_memory()
        health["metrics"]["memory"] = memory
        if memory.get("percent", 0) > 90:
            health["status"] = "unhealthy"
            health["issues"].append(f"High memory usage: {memory['percent']:.1f}%")

        # Check CPU usage
        cpu = self._check_cpu()
        health["metrics"]["cpu"] = cpu
        if cpu.get("percent", 0) > 90:
            health["status"] = "unhealthy"
            health["issues"].append(f"High CPU usage: {cpu['percent']:.1f}%")

        # Check API latency
        latency = self._check_latency()
        health["metrics"]["latency"] = latency
        if latency.get("avg_ms", 0) > 1000:
            health["status"] = "unhealthy"
            health["issues"].append(f"High latency: {latency['avg_ms']:.0f}ms")

        # Check error rate
        error_rate = self._check_errors()
        health["metrics"]["error_rate"] = error_rate
        if error_rate.get("rate", 0) > 0.05:  # >5% error rate
            health["status"] = "unhealthy"
            health["issues"].append(f"High error rate: {error_rate['rate']:.1%}")

        return health

    def _check_services(self) -> Dict:
        """Check if core services are running"""
        services = {
            "monitor": True,  # Assume running if we can check
            "regulator": True,
            "memory": True,
            "all_running": True,
        }

        # In real implementation, would check actual service status
        # For now, basic heuristic checks

        return services

    def _check_memory(self) -> Dict:
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            return {
                "total_gb": memory.total / (1024**3),
                "used_gb": memory.used / (1024**3),
                "available_gb": memory.available / (1024**3),
                "percent": memory.percent,
            }
        except Exception as e:
            logger.error(f"Error checking memory: {e}")
            return {"percent": 0, "error": str(e)}

    def _check_cpu(self) -> Dict:
        """Check CPU usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            return {
                "percent": cpu_percent,
                "cores": cpu_count,
                "per_core": psutil.cpu_percent(interval=1, percpu=True),
            }
        except Exception as e:
            logger.error(f"Error checking CPU: {e}")
            return {"percent": 0, "error": str(e)}

    def _check_latency(self) -> Dict:
        """Check API response latency"""
        if len(self.response_times) == 0:
            return {"avg_ms": 0, "min_ms": 0, "max_ms": 0, "p95_ms": 0}

        recent_times = self.response_times[-100:]  # Last 100 requests
        sorted_times = sorted(recent_times)

        return {
            "avg_ms": sum(recent_times) / len(recent_times) * 1000,
            "min_ms": min(recent_times) * 1000,
            "max_ms": max(recent_times) * 1000,
            "p95_ms": (
                sorted_times[int(len(sorted_times) * 0.95)] * 1000
                if sorted_times
                else 0
            ),
        }

    def _check_errors(self) -> Dict:
        """Check error rate"""
        if self.total_requests == 0:
            return {"rate": 0.0, "total_errors": 0, "total_requests": 0}

        return {
            "rate": self.error_count / self.total_requests,
            "total_errors": self.error_count,
            "total_requests": self.total_requests,
        }

    def record_request(self, duration: float, error: bool = False):
        """
        Record a request for monitoring

        Args:
            duration: Request duration in seconds
            error: Whether the request resulted in an error
        """
        self.total_requests += 1
        self.response_times.append(duration)

        if error:
            self.error_count += 1

        # Keep only last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]

    def get_health_report(self) -> str:
        """
        Generate human-readable health report

        Returns:
            Formatted health report string
        """
        health = self.check_system_health()

        status_icon = "✅ HEALTHY" if health["status"] == "healthy" else "⚠️  UNHEALTHY"

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           ENTROPIC CORE - SYSTEM HEALTH REPORT               ║
╠══════════════════════════════════════════════════════════════╣
║ Status: {status_icon}
║ Timestamp: {health['timestamp']}
╠══════════════════════════════════════════════════════════════╣
║ RESOURCE USAGE:
║   CPU: {health['metrics']['cpu'].get('percent', 0):.1f}%
║   Memory: {health['metrics']['memory'].get('percent', 0):.1f}% ({health['metrics']['memory'].get('used_gb', 0):.1f}GB / {health['metrics']['memory'].get('total_gb', 0):.1f}GB)
╠══════════════════════════════════════════════════════════════╣
║ PERFORMANCE:
║   Avg Latency: {health['metrics']['latency'].get('avg_ms', 0):.0f}ms
║   P95 Latency: {health['metrics']['latency'].get('p95_ms', 0):.0f}ms
║   Error Rate: {health['metrics']['error_rate'].get('rate', 0):.2%}
╠══════════════════════════════════════════════════════════════╣
"""

        if health["issues"]:
            report += "║ ISSUES:\n"
            for issue in health["issues"]:
                report += f"║   • {issue}\n"
            report += (
                "╠══════════════════════════════════════════════════════════════╣\n"
            )

        report += "╚══════════════════════════════════════════════════════════════╝"

        return report

    def get_metrics_summary(self) -> Dict:
        """Get summary of key metrics over time"""
        if len(self.health_history) == 0:
            return {"error": "No health history available"}

        recent_checks = self.health_history[-10:]  # Last 10 checks

        healthy_count = sum(
            1 for check in recent_checks if check["status"]["status"] == "healthy"
        )

        return {
            "total_checks": len(self.health_history),
            "recent_health_rate": healthy_count / len(recent_checks),
            "current_status": recent_checks[-1]["status"] if recent_checks else None,
            "uptime_estimate": healthy_count / len(recent_checks) * 100,
        }
