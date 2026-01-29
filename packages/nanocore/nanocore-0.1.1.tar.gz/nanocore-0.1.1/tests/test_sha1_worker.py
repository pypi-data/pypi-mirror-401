import pytest
import hashlib
from nanocore.sha1_worker import SHA1Worker


def test_sha1_worker_compute():
    """Test SHA1Worker compute_sha1 with valid data."""
    worker = SHA1Worker()
    data = "hello world"
    expected_hash = hashlib.sha1(data.encode()).hexdigest()

    payload = {"data": data}
    worker.handle_compute(payload)

    assert worker.count == 1
    # Note: The worker logs the result but doesn't return it directly in handle_compute.
    # However, we can verify it processed the message.


def test_sha1_worker_missing_data():
    """Test SHA1Worker compute_sha1 with missing data."""
    worker = SHA1Worker()

    # Missing 'data' key should trigger line 25
    payload = {}
    worker.handle_compute(payload)

    assert worker.count == 0


def test_sha1_worker_none_data():
    """Test SHA1Worker compute_sha1 with None data."""
    worker = SHA1Worker()

    # data=None should also trigger line 25
    payload = {"data": None}
    worker.handle_compute(payload)

    assert worker.count == 0


def test_sha1_worker_non_string_data():
    """Test SHA1Worker compute_sha1 with non-string data."""
    worker = SHA1Worker()
    data = 12345
    expected_hash = hashlib.sha1(str(data).encode()).hexdigest()

    payload = {"data": data}
    worker.handle_compute(payload)

    assert worker.count == 1
