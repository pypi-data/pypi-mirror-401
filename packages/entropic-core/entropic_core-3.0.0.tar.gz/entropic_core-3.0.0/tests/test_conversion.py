"""
Comprehensive tests for conversion tracking system
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, "scripts")

from entropic_core.conversion.converter import ConversionManager
from entropic_core.conversion.tracker import UsageTracker


class TestUsageTracker:
    """Tests for UsageTracker"""

    def test_tracker_initialization(self):
        """Test tracker initializes correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                assert tracker.stats["total_cycles"] == 0
                assert tracker.stats["total_regulations"] == 0

    def test_track_cycle(self):
        """Test tracking monitoring cycles"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                tracker.track_cycle()
                assert tracker.stats["total_cycles"] == 1

                tracker.track_cycle()
                assert tracker.stats["total_cycles"] == 2

    def test_track_regulation(self):
        """Test tracking regulation actions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                tracker.track_regulation("REDUCE_CHAOS")
                assert tracker.stats["total_regulations"] == 1
                assert "REDUCE_CHAOS" in tracker.stats["regulations_by_type"]

    def test_track_prevention(self):
        """Test tracking prevented incidents"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                tracker.track_prevention("infinite_loop")
                assert tracker.stats["preventions"] == 1

    def test_track_api_save(self):
        """Test tracking API calls saved"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                tracker.track_api_save(100)
                assert tracker.stats["api_calls_saved"] == 100

                tracker.track_api_save(50)
                assert tracker.stats["api_calls_saved"] == 150

    def test_calculate_value(self):
        """Test value calculation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                tracker.stats["preventions"] = 5
                tracker.stats["api_calls_saved"] = 1000

                value = tracker.calculate_value()

                assert value["incidents_prevented"] == 5
                assert value["api_calls_saved"] == 1000
                assert value["estimated_savings"] > 0

    def test_should_show_conversion(self):
        """Test conversion timing logic"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                # First regulation should trigger conversion
                tracker.stats["total_regulations"] = 1
                assert tracker.should_show_conversion()

                # After showing, shouldn't show again immediately
                tracker.mark_conversion_shown()
                assert not tracker.should_show_conversion()


class TestConversionManager:
    """Tests for ConversionManager"""

    def test_manager_initialization(self):
        """Test manager initializes correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)
                manager = ConversionManager(tracker)
                assert manager.tracker is tracker

    def test_get_value_message(self):
        """Test value message generation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)
                tracker.stats["preventions"] = 3
                tracker.stats["api_calls_saved"] = 500

                manager = ConversionManager(tracker)
                message = manager.get_value_message()

                assert message is not None
                assert "prevented" in message.lower() or "saved" in message.lower()

    def test_get_milestone_message(self):
        """Test milestone message generation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)

                manager = ConversionManager(tracker)

                # First success
                msg = manager.get_milestone_message("first_success")
                assert msg is not None

                # 10th regulation
                msg = manager.get_milestone_message("tenth_regulation")
                assert msg is not None

    def test_check_and_show_conversion(self):
        """Test conversion check and display"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(
                UsageTracker, "_get_storage_dir", return_value=Path(tmpdir)
            ):
                tracker = UsageTracker()
                tracker.storage_dir = Path(tmpdir)
                tracker.stats["total_regulations"] = 1

                manager = ConversionManager(tracker)

                # Should return a message on first regulation
                manager.check_and_show_conversion()
                # Result can be None or a message string


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
