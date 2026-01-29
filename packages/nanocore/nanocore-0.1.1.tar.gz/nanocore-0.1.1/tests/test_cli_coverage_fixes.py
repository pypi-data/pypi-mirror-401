import pytest
import asyncio
import json
import websockets
import typer
from unittest.mock import AsyncMock, patch, MagicMock
from nanocore.cli import ws_listener, heartbeat_loop, run_client, state


@pytest.mark.asyncio
async def test_ws_listener_json_decode_error():
    """Test ws_listener handles invalid JSON (covers lines 47-48)."""
    mock_ws = AsyncMock()
    # Mock iterator to return one invalid JSON message then exit
    mock_ws.__aiter__.return_value = ["invalid json"]

    from nanocore.cli import console

    with patch.object(console, "print") as mock_print:
        await ws_listener(mock_ws)
        mock_print.assert_any_call("[yellow]Raw Server:[/yellow] invalid json")


@pytest.mark.asyncio
async def test_ws_listener_generic_exception():
    """Test ws_listener handles generic exception (covers lines 43-44)."""
    mock_ws = AsyncMock()
    # Raise exception during iteration
    mock_ws.__aiter__.side_effect = Exception("Generic Error")

    with patch("nanocore.cli.logger.error") as mock_log:
        await ws_listener(mock_ws)
        mock_log.assert_called()
        assert "Listener error: Generic Error" in mock_log.call_args[0][0]


@pytest.mark.asyncio
async def test_heartbeat_loop_send_failure():
    """Test heartbeat_loop handles send failure (covers lines 62-64)."""
    mock_ws = AsyncMock()
    mock_ws.send.side_effect = Exception("Send failure")
    state.is_connected = True

    with patch("nanocore.cli.logger.error") as mock_log:
        await heartbeat_loop(mock_ws)
        mock_log.assert_called()
        assert "Failed to send heartbeat: Send failure" in mock_log.call_args[0][0]
        assert not state.is_connected


@pytest.mark.asyncio
async def test_run_client_generic_exception():
    """Test run_client handles generic exception (covers lines 187-188, 194)."""
    # Mock async functions to prevent "coroutine was never awaited" warnings
    with patch("nanocore.cli.ws_listener", new_callable=AsyncMock):
        with patch("nanocore.cli.heartbeat_loop", new_callable=AsyncMock):
            with patch("nanocore.cli.shell_loop", new_callable=AsyncMock):
                with patch(
                    "websockets.connect", side_effect=Exception("Random socket error")
                ):
                    from nanocore.cli import console

                    with patch.object(console, "print") as mock_print:
                        with pytest.raises(typer.Exit) as excinfo:
                            await run_client("ws://localhost")
                        assert excinfo.value.exit_code == 1
                        mock_print.assert_any_call(
                            "[red]Failed to connect: Random socket error[/red]"
                        )
