import asyncio
import pytest
from nanocore.rpn_worker import RPNWorker


@pytest.fixture
def rpn_worker():
    return RPNWorker()


@pytest.mark.asyncio
async def test_rpn_basic_ops(rpn_worker):
    run_task = asyncio.create_task(rpn_worker.run())
    rpn_worker.start()
    await asyncio.sleep(0.1)

    # 10 5 +
    rpn_worker.submit({"type": "push", "value": 10})
    rpn_worker.submit({"type": "push", "value": 5})
    rpn_worker.submit({"type": "add"})

    await rpn_worker.queue.join()
    assert rpn_worker.stack == [15]

    # - 2 *
    rpn_worker.submit({"type": "push", "value": 2})
    rpn_worker.submit({"type": "mul"})

    await rpn_worker.queue.join()
    assert rpn_worker.stack == [30]

    rpn_worker.stop()
    await run_task


@pytest.mark.asyncio
async def test_rpn_sub_div(rpn_worker):
    run_task = asyncio.create_task(rpn_worker.run())
    rpn_worker.start()
    await asyncio.sleep(0.1)

    # 20 5 - (15)
    rpn_worker.submit({"type": "push", "value": 20})
    rpn_worker.submit({"type": "push", "value": 5})
    rpn_worker.submit({"type": "sub"})

    # 15 3 / (5)
    rpn_worker.submit({"type": "push", "value": 3})
    rpn_worker.submit({"type": "div"})

    await rpn_worker.queue.join()
    assert rpn_worker.stack == [5.0]

    rpn_worker.stop()
    await run_task


@pytest.mark.asyncio
async def test_rpn_insufficient_operands(rpn_worker):
    run_task = asyncio.create_task(rpn_worker.run())
    rpn_worker.start()
    await asyncio.sleep(0.1)

    rpn_worker.submit({"type": "push", "value": 10})
    rpn_worker.submit({"type": "add"})  # Should fail gracefully

    await rpn_worker.queue.join()
    assert rpn_worker.stack == [10]

    rpn_worker.stop()
    await run_task


@pytest.mark.asyncio
async def test_rpn_clear(rpn_worker):
    run_task = asyncio.create_task(rpn_worker.run())
    rpn_worker.start()
    await asyncio.sleep(0.1)

    rpn_worker.submit({"type": "push", "value": 10})
    rpn_worker.submit({"type": "clear"})

    await rpn_worker.queue.join()
    assert rpn_worker.stack == []

    rpn_worker.stop()
    await run_task
