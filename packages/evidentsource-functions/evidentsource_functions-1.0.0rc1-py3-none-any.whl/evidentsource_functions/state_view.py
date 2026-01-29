"""State view implementation helpers.

This module provides the base class and utilities for implementing
state views that run as WASM components.

A state view is a materialized view computed by folding over events.
The host calls the `evolve` function with the current state and a batch
of events, and the state view returns the new state.

Example:
    ```python
    from dataclasses import dataclass, field
    from evidentsource_functions import StateViewBase, Event
    import json

    @dataclass
    class AccountSummary(StateViewBase):
        balance: float = 0.0
        transaction_count: int = 0

        def evolve_event(self, event: Event) -> None:
            if event.event_type == "account.credited":
                data = json.loads(event.data_as_string() or "{}")
                self.balance += data.get("amount", 0)
                self.transaction_count += 1
            elif event.event_type == "account.debited":
                data = json.loads(event.data_as_string() or "{}")
                self.balance -= data.get("amount", 0)
                self.transaction_count += 1

        def to_dict(self) -> dict:
            return {
                "balance": self.balance,
                "transaction_count": self.transaction_count,
            }

        @classmethod
        def from_dict(cls, data: dict) -> "AccountSummary":
            return cls(
                balance=data.get("balance", 0.0),
                transaction_count=data.get("transaction_count", 0),
            )
    ```
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypeVar

from evidentsource_core import Event

from evidentsource_functions.content import deserialize_state, serialize_state

S = TypeVar("S", bound="StateViewBase")


@dataclass
class StateViewContext:
    """Context information for a state view invocation.

    This contains metadata about the state view being computed.
    """

    database: str
    name: str
    version: int
    database_revision: int
    database_revision_timestamp: datetime
    content_type: str | None = None
    content_schema: str | None = None


@dataclass
class RenderedStateView:
    """A rendered state view with content and metadata."""

    context: StateViewContext
    content: bytes | None
    last_modified_revision: int
    last_modified_timestamp: datetime


class StateViewBase(ABC):
    """Base class for state view implementations.

    Subclass this to create a state view. You need to implement:
    - `evolve_event(event)`: Process a single event, updating state in place
    - `to_dict()`: Serialize state to a dict for JSON encoding
    - `from_dict(data)`: Deserialize state from a dict

    The `evolve` method handles batched events automatically.

    Example:
        ```python
        @dataclass
        class OrderSummary(StateViewBase):
            total_orders: int = 0
            total_amount: float = 0.0

            def evolve_event(self, event: Event) -> None:
                if event.event_type == "order.placed":
                    self.total_orders += 1
                    data = json.loads(event.data_as_string() or "{}")
                    self.total_amount += data.get("amount", 0)

            def to_dict(self) -> dict:
                return {"total_orders": self.total_orders, "total_amount": self.total_amount}

            @classmethod
            def from_dict(cls, data: dict) -> "OrderSummary":
                return cls(
                    total_orders=data.get("total_orders", 0),
                    total_amount=data.get("total_amount", 0.0),
                )
        ```
    """

    @abstractmethod
    def evolve_event(self, event: Event) -> None:
        """Process a single event, updating state in place.

        This is called for each event in the batch. Override this
        to implement your state evolution logic.

        Args:
            event: The event to process
        """
        ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize state to a dictionary for JSON encoding.

        Returns:
            A dict that can be JSON encoded
        """
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls: type[S], data: dict[str, Any]) -> S:
        """Deserialize state from a dictionary.

        Args:
            data: The dict to deserialize from

        Returns:
            A new instance of the state view
        """
        ...

    def evolve(self, events: list[Event]) -> None:
        """Process a batch of events.

        This calls `evolve_event` for each event in order.
        Override this if you need custom batching behavior.

        Args:
            events: The events to process
        """
        for event in events:
            self.evolve_event(event)

    def serialize(self, content_type: str | None = None) -> bytes | None:
        """Serialize the state to bytes.

        Args:
            content_type: The content type (defaults to application/json)

        Returns:
            The serialized bytes
        """
        return serialize_state(self.to_dict(), content_type)

    @classmethod
    def deserialize(
        cls: type[S],
        data: bytes | None,
        content_type: str | None = None,
    ) -> S:
        """Deserialize state from bytes.

        Args:
            data: The bytes to deserialize
            content_type: The content type (defaults to application/json)

        Returns:
            A new instance of the state view
        """
        parsed = deserialize_state(data, content_type)
        if parsed is None:
            # Return default instance - subclasses should have default values
            return cls.from_dict({})
        return cls.from_dict(parsed)


def create_state_view_handler(
    state_class: type[StateViewBase],
) -> Callable[[RenderedStateView, list[Event]], bytes | None]:
    """Create a state view handler function.

    This creates the `evolve` function that the WASM component exports.
    The function handles deserialization, event processing, and serialization.

    Args:
        state_class: The state view class to use

    Returns:
        An evolve function matching the WIT interface

    Example:
        ```python
        from evidentsource_functions import create_state_view_handler

        class MyStateView(StateViewBase):
            # ... implementation

        # This creates the exported function
        evolve = create_state_view_handler(MyStateView)
        ```
    """

    def evolve(
        state_view: RenderedStateView,
        events: list[Event],
    ) -> bytes | None:
        # Deserialize previous state
        state = state_class.deserialize(
            state_view.content,
            state_view.context.content_type,
        )

        # Process events
        state.evolve(events)

        # Serialize new state
        return state.serialize(state_view.context.content_type)

    return evolve
