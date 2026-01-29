"""WebSocket server for real-time entropy streaming."""

import asyncio
import json
import logging
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Set

try:
    import websockets
    from websockets.asyncio.server import ServerConnection  # New non-deprecated API

    WEBSOCKETS_AVAILABLE = True
    WebSocketType = ServerConnection
except ImportError:
    try:
        # Fallback to legacy API if new one not available
        import websockets
        from websockets.server import WebSocketServerProtocol

        WEBSOCKETS_AVAILABLE = True
        WebSocketType = WebSocketServerProtocol
    except ImportError:
        WEBSOCKETS_AVAILABLE = False
        WebSocketType = Any

logger = logging.getLogger(__name__)


@dataclass
class StreamingMessage:
    """Message sent over WebSocket."""

    event: str
    data: Dict[str, Any]
    timestamp: float


class WebSocketServer:
    """WebSocket server for real-time streaming."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets package required. Install with: pip install websockets"
            )

        self.host = host
        self.port = port
        self.clients: Set[WebSocketType] = set()
        self.server = None
        self.loop = None
        self.thread = None
        self.running = False
        self.logger = logging.getLogger("streaming.websocket")

    def start(self) -> None:
        """Start WebSocket server in background thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        self.logger.info(f"WebSocket server starting on ws://{self.host}:{self.port}")

    def _run_server(self) -> None:
        """Run server in event loop."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        start_server = websockets.serve(self._handle_client, self.host, self.port)
        self.server = self.loop.run_until_complete(start_server)

        self.logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        self.loop.run_forever()

    async def _handle_client(self, websocket: WebSocketType, path: str = None) -> None:
        """Handle new client connection."""
        self.clients.add(websocket)
        remote_addr = getattr(websocket, "remote_address", "unknown")
        self.logger.info(f"Client connected: {remote_addr}")

        try:
            # Send welcome message
            await self._send_to_client(
                websocket,
                {
                    "event": "connected",
                    "data": {"message": "Connected to Entropic Core streaming"},
                },
            )

            # Keep connection alive and handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(websocket, data)
                except json.JSONDecodeError:
                    await self._send_to_client(
                        websocket,
                        {"event": "error", "data": {"message": "Invalid JSON"}},
                    )

        except Exception:  # Generic exception for both old and new API
            pass
        finally:
            self.clients.remove(websocket)
            self.logger.info(f"Client disconnected: {remote_addr}")

    async def _handle_message(self, websocket: WebSocketType, data: Dict) -> None:
        """Handle message from client."""
        event = data.get("event")

        if event == "ping":
            await self._send_to_client(
                websocket,
                {"event": "pong", "data": {"timestamp": datetime.now().isoformat()}},
            )

        elif event == "subscribe":
            await self._send_to_client(
                websocket,
                {"event": "subscribed", "data": {"channels": data.get("channels", [])}},
            )

    async def _send_to_client(self, websocket: WebSocketType, message: Dict) -> None:
        """Send message to specific client."""
        try:
            await websocket.send(
                json.dumps({**message, "timestamp": datetime.now().timestamp()})
            )
        except Exception as e:
            self.logger.error(f"Error sending to client: {e}")

    def broadcast(self, event: str, data: Dict[str, Any]) -> None:
        """Broadcast message to all connected clients."""
        if not self.running or not self.clients:
            return

        message = {
            "event": event,
            "data": data,
            "timestamp": datetime.now().timestamp(),
        }

        # Schedule broadcast in event loop
        if self.loop:
            asyncio.run_coroutine_threadsafe(self._broadcast_async(message), self.loop)

    async def _broadcast_async(self, message: Dict) -> None:
        """Async broadcast to all clients."""
        if self.clients:
            await asyncio.gather(
                *[client.send(json.dumps(message)) for client in self.clients],
                return_exceptions=True,
            )

    def stop(self) -> None:
        """Stop WebSocket server."""
        if not self.running:
            return

        self.running = False

        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

        if self.thread:
            self.thread.join(timeout=5)

        self.logger.info("WebSocket server stopped")


class StreamingManager:
    """Manages streaming of entropy data."""

    def __init__(self, brain_instance, enable_websocket: bool = True):
        self.brain = brain_instance
        self.websocket_server = None
        self.streaming_enabled = False
        self.logger = logging.getLogger("streaming.manager")

        if enable_websocket and WEBSOCKETS_AVAILABLE:
            self.websocket_server = WebSocketServer()

    def start(self) -> None:
        """Start streaming."""
        if self.websocket_server:
            self.websocket_server.start()

        self.streaming_enabled = True
        self.logger.info("Streaming started")

    def stop(self) -> None:
        """Stop streaming."""
        if self.websocket_server:
            self.websocket_server.stop()

        self.streaming_enabled = False
        self.logger.info("Streaming stopped")

    def stream_entropy_update(self, entropy: float, metrics: Dict) -> None:
        """Stream entropy update to clients."""
        if not self.streaming_enabled or not self.websocket_server:
            return

        self.websocket_server.broadcast(
            "entropy_update",
            {
                "entropy": entropy,
                "metrics": metrics,
                "agents_count": (
                    len(self.brain.agents) if hasattr(self.brain, "agents") else 0
                ),
            },
        )

    def stream_regulation_event(self, action: str, result: Dict) -> None:
        """Stream regulation event to clients."""
        if not self.streaming_enabled or not self.websocket_server:
            return

        self.websocket_server.broadcast(
            "regulation_event", {"action": action, "result": result}
        )

    def stream_alert(self, message: str, severity: str) -> None:
        """Stream alert to clients."""
        if not self.streaming_enabled or not self.websocket_server:
            return

        self.websocket_server.broadcast(
            "alert", {"message": message, "severity": severity}
        )
