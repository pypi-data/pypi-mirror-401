import logging
from typing import Any
from nanocore.worker import Worker

logger = logging.getLogger(__name__)


class RPNWorker(Worker):
    """
    A worker that performs Reverse Polish Notation (RPN) arithmetic.
    """

    def __init__(self):
        super().__init__()
        self.stack = []

        # Register handlers
        self.register_handler("push", self.handle_push)
        self.register_handler("add", self.handle_add)
        self.register_handler("sub", self.handle_sub)
        self.register_handler("mul", self.handle_mul)
        self.register_handler("div", self.handle_div)
        self.register_handler("clear", self.handle_clear)

    def handle_push(self, message: Any):
        value = message.get("value")
        if value is not None:
            self.stack.append(value)
            logger.info(f"Pushed {value} to stack. Current stack: {self.stack}")
        else:
            logger.warning("Push message missing 'value'")

    def _pop_two(self):
        if len(self.stack) < 2:
            logger.error(f"Insufficient operands in stack: {self.stack}")
            return None, None
        b = self.stack.pop()
        a = self.stack.pop()
        return a, b

    def handle_add(self, message: Any):
        a, b = self._pop_two()
        if a is not None:
            result = a + b
            self.stack.append(result)
            logger.info(f"Added {a} + {b} = {result}. Current stack: {self.stack}")

    def handle_sub(self, message: Any):
        a, b = self._pop_two()
        if a is not None:
            result = a - b
            self.stack.append(result)
            logger.info(f"Subtracted {a} - {b} = {result}. Current stack: {self.stack}")

    def handle_mul(self, message: Any):
        a, b = self._pop_two()
        if a is not None:
            result = a * b
            self.stack.append(result)
            logger.info(f"Multiplied {a} * {b} = {result}. Current stack: {self.stack}")

    def handle_div(self, message: Any):
        a, b = self._pop_two()
        if a is not None:
            if b == 0:
                logger.error("Division by zero")
                self.stack.append(
                    a
                )  # Put back 'a'? Or keep popped? Let's put both back or error.
                self.stack.append(b)
                return
            result = a / b
            self.stack.append(result)
            logger.info(f"Divided {a} / {b} = {result}. Current stack: {self.stack}")

    def handle_clear(self, message: Any):
        self.stack.clear()
        logger.info("Stack cleared")
