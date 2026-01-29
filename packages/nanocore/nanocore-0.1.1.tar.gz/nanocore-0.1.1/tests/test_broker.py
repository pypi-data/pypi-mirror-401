import pytest

from nanocore.broker import Broker
from nanocore.schema import create_message
from nanocore.worker import Worker


@pytest.fixture
def broker():
    return Broker()


@pytest.fixture
def workers():
    return [Worker() for _ in range(3)]


def test_broker_registration(broker, workers):
    broker.register_worker("w1", workers[0], groups=["g1"])
    broker.register_worker("w2", workers[1], groups=["g1", "g2"])

    assert "w1" in broker._workers
    assert "w2" in broker._workers
    assert "w1" in broker._groups["g1"]
    assert "w2" in broker._groups["g1"]
    assert "w2" in broker._groups["g2"]


def test_dispatch_direct(broker, workers):
    broker.register_worker("w1", workers[0])
    msg = create_message(
        msg_type="test", body={"data": "direct"}, receiver="w1", routing_key="direct"
    )

    broker.dispatch(msg)

    assert workers[0].queue.qsize() == 1
    received = workers[0].queue.get_nowait()
    assert received == msg


def test_dispatch_broadcast(broker, workers):
    broker.register_worker("w1", workers[0], groups=["g1"])
    broker.register_worker("w2", workers[1], groups=["g1"])
    broker.register_worker("w3", workers[2], groups=["g2"])

    msg = create_message(
        msg_type="test",
        body={"data": "broadcast"},
        receiver="g1",
        routing_key="broadcast",
    )
    broker.dispatch(msg)

    assert workers[0].queue.qsize() == 1
    assert workers[1].queue.qsize() == 1
    assert workers[2].queue.qsize() == 0


def test_dispatch_round_robin(broker, workers):
    broker.register_worker("w1", workers[0], groups=["g1"])
    broker.register_worker("w2", workers[1], groups=["g1"])

    msg1 = create_message(
        msg_type="test", body={"val": 1}, receiver="g1", routing_key="round_robin"
    )
    msg2 = create_message(
        msg_type="test", body={"val": 2}, receiver="g1", routing_key="round_robin"
    )
    msg3 = create_message(
        msg_type="test", body={"val": 3}, receiver="g1", routing_key="round_robin"
    )

    broker.dispatch(msg1)
    broker.dispatch(msg2)
    broker.dispatch(msg3)

    # w1 should get msg1 and msg3
    # w2 should get msg2
    assert workers[0].queue.qsize() == 2
    assert workers[1].queue.qsize() == 1

    assert workers[0].queue.get_nowait() == msg1
    assert workers[1].queue.get_nowait() == msg2
    assert workers[0].queue.get_nowait() == msg3


def test_dispatch_invalid_strategy(broker):
    msg = create_message(msg_type="test", body={})
    with pytest.raises(ValueError, match="Unknown dispatch strategy"):
        broker.dispatch(msg, strategy="invalid")
