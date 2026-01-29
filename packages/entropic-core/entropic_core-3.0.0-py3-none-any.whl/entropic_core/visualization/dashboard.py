"""
Web Dashboard for Real-time Entropy Monitoring
Provides live visualization and interactive controls
"""

import threading
from datetime import datetime
from typing import Dict, List

from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS


class EntropyDashboard:
    """
    Real-time web dashboard for entropy monitoring
    Provides live graphs, agent heatmaps, and control panel
    """

    def __init__(self, brain=None, host="0.0.0.0", port=5000):
        self.brain = brain
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        self._setup_routes()
        self._monitoring_active = False

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route("/")
        def index():
            return render_template_string(self._get_dashboard_html())

        @self.app.route("/health")
        def health():
            """Health check endpoint for Docker"""
            from entropic_core.utils.health_monitor import HealthMonitor

            hm = HealthMonitor()
            health_status = hm.check_system_health()

            return jsonify(health_status), (
                200 if health_status["status"] == "healthy" else 503
            )

        @self.app.route("/api/entropy/current")
        def get_current_entropy():
            """Get current entropy metrics"""
            if not self.brain or not self.brain.wrapped_agents:
                return jsonify(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "metrics": {
                            "combined": 0.0,
                            "decision": 0.0,
                            "dispersion": 0.0,
                            "communication": 0.0,
                        },
                        "agent_count": 0,
                        "status": "NO_AGENTS",
                    }
                )

            metrics = self.brain.measure()
            return jsonify(
                {
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics,
                    "agent_count": len(self.brain.agents),
                    "status": self._get_system_status(metrics["combined"]),
                }
            )

        @self.app.route("/api/entropy/history")
        def get_entropy_history():
            """Get historical entropy data"""
            hours = int(request.args.get("hours", 1))

            if not self.brain:
                return jsonify({"data": [], "summary": {}})

            history = self.brain.memory.get_metrics_history(hours=hours)
            return jsonify(
                {"data": history, "summary": self._calculate_summary(history)}
            )

        @self.app.route("/api/entropy/forecast")
        def get_forecast():
            """Get entropy forecast"""
            if (
                not self.brain
                or not hasattr(self.brain, "predictive_engine")
                or not self.brain.predictive_engine
            ):
                return jsonify({"error": "Predictive engine not available"}), 404

            try:
                forecast = self.brain.forecast()
                return jsonify(forecast)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/agents/status")
        def get_agents_status():
            """Get status of all agents"""
            if not self.brain:
                return jsonify({"agents": []})

            agents_data = []
            for i, agent in enumerate(self.brain.wrapped_agents):
                state = agent.get_state() if hasattr(agent, "get_state") else {}
                agents_data.append(
                    {
                        "id": state.get("agent_id", f"agent_{i}"),
                        "name": getattr(agent, "name", f"Agent {i}"),
                        "state": state.get("current_state", "active"),
                        "last_action": state.get("last_action", None),
                        "entropy_contribution": 0.5,  # Simplified
                    }
                )
            return jsonify({"agents": agents_data})

        @self.app.route("/api/alerts/active")
        def get_active_alerts():
            """Get active system alerts"""
            alerts = self._generate_alerts()
            return jsonify({"alerts": alerts})

        @self.app.route("/api/control/regulate", methods=["POST"])
        def manual_regulate():
            """Manually trigger regulation"""
            if not self.brain:
                return jsonify({"error": "No brain connected"}), 400

            result = self.brain.regulate()
            return jsonify(result)

    def _get_system_status(self, entropy: float) -> str:
        """Determine system status from entropy"""
        if entropy < 0.3:
            return "STAGNANT"
        elif entropy > 0.8:
            return "CHAOTIC"
        elif 0.4 <= entropy <= 0.6:
            return "OPTIMAL"
        else:
            return "STABLE"

    def _calculate_summary(self, history: List[Dict]) -> Dict:
        """Calculate summary statistics from history"""
        if not history:
            return {"avg": 0, "min": 0, "max": 0, "trend": "stable"}

        values = [
            h.get("combined", 0) for h in history if h.get("combined") is not None
        ]
        if not values:
            return {"avg": 0, "min": 0, "max": 0, "trend": "stable"}

        return {
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "trend": (
                "increasing"
                if len(values) > 1 and values[-1] > values[0]
                else "decreasing"
            ),
        }

    def _generate_alerts(self) -> List[Dict]:
        """Generate current system alerts"""
        alerts = []

        if not self.brain or not self.brain.wrapped_agents:
            return alerts

        current_entropy = self.brain.measure()

        if current_entropy["combined"] > 0.8:
            alerts.append(
                {
                    "level": "critical",
                    "message": "System entropy critically high",
                    "timestamp": datetime.now().isoformat(),
                    "value": current_entropy["combined"],
                }
            )
        elif current_entropy["combined"] < 0.2:
            alerts.append(
                {
                    "level": "warning",
                    "message": "System entropy too low - risk of stagnation",
                    "timestamp": datetime.now().isoformat(),
                    "value": current_entropy["combined"],
                }
            )

        return alerts

    def _get_dashboard_html(self) -> str:
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Entropic Core - Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.18.0.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .header h1 { font-size: 32px; margin-bottom: 8px; }
        .header p { opacity: 0.9; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
        }
        .card h3 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #667eea;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #333;
        }
        .metric:last-child { border-bottom: none; }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
        }
        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: bold;
        }
        .status-optimal { background: #10b981; color: white; }
        .status-stable { background: #3b82f6; color: white; }
        .status-chaotic { background: #ef4444; color: white; }
        .status-stagnant { background: #f59e0b; color: white; }
        .alert {
            background: #ef4444;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        .alert-warning { background: #f59e0b; }
        #entropyChart { height: 400px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Entropic Core Dashboard</h1>
        <p>Real-time Multi-Agent System Monitoring - 100% FREE</p>
    </div>
    
    <div class="grid">
        <div class="card">
            <h3>System Status</h3>
            <div class="metric">
                <span>Current Entropy</span>
                <span class="metric-value" id="currentEntropy">--</span>
            </div>
            <div class="metric">
                <span>Status</span>
                <span id="systemStatus">--</span>
            </div>
            <div class="metric">
                <span>Active Agents</span>
                <span class="metric-value" id="agentCount">--</span>
            </div>
        </div>
        
        <div class="card">
            <h3>Predictions</h3>
            <div class="metric">
                <span>Next Value</span>
                <span class="metric-value" id="nextValue">--</span>
            </div>
            <div class="metric">
                <span>Confidence</span>
                <span id="confidence">--</span>
            </div>
            <div class="metric">
                <span>Risk Level</span>
                <span id="riskLevel">--</span>
            </div>
        </div>
        
        <div class="card">
            <h3>Active Alerts</h3>
            <div id="alertsContainer">
                <p style="opacity: 0.5;">No active alerts</p>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h3>Entropy History</h3>
        <div id="entropyChart"></div>
    </div>
    
    <script>
        function updateDashboard() {
            fetch('/api/entropy/current')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('currentEntropy').textContent = 
                        data.metrics.combined.toFixed(3);
                    document.getElementById('agentCount').textContent = 
                        data.agent_count;
                    
                    const statusEl = document.getElementById('systemStatus');
                    statusEl.textContent = data.status;
                    statusEl.className = 'status status-' + data.status.toLowerCase();
                });
            
            fetch('/api/entropy/forecast')
                .then(r => r.json())
                .then(data => {
                    if (!data.error) {
                        document.getElementById('nextValue').textContent = 
                            (data.next_entropy_value || 0).toFixed(3);
                        document.getElementById('confidence').textContent = 
                            ((data.confidence || 0) * 100).toFixed(1) + '%';
                        document.getElementById('riskLevel').textContent = 
                            data.risk_level || 'UNKNOWN';
                    }
                })
                .catch(() => {
                    document.getElementById('nextValue').textContent = 'N/A';
                    document.getElementById('confidence').textContent = 'N/A';
                    document.getElementById('riskLevel').textContent = 'N/A';
                });
            
            fetch('/api/alerts/active')
                .then(r => r.json())
                .then(data => {
                    const container = document.getElementById('alertsContainer');
                    if (data.alerts.length === 0) {
                        container.innerHTML = '<p style="opacity: 0.5;">No active alerts</p>';
                    } else {
                        container.innerHTML = data.alerts.map(alert => 
                            `<div class="alert alert-${alert.level}">${alert.message}</div>`
                        ).join('');
                    }
                });
            
            fetch('/api/entropy/history?hours=1')
                .then(r => r.json())
                .then(data => {
                    const trace = {
                        x: data.data.map(d => d.timestamp),
                        y: data.data.map(d => d.combined),
                        type: 'scatter',
                        mode: 'lines',
                        line: { color: '#667eea', width: 2 }
                    };
                    
                    const layout = {
                        paper_bgcolor: '#1a1a1a',
                        plot_bgcolor: '#1a1a1a',
                        font: { color: '#e0e0e0' },
                        xaxis: { gridcolor: '#333' },
                        yaxis: { gridcolor: '#333', range: [0, 1] },
                        margin: { t: 20, r: 20, b: 40, l: 50 }
                    };
                    
                    Plotly.newPlot('entropyChart', [trace], layout, {responsive: true});
                });
        }
        
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
        """

    def run(self, host=None, port=None, debug=False):
        """Start the dashboard server"""
        host = host or self.host
        port = port or self.port
        print(f"Starting Entropic Core Dashboard on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug, threaded=True)

    def start_background(self):
        """Start dashboard in background thread"""
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread
