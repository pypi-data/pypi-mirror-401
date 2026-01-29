import asyncio
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class Worker:
    """
    Base Worker class that processes messages from an asynchronous queue.
    """

    STOP_SENTINEL = object()

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.running_signal: asyncio.Event = asyncio.Event()
        self._handlers: Dict[str, Callable] = {}
        self._main_task: Optional[asyncio.Task] = None

    def register_handler(self, message_type: str, handler: Callable):
        """Registers a handler for a specific message type."""
        self._handlers[message_type] = handler

    @property
    def handlers(self) -> Dict[str, Callable]:
        """Returns the registered message handlers for introspection."""
        return self._handlers

    def submit(self, message: Any):
        """Submits a message to the worker's queue."""
        self.queue.put_nowait(message)

    async def run(self):
        """
        Main loop. Waits for the start signal, then processes messages.
        """
        logger.info("Worker waiting for start signal...")
        await self.running_signal.wait()
        logger.info("Worker started.")

        try:
            while True:
                message = await self.queue.get()

                if message is self.STOP_SENTINEL:
                    self.queue.task_done()
                    logger.info("Stop sentinel received. Shutting down worker.")
                    break

                await self._process_message(message)
                self.queue.task_done()
        except asyncio.CancelledError:
            logger.info("Worker task cancelled.")
            raise
        finally:
            logger.info("Worker stopped.")

    async def _process_message(self, message: Any):
        """Dispatches the message to the appropriate handler."""
        from nanocore.schema import validate_message

        if validate_message(message):
            msg_type = message["header"]["msg_type"]
            payload = message["body"]
        else:
            # Fallback for old style messages or non-compliant ones
            msg_type = getattr(message, "type", None) or (
                message.get("type") if isinstance(message, dict) else None
            )
            payload = message

        if not msg_type:
            logger.warning(f"Message received without type: {message}")
            return

        handler = self._handlers.get(msg_type)
        if handler:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(payload)
                else:
                    handler(payload)
            except Exception as e:
                logger.error(f"Error handling message {msg_type}: {e}")
        else:
            logger.warning(f"No handler registered for message type: {msg_type}")

    def start(self):
        """Sets the running signal to allow processing."""
        self.running_signal.set()

    def stop(self):
        """Clears the running signal and submits a stop sentinel."""
        self.running_signal.clear()
        self.submit(self.STOP_SENTINEL)
