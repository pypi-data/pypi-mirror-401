"""Testing utilities for WASM components.

This module provides mock implementations and test helpers for testing
state changes and state views without a running server.

Example:
    ```python
    from evidentsource_functions.testing import MockDatabase, TestEventBuilder

    # Create a mock database
    db = MockDatabase("test-db").with_revision(100)

    # Add state view data
    db.insert_state_view("my-view", 1, {"count": 5}, 50)

    # Add events
    event = TestEventBuilder("order.created").stream("orders").subject("order-1").build_stored()
    db.insert_event(event)

    # Use in tests
    result = db.view_state("my-view", 1)
    events = db.query_events(EventSelector.event_type_equals("order.created"))
    ```
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, TypeVar

from evidentsource_core import (
    Event,
    EventData,
    EventSelector,
    ProspectiveEvent,
    StringEventData,
)

T = TypeVar("T")


@dataclass
class StateViewResult[T]:
    """Result from a state view query, containing the deserialized data and revision.

    Attributes:
        data: The deserialized state view data
        revision: The revision at which this state was last modified
    """

    data: T
    revision: int


# =============================================================================
# MockDatabase - simulates the Database wrapper for testing state changes
# =============================================================================


@dataclass(frozen=True)
class _StateViewKey:
    """Key for state view lookups."""

    name: str
    version: int
    parameters: tuple[tuple[str, str], ...]  # Sorted parameters for consistent hashing


@dataclass
class _MockStateViewData:
    """Stored state view data."""

    content: bytes
    last_modified_revision: int
    last_modified_timestamp: datetime


class MockDatabase:
    """Mock database for testing state change logic.

    This simulates the Database wrapper, providing a domain-type API for
    unit tests without requiring WASM or a server.

    Example:
        ```python
        from evidentsource_functions.testing import MockDatabase

        db = MockDatabase("test-db").with_revision(100)

        # Add state view data
        db.insert_state_view("my-view", 1, {"count": 5}, 50)

        # Add events
        db.insert_event(event)

        # Use in tests
        result = db.view_state("my-view", 1)
        events = db.query_events(selector)
        ```
    """

    def __init__(self, name: str) -> None:
        """Create a new mock database with the given name.

        Uses current time for timestamps and revision 0.
        """
        now = datetime.now(UTC)
        self._name = name
        self._created_at = now
        self._revision = 0
        self._revision_timestamp = now
        self._effective_timestamp: datetime | None = None
        self._events: list[Event] = []
        self._state_views: dict[_StateViewKey, _MockStateViewData] = {}

    def with_revision(self, revision: int) -> MockDatabase:
        """Set the revision (builder pattern)."""
        self._revision = revision
        return self

    def with_revision_timestamp(self, timestamp: datetime) -> MockDatabase:
        """Set the revision timestamp (builder pattern)."""
        self._revision_timestamp = timestamp
        return self

    def with_created_at(self, timestamp: datetime) -> MockDatabase:
        """Set the created_at timestamp (builder pattern)."""
        self._created_at = timestamp
        return self

    def with_events(self, events: list[Event]) -> MockDatabase:
        """Set events (builder pattern)."""
        self._events = list(events)
        return self

    @property
    def name(self) -> str:
        """Get the database name."""
        return self._name

    @property
    def created_at(self) -> datetime:
        """Get when the database was created."""
        return self._created_at

    @property
    def revision(self) -> int:
        """Get the current revision."""
        return self._revision

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp of the current revision."""
        return self._revision_timestamp

    @property
    def effective_timestamp(self) -> datetime | None:
        """Get the effective timestamp, if scoped."""
        return self._effective_timestamp

    def insert_event(self, event: Event) -> None:
        """Insert a single event."""
        self._events.append(event)

    def insert_state_view(
        self,
        name: str,
        version: int,
        data: Any,
        revision: int,
    ) -> None:
        """Insert a state view response.

        Args:
            name: State view name
            version: State view version
            data: The data to return (will be serialized to JSON)
            revision: The last modified revision
        """
        key = _StateViewKey(name=name, version=version, parameters=())
        content = json.dumps(data).encode("utf-8")
        self._state_views[key] = _MockStateViewData(
            content=content,
            last_modified_revision=revision,
            last_modified_timestamp=self._revision_timestamp,
        )

    def insert_state_view_with_params(
        self,
        name: str,
        version: int,
        params: dict[str, str],
        data: Any,
        revision: int,
    ) -> None:
        """Insert a state view response with parameters.

        Args:
            name: State view name
            version: State view version
            params: Parameter bindings (e.g., {"account_id": "123"})
            data: The data to return (will be serialized to JSON)
            revision: The last modified revision
        """
        sorted_params = tuple(sorted(params.items()))
        key = _StateViewKey(name=name, version=version, parameters=sorted_params)
        content = json.dumps(data).encode("utf-8")
        self._state_views[key] = _MockStateViewData(
            content=content,
            last_modified_revision=revision,
            last_modified_timestamp=self._revision_timestamp,
        )

    def query_events(self, selector: EventSelector) -> list[Event]:
        """Query events matching the selector.

        Uses EventSelector.matches() for client-side filtering.
        """
        return [e for e in self._events if selector.matches(e)]

    def all_events(self) -> list[Event]:
        """Get all events (unfiltered)."""
        return list(self._events)

    def view_state(
        self,
        name: str,
        version: int,
        params: dict[str, str] | None = None,
    ) -> StateViewResult[dict[str, Any]] | None:
        """View a state view.

        Args:
            name: State view name
            version: State view version
            params: Optional parameter bindings

        Returns:
            StateViewResult with parsed JSON data and revision, or None if not found
        """
        if params is None:
            params = {}
        sorted_params = tuple(sorted(params.items()))
        key = _StateViewKey(name=name, version=version, parameters=sorted_params)

        data = self._state_views.get(key)
        if data is None:
            return None

        deserialized = json.loads(data.content.decode("utf-8"))
        return StateViewResult(data=deserialized, revision=data.last_modified_revision)

    def at_effective_timestamp(self, ts: datetime) -> MockDatabaseAtEffectiveTimestamp:
        """Navigate to an effective timestamp for bi-temporal queries."""
        return MockDatabaseAtEffectiveTimestamp(basis=self, effective_ts=ts)

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> MockSpeculativeDatabase:
        """Create a speculative view with additional prospective events."""
        return MockSpeculativeDatabase(
            basis=self,
            speculated_transactions=[events],
        )


class MockDatabaseAtEffectiveTimestamp:
    """Mock database scoped to an effective timestamp."""

    def __init__(self, basis: MockDatabase, effective_ts: datetime) -> None:
        self._basis = basis
        self._effective_ts = effective_ts

    @property
    def effective_timestamp(self) -> datetime:
        """Get the effective timestamp."""
        return self._effective_ts

    @property
    def name(self) -> str:
        """Get the database name."""
        return self._basis.name

    @property
    def revision(self) -> int:
        """Get the revision."""
        return self._basis.revision

    @property
    def revision_timestamp(self) -> datetime:
        """Get the revision timestamp."""
        return self._basis.revision_timestamp

    def query_events(self, selector: EventSelector) -> list[Event]:
        """Query events (delegates to basis)."""
        return self._basis.query_events(selector)

    def view_state(
        self,
        name: str,
        version: int,
        params: dict[str, str] | None = None,
    ) -> StateViewResult[dict[str, Any]] | None:
        """View a state view (delegates to basis)."""
        return self._basis.view_state(name, version, params)

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> MockSpeculativeDatabase:
        """Create a speculative view with additional prospective events."""
        return MockSpeculativeDatabase(
            basis=self._basis,
            speculated_transactions=[events],
            effective_timestamp=self._effective_ts,
        )


class MockSpeculativeDatabase:
    """Mock speculative database with uncommitted prospective events."""

    def __init__(
        self,
        basis: MockDatabase,
        speculated_transactions: list[list[ProspectiveEvent]],
        effective_timestamp: datetime | None = None,
    ) -> None:
        self._basis = basis
        self._speculated_transactions = speculated_transactions
        self._effective_timestamp = effective_timestamp

    @property
    def name(self) -> str:
        """Get the database name (same as basis)."""
        return self._basis.name

    @property
    def created_at(self) -> datetime:
        """Get when the database was created (same as basis)."""
        return self._basis.created_at

    @property
    def revision(self) -> int:
        """Get the speculative revision (basis + event count)."""
        return self._basis.revision + self.speculated_event_count

    @property
    def revision_timestamp(self) -> datetime:
        """Get the revision timestamp (same as basis)."""
        return self._basis.revision_timestamp

    @property
    def effective_timestamp(self) -> datetime | None:
        """Get the effective timestamp, if scoped."""
        return self._effective_timestamp

    @property
    def speculated_event_count(self) -> int:
        """Get the count of speculated events."""
        return sum(len(txn) for txn in self._speculated_transactions)

    @property
    def basis(self) -> MockDatabase:
        """Get the basis database."""
        return self._basis

    @property
    def speculated_transactions(self) -> list[list[ProspectiveEvent]]:
        """Get the transactions of speculated events."""
        return self._speculated_transactions

    def query_events(self, selector: EventSelector) -> list[Event]:
        """Query events including basis events.

        Note: Speculated events are not included in this query.
        Use query_speculated_events to query speculated events.
        """
        return self._basis.query_events(selector)

    def query_speculated_events(self, selector: EventSelector) -> list[ProspectiveEvent]:
        """Query prospective events only (speculated events)."""
        return [
            e
            for txn in self._speculated_transactions
            for e in txn
            if selector.matches_prospective(e)
        ]

    def view_state(
        self,
        name: str,
        version: int,
        params: dict[str, str] | None = None,
    ) -> StateViewResult[dict[str, Any]] | None:
        """View a state view (delegates to basis - cannot compute speculatively).

        Note: Mock cannot compute state views speculatively.
        This returns the basis state view, which is acceptable for many tests.
        """
        return self._basis.view_state(name, version, params)

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> MockSpeculativeDatabase:
        """Add more speculated events."""
        return MockSpeculativeDatabase(
            basis=self._basis,
            speculated_transactions=[*self._speculated_transactions, events],
            effective_timestamp=self._effective_timestamp,
        )

    def at_effective_timestamp(self, ts: datetime) -> MockSpeculativeDatabase:
        """Navigate to an effective timestamp."""
        return MockSpeculativeDatabase(
            basis=self._basis,
            speculated_transactions=self._speculated_transactions,
            effective_timestamp=ts,
        )


# =============================================================================
# TestEventBuilder - builder for creating test events
# =============================================================================


class EventBuilder:
    """Builder for creating test ProspectiveEvents.

    This provides a simplified API for creating events in tests.

    Example:
        ```python
        from evidentsource_functions.testing import EventBuilder

        event = (
            EventBuilder("account.opened")
            .subject("account-123")
            .stream("test-stream")
            .data({"account_id": "123", "customer_id": "cust-456"})
            .build()
        )
        ```
    """

    def __init__(self, event_type: str) -> None:
        """Create a new test event builder."""
        self._event_type = event_type
        self._stream: str | None = None
        self._subject: str | None = None
        self._data: EventData | None = None
        self._time: datetime | None = None
        self._extensions: dict[str, Any] = {}

    def subject(self, subject: str) -> EventBuilder:
        """Set the subject."""
        self._subject = subject
        return self

    def stream(self, stream: str) -> EventBuilder:
        """Set the stream."""
        self._stream = stream
        return self

    def data(self, data: Any) -> EventBuilder:
        """Set the data from a serializable value."""
        json_str = json.dumps(data)
        self._data = StringEventData(json_str)
        return self

    def date(self, date: Any) -> EventBuilder:
        """Set the timestamp from a date (at midnight UTC).

        Args:
            date: A date object with year, month, day attributes
        """
        from datetime import date as date_type

        if isinstance(date, date_type):
            self._time = datetime(date.year, date.month, date.day, tzinfo=UTC)
        return self

    def timestamp(self, dt: datetime) -> EventBuilder:
        """Set the timestamp."""
        self._time = dt
        return self

    def extension(self, key: str, value: str) -> EventBuilder:
        """Add a string extension attribute."""
        self._extensions[key] = value
        return self

    def build(self) -> ProspectiveEvent:
        """Build the ProspectiveEvent.

        Raises:
            ValueError: If stream is not set
        """
        if self._stream is None:
            raise ValueError("Failed to build test event - stream is required")

        return ProspectiveEvent(
            id=str(uuid.uuid4()),
            stream=self._stream,
            event_type=self._event_type,
            subject=self._subject,
            data=self._data,
            time=self._time,
            datacontenttype="application/json" if self._data else None,
            dataschema=None,
            extensions=self._extensions,
        )

    def build_stored(self) -> Event:
        """Build as a stored Event (for mocking query results).

        Converts the prospective event to a stored event by creating
        a mock source URI.
        """
        prospective = self.build()
        return Event(
            id=prospective.id,
            source=f"https://test.local/db/test/streams/{prospective.stream}",
            event_type=prospective.event_type,
            subject=prospective.subject,
            data=prospective.data,
            time=prospective.time,
            datacontenttype=prospective.datacontenttype,
            dataschema=prospective.dataschema,
            extensions=prospective.extensions,
        )


# Alias for backwards compatibility
TestEventBuilder = EventBuilder


# =============================================================================
# Helper functions
# =============================================================================


def create_prospective_event(
    event_type: str,
    subject: str | None = None,
    data: Any = None,
    stream: str = "test-stream",
) -> ProspectiveEvent:
    """Helper to create a simple test ProspectiveEvent with minimal fields.

    Automatically sets a default stream ("test-stream") to satisfy requirements.

    Args:
        event_type: The event type
        subject: Optional subject
        data: Optional data (will be JSON serialized)
        stream: Stream name (defaults to "test-stream")

    Returns:
        A ProspectiveEvent for testing
    """
    builder = EventBuilder(event_type).stream(stream)

    if subject is not None:
        builder = builder.subject(subject)

    if data is not None:
        builder = builder.data(data)

    return builder.build()


def create_stored_event(
    event_type: str,
    subject: str | None = None,
    data: Any = None,
    stream: str = "test-stream",
) -> Event:
    """Helper to create a simple test stored Event with minimal fields.

    Automatically sets a default stream ("test-stream") and mock source URI.

    Args:
        event_type: The event type
        subject: Optional subject
        data: Optional data (will be JSON serialized)
        stream: Stream name (defaults to "test-stream")

    Returns:
        A stored Event for testing
    """
    builder = EventBuilder(event_type).stream(stream)

    if subject is not None:
        builder = builder.subject(subject)

    if data is not None:
        builder = builder.data(data)

    return builder.build_stored()
