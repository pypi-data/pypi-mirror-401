"""Content negotiation utilities.

This module provides helpers for JSON serialization/deserialization
in state views and state changes, matching the content negotiation
pattern from the Rust SDK.
"""

from __future__ import annotations

import json
from typing import Any, TypeVar

from evidentsource_functions.errors import (
    DeserializationFailed,
    NoBody,
    UnsupportedContentType,
)

T = TypeVar("T")


def negotiate_command(content_type: str, body: bytes | None) -> Any:
    """Parse command body based on content type.

    Currently supports JSON content types.

    Args:
        content_type: The content type of the body
        body: The raw body bytes

    Returns:
        The parsed body (typically a dict for JSON)

    Raises:
        NoBody: If body is None or empty
        UnsupportedContentType: If content type is not supported
        DeserializationFailed: If parsing fails

    Example:
        ```python
        def parse_command(cmd: Command) -> MyCommand:
            data = negotiate_command(cmd.content_type, cmd.body)
            return MyCommand(**data)
        ```
    """
    if body is None or len(body) == 0:
        raise NoBody()

    if not _is_json_content_type(content_type):
        raise UnsupportedContentType(content_type)

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise DeserializationFailed(str(e)) from e


def serialize_state(state: Any, content_type: str | None = None) -> bytes | None:
    """Serialize state to bytes based on content type.

    Currently supports JSON serialization.

    Args:
        state: The state to serialize
        content_type: The content type (defaults to application/json)

    Returns:
        The serialized bytes, or None if state is None

    Example:
        ```python
        class MyState:
            def to_dict(self):
                return {"balance": self.balance}

        content = serialize_state(state.to_dict())
        ```
    """
    if state is None:
        return None

    content_type = content_type or "application/json"

    if _is_json_content_type(content_type):
        return json.dumps(state).encode("utf-8")

    # Default to JSON
    return json.dumps(state).encode("utf-8")


def deserialize_state(
    data: bytes | None,
    content_type: str | None = None,
) -> Any:
    """Deserialize state from bytes.

    Currently supports JSON deserialization.

    Args:
        data: The raw bytes to deserialize
        content_type: The content type (defaults to application/json)

    Returns:
        The deserialized data, or None if data is None/empty

    Example:
        ```python
        data = deserialize_state(state_view.content)
        state = MyState(**data) if data else MyState()
        ```
    """
    if data is None or len(data) == 0:
        return None

    content_type = content_type or "application/json"

    if _is_json_content_type(content_type):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return None

    # Default to JSON
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


def _is_json_content_type(content_type: str) -> bool:
    """Check if content type is a JSON type."""
    return content_type == "application/json" or content_type.endswith("+json")
