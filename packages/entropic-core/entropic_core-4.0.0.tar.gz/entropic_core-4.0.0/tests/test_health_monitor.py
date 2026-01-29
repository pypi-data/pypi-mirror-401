import pytest
import time
from unittest.mock import patch, MagicMock
from entropic_core.utils.health_monitor import HealthMonitor


class TestHealthMonitor:
    """Test HealthMonitor functionality"""
    
    def test_health_monitor_init(self):
        """Test HealthMonitor initialization"""
        monitor = HealthMonitor(check_interval=30)
        assert monitor.check_interval == 30
        assert monitor.is_monitoring is False
        assert len(monitor.health_history) == 0
    
    def test_start_monitoring(self):
        """Test starting health monitoring"""
        monitor = HealthMonitor(check_interval=1)
        monitor.start_monitoring()
        assert monitor.is_monitoring is True
        assert monitor._monitor_thread is not None
        time.sleep(0.5)
        monitor.stop_monitoring()
    
    def test_stop_monitoring(self):
        """Test stopping health monitoring"""
        monitor = HealthMonitor()
        monitor.start_monitoring()
        assert monitor.is_monitoring is True
        monitor.stop_monitoring()
        assert monitor.is_monitoring is False
    
    def test_start_monitoring_twice(self):
        """Test starting monitoring twice"""
        monitor = HealthMonitor()
        monitor.start_monitoring()
        monitor.start_monitoring()  # Should not crash
        assert monitor.is_monitoring is True
        monitor.stop_monitoring()
    
    def test_check_system_health(self):
        """Test system health check"""
        monitor = HealthMonitor()
        health = monitor.check_system_health()
        
        assert 'timestamp' in health
        assert 'status' in health
        assert 'metrics' in health
        assert 'issues' in health
        assert health['status'] in ['healthy', 'unhealthy']
    
    def test_record_request(self):
        """Test recording request for monitoring"""
        monitor = HealthMonitor()
        monitor.record_request(0.5, error=False)
        monitor.record_request(0.3, error=False)
        monitor.record_request(0.7, error=True)
        
        assert monitor.total_requests == 3
        assert monitor.error_count == 1
        assert len(monitor.response_times) == 3
    
    def test_response_times_history_limit(self):
        """Test response times are limited to 1000 entries"""
        monitor = HealthMonitor()
        
        # Add 1500 requests
        for i in range(1500):
            monitor.record_request(0.1, error=False)
        
        assert len(monitor.response_times) <= 1000
    
    def test_health_history_limit(self):
        """Test health history is limited to 1000 entries"""
        monitor = HealthMonitor(check_interval=0.01)
        monitor.start_monitoring()
        
        time.sleep(0.5)  # Let it collect some history
        
        # Manually add entries to exceed limit
        while len(monitor.health_history) < 1500:
            monitor.health_history.append({
                'timestamp': time.time(),
                'status': {'status': 'healthy', 'issues': [], 'metrics': {}}
            })
        
        monitor.stop_monitoring()
        assert len(monitor.health_history) <= 1000
    
    def test_get_health_report(self):
        """Test health report generation"""
        monitor = HealthMonitor()
        monitor.record_request(0.1)
        monitor.record_request(0.2)
        
        report = monitor.get_health_report()
        assert isinstance(report, str)
        assert 'CPU' in report
        assert 'Memory' in report
        assert 'Error Rate' in report
    
    def test_get_metrics_summary(self):
        """Test metrics summary"""
        monitor = HealthMonitor()
        
        # Add some health history
        for _ in range(5):
            health_entry = {
                'status': {'status': 'healthy', 'issues': [], 'metrics': {}},
                'timestamp': time.time()
            }
            monitor.health_history.append(health_entry)
        
        summary = monitor.get_metrics_summary()
        assert 'total_checks' in summary
        assert 'recent_health_rate' in summary
        assert 'uptime_estimate' in summary
    
    def test_metrics_summary_no_history(self):
        """Test metrics summary with no history"""
        monitor = HealthMonitor()
        summary = monitor.get_metrics_summary()
        
        assert 'error' in summary
        assert 'No health history' in summary['error']
    
    @patch('psutil.virtual_memory')
    def test_check_memory(self, mock_memory):
        """Test memory check"""
        mock_mem = MagicMock()
        mock_mem.total = 16 * 1024**3
        mock_mem.used = 8 * 1024**3
        mock_mem.available = 8 * 1024**3
        mock_mem.percent = 50.0
        mock_memory.return_value = mock_mem
        
        monitor = HealthMonitor()
        memory = monitor._check_memory()
        
        assert 'total_gb' in memory
        assert 'used_gb' in memory
        assert 'percent' in memory
    
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    def test_check_cpu(self, mock_count, mock_percent):
        """Test CPU check"""
        mock_percent.return_value = 45.0
        mock_count.return_value = 4
        
        monitor = HealthMonitor()
        cpu = monitor._check_cpu()
        
        assert 'percent' in cpu
        assert 'cores' in cpu
