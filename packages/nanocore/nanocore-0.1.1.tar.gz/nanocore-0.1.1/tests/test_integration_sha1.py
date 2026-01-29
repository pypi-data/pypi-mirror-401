import asyncio
import pytest
from nanocore.broker import Broker
from nanocore.sha1_worker import SHA1Worker
from nanocore.schema import create_message


@pytest.mark.asyncio
async def test_integration_sha1_load():
    broker = Broker()
    w1 = SHA1Worker()
    w2 = SHA1Worker()

    broker.register_worker("w1", w1, groups=["sha1_group"])
    broker.register_worker("w2", w2, groups=["sha1_group"])

    # Start workers
    t1 = asyncio.create_task(w1.run())
    t2 = asyncio.create_task(w2.run())
    broker.start()

    num_messages = 10000
    for i in range(num_messages):
        msg = create_message(
            msg_type="compute_sha1",
            body={"data": f"message_{i}"},
            receiver="sha1_group",
            routing_key="round_robin",
        )
        broker.dispatch(msg)

    # Wait for all messages to be processed
    # We can join both queues
    await w1.queue.join()
    await w2.queue.join()

    # Verify distribution
    assert w1.count + w2.count == num_messages
    # With round robin and 10000 messages, it should be exactly 5000 each
    assert w1.count == 5000
    assert w2.count == 5000

    # Stop workers
    broker.stop()
    await t1
    await t2
