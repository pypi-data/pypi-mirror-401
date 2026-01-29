import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from entropic_core.streaming.websocket_server import WebSocketServer, StreamingManager, StreamingMessage


class TestWebSocketServer:
    """Test WebSocket server"""
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_websocket_server_init(self):
        """Test WebSocket server initialization"""
        server = WebSocketServer(host="0.0.0.0", port=8765)
        
        assert server.host == "0.0.0.0"
        assert server.port == 8765
        assert len(server.clients) == 0
        assert server.running is False
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', False)
    def test_websocket_server_unavailable(self):
        """Test WebSocket server when websockets not available"""
        with pytest.raises(ImportError):
            WebSocketServer()
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_streaming_message_creation(self):
        """Test StreamingMessage creation"""
        msg = StreamingMessage(
            event="test_event",
            data={"key": "value"},
            timestamp=123456.789
        )
        
        assert msg.event == "test_event"
        assert msg.data == {"key": "value"}


class TestStreamingManager:
    """Test StreamingManager"""
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_streaming_manager_init(self):
        """Test StreamingManager initialization"""
        brain = MagicMock()
        manager = StreamingManager(brain, enable_websocket=True)
        
        assert manager.brain == brain
        assert manager.streaming_enabled is False
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_streaming_manager_start_stop(self):
        """Test starting and stopping streaming"""
        brain = MagicMock()
        manager = StreamingManager(brain, enable_websocket=False)
        
        manager.start()
        assert manager.streaming_enabled is True
        
        manager.stop()
        assert manager.streaming_enabled is False
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_stream_entropy_update(self):
        """Test streaming entropy update"""
        brain = MagicMock()
        manager = StreamingManager(brain, enable_websocket=False)
        
        manager.streaming_enabled = True
        manager.stream_entropy_update(0.5, {'agents': 3})
        # Should not crash
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_stream_regulation_event(self):
        """Test streaming regulation event"""
        brain = MagicMock()
        manager = StreamingManager(brain, enable_websocket=False)
        
        manager.streaming_enabled = True
        manager.stream_regulation_event('increase_chaos', {'result': 'success'})
        # Should not crash
    
    @patch('entropic_core.streaming.websocket_server.WEBSOCKETS_AVAILABLE', True)
    def test_stream_alert(self):
        """Test streaming alert"""
        brain = MagicMock()
        manager = StreamingManager(brain, enable_websocket=False)
        
        manager.streaming_enabled = True
        manager.stream_alert('High entropy detected', 'high')
        # Should not crash
