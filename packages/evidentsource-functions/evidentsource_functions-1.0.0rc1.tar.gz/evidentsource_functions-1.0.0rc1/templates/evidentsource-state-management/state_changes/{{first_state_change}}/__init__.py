"""{{first_state_change}} state change component.

This component handles the {{first_state_change}} command.
"""

import json
import uuid
from typing import Any

from evidentsource_functions import (
    Command,
    Constraint,
    DatabaseAccess,
    DecideResult,
    ProspectiveEvent,
    StateChangeError,
    StateChangeMetadata,
    StringEventData,
    create_state_change_handler,
)

from domain import ExampleCommand, ExampleEventOccurred


def decide(
    db: DatabaseAccess,
    command: ExampleCommand,
    metadata: StateChangeMetadata,
) -> DecideResult:
    """Process the command and return events to emit.

    Args:
        db: Database access for querying state views
        command: The parsed command
        metadata: Metadata about the command invocation

    Returns:
        Tuple of (events to emit, constraints to enforce)

    Raises:
        StateChangeError: If command validation or processing fails
    """
    # TODO: Query any required state views using db.view_state()
    # Example:
    # result = db.view_state("calendar", 1, [])
    # if result is not None:
    #     calendar_data = json.loads(result.content or b"{}")
    #     # Use calendar_data...

    # TODO: Implement your business logic here
    # Validate the command, check preconditions, etc.

    # Create domain event
    event_data = ExampleEventOccurred(
        id=command.id,
        timestamp=command.processing_day,
    )

    # Convert domain event to ProspectiveEvent
    event = ProspectiveEvent(
        id=str(uuid.uuid4()),
        stream=event_data.stream(command.processing_day),
        event_type=event_data.event_type,
        subject=event_data.subject,
        data=StringEventData(json.dumps(event_data.to_dict())),
        datacontenttype="application/json",
    )

    # Create batch constraints
    # This ensures that the same command hasn't been processed before
    constraints = [
        Constraint.max_subject_type(
            subject=command.id,
            event_type=event_data.event_type,
            max_revision=0,  # Revision 0 means the event must not exist yet
        ),
    ]

    return ([event], constraints)


# Create the handler that will be exported to WASM
# This handles command parsing and error conversion
handler = create_state_change_handler(ExampleCommand, decide)


# For componentize-py, we export the handler as the module's decide function
def wit_decide(
    db: Any,
    command: Any,
    metadata: Any,
) -> Any:
    """WIT-compatible decide function.

    This wraps the typed handler for the WASM component interface.
    In production, the WIT bindings will call this function.
    """
    # Convert WIT types to SDK types and call handler
    from evidentsource_functions.wit_types import (
        constraint_to_wit,
        datetime_from_wit,
        prospective_event_to_wit_cloudevent,
    )

    sdk_command = Command(
        body=command.body,
        content_type=command.content_type,
        content_schema=command.content_schema,
    )

    sdk_metadata = StateChangeMetadata(
        state_change_name=metadata.state_change_name,
        state_change_version=metadata.state_change_version,
        last_seen_revision=metadata.last_seen_revision,
        command_received_at=datetime_from_wit(metadata.command_received_at),
        command_headers=list(metadata.command_headers),
    )

    try:
        events, constraints = handler(db, sdk_command, sdk_metadata)

        # Convert back to WIT types
        wit_events = [prospective_event_to_wit_cloudevent(e) for e in events]
        wit_constraints = [constraint_to_wit(c) for c in constraints]

        return (wit_events, wit_constraints)
    except StateChangeError as e:
        # Convert to WIT error type
        raise e
