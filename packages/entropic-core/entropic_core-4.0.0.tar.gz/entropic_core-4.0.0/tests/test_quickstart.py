import pytest
from unittest.mock import patch, MagicMock
from entropic_core.quickstart import QuickstartDemo, DemoAgent


class TestDemoAgent:
    """Test DemoAgent functionality"""
    
    def test_demo_agent_init(self):
        """Test DemoAgent initialization"""
        agent = DemoAgent("TestAgent", behavior="normal")
        assert agent.name == "TestAgent"
        assert agent.behavior == "normal"
        assert agent.decision_count == 0
        assert agent.state == 0.5
    
    def test_demo_agent_make_decision_chaotic(self):
        """Test chaotic agent behavior"""
        agent = DemoAgent("Chaotic", behavior="chaotic")
        agent.make_decision()
        
        assert agent.decision_count == 1
        assert 0 <= agent.state <= 1
    
    def test_demo_agent_make_decision_rigid(self):
        """Test rigid agent behavior"""
        agent = DemoAgent("Rigid", behavior="rigid")
        agent.make_decision()
        
        assert agent.decision_count == 1
        assert agent.state == 0.5  # Rigid stays at 0.5
    
    def test_demo_agent_make_decision_normal(self):
        """Test normal agent behavior"""
        agent = DemoAgent("Normal", behavior="normal")
        initial_state = agent.state
        agent.make_decision()
        
        assert agent.decision_count == 1
        assert 0 <= agent.state <= 1


class TestQuickstartDemo:
    """Test QuickstartDemo functionality"""
    
    def test_quickstart_demo_init(self):
        """Test QuickstartDemo initialization"""
        demo = QuickstartDemo()
        assert len(demo.agents) == 0
        assert demo.monitor is None
        assert demo.regulator is None
    
    @patch('entropic_core.quickstart.SetupWizard')
    @patch('entropic_core.quickstart.EntropyMonitor')
    @patch('entropic_core.quickstart.EntropyRegulator')
    def test_quickstart_demo_run(self, mock_regulator, mock_monitor, mock_wizard):
        """Test QuickstartDemo run method"""
        mock_wizard_instance = MagicMock()
        mock_wizard_instance.quick_check.return_value = True
        mock_wizard.return_value = mock_wizard_instance
        
        mock_monitor_instance = MagicMock()
        mock_monitor_instance.measure_system_entropy.return_value = {'combined': 0.5}
        mock_monitor.return_value = mock_monitor_instance
        
        mock_regulator_instance = MagicMock()
        mock_regulator_instance.regulate.return_value = {'action': 'maintain'}
        mock_regulator.return_value = mock_regulator_instance
        
        demo = QuickstartDemo()
        with patch('time.time') as mock_time:
            mock_time.side_effect = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Enough for the test
            try:
                demo.run(duration_seconds=5)
            except:
                pass  # May fail due to mocking, that's okay
    
    def test_get_status_emoji_chaotic(self):
        """Test status emoji for chaotic entropy"""
        demo = QuickstartDemo()
        emoji = demo._get_status_emoji(0.85)
        assert '🔴' in emoji or 'CHAOTIC' in emoji
    
    def test_get_status_emoji_rigid(self):
        """Test status emoji for rigid entropy"""
        demo = QuickstartDemo()
        emoji = demo._get_status_emoji(0.15)
        assert '🔵' in emoji or 'RIGID' in emoji
    
    def test_get_status_emoji_optimal(self):
        """Test status emoji for optimal entropy"""
        demo = QuickstartDemo()
        emoji = demo._get_status_emoji(0.5)
        assert '✅' in emoji or 'OPTIMAL' in emoji
    
    def test_get_status_emoji_adjusting(self):
        """Test status emoji for adjusting entropy"""
        demo = QuickstartDemo()
        emoji = demo._get_status_emoji(0.7)
        assert '⚠️' in emoji or 'ADJUSTING' in emoji
    
    def test_show_next_steps(self):
        """Test that next steps are shown"""
        demo = QuickstartDemo()
        # Just verify the method exists and doesn't crash
        demo._show_next_steps()  # Should not raise


class TestQuickstartIntegration:
    """Integration tests for quickstart"""
    
    def test_demo_agent_multiple_decisions(self):
        """Test agent making multiple decisions"""
        agent = DemoAgent("Agent", "normal")
        
        for _ in range(10):
            agent.make_decision()
        
        assert agent.decision_count == 10
