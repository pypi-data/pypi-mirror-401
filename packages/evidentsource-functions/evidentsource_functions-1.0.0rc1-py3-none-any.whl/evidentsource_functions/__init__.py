"""EvidentSource SDK for Python.

This SDK provides utilities for building WebAssembly state changes
and state views that run on the EvidentSource event sourcing platform.

## Design Philosophy

The SDK provides a clean separation between WIT types (internal implementation
details) and domain types (what users work with). Users define their own
domain types and use simple conversion methods to bridge the gap.

**Key Points:**
- State changes emit `ProspectiveEvent` (events before storage)
- State views receive `Event` (stored events with metadata)
- WIT types are never exposed to user code

The SDK provides:
- **StateViewBase**: Base class for implementing state views
- **StateChangeError**: Structured errors for state change failures
- **Content negotiation**: Automatic JSON serialization/deserialization
- **Type conversions**: WIT ↔ domain type utilities

## Quick Start - State View

```python
from dataclasses import dataclass
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

## Quick Start - State Change

```python
from dataclasses import dataclass
from evidentsource_functions import (
    StateChangeError,
    Command,
    StateChangeMetadata,
    DatabaseAccess,
)
from evidentsource_core import ProspectiveEvent, StringEventData, Selector, Constraint
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
    db: DatabaseAccess,
    command: DepositCommand,
    metadata: StateChangeMetadata,
) -> tuple[list[ProspectiveEvent], list]:
    if command.amount <= 0:
        raise StateChangeError.validation("Amount must be positive")

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

    return ([event], [])
```

## Building WASM Components

Use componentize-py to build your state views and state changes:

```bash
# Build a state view
componentize-py -d ./interface/decider.wit -w state-view \\
    componentize -o state_view.wasm state_view

# Build a state change
componentize-py -d ./interface/decider.wit -w state-change \\
    componentize -o state_change.wasm state_change
```
"""

# Core types from evidentsource-core
from evidentsource_core import (
    AppendCondition,
    BinaryEventData,
    BooleanExtension,
    # Constraints
    Constraint,
    # Identifiers
    DatabaseName,
    # Events
    Event,
    EventData,
    EventId,
    EventSelector,
    EventSubject,
    EventType,
    ExtensionValue,
    IntegerExtension,
    ProspectiveEvent,
    # Selectors
    Selector,
    StateChangeName,
    StateViewName,
    StreamName,
    StringEventData,
    StringExtension,
)

# Content negotiation
from evidentsource_functions.content import (
    deserialize_state,
    negotiate_command,
    serialize_state,
)

# Errors
from evidentsource_functions.errors import (
    ContentNegotiationError,
    DatabaseAccessError,
    DeserializationFailed,
    NoBody,
    StateChangeError,
    StateChangeErrorKind,
    UnsupportedContentType,
)

# State change
from evidentsource_functions.state_change import (
    Command,
    DatabaseAccess,
    DecideResult,
    SpeculativeDatabase,
    StateChangeMetadata,
    create_state_change_handler,
)

# State view
from evidentsource_functions.state_view import (
    RenderedStateView,
    StateViewBase,
    StateViewContext,
    create_state_view_handler,
)

# Testing utilities
from evidentsource_functions.testing import (
    EventBuilder,
    MockDatabase,
    MockDatabaseAtEffectiveTimestamp,
    MockSpeculativeDatabase,
    StateViewResult,
    TestEventBuilder,  # Alias for backwards compatibility
)
from evidentsource_functions.testing import (
    create_prospective_event as test_event,
)
from evidentsource_functions.testing import (
    create_stored_event as test_stored_event,
)

# WIT type conversions
from evidentsource_functions.wit_types import (
    WitDatetime,
    condition_to_wit,
    datetime_from_wit,
    datetime_to_wit,
    prospective_event_to_wit_cloudevent,
    selector_to_wit,
    wit_cloudevent_to_event,
)

__version__ = "0.8.0"

__all__ = [
    # Core event types
    "Event",
    "ProspectiveEvent",
    "EventData",
    "BinaryEventData",
    "StringEventData",
    "ExtensionValue",
    "BooleanExtension",
    "IntegerExtension",
    "StringExtension",
    # Selectors
    "Selector",
    "EventSelector",
    # Constraints
    "Constraint",
    "AppendCondition",
    # Identifiers
    "DatabaseName",
    "StreamName",
    "EventId",
    "EventType",
    "EventSubject",
    "StateViewName",
    "StateChangeName",
    # State view
    "StateViewBase",
    "StateViewContext",
    "RenderedStateView",
    "create_state_view_handler",
    # State change
    "Command",
    "StateChangeMetadata",
    "DatabaseAccess",
    "SpeculativeDatabase",
    "DecideResult",
    "create_state_change_handler",
    # Errors
    "StateChangeError",
    "StateChangeErrorKind",
    "DatabaseAccessError",
    "ContentNegotiationError",
    "NoBody",
    "UnsupportedContentType",
    "DeserializationFailed",
    # Content negotiation
    "negotiate_command",
    "serialize_state",
    "deserialize_state",
    # WIT conversions
    "WitDatetime",
    "datetime_from_wit",
    "datetime_to_wit",
    "wit_cloudevent_to_event",
    "prospective_event_to_wit_cloudevent",
    "selector_to_wit",
    "condition_to_wit",
    # Testing utilities
    "MockDatabase",
    "MockDatabaseAtEffectiveTimestamp",
    "MockSpeculativeDatabase",
    "StateViewResult",
    "EventBuilder",
    "TestEventBuilder",  # Alias for backwards compatibility
    "test_event",
    "test_stored_event",
]
