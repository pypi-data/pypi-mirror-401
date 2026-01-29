import asyncio
import pytest
import time
from fastapi.testclient import TestClient
from nanocore.app import app


@pytest.mark.asyncio
async def test_websocket_heartbeat():
    # TestClient for WebSockets
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            # Wait for a ping message
            # The heartbeat loop runs every 5s, let's wait a bit
            # Note: TestClient WebSocket is synchronous in its methods,
            # but the server loop is async.

            # Since TestClient is synchronous, we might need to be careful with timing.
            # But let's try to receive the first ping.
            data = websocket.receive_json()
            assert data["type"] == "ping"

            # Send pong
            websocket.send_json({"type": "pong"})

            # Verify we are still connected after another check
            # (We just proved we can receive and send)
            response = client.get("/health")
            assert response.json()["connections"] == 1


@pytest.mark.asyncio
async def test_websocket_timeout():
    # Override config values for this test
    from nanocore.config import config

    config.timeout_threshold = 0.5
    config.ping_interval = 0.2

    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            # Connected
            assert client.get("/health").json()["connections"] == 1

            # Receive ping but DON'T send pong
            data = websocket.receive_json()
            assert data["type"] == "ping"

            # Wait for timeout ( threshold is 0.5s)
            await asyncio.sleep(1.0)

            # Should be disconnected
            response = client.get("/health")
            assert response.json()["connections"] == 0

    # Reset config for other tests (optional but good practice)
    config.timeout_threshold = 10.0
    config.ping_interval = 5.0
