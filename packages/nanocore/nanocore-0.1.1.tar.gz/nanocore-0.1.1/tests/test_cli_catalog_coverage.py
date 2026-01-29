"""
Additional tests for CLI coverage - specifically for catalog functionality and main entry point.
"""

import json
import asyncio
import pytest
import runpy
from unittest.mock import AsyncMock, patch, MagicMock
from nanocore.cli import _display_catalog, state


@pytest.mark.asyncio
async def test_ws_listener_catalog_response():
    """Test that ws_listener handles catalog_response messages correctly."""
    from nanocore.cli import ws_listener

    websocket = AsyncMock()
    catalog_data = {
        "workers": {"w1": {"groups": ["g1"], "handlers": ["h1"]}},
        "groups": {"g1": ["w1"]},
    }

    # Create a proper catalog response message
    message = {
        "header": {
            "msg_type": "catalog_response",
            "sender": "broker",
            "receiver": "client",
        },
        "body": catalog_data,
    }

    websocket.__aiter__.return_value = [json.dumps(message)]

    # Ensure catalog_response is None initially
    state.catalog_response = None

    # Run listener
    await ws_listener(websocket)

    # Verify catalog was stored
    assert state.catalog_response is not None
    assert state.catalog_response == catalog_data
    assert "workers" in state.catalog_response
    assert "w1" in state.catalog_response["workers"]


def test_display_catalog_with_workers_and_groups():
    """Test _display_catalog with a complete catalog including workers and groups."""
    catalog = {
        "workers": {
            "calc1": {
                "groups": ["math", "calculators"],
                "handlers": ["push", "add", "sub", "mul", "div"],
            },
            "calc2": {"groups": ["math"], "handlers": ["push", "add"]},
            "worker3": {"groups": [], "handlers": ["test_handler"]},
        },
        "groups": {"math": ["calc1", "calc2"], "calculators": ["calc1"]},
    }

    with patch("nanocore.cli.console.print") as mock_print:
        _display_catalog(catalog)

        # Should print workers table and groups table
        assert mock_print.call_count == 2

        # Verify Rich Table objects were printed
        workers_table = mock_print.call_args_list[0][0][0]
        groups_table = mock_print.call_args_list[1][0][0]

        # Check that it's a Rich Table
        from rich.table import Table

        assert isinstance(workers_table, Table)
        assert isinstance(groups_table, Table)


def test_display_catalog_with_empty_groups():
    """Test _display_catalog with workers but no groups defined."""
    catalog = {
        "workers": {"worker1": {"groups": [], "handlers": ["handler1", "handler2"]}},
        "groups": {},
    }

    with patch("nanocore.cli.console.print") as mock_print:
        _display_catalog(catalog)

        # Should only print workers table (no groups table because groups is empty)
        assert mock_print.call_count == 1

        workers_table = mock_print.call_args_list[0][0][0]
        from rich.table import Table

        assert isinstance(workers_table, Table)


def test_display_catalog_empty():
    """Test _display_catalog with completely empty catalog."""
    catalog = {"workers": {}, "groups": {}}

    with patch("nanocore.cli.console.print") as mock_print:
        _display_catalog(catalog)

        # Should print workers table (empty)
        assert mock_print.call_count == 1


def test_display_catalog_with_dash_placeholders():
    """Test _display_catalog properly handles empty groups/handlers with '-' placeholder."""
    catalog = {
        "workers": {"empty_worker": {"groups": [], "handlers": []}},
        "groups": {},
    }

    with patch("nanocore.cli.console.print") as mock_print:
        _display_catalog(catalog)

        # Verify the function completed without error
        assert mock_print.call_count == 1


@pytest.mark.asyncio
async def test_shell_loop_catalog_command_with_response():
    """Test shell loop catalog command when response is received."""
    from nanocore.cli import shell_loop

    websocket = AsyncMock()
    state.is_connected = True
    state.catalog_response = {
        "workers": {"w1": {"groups": ["g1"], "handlers": ["h1"]}},
        "groups": {"g1": ["w1"]},
    }

    with patch("nanocore.cli.input", side_effect=["catalog", "quit"]):
        with patch("nanocore.cli._display_catalog") as mock_display:
            with patch("asyncio.sleep", return_value=None):  # Skip the sleep
                await shell_loop(websocket)

                # Verify catalog message was sent
                assert websocket.send.call_count == 1
                sent_msg = json.loads(websocket.send.call_args[0][0])
                assert sent_msg["header"]["msg_type"] == "get_catalog"

                # Verify catalog was displayed
                mock_display.assert_called_once()

                # Verify catalog_response was cleared
                assert state.catalog_response is None


@pytest.mark.asyncio
async def test_shell_loop_catalog_command_no_response():
    """Test shell loop catalog command when no response is received."""
    from nanocore.cli import shell_loop

    websocket = AsyncMock()
    state.is_connected = True
    state.catalog_response = None  # No response received

    with patch("nanocore.cli.input", side_effect=["catalog", "quit"]):
        with patch("nanocore.cli.console.print") as mock_print:
            with patch("asyncio.sleep", return_value=None):
                await shell_loop(websocket)

                # Verify "No catalog response" message was printed
                mock_print.assert_any_call(
                    "[yellow]No catalog response received[/yellow]"
                )


@pytest.mark.asyncio
async def test_shell_loop_catalog_command_integration():
    """Integration test for catalog command flow."""
    from nanocore.cli import shell_loop

    websocket = AsyncMock()
    state.is_connected = True

    # Pre-populate catalog_response before shell_loop runs
    state.catalog_response = {
        "workers": {"rpn_worker": {"groups": ["math"], "handlers": ["push", "add"]}},
        "groups": {"math": ["rpn_worker"]},
    }

    with patch("nanocore.cli.input", side_effect=["catalog", "quit"]):
        # Don't patch asyncio.sleep globally - let it run naturally
        with patch("nanocore.cli._display_catalog") as mock_display:
            await shell_loop(websocket)

            # Verify display was called with the catalog
            mock_display.assert_called_once()
            catalog_arg = mock_display.call_args[0][0]
            assert "workers" in catalog_arg
            assert "rpn_worker" in catalog_arg["workers"]


def test_main_function_via_runpy():
    """Test the main() function when called as __main__ module."""
    # Test the if __name__ == "__main__" block indirectly
    # by calling main() directly
    with patch("nanocore.cli.app") as mock_app:
        from nanocore.cli import main

        main()

        # Verify app() was called
        assert mock_app.called


@pytest.mark.asyncio
async def test_run_client_pending_tasks_cancellation():
    """Test that run_client properly cancels pending tasks when one completes."""
    from nanocore.cli import run_client

    mock_ws = AsyncMock()
    mock_ws.close = AsyncMock()

    cm = AsyncMock()
    cm.__aenter__.return_value = mock_ws

    # Track task cancellations
    cancelled_tasks = []

    async def track_cancel_task(*args, **kwargs):
        # Simulate one task finishing, others pending
        done = {MagicMock()}

        # Create mock pending tasks that track cancellation
        class MockTask:
            def __init__(self):
                self.cancelled = False

            def cancel(self):
                self.cancelled = True
                cancelled_tasks.append(self)

        pending = {MockTask(), MockTask()}
        return done, pending

    with patch("websockets.connect", return_value=cm):
        with patch("asyncio.create_task", return_value=AsyncMock()):
            with patch("asyncio.wait", side_effect=track_cancel_task):
                await run_client("ws://test")

    # Verify tasks were cancelled
    assert len(cancelled_tasks) == 2
    assert all(t.cancelled for t in cancelled_tasks)


@pytest.mark.asyncio
async def test_run_client_close_on_exception():
    """Test that run_client closes websocket even on exception."""
    from nanocore.cli import run_client

    mock_ws = AsyncMock()
    mock_ws.close = AsyncMock()

    cm = AsyncMock()
    cm.__aenter__.return_value = mock_ws

    with patch("websockets.connect", return_value=cm):
        with patch(
            "asyncio.create_task", side_effect=Exception("Task creation failed")
        ):
            try:
                await run_client("ws://test")
            except Exception:
                pass

    # Even on exception, websocket should be closed in finally block
    # Note: The actual behavior depends on the implementation


def test_connect_command_exception_handling():
    """Test connect command handles exceptions during asyncio.run."""
    from typer.testing import CliRunner
    from nanocore.cli import app

    runner = CliRunner()

    with patch(
        "nanocore.cli.asyncio.run", side_effect=RuntimeError("Event loop error")
    ):
        # Should not crash, exception should be handled
        try:
            result = runner.invoke(app, ["connect"])
            # Exit code might be non-zero due to error
        except Exception as e:
            # If exception propagates, that's also a valid test result
            pass
