import asyncio
import pytest
from nanocore.worker import Worker
from nanocore.broker import Broker
from nanocore.rpn_worker import RPNWorker
from nanocore.schema import create_message


@pytest.mark.asyncio
async def test_multi_worker_concurrent_processing():
    """
    Test involving 2 running workers to verify concurrent operation and routing.
    """
    broker = Broker()

    # Worker 1: RPN Worker
    worker_rpn = RPNWorker()
    broker.register_worker("rpn1", worker_rpn, groups=["math"])

    # Worker 2: Generic Worker with a custom handler
    worker_gen = Worker()
    processed_messages = []

    async def custom_handler(payload):
        processed_messages.append(payload)
        # Simulate some async work
        await asyncio.sleep(0.05)

    worker_gen.register_handler("gen_msg", custom_handler)
    broker.register_worker("gen1", worker_gen, groups=["general"])

    # Start all workers via Broker
    broker.start()

    # Run the main loops for both workers
    rpn_task = asyncio.create_task(worker_rpn.run())
    gen_task = asyncio.create_task(worker_gen.run())

    # Allow some time for workers to settle
    await asyncio.sleep(0.1)

    # 1. Direct routing to RPN Worker
    msg_push = create_message(
        msg_type="push", body={"value": 10.0}, receiver="rpn1", routing_key="direct"
    )
    broker.dispatch(msg_push)

    # 2. Direct routing to General Worker
    msg_gen = create_message(
        msg_type="gen_msg",
        body={"data": "hello"},
        receiver="gen1",
        routing_key="direct",
    )
    broker.dispatch(msg_gen)

    # Wait for processing
    await asyncio.sleep(0.2)

    # Invariants check
    assert len(worker_rpn.stack) == 1
    assert worker_rpn.stack[0] == 10.0
    assert len(processed_messages) == 1
    assert processed_messages[0] == {"data": "hello"}

    # 3. Broadcast routing (should potentially reach both if they had handlers for it)
    # Let's register a shared handler to verify broadcast
    shared_results = []

    async def shared_handler(payload):
        shared_results.append(payload)

    worker_rpn.register_handler("broadcast_msg", shared_handler)
    worker_gen.register_handler("broadcast_msg", shared_handler)

    msg_bcast = create_message(
        msg_type="broadcast_msg",
        body={"info": "all"},
        receiver="all",
        routing_key="broadcast",
    )
    broker.dispatch(msg_bcast)

    await asyncio.sleep(0.2)

    # Both should have processed it
    assert len(shared_results) == 2

    # Stop workers
    broker.stop()
    await asyncio.gather(rpn_task, gen_task)

    assert not worker_rpn.running_signal.is_set()
    assert not worker_gen.running_signal.is_set()
