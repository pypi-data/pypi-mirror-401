import asyncio
from unittest.mock import patch

import pytest

from nanocore.worker import Worker


@pytest.mark.asyncio
async def test_worker_start_stop():
    worker = Worker()
    run_task = asyncio.create_task(worker.run())

    # Worker should be waiting
    assert not worker.running_signal.is_set()

    worker.start()
    assert worker.running_signal.is_set()

    # Give the worker a chance to proceed beyond the wait()
    await asyncio.sleep(0.1)

    worker.stop()
    await run_task
    assert not worker.running_signal.is_set()


@pytest.mark.asyncio
async def test_worker_message_processing():
    worker = Worker()
    processed_messages = []

    async def handler(msg):
        processed_messages.append(msg)

    worker.register_handler("test_msg", handler)

    run_task = asyncio.create_task(worker.run())
    worker.start()
    await asyncio.sleep(0.1)

    msg = {"type": "test_msg", "data": "hello"}
    worker.submit(msg)

    # Wait for queue to be processed
    await worker.queue.join()

    assert len(processed_messages) == 1
    assert processed_messages[0] == msg

    worker.stop()
    await run_task


@pytest.mark.asyncio
async def test_worker_multiple_handlers():
    worker = Worker()
    results = {}

    def handler1(msg):
        results["h1"] = msg["val"]

    async def handler2(msg):
        results["h2"] = msg["val"]

    worker.register_handler("msg1", handler1)
    worker.register_handler("msg2", handler2)

    run_task = asyncio.create_task(worker.run())
    worker.start()
    await asyncio.sleep(0.1)

    worker.submit({"type": "msg1", "val": 10})
    worker.submit({"type": "msg2", "val": 20})

    await worker.queue.join()

    assert results["h1"] == 10
    assert results["h2"] == 20

    worker.stop()
    await run_task


@pytest.mark.asyncio
async def test_worker_no_type():
    worker = Worker()
    worker.start()
    with patch("nanocore.worker.logger") as mock_logger:
        await worker._process_message({"header": {"msg_type": ""}, "body": {}})
        mock_logger.warning.assert_called()


@pytest.mark.asyncio
async def test_worker_handler_exception():
    worker = Worker()

    async def failing_handler(payload):
        raise Exception("Handler failed")

    worker.register_handler("fail", failing_handler)
    worker.start()

    # This call should catch the exception and log it, but not bubble it up.
    await worker._process_message({"header": {"msg_type": "fail"}, "body": {}})
    # If we reach here, it didn't crash.


@pytest.mark.asyncio
async def test_worker_run_cancelled():
    worker = Worker()
    worker.start()

    task = asyncio.create_task(worker.run())
    await asyncio.sleep(0.1)
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task


@pytest.mark.asyncio
async def test_worker_no_handler():
    worker = Worker()
    run_task = asyncio.create_task(worker.run())
    worker.start()
    await asyncio.sleep(0.1)

    worker.submit({"type": "unknown", "val": 1})
    await worker.queue.join()

    # Should complete without error
    worker.stop()
    await run_task
