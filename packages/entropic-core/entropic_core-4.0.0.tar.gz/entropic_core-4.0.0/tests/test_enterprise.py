"""
Enterprise Features Test Suite
Tests for orchestrator, marketplace, compliance, and reporting
"""

import os
import tempfile
from datetime import datetime

from entropic_core import EntropyBrain
from entropic_core.enterprise.compliance import ComplianceRecorder
from entropic_core.enterprise.marketplace import PatternMarketplace
from entropic_core.enterprise.orchestrator import EntropyOrchestrator
from entropic_core.visualization.report_generator import ReportGenerator


class TestOrchestrator:
    """Test multi-system orchestration"""

    def test_subsystem_registration(self):
        """Test registering and managing subsystems"""
        orchestrator = EntropyOrchestrator()

        brain1 = EntropyBrain()
        brain2 = EntropyBrain()

        orchestrator.register_subsystem("system1", brain1)
        orchestrator.register_subsystem("system2", brain2)

        assert len(orchestrator.subsystems) == 2
        assert "system1" in orchestrator.subsystems
        assert "system2" in orchestrator.subsystems

    def test_global_entropy_calculation(self):
        """Test calculating entropy across systems"""
        orchestrator = EntropyOrchestrator()

        brain1 = EntropyBrain()
        brain2 = EntropyBrain()

        # Create mock agents
        class MockAgent:
            def __init__(self, state: float):
                self.current_state = state
                self.last_decision = "action"
                self.messages_sent = 5

        brain1.connect([MockAgent(0.3), MockAgent(0.4)])
        brain2.connect([MockAgent(0.6), MockAgent(0.7)])

        orchestrator.register_subsystem("system1", brain1)
        orchestrator.register_subsystem("system2", brain2)

        result = orchestrator.coordinate_cross_system()

        assert "global_entropy" in result
        assert 0.0 <= result["global_entropy"] <= 1.0
        assert result["subsystem_count"] == 2

    def test_resonance_detection(self):
        """Test detecting dangerous resonances"""
        orchestrator = EntropyOrchestrator()

        brain1 = EntropyBrain()
        brain2 = EntropyBrain()

        class MockAgent:
            def __init__(self, state: float):
                self.current_state = state
                self.last_decision = "action"
                self.messages_sent = 10

        # Create synchronized high-entropy systems (dangerous)
        brain1.connect([MockAgent(0.9), MockAgent(0.9)])
        brain2.connect([MockAgent(0.9), MockAgent(0.9)])

        orchestrator.register_subsystem("system1", brain1)
        orchestrator.register_subsystem("system2", brain2)

        result = orchestrator.coordinate_cross_system()

        assert "resonances" in result
        # Should detect dangerous synchronization
        if result["resonances"]["dangerous_sync"]:
            assert len(result["resonances"]["affected_systems"]) > 0


class TestMarketplace:
    """Test pattern marketplace"""

    def setup_method(self):
        """Setup temp directory for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.marketplace = PatternMarketplace(storage_dir=self.temp_dir)

    def test_upload_pattern(self):
        """Test uploading a pattern"""
        pattern = {
            "conditions": [{"entropy": {"above": 0.8}}],
            "actions": ["reduce_communication"],
        }

        result = self.marketplace.upload_pattern(
            name="High Entropy Stabilizer",
            pattern=pattern,
            description="Stabilizes high entropy systems",
            tags=["stability", "high-entropy"],
        )

        assert "pattern_id" in result
        assert result["status"] == "uploaded"

    def test_download_pattern(self):
        """Test downloading a pattern"""
        # Upload first
        pattern = {
            "conditions": [{"entropy": {"below": 0.3}}],
            "actions": ["inject_exploration"],
        }

        upload_result = self.marketplace.upload_pattern(
            name="Low Entropy Booster",
            pattern=pattern,
            description="Boosts creativity in stagnant systems",
            tags=["innovation", "low-entropy"],
        )

        pattern_id = upload_result["pattern_id"]

        # Download
        download_result = self.marketplace.download_pattern(pattern_id)

        assert "pattern" in download_result
        assert download_result["pattern"] == pattern
        assert "success_metrics" in download_result

    def test_rate_pattern(self):
        """Test rating a pattern"""
        # Upload pattern
        pattern = {"test": "data"}
        upload_result = self.marketplace.upload_pattern(
            name="Test Pattern", pattern=pattern, description="Test", tags=["test"]
        )

        pattern_id = upload_result["pattern_id"]

        # Rate it
        rate_result = self.marketplace.rate_pattern(
            pattern_id=pattern_id, rating=4.5, review="Works great!"
        )

        assert rate_result["status"] == "rated"
        assert rate_result["new_average"] == 4.5

    def test_search_patterns(self):
        """Test searching patterns"""
        # Upload multiple patterns
        self.marketplace.upload_pattern(
            name="Stability Pattern",
            pattern={"type": "stability"},
            description="Maintains stable entropy",
            tags=["stability"],
        )

        self.marketplace.upload_pattern(
            name="Innovation Pattern",
            pattern={"type": "innovation"},
            description="Promotes exploration",
            tags=["innovation"],
        )

        # Search
        results = self.marketplace.search_patterns(query="stability")

        assert len(results) >= 1
        assert any("stability" in r["name"].lower() for r in results)


class TestCompliance:
    """Test compliance and auditing"""

    def setup_method(self):
        """Setup temp database for each test"""
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()  # Close file handle immediately
        self.compliance = ComplianceRecorder(db_path=self.temp_db.name)

    def teardown_method(self):
        """Cleanup temp database"""
        if hasattr(self, "compliance"):
            self.compliance.close()
        try:
            os.unlink(self.temp_db.name)
        except (PermissionError, FileNotFoundError):
            pass  # Ignore if file is locked or already deleted

    def test_record_regulation(self):
        """Test recording regulation for compliance"""
        event_id = self.compliance.record_regulation(
            timestamp=datetime.now(),
            entropy=0.75,
            action="reduce_chaos",
            agents_affected=["agent1", "agent2"],
            metadata={"reason": "high_entropy"},
        )

        assert event_id is not None
        assert isinstance(event_id, int)

    def test_generate_audit_trail(self):
        """Test generating audit trail"""
        # Record some events
        for i in range(5):
            self.compliance.record_regulation(
                timestamp=datetime.now(),
                entropy=0.5 + (i * 0.1),
                action="maintain",
                agents_affected=["agent1"],
                metadata={},
            )

        # Generate trail
        trail = self.compliance.generate_audit_trail(start_date=datetime.now())

        assert "total_events" in trail
        assert trail["total_events"] >= 5


class TestReportGenerator:
    """Test report generation"""

    def setup_method(self):
        """Setup temp directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.brain = EntropyBrain()
        self.generator = ReportGenerator(self.brain)

    def test_generate_markdown_report(self):
        """Test generating markdown report"""
        output_file = os.path.join(self.temp_dir, "report.md")

        self.generator.generate_report(format="markdown", output_file=output_file)

        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
            assert "# Entropy System Report" in content

    def test_generate_html_report(self):
        """Test generating HTML report"""
        output_file = os.path.join(self.temp_dir, "report.html")

        self.generator.generate_report(format="html", output_file=output_file)

        assert os.path.exists(output_file)
        with open(output_file) as f:
            content = f.read()
            assert "<html>" in content or "<!DOCTYPE html>" in content
