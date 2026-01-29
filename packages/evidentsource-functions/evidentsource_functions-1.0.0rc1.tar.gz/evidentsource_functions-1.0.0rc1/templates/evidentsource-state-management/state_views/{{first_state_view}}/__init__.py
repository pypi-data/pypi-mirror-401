"""{{first_state_view}} state view component.

This component maintains a materialized view of {{first_state_view}}.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from evidentsource_functions import (
    Event,
    StateViewBase,
    create_state_view_handler,
)

from domain import ExampleEventOccurred


@dataclass
class ViewState(StateViewBase):
    """The materialized view state.

    This class defines the state that is computed by folding over events.
    It must implement evolve_event, to_dict, and from_dict.
    """

    # TODO: Define your view state structure
    items: list[str] = field(default_factory=list)
    last_updated: datetime | None = None

    def evolve_event(self, event: Event) -> None:
        """Process a single event, updating state in place.

        Args:
            event: The event to process
        """
        # Parse event data based on event type
        if event.event_type == "com.example.event.occurred":
            data_str = event.data_as_string()
            if data_str:
                data = json.loads(data_str)
                domain_event = ExampleEventOccurred.from_dict(data)

                # TODO: Update your view state based on the event
                self.items.append(domain_event.id)
                self.last_updated = event.time

    def to_dict(self) -> dict[str, Any]:
        """Serialize state to a dictionary for JSON encoding.

        Returns:
            A dict that can be JSON encoded
        """
        return {
            "items": self.items,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ViewState":
        """Deserialize state from a dictionary.

        Args:
            data: The dict to deserialize from

        Returns:
            A new instance of the state view
        """
        last_updated = data.get("last_updated")
        return cls(
            items=data.get("items", []),
            last_updated=datetime.fromisoformat(last_updated) if last_updated else None,
        )


# Create the handler that will be exported to WASM
# This handles deserialization, event processing, and serialization
handler = create_state_view_handler(ViewState)


# For componentize-py, we export the handler as the module's evolve function
def wit_evolve(
    state_view: Any,
    events: list[Any],
) -> bytes | None:
    """WIT-compatible evolve function.

    This wraps the typed handler for the WASM component interface.
    In production, the WIT bindings will call this function.
    """
    from evidentsource_functions import RenderedStateView, StateViewContext
    from evidentsource_functions.wit_types import datetime_from_wit, wit_cloudevent_to_event

    # Convert WIT types to SDK types
    context = StateViewContext(
        database=state_view.context.database,
        name=state_view.context.name,
        version=state_view.context.version,
        database_revision=state_view.context.database_revision,
        database_revision_timestamp=datetime_from_wit(
            state_view.context.database_revision_timestamp
        ),
        content_type=state_view.context.content_type,
        content_schema=state_view.context.content_schema,
    )

    sdk_state_view = RenderedStateView(
        context=context,
        content=state_view.content,
        last_modified_revision=state_view.last_modified_revision,
        last_modified_timestamp=datetime_from_wit(state_view.last_modified_timestamp),
    )

    sdk_events = [wit_cloudevent_to_event(e) for e in events]

    return handler(sdk_state_view, sdk_events)
