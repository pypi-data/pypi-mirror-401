import pytest
from hypothesis import given, settings, strategies as st
from nanocore.broker import Broker
from nanocore.worker import Worker


@st.composite
def broker_action(draw):
    """Hypothesis strategy to generate random broker actions (register/dispatch)."""
    action = draw(st.sampled_from(["register", "dispatch"]))
    if action == "register":
        # Generate alphanumeric IDs to avoid weird character issues in tests
        worker_id = draw(
            st.text(
                min_size=1, max_size=10, alphabet="abcdefghijklmnopqrstuvwxyz0123456789"
            )
        )
        groups = draw(
            st.lists(
                st.text(min_size=1, max_size=5, alphabet="abcdefghijklmnopqrstuvwxyz"),
                max_size=3,
            )
        )
        return {"action": "register", "id": worker_id, "groups": groups}
    else:
        strategy = draw(st.sampled_from(["direct", "broadcast", "round_robin"]))
        # one_of(none, random string)
        group = draw(
            st.one_of(
                st.none(),
                st.text(min_size=1, max_size=5, alphabet="abcdefghijklmnopqrstuvwxyz"),
            )
        )
        worker_id = draw(
            st.one_of(
                st.none(),
                st.text(
                    min_size=1,
                    max_size=10,
                    alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
                ),
            )
        )
        return {
            "action": "dispatch",
            "strategy": strategy,
            "group": group,
            "worker_id": worker_id,
        }


@settings(max_examples=100, deadline=None)
@given(st.lists(broker_action(), min_size=1, max_size=50))
def test_broker_no_crash_fuzz(actions):
    """Fuzz test to ensure the broker does not crash under random sequences of actions."""
    broker = Broker()

    for action in actions:
        if action["action"] == "register":
            worker = Worker()
            broker.register_worker(action["id"], worker, action["groups"])
        elif action["action"] == "dispatch":
            try:
                broker.dispatch(
                    {"type": "fuzz_test"},
                    strategy=action["strategy"],
                    group=action["group"],
                    worker_id=action["worker_id"],
                )
            except ValueError:
                # Expected when worker_id is missing for direct or worker not found
                pass


def test_broker_round_robin_fairness_fuzz():
    """Verify round-robin dispatch fairness with multiple workers."""
    # Specific test for RR fairness with multiple workers
    broker = Broker()
    worker_ids = [f"w{i}" for i in range(5)]
    workers = {wid: Worker() for wid in worker_ids}

    for wid, w in workers.items():
        broker.register_worker(wid, w)

    # Dispatch 10 times, each worker should get exactly 2 messages
    for _ in range(10):
        broker.dispatch({"type": "test"}, strategy="round_robin")

    for wid in worker_ids:
        # Check queue size
        assert workers[wid].queue.qsize() == 2


def test_broker_broadcast_coverage_fuzz():
    """Verify that broadcast messages reach all registered workers in a group."""
    broker = Broker()
    group_name = "test_group"
    worker_ids = [f"w{i}" for i in range(5)]
    workers = {wid: Worker() for wid in worker_ids}

    for wid, w in workers.items():
        broker.register_worker(wid, w, groups=[group_name])

    broker.dispatch({"type": "test"}, strategy="broadcast", group=group_name)

    for wid in worker_ids:
        assert workers[wid].queue.qsize() == 1
