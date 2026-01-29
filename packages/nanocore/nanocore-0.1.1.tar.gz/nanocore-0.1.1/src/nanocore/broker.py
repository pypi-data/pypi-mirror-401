import logging
from typing import Any, Dict, List, Optional
from nanocore.worker import Worker
from nanocore.schema import validate_message

logger = logging.getLogger(__name__)


class Broker:
    """
    Manages worker registration and message dispatching.
    """

    def __init__(self):
        self._workers: Dict[str, Worker] = {}
        self._groups: Dict[str, List[str]] = {}  # group_name -> list of worker_ids
        self._rr_indices: Dict[str, int] = {}  # group_name -> last index used for RR

    def register_worker(
        self, worker_id: str, worker: Worker, groups: Optional[List[str]] = None
    ):
        """Registers a worker with an optional list of groups."""
        if worker_id in self._workers:
            logger.warning(f"Worker {worker_id} already registered. Overwriting.")

        self._workers[worker_id] = worker

        if groups:
            for group in groups:
                if group not in self._groups:
                    self._groups[group] = []
                    self._rr_indices[group] = 0
                if worker_id not in self._groups[group]:
                    self._groups[group].append(worker_id)

        logger.info(f"Worker {worker_id} registered (groups: {groups})")

    def dispatch(
        self,
        message: Any,
        strategy: Optional[str] = None,
        group: Optional[str] = None,
        worker_id: Optional[str] = None,
    ):
        """
        Dispatches a message to workers based on the specified strategy or header.
        """
        if validate_message(message):
            header = message["header"]
            # Use header if explicit values are not provided
            if not strategy:
                # Interpret routing_key as strategy if it matches one, otherwise default to round_robin
                if header["routing_key"] in ("direct", "broadcast", "round_robin"):
                    strategy = header["routing_key"]
                else:
                    strategy = "round_robin"

            if not group and not worker_id:
                # If receiver is specified and is not "all", treat as worker_id or group
                receiver = header["receiver"]
                if receiver != "all":
                    if receiver in self._workers:
                        worker_id = receiver
                        strategy = strategy or "direct"
                    elif receiver in self._groups:
                        group = receiver

        # Fallback to defaults if still not set
        strategy = strategy or "round_robin"

        if strategy == "direct":
            self._dispatch_direct(message, worker_id)
        elif strategy == "broadcast":
            self._dispatch_broadcast(message, group)
        elif strategy == "round_robin":
            self._dispatch_round_robin(message, group)
        else:
            raise ValueError(f"Unknown dispatch strategy: {strategy}")

    def _dispatch_direct(self, message: Any, worker_id: Optional[str]):
        if not worker_id:
            raise ValueError("worker_id is required for direct strategy")

        worker = self._workers.get(worker_id)
        if not worker:
            raise ValueError(f"Worker {worker_id} not found")

        worker.submit(message)

    def _dispatch_broadcast(self, message: Any, group: Optional[str]):
        target_ids = self._groups.get(group) if group else list(self._workers.keys())

        if not target_ids:
            logger.warning(f"No workers found for broadcast (group: {group})")
            return

        for wid in target_ids:
            self._workers[wid].submit(message)

    def _dispatch_round_robin(self, message: Any, group: Optional[str]):
        target_ids = self._groups.get(group) if group else list(self._workers.keys())

        if not target_ids:
            logger.warning(f"No workers found for round_robin (group: {group})")
            return

        # Use group name or a default key for global RR
        rr_key = group or "__global__"
        if rr_key not in self._rr_indices:
            self._rr_indices[rr_key] = 0

        index = self._rr_indices[rr_key] % len(target_ids)
        wid = target_ids[index]
        self._workers[wid].submit(message)

        self._rr_indices[rr_key] = (index + 1) % len(target_ids)

    def get_catalog(self) -> dict:
        """
        Returns a catalog of all registered workers and their capabilities.

        Returns:
            dict: A catalog containing:
                - workers: Dict mapping worker_id to {groups, handlers}
                - groups: Dict mapping group name to list of worker_ids
        """
        catalog = {"workers": {}, "groups": {}}

        # Build workers section
        for worker_id, worker in self._workers.items():
            # Find all groups this worker belongs to
            worker_groups = [g for g, wids in self._groups.items() if worker_id in wids]

            catalog["workers"][worker_id] = {
                "groups": worker_groups,
                "handlers": list(worker.handlers.keys()),
            }

        # Build groups section
        for group, worker_ids in self._groups.items():
            catalog["groups"][group] = list(worker_ids)

        return catalog

    def start(self):
        """Starts all registered workers."""
        for worker in self._workers.values():
            worker.start()

    def stop(self):
        """Stops all registered workers."""
        for worker in self._workers.values():
            worker.stop()
