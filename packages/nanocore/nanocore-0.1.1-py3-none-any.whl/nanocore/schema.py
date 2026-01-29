import time
import uuid
from typing import Any, Dict, Optional, TypedDict


class MessageHeader(TypedDict):
    sender: str
    receiver: str
    routing_key: str
    msg_type: str
    timestamp: float
    uuid: str


class Message(TypedDict):
    header: MessageHeader
    body: Dict[str, Any]


def create_message(
    msg_type: str,
    body: Dict[str, Any],
    sender: str = "unknown",
    receiver: str = "all",
    routing_key: str = "",
    msg_uuid: Optional[str] = None,
) -> Message:
    """
    Creates a message with the specified header and body.
    """
    return {
        "header": {
            "sender": sender,
            "receiver": receiver,
            "routing_key": routing_key,
            "msg_type": msg_type,
            "timestamp": time.time(),
            "uuid": msg_uuid or str(uuid.uuid4()),
        },
        "body": dict(body),  # Ensure a copy is made
    }


def validate_message(msg: Any) -> bool:
    """
    Validates that a dictionary matches the Message structure.
    """
    if not isinstance(msg, dict):
        return False
    if "header" not in msg or "body" not in msg:
        return False

    header = msg["header"]
    body = msg["body"]

    if not isinstance(header, dict) or not isinstance(body, dict):
        return False

    required_header_keys = {
        "sender",
        "receiver",
        "routing_key",
        "msg_type",
        "timestamp",
        "uuid",
    }
    if not required_header_keys.issubset(header.keys()):
        return False

    return True
