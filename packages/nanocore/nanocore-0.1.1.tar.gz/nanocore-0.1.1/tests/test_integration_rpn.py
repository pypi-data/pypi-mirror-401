import asyncio
import pytest
from nanocore.broker import Broker
from nanocore.rpn_worker import RPNWorker


@pytest.mark.asyncio
async def test_rpn_integration():
    broker = Broker()
    calc = RPNWorker()

    # Register worker
    broker.register_worker("calc_id", calc, groups=["math"])

    # Start worker and broker
    run_task = asyncio.create_task(calc.run())
    broker.start()  # This calls calc.start()

    # Allow some time for startup
    await asyncio.sleep(0.1)

    # Sequence: (5 + 3) * 2 = 16
    # We use different strategies to test them
    broker.dispatch(
        {"type": "push", "value": 5}, strategy="direct", worker_id="calc_id"
    )
    broker.dispatch({"type": "push", "value": 3}, strategy="round_robin", group="math")
    broker.dispatch({"type": "add"}, strategy="broadcast", group="math")
    broker.dispatch({"type": "push", "value": 2}, strategy="round_robin")  # global RR
    broker.dispatch({"type": "mul"}, strategy="direct", worker_id="calc_id")

    # Wait for all messages to be processed
    await calc.queue.join()

    assert calc.stack == [16]

    # Shutdown
    broker.stop()
    await run_task
    assert not calc.running_signal.is_set()
