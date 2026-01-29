import pytest
from unittest.mock import MagicMock, patch
from entropic_core.integrations.crewai_adapter import (
    CrewAIEntropyAdapter, CrewAIEntropyCallback
)


class TestCrewAIEntropyAdapter:
    """Test CrewAIEntropyAdapter"""
    
    def test_adapter_init(self):
        """Test adapter initialization"""
        crew = MagicMock()
        crew.agents = [MagicMock(), MagicMock()]
        
        adapter = CrewAIEntropyAdapter(crew, enable_intervention=True)
        
        assert adapter.crew == crew
        assert len(adapter.wrapped_agents) >= 0
    
    def test_adapter_with_existing_brain(self):
        """Test adapter with existing brain"""
        crew = MagicMock()
        crew.agents = []
        brain = MagicMock()
        brain._intervention_enabled = True
        
        adapter = CrewAIEntropyAdapter(crew, entropy_brain=brain)
        
        assert adapter.entropy_brain == brain
    
    def test_get_entropy_report(self):
        """Test getting entropy report"""
        crew = MagicMock()
        crew.agents = [MagicMock()]
        
        adapter = CrewAIEntropyAdapter(crew)
        
        # Add some events
        adapter.task_entropy_history.append({
            'entropy': {'combined': 0.5},
            'event_type': 'test'
        })
        
        report = adapter.get_entropy_report()
        
        assert 'total_events' in report
        assert 'avg_entropy' in report
        assert 'events' in report
    
    def test_kickoff_execution(self):
        """Test kickoff execution"""
        crew = MagicMock()
        crew.agents = []
        crew.kickoff.return_value = MagicMock()
        
        adapter = CrewAIEntropyAdapter(crew)
        result = adapter.kickoff(inputs={'test': 'data'})
        
        crew.kickoff.assert_called_once()


class TestCrewAIEntropyCallback:
    """Test CrewAIEntropyCallback"""
    
    def test_callback_init(self):
        """Test callback initialization"""
        brain = MagicMock()
        callback = CrewAIEntropyCallback(brain)
        
        assert callback.entropy_brain == brain
        assert len(callback.events) == 0
    
    def test_on_task_start(self):
        """Test on_task_start callback"""
        brain = MagicMock()
        brain.measure.return_value = {'combined': 0.5}
        
        callback = CrewAIEntropyCallback(brain)
        
        task = MagicMock()
        task.description = "Test task"
        
        callback.on_task_start(task)
        
        assert len(callback.events) == 1
        assert callback.events[0]['type'] == 'task_start'
    
    def test_on_task_end(self):
        """Test on_task_end callback"""
        brain = MagicMock()
        brain.measure.return_value = {'combined': 0.5}
        
        callback = CrewAIEntropyCallback(brain)
        
        task = MagicMock()
        task.description = "Test task"
        
        callback.on_task_end(task, "output")
        
        assert len(callback.events) == 1
        assert callback.events[0]['type'] == 'task_end'
    
    def test_get_summary(self):
        """Test getting summary"""
        brain = MagicMock()
        callback = CrewAIEntropyCallback(brain)
        
        callback.events = [
            {'type': 'task_start'},
            {'type': 'task_end'}
        ]
        
        summary = callback.get_summary()
        
        assert summary['total_events'] == 2
