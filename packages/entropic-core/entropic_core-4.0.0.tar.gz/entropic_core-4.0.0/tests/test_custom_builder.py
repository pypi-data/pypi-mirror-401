import pytest
from unittest.mock import MagicMock, patch
from entropic_core.integrations.custom_builder import CustomAdapterBuilder, CustomAdapter


class TestCustomAdapterBuilder:
    """Test CustomAdapterBuilder"""
    
    def test_builder_init(self):
        """Test builder initialization"""
        builder = CustomAdapterBuilder()
        
        assert builder.brain is None
        assert len(builder.hooks) == 4
        assert len(builder.custom_metrics) == 0
    
    def test_builder_set_brain(self):
        """Test setting brain"""
        builder = CustomAdapterBuilder()
        brain = MagicMock()
        
        result = builder.set_brain(brain)
        
        assert builder.brain == brain
        assert result is builder  # Chainable
    
    def test_builder_add_hook(self):
        """Test adding hook"""
        builder = CustomAdapterBuilder()
        hook = MagicMock()
        
        result = builder.add_hook('before_action', hook)
        
        assert len(builder.hooks['before_action']) == 1
        assert result is builder  # Chainable
    
    def test_builder_add_metric(self):
        """Test adding custom metric"""
        builder = CustomAdapterBuilder()
        calculator = lambda state: 0.5
        
        result = builder.add_metric('custom_metric', calculator)
        
        assert 'custom_metric' in builder.custom_metrics
        assert result is builder
    
    def test_builder_set_config(self):
        """Test setting configuration"""
        builder = CustomAdapterBuilder()
        
        result = builder.set_config('timeout', 30)
        
        assert builder.config['timeout'] == 30
        assert result is builder
    
    def test_builder_register_state_extractor(self):
        """Test registering state extractor"""
        builder = CustomAdapterBuilder()
        extractor = lambda agent: agent.state
        
        result = builder.register_state_extractor(extractor)
        
        assert builder.state_extractor == extractor
        assert result is builder
    
    def test_builder_register_decision_extractor(self):
        """Test registering decision extractor"""
        builder = CustomAdapterBuilder()
        extractor = lambda agent: agent.last_decision
        
        result = builder.register_decision_extractor(extractor)
        
        assert builder.decision_extractor == extractor
        assert result is builder
    
    def test_builder_register_message_counter(self):
        """Test registering message counter"""
        builder = CustomAdapterBuilder()
        counter = lambda agent: len(agent.messages)
        
        result = builder.register_message_counter(counter)
        
        assert builder.message_counter == counter
        assert result is builder
    
    def test_builder_build(self):
        """Test building adapter"""
        builder = CustomAdapterBuilder()
        brain = MagicMock()
        builder.set_brain(brain)
        
        adapter = builder.build()
        
        assert isinstance(adapter, CustomAdapter)
        assert adapter.brain == brain
    
    def test_builder_build_without_brain(self):
        """Test building adapter without explicit brain"""
        builder = CustomAdapterBuilder()
        adapter = builder.build()
        
        assert isinstance(adapter, CustomAdapter)


class TestCustomAdapter:
    """Test CustomAdapter"""
    
    def test_adapter_init(self):
        """Test adapter initialization"""
        brain = MagicMock()
        adapter = CustomAdapter(
            brain=brain,
            hooks={'before_action': [], 'after_action': [], 'on_communicate': [], 'on_error': []},
            custom_metrics={},
            config={}
        )
        
        assert adapter.brain == brain
        assert len(adapter.wrapped_agents) == 0
    
    def test_adapter_wrap_agent(self):
        """Test wrapping an agent"""
        brain = MagicMock()
        brain.connect = MagicMock()
        
        adapter = CustomAdapter(
            brain=brain,
            hooks={'before_action': [], 'after_action': [], 'on_communicate': [], 'on_error': []},
            custom_metrics={},
            config={'methods_to_wrap': ['act']}
        )
        
        agent = MagicMock()
        agent.act = MagicMock(return_value="action_result")
        
        wrapped_agent = adapter.wrap_agent(agent)
        
        assert agent in adapter.wrapped_agents
    
    def test_adapter_get_analytics(self):
        """Test getting analytics"""
        brain = MagicMock()
        adapter = CustomAdapter(
            brain=brain,
            hooks={'before_action': [], 'after_action': [], 'on_communicate': [], 'on_error': []},
            custom_metrics={},
            config={}
        )
        
        # Add some events
        adapter.event_log.append({
            'entropy_after': 0.5,
            'entropy_change': 0.1,
            'error': None,
            'metrics_after': {}
        })
        
        analytics = adapter.get_analytics()
        
        assert 'total_events' in analytics
        assert 'wrapped_agents' in analytics
        assert analytics['total_events'] == 1
