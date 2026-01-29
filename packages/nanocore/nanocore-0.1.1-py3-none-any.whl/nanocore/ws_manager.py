import asyncio
import logging
import time
from typing import Dict, Set, Optional
from fastapi import WebSocket
from nanocore.config import config

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections and implements heartbeat logic.
    """

    def __init__(
        self,
        ping_interval: Optional[float] = None,
        timeout_threshold: Optional[float] = None,
    ):
        self.active_connections: Set[WebSocket] = set()
        self.last_pong: Dict[WebSocket, float] = {}
        self.ping_interval = ping_interval or config.ping_interval
        self.timeout_threshold = timeout_threshold or config.timeout_threshold
        self._heartbeat_task: Optional[asyncio.Task] = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        self.last_pong[websocket] = time.time()
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        self.last_pong.pop(websocket, None)
        logger.info(
            f"WebSocket disconnected. Remaining: {len(self.active_connections)}"
        )

    def on_pong(self, websocket: WebSocket):
        """Update last seen timestamp for the client."""
        self.last_pong[websocket] = time.time()

    async def broadcast_ping(self):
        """Sends a ping message to all active connections."""
        if not self.active_connections:
            return

        logger.debug(f"Broadcasting ping to {len(self.active_connections)} clients")
        ping_msg = {"type": "ping", "timestamp": time.time()}

        for websocket in list(self.active_connections):
            try:
                await websocket.send_json(ping_msg)
            except Exception as e:
                logger.error(f"Failed to send ping: {e}")
                await self._force_disconnect(websocket)

    async def check_timeouts(self):
        """Identifies and disconnects inactive clients."""
        now = time.time()
        logger.debug(
            f"Checking timeouts for {len(self.active_connections)} connections. Threshold: {self.timeout_threshold}s"
        )
        for websocket in list(self.active_connections):
            last_seen = self.last_pong.get(websocket, 0)
            diff = now - last_seen
            logger.debug(f"WS {id(websocket)}: last seen {diff:.2f}s ago")
            if diff > self.timeout_threshold:
                logger.warning(
                    f"Client {id(websocket)} timeout detected ({diff:.1f}s). Disconnecting."
                )
                await self._force_disconnect(websocket)

    async def _force_disconnect(self, websocket: WebSocket):
        try:
            await websocket.close()
        except Exception:
            pass
        finally:
            if websocket in self.active_connections:
                self.disconnect(websocket)

    async def heartbeat_loop(self):
        """Background loop for pings and timeout checks."""
        logger.info("Heartbeat loop started.")
        try:
            while True:
                await self.broadcast_ping()
                await asyncio.sleep(
                    self.ping_interval / 2
                )  # Check more frequently than interval
                await self.check_timeouts()
                await asyncio.sleep(self.ping_interval / 2)
        except asyncio.CancelledError:
            logger.info("Heartbeat loop cancelled.")
            raise
