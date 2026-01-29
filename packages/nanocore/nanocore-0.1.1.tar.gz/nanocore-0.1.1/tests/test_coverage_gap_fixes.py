import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from nanocore.app import lifespan
from nanocore.config import Config
from nanocore.rpn_worker import RPNWorker
from nanocore.schema import validate_message
from nanocore.worker import Worker
from nanocore.workers.task_automation import TaskAutomationWorker


@asynccontextmanager
async def async_lifespan_manager(app: FastAPI):
    async with app.router.lifespan_context(app) as state:
        yield state


def test_config_debug_and_mkdir_v2():
    """Test config debug mode and directory creation (covers lines 12, 19)."""
    # Force a reload or just create a new instance with different env
    with patch.dict(
        os.environ, {"DEBUG": "true", "WORKSPACE_DIR": "/tmp/nanocore_test_ws_unique"}
    ):
        from nanocore.config import Config

        c = Config()
        assert c.debug is True
        assert c.workspace_dir.exists()


def test_rpn_worker_push_missing_value():
    """Test RPNWorker push with missing value (covers line 30)."""
    worker = RPNWorker()
    with patch("nanocore.rpn_worker.logger.warning") as mock_warn:
        worker.handle_push({})
        mock_warn.assert_called_with("Push message missing 'value'")


def test_schema_validate_non_dict():
    """Test validate_message with non-dict input (covers line 53)."""
    assert validate_message("not a dict") is False
    # This hits line 53
    assert validate_message({"header": "not a dict", "body": {}}) is False
    assert validate_message({"header": {}, "body": "not a dict"}) is False


@pytest.mark.asyncio
async def test_worker_handler_exception():
    """Test worker handles exception in handler (covers lines 76-77)."""
    worker = Worker()

    def failing_handler(payload):
        raise ValueError("Subscribed failure")

    worker.register_handler("fail", failing_handler)
    worker.start()

    # We can call _process_message directly to simplify
    msg = {
        "header": {
            "sender": "test",
            "receiver": "test",
            "routing_key": "direct",
            "msg_type": "fail",
            "timestamp": 123,
            "uuid": "abc",
        },
        "body": {},
    }

    with patch("nanocore.worker.logger.error") as mock_error:
        await worker._process_message(msg)
        mock_error.assert_called()
        assert "Error handling message fail" in mock_error.call_args[0][0]


@pytest.mark.asyncio
async def test_task_automation_continue_on_error():
    """Test TaskAutomationWorker continues pipeline when stop_on_error=False (covers line 86)."""
    worker = TaskAutomationWorker()

    # Mock run_subprocess to fail
    with patch.object(worker, "run_subprocess", side_effect=Exception("Task Failed")):
        payload = {
            "tasks": [
                {"name": "fail_but_continue", "command": "false"},
                {"name": "second_task", "command": "true"},
            ],
            "stop_on_error": False,
        }
        results = await worker.handle_run_pipeline(payload)

        assert results["status"] == "failed"
        assert len(results["tasks"]) == 2
        assert results["tasks"][0]["status"] == "failed"
        assert (
            results["tasks"][1]["status"] == "failed"
        )  # Both fail because of mock, but it tried both
