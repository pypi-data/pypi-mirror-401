import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from pathlib import Path
from entropic_core.visualization.report_generator import ReportGenerator


class TestReportGenerator:
    """Test ReportGenerator"""
    
    def test_report_generator_init(self):
        """Test ReportGenerator initialization"""
        brain = MagicMock()
        gen = ReportGenerator(brain)
        
        assert gen.brain == brain
    
    def test_generate_report_markdown(self):
        """Test generating markdown report"""
        brain = MagicMock()
        brain.measure.return_value = 0.5
        brain.agents = [MagicMock(), MagicMock()]
        
        gen = ReportGenerator(brain)
        report = gen.generate_report(format='markdown')
        
        assert isinstance(report, str)
        assert 'Entropy' in report or 'entropy' in report.lower()
    
    def test_generate_report_html(self):
        """Test generating HTML report"""
        brain = MagicMock()
        brain.measure.return_value = 0.5
        brain.agents = []
        
        gen = ReportGenerator(brain)
        report = gen.generate_report(format='html')
        
        assert '<!DOCTYPE html>' in report or '<html>' in report
    
    def test_generate_report_with_file_output(self):
        """Test generating report to file"""
        brain = MagicMock()
        gen = ReportGenerator(brain)
        
        with patch('builtins.open', create=True):
            with patch('pathlib.Path.mkdir'):
                with patch('pathlib.Path.write_text'):
                    report = gen.generate_report(format='markdown', output_file='/tmp/test.md')
                    assert isinstance(report, str)
    
    def test_generate_daily_report(self):
        """Test generating daily report"""
        brain = MagicMock()
        brain.memory = MagicMock()
        brain.memory.get_entropy_history_range.return_value = [
            {'entropy': 0.5, 'timestamp': datetime.now(), 'regulated': False}
        ]
        
        gen = ReportGenerator(brain)
        report = gen.generate_daily_report()
        
        assert 'date' in report
        assert 'metrics' in report
        assert 'recommendations' in report
    
    def test_generate_weekly_report(self):
        """Test generating weekly report"""
        brain = MagicMock()
        brain.memory = MagicMock()
        brain.memory.get_entropy_history_range.return_value = []
        
        gen = ReportGenerator(brain)
        report = gen.generate_weekly_report()
        
        assert 'week_start' in report
        assert 'metrics' in report
    
    def test_export_to_markdown(self):
        """Test exporting to markdown"""
        gen = ReportGenerator(None)
        
        report_data = {
            'date': '2024-01-01',
            'summary': 'Test summary',
            'metrics': {'avg_entropy': 0.5},
            'events': [],
            'recommendations': ['Test recommendation']
        }
        
        md = gen.export_to_markdown(report_data)
        
        assert 'Entropic Core Report' in md
        assert 'Test recommendation' in md
    
    def test_export_to_html(self):
        """Test exporting to HTML"""
        gen = ReportGenerator(None)
        
        report_data = {
            'date': '2024-01-01',
            'summary': 'Test summary',
            'metrics': {'avg_entropy': 0.5},
            'events': [],
            'recommendations': ['Test recommendation']
        }
        
        html = gen.export_to_html(report_data)
        
        assert '<!DOCTYPE html>' in html or '<html>' in html
    
    def test_save_report(self):
        """Test saving report to file"""
        gen = ReportGenerator(None)
        
        report_data = {
            'date': '2024-01-01',
            'summary': 'Test',
            'metrics': {},
            'events': [],
            'recommendations': []
        }
        
        with patch('pathlib.Path.mkdir'):
            with patch('pathlib.Path.write_text'):
                filepath = gen.save_report(report_data, format='markdown')
                assert filepath is not None
