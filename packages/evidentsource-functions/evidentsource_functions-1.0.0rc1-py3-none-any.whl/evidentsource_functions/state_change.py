"""State change implementation helpers.

This module provides utilities for implementing state changes that run
as WASM components.

A state change is a command handler that:
1. Receives a command and database access
2. Validates the command against current state
3. Returns events to be committed (with optional constraints)

Example:
    ```python
    from dataclasses import dataclass
    from evidentsource_functions import (
        StateChangeError,
        Database,
        StateChangeMetadata,
        ProspectiveEvent,
        StringEventData,
        Selector,
        Constraint,
    )
    import json
    import uuid

    @dataclass
    class DepositCommand:
        account_id: str
        amount: float

        @classmethod
        def from_dict(cls, data: dict) -> "DepositCommand":
            return cls(
                account_id=data["account_id"],
                amount=data["amount"],
            )

    def decide(
        db: Database,
        command: DepositCommand,
        metadata: StateChangeMetadata,
    ) -> tuple[list[ProspectiveEvent], list]:
        # Validate
        if command.amount <= 0:
            raise StateChangeError.validation("Amount must be positive")

        # Create event
        event = ProspectiveEvent(
            id=str(uuid.uuid4()),
            stream="accounts",
            event_type="account.credited",
            subject=command.account_id,
            data=StringEventData(json.dumps({
                "account_id": command.account_id,
                "amount": command.amount,
            })),
            datacontenttype="application/json",
        )

        # Optional: add constraint to ensure account exists
        constraints = [
            Constraint.must_exist(Selector.subject(command.account_id))
        ]

        return ([event], constraints)
    ```
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol, TypeVar

from evidentsource_core import (
    AppendCondition,
    Event,
    EventSelector,
    ProspectiveEvent,
    StateView,
)

from evidentsource_functions.content import negotiate_command
from evidentsource_functions.errors import StateChangeError


@dataclass
class Command:
    """A command received by a state change.

    This mirrors the WIT Command type.
    """

    body: bytes | None
    content_type: str
    content_schema: str | None = None

    def parse_json(self) -> Any:
        """Parse the command body as JSON.

        Returns:
            The parsed JSON data

        Raises:
            NoBody: If body is None or empty
            UnsupportedContentType: If content type is not JSON
            DeserializationFailed: If parsing fails
        """
        return negotiate_command(self.content_type, self.body)


@dataclass
class StateChangeMetadata:
    """Metadata about the state change invocation.

    This contains information about the command context.
    """

    state_change_name: str
    state_change_version: int
    last_seen_revision: int
    command_received_at: datetime
    command_headers: list[tuple[str, str]] = field(default_factory=list)

    def get_header(self, name: str) -> str | None:
        """Get a header value by name (case-insensitive)."""
        name_lower = name.lower()
        for key, value in self.command_headers:
            if key.lower() == name_lower:
                return value
        return None


class SpeculativeDatabase(Protocol):
    """Protocol for speculative database access within a state change.

    This allows querying the database as if certain events had been committed.
    """

    @property
    def name(self) -> str:
        """Get the database name."""
        ...

    @property
    def revision(self) -> int:
        """Get the current revision (basis + speculated event count)."""
        ...

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp of the basis revision."""
        ...

    @property
    def effective_timestamp(self) -> datetime | None:
        """Get the effective timestamp this view is scoped to, if any."""
        ...

    @property
    def speculated_event_count(self) -> int:
        """Get the number of speculated events."""
        ...

    def at_effective_timestamp(self, timestamp: datetime) -> SpeculativeDatabase:
        """Get a view scoped to a specific effective timestamp."""
        ...

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabase:
        """Add another transaction of speculative events."""
        ...

    def query_events(self, selector: EventSelector) -> list[Event]:
        """Query events matching the selector (includes speculated events)."""
        ...

    def view_state(
        self,
        name: str,
        version: int,
        parameters: list[tuple[str, Any]] | None = None,
    ) -> StateView | None:
        """Fetch a state view."""
        ...


class DatabaseAccess(Protocol):
    """Protocol for database access within a state change.

    This provides the API for querying events and state views
    during command processing. Supports bi-temporal queries via
    at_effective_timestamp() and speculative queries via speculate_with_transaction().
    """

    @property
    def name(self) -> str:
        """Get the database name."""
        ...

    @property
    def revision(self) -> int:
        """Get the current revision."""
        ...

    @property
    def revision_timestamp(self) -> datetime:
        """Get the timestamp of the current revision."""
        ...

    @property
    def effective_timestamp(self) -> datetime | None:
        """Get the effective timestamp this view is scoped to, if any."""
        ...

    def at_effective_timestamp(self, timestamp: datetime) -> DatabaseAccess:
        """Get a view scoped to a specific effective timestamp (for bi-temporal queries).

        This allows querying the database state as it was understood at a
        particular point in effective time.

        Example:
            ```python
            from datetime import datetime, timezone

            # Query account balance as of end of business day
            eod = datetime(2025, 3, 15, 23, 59, 59, 999999, tzinfo=timezone.utc)
            db_at_eod = db.at_effective_timestamp(eod)
            account = db_at_eod.view_state("account-summary", 1, [("account_id", account_id)])
            ```
        """
        ...

    def speculate_with_transaction(self, events: list[ProspectiveEvent]) -> SpeculativeDatabase:
        """Create a speculative view with additional uncommitted events.

        This allows testing what the database would look like if certain
        events were committed, useful for validation scenarios.

        Example:
            ```python
            # Simulate depositing funds to check resulting balance
            deposit_event = ProspectiveEvent(...)
            spec_db = db.speculate_with_transaction([deposit_event])
            new_balance = spec_db.view_state("account-summary", 1, [...])
            ```
        """
        ...

    def query_events(self, selector: EventSelector) -> list[Event]:
        """Query events matching the selector."""
        ...

    def view_state(
        self,
        name: str,
        version: int,
        parameters: list[tuple[str, Any]] | None = None,
    ) -> StateView | None:
        """Fetch a state view."""
        ...


T = TypeVar("T")


DecideResult = tuple[list[ProspectiveEvent], list[AppendCondition]]
"""Result type for decide functions: (events, conditions)."""


DecideFunc = Callable[[DatabaseAccess, T, StateChangeMetadata], DecideResult]
"""Type for decide functions that take a typed command."""


def create_state_change_handler(
    command_type: type[T],
    decide_func: DecideFunc[T],
) -> Callable[[DatabaseAccess, Command, StateChangeMetadata], DecideResult]:
    """Create a state change handler function.

    This creates the `decide` function that the WASM component exports.
    It handles command parsing and error conversion.

    Args:
        command_type: The command class (must have `from_dict` method)
        decide_func: The decide function that processes commands

    Returns:
        A decide function matching the WIT interface

    Example:
        ```python
        from evidentsource_functions import create_state_change_handler

        @dataclass
        class MyCommand:
            value: str

            @classmethod
            def from_dict(cls, data: dict) -> "MyCommand":
                return cls(value=data["value"])

        def my_decide(db, command: MyCommand, metadata):
            # ... implementation
            return (events, constraints)

        decide = create_state_change_handler(MyCommand, my_decide)
        ```
    """

    def decide(
        db: DatabaseAccess,
        command: Command,
        metadata: StateChangeMetadata,
    ) -> DecideResult:
        # Parse command
        try:
            data = command.parse_json()
            # Type ignore: command_type is expected to have from_dict method
            typed_command = command_type.from_dict(data)  # type: ignore[attr-defined]
        except Exception as e:
            raise StateChangeError.validation(f"Failed to parse command: {e}") from e

        # Execute decide function
        return decide_func(db, typed_command, metadata)

    return decide
