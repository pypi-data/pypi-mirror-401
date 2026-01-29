import pytest
import tempfile
import os
from nanocore.workers.task_automation import TaskAutomationWorker


@pytest.mark.asyncio
async def test_task_pipeline_success():
    with tempfile.TemporaryDirectory() as tmpdirname:
        worker = TaskAutomationWorker()

        payload = {
            "tasks": [
                {
                    "name": "Create File",
                    "command": "touch",
                    "args": ["test.txt"],
                    "cwd": tmpdirname,
                },
                {
                    "name": "List Files",
                    "command": "ls",
                    "args": ["-l"],
                    "cwd": tmpdirname,
                },
            ]
        }

        results = await worker.handle_run_pipeline(payload)

        assert results["status"] == "success"
        assert len(results["tasks"]) == 2
        assert os.path.exists(os.path.join(tmpdirname, "test.txt"))
        assert len(worker.pipeline_history) == 1


@pytest.mark.asyncio
async def test_task_pipeline_stop_on_error():
    worker = TaskAutomationWorker()

    payload = {
        "tasks": [
            {"name": "Fail Task", "command": "false", "args": []},
            {
                "name": "Should Not Run",
                "command": "touch",
                "args": ["should_not_exist.txt"],
            },
        ],
        "stop_on_error": True,
    }

    results = await worker.handle_run_pipeline(payload)

    assert results["status"] == "failed"
    assert len(results["tasks"]) == 1
    assert results["tasks"][0]["status"] == "failed"


@pytest.mark.asyncio
async def test_task_pipeline_continue_on_error():
    worker = TaskAutomationWorker()

    payload = {
        "tasks": [
            {"name": "Fail Task", "command": "false", "args": []},
            {"name": "Continue Task", "command": "echo", "args": ["still running"]},
        ],
        "stop_on_error": False,
    }

    results = await worker.handle_run_pipeline(payload)

    assert results["status"] == "failed"  # Pipeline contains failures
    assert len(results["tasks"]) == 2
    assert results["tasks"][0]["status"] == "failed"
    assert results["tasks"][1]["status"] == "success"


@pytest.mark.asyncio
async def test_task_pipeline_skip_invalid():
    worker = TaskAutomationWorker()

    payload = {"tasks": [{"name": "Invalid Task", "args": []}]}

    results = await worker.handle_run_pipeline(payload)
    assert results["tasks"][0]["status"] == "skipped"
