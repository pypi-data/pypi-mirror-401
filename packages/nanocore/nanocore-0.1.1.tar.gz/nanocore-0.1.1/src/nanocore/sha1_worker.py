import hashlib
import logging
from typing import Any
from nanocore.worker import Worker

logger = logging.getLogger(__name__)


class SHA1Worker(Worker):
    """
    A worker that computes the SHA1 hash of a given string.
    """

    def __init__(self):
        super().__init__()
        self.count = 0
        self.register_handler("compute_sha1", self.handle_compute)

    def handle_compute(self, payload: Any):
        data = payload.get("data")
        if data is not None:
            sha1 = hashlib.sha1(str(data).encode()).hexdigest()
            self.count += 1
            logger.debug(f"Computed SHA1: {sha1} (Total: {self.count})")
        else:
            logger.warning("Compute SHA1 message missing 'data'")
