import pytest
import asyncio
import time
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import WebSocket
from nanocore.ws_manager import ConnectionManager


@pytest.mark.asyncio
async def test_connection_manager_connect():
    manager = ConnectionManager(ping_interval=1.0, timeout_threshold=2.0)
    mock_ws = AsyncMock(spec=WebSocket)

    await manager.connect(mock_ws)

    assert mock_ws in manager.active_connections
    assert mock_ws in manager.last_pong
    mock_ws.accept.assert_called_once()


@pytest.mark.asyncio
async def test_connection_manager_disconnect():
    manager = ConnectionManager()
    mock_ws = AsyncMock(spec=WebSocket)

    await manager.connect(mock_ws)
    manager.disconnect(mock_ws)

    assert mock_ws not in manager.active_connections
    assert mock_ws not in manager.last_pong


@pytest.mark.asyncio
async def test_connection_manager_broadcast_ping_success():
    manager = ConnectionManager()
    mock_ws1 = AsyncMock(spec=WebSocket)
    mock_ws2 = AsyncMock(spec=WebSocket)

    await manager.connect(mock_ws1)
    await manager.connect(mock_ws2)

    await manager.broadcast_ping()

    mock_ws1.send_json.assert_called_once()
    mock_ws2.send_json.assert_called_once()


@pytest.mark.asyncio
async def test_connection_manager_broadcast_ping_failure():
    """Verify that failed pings trigger disconnection (covers lines 48-50)."""
    manager = ConnectionManager()
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.send_json.side_effect = Exception("Send failed")

    await manager.connect(mock_ws)

    with patch.object(
        manager, "_force_disconnect", new_callable=AsyncMock
    ) as mock_force:
        await manager.broadcast_ping()
        mock_force.assert_called_once_with(mock_ws)


@pytest.mark.asyncio
async def test_connection_manager_check_timeouts_none():
    manager = ConnectionManager(timeout_threshold=100)
    mock_ws = AsyncMock(spec=WebSocket)
    await manager.connect(mock_ws)

    await manager.check_timeouts()
    assert mock_ws in manager.active_connections


@pytest.mark.asyncio
async def test_connection_manager_check_timeouts_trigger():
    """Verify that timeouts trigger disconnection (covers line 61-62)."""
    manager = ConnectionManager(timeout_threshold=0.1)
    mock_ws = AsyncMock(spec=WebSocket)
    await manager.connect(mock_ws)

    # Wait for timeout
    await asyncio.sleep(0.2)

    with patch.object(
        manager, "_force_disconnect", new_callable=AsyncMock
    ) as mock_force:
        await manager.check_timeouts()
        mock_force.assert_called_once_with(mock_ws)


@pytest.mark.asyncio
async def test_connection_manager_force_disconnect_success():
    manager = ConnectionManager()
    mock_ws = AsyncMock(spec=WebSocket)
    await manager.connect(mock_ws)

    await manager._force_disconnect(mock_ws)

    mock_ws.close.assert_called_once()
    assert mock_ws not in manager.active_connections


@pytest.mark.asyncio
async def test_connection_manager_force_disconnect_failure():
    """Verify that force disconnect handles exceptions in close (covers lines 67-68)."""
    manager = ConnectionManager()
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.close.side_effect = Exception("Close failed")
    await manager.connect(mock_ws)

    await manager._force_disconnect(mock_ws)

    # Should still be disconnected
    assert mock_ws not in manager.active_connections


@pytest.mark.asyncio
async def test_connection_manager_heartbeat_loop_cancellation():
    manager = ConnectionManager(ping_interval=0.01)

    async def run_loop():
        await manager.heartbeat_loop()

    task = asyncio.create_task(run_loop())
    await asyncio.sleep(0.05)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_connection_manager_on_pong():
    manager = ConnectionManager()
    mock_ws = AsyncMock(spec=WebSocket)
    await manager.connect(mock_ws)

    old_time = manager.last_pong[mock_ws]
    await asyncio.sleep(0.01)
    manager.on_pong(mock_ws)

    assert manager.last_pong[mock_ws] > old_time
