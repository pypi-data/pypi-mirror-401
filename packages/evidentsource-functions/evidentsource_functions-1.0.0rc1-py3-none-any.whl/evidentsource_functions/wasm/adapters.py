"""Adapters between componentize-py WIT types and SDK domain types.

This module provides adapter classes that bridge the gap between
the componentize-py generated WIT types and the EvidentSource SDK types.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, TypeVar

from componentize_py_types import Err
from evidentsource_core import (
    AppendCondition,
    BinaryEventData,
    BooleanExtension,
    Event,
    IntegerExtension,
    MaxConstraint,
    MinConstraint,
    ProspectiveEvent,
    RangeConstraint,
    StateView,
    StringEventData,
    StringExtension,
)

from evidentsource_functions.errors import StateChangeError, StateChangeErrorKind
from evidentsource_functions.state_change import Command, StateChangeMetadata

# Import generated WIT types for state changes
from evidentsource_functions.wasm.state_change.wit_world.imports import (
    cloudevents as sc_cloudevents,
)
from evidentsource_functions.wasm.state_change.wit_world.imports import (
    state_change_types as sc_types,
)

# Import generated WIT types for state views
from evidentsource_functions.wasm.state_view.wit_world.imports import cloudevents as sv_cloudevents
from evidentsource_functions.wasm.state_view.wit_world.imports import state_view_types as sv_types

# =============================================================================
# Type Conversions - CloudEvents
# =============================================================================


def wit_datetime_to_datetime(dt: sc_cloudevents.Datetime) -> datetime:
    """Convert WIT datetime to Python datetime."""
    return datetime.fromtimestamp(
        dt.seconds + dt.nanoseconds / 1_000_000_000,
        tz=UTC,
    )


def datetime_to_wit_datetime(dt: datetime) -> sc_cloudevents.Datetime:
    """Convert Python datetime to WIT datetime."""
    dt = dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)
    return sc_cloudevents.Datetime(
        seconds=int(dt.timestamp()),
        nanoseconds=dt.microsecond * 1000,
    )


def wit_cloudevent_to_event(ce: sc_cloudevents.Cloudevent) -> Event:
    """Convert a WIT CloudEvent to a domain Event."""
    subject: str | None = None
    time: datetime | None = None
    datacontenttype: str | None = None
    dataschema: str | None = None
    extensions: list[tuple[str, StringExtension | BooleanExtension | IntegerExtension]] = []

    # Process attributes
    for key, attr in ce.attributes:
        if key == "subject" and isinstance(attr, sc_cloudevents.CloudeventAttributeValue_String):
            subject = attr.value
        elif key == "time" and isinstance(attr, sc_cloudevents.CloudeventAttributeValue_Timestamp):
            time = wit_datetime_to_datetime(attr.value)
        elif key == "datacontenttype" and isinstance(
            attr, sc_cloudevents.CloudeventAttributeValue_String
        ):
            datacontenttype = attr.value
        elif key == "dataschema" and isinstance(
            attr,
            (
                sc_cloudevents.CloudeventAttributeValue_Uri,
                sc_cloudevents.CloudeventAttributeValue_UriRef,
            ),
        ):
            dataschema = attr.value
        elif isinstance(attr, sc_cloudevents.CloudeventAttributeValue_String):
            extensions.append((key, StringExtension(attr.value)))
        elif isinstance(attr, sc_cloudevents.CloudeventAttributeValue_Boolean):
            extensions.append((key, BooleanExtension(attr.value)))
        elif isinstance(attr, sc_cloudevents.CloudeventAttributeValue_Integer):
            extensions.append((key, IntegerExtension(attr.value)))

    # Handle data
    data = None
    if ce.data is not None:
        if isinstance(ce.data, sc_cloudevents.CloudeventData_Binary):
            data = BinaryEventData(ce.data.value)
        elif isinstance(ce.data, sc_cloudevents.CloudeventData_String):
            data = StringEventData(ce.data.value)

    return Event(
        id=ce.id,
        source=ce.source,
        event_type=ce.type,
        subject=subject,
        data=data,
        time=time,
        datacontenttype=datacontenttype,
        dataschema=dataschema,
        extensions=extensions,
    )


def prospective_event_to_wit_cloudevent(event: ProspectiveEvent) -> sc_cloudevents.Cloudevent:
    """Convert a ProspectiveEvent to a WIT CloudEvent."""
    attributes: list[tuple[str, sc_cloudevents.CloudeventAttributeValue]] = []

    if event.subject is not None:
        attributes.append(
            ("subject", sc_cloudevents.CloudeventAttributeValue_String(event.subject))
        )

    if event.time is not None:
        attributes.append(
            (
                "time",
                sc_cloudevents.CloudeventAttributeValue_Timestamp(
                    datetime_to_wit_datetime(event.time)
                ),
            )
        )

    if event.datacontenttype is not None:
        attributes.append(
            (
                "datacontenttype",
                sc_cloudevents.CloudeventAttributeValue_String(event.datacontenttype),
            )
        )

    if event.dataschema is not None:
        attributes.append(
            ("dataschema", sc_cloudevents.CloudeventAttributeValue_Uri(event.dataschema))
        )

    # Add extensions
    for key, ext in event.extensions:
        if isinstance(ext, StringExtension):
            attributes.append((key, sc_cloudevents.CloudeventAttributeValue_String(ext.value)))
        elif isinstance(ext, BooleanExtension):
            attributes.append((key, sc_cloudevents.CloudeventAttributeValue_Boolean(ext.value)))
        elif isinstance(ext, IntegerExtension):
            attributes.append((key, sc_cloudevents.CloudeventAttributeValue_Integer(ext.value)))

    # Handle data
    data: sc_cloudevents.CloudeventData | None = None
    if event.data is not None:
        if isinstance(event.data, BinaryEventData):
            data = sc_cloudevents.CloudeventData_Binary(event.data.value)
        elif isinstance(event.data, StringEventData):
            data = sc_cloudevents.CloudeventData_String(event.data.value)

    return sc_cloudevents.Cloudevent(
        id=event.id,
        source=event.stream,
        specversion="1.0",
        type=event.event_type,
        data=data,
        attributes=attributes,
    )


# =============================================================================
# Type Conversions - Constraints
# =============================================================================


def constraint_to_wit(constraint: AppendCondition) -> sc_types.BatchConstraint:
    """Convert a domain BatchConstraint to WIT representation."""
    if isinstance(constraint, MinConstraint):
        return sc_types.BatchConstraint_Min(
            sc_types.BatchConstraintMin(
                selector=selector_to_wit(constraint.selector),
                revision=constraint.revision,
            )
        )
    elif isinstance(constraint, MaxConstraint):
        return sc_types.BatchConstraint_Max(
            sc_types.BatchConstraintMax(
                selector=selector_to_wit(constraint.selector),
                revision=constraint.revision,
            )
        )
    elif isinstance(constraint, RangeConstraint):
        return sc_types.BatchConstraint_Range(
            sc_types.BatchConstraintRange(
                selector=selector_to_wit(constraint.selector),
                min=constraint.range.min,
                max=constraint.range.max,
            )
        )
    raise TypeError(f"Unknown constraint type: {type(constraint)}")


def selector_to_wit(selector) -> sc_types.EventSelector:
    """Convert a domain EventSelector to WIT representation."""
    from evidentsource_core import (
        EventTypeAttribute,
        EventTypePrefix,
        FlatAndNode,
        FlatEqualsNode,
        FlatOrNode,
        FlatStartsWithNode,
        StreamAttribute,
        StreamPrefix,
        SubjectAttribute,
        SubjectPrefix,
    )

    flat_nodes = selector.flatten()
    wit_nodes: list[sc_types.EventSelectorNode] = []

    for node in flat_nodes:
        if isinstance(node, FlatEqualsNode):
            attr = node.attribute
            if isinstance(attr, StreamAttribute):
                wit_attr = sc_types.EventAttribute_Stream(str(attr.stream))
            elif isinstance(attr, SubjectAttribute):
                wit_attr = sc_types.EventAttribute_Subject(
                    str(attr.subject) if attr.subject else None
                )
            elif isinstance(attr, EventTypeAttribute):
                wit_attr = sc_types.EventAttribute_EventType(str(attr.event_type))
            else:
                raise TypeError(f"Unknown attribute type: {type(attr)}")
            wit_nodes.append(sc_types.EventSelectorNode_Equals(wit_attr))
        elif isinstance(node, FlatStartsWithNode):
            prefix = node.prefix
            if isinstance(prefix, StreamPrefix):
                wit_prefix = sc_types.EventAttributePrefix_Stream(str(prefix.stream))
            elif isinstance(prefix, SubjectPrefix):
                wit_prefix = sc_types.EventAttributePrefix_Subject(str(prefix.subject))
            elif isinstance(prefix, EventTypePrefix):
                wit_prefix = sc_types.EventAttributePrefix_EventType(str(prefix.event_type))
            else:
                raise TypeError(f"Unknown prefix type: {type(prefix)}")
            wit_nodes.append(sc_types.EventSelectorNode_StartsWith(wit_prefix))
        elif isinstance(node, FlatAndNode):
            wit_nodes.append(sc_types.EventSelectorNode_And((node.left, node.right)))
        elif isinstance(node, FlatOrNode):
            wit_nodes.append(sc_types.EventSelectorNode_Or((node.left, node.right)))

    return sc_types.EventSelector(nodes=wit_nodes)


# =============================================================================
# Type Conversions - Command and Metadata
# =============================================================================


def wit_command_to_sdk(cmd: sc_types.Command) -> Command:
    """Convert WIT Command to SDK Command."""
    return Command(
        body=cmd.body,
        content_type=cmd.content_type,
        content_schema=cmd.content_schema,
    )


def wit_metadata_to_sdk(meta: sc_types.StateChangeMetadata) -> StateChangeMetadata:
    """Convert WIT StateChangeMetadata to SDK StateChangeMetadata."""
    return StateChangeMetadata(
        state_change_name=meta.state_change_name,
        state_change_version=meta.state_change_version,
        last_seen_revision=meta.last_seen_revision,
        command_received_at=wit_datetime_to_datetime(meta.command_received_at),
        command_headers=list(meta.command_headers),
    )


def sdk_error_to_wit(error: StateChangeError) -> sc_types.StateChangeError:
    """Convert SDK StateChangeError to WIT StateChangeError."""
    if error.kind == StateChangeErrorKind.VALIDATION:
        return sc_types.StateChangeError_Validation(error.message)
    elif error.kind == StateChangeErrorKind.CONFLICT:
        return sc_types.StateChangeError_Conflict(error.message)
    elif error.kind == StateChangeErrorKind.NOT_FOUND:
        return sc_types.StateChangeError_NotFound(error.message)
    elif error.kind == StateChangeErrorKind.UNAUTHORIZED:
        return sc_types.StateChangeError_Unauthorized(error.message)
    else:
        return sc_types.StateChangeError_Internal(error.message)


# =============================================================================
# Database Wrapper
# =============================================================================


class DatabaseWrapper:
    """Wraps a WIT Database resource to provide SDK-compatible interface."""

    def __init__(self, db: sc_types.Database):
        self._db = db

    @property
    def name(self) -> str:
        return self._db.name()

    @property
    def revision(self) -> int:
        return self._db.revision()

    @property
    def revision_timestamp(self) -> datetime:
        return wit_datetime_to_datetime(self._db.revision_timestamp())

    @property
    def effective_timestamp(self) -> datetime | None:
        ts = self._db.effective_timestamp()
        return wit_datetime_to_datetime(ts) if ts else None

    def at_effective_timestamp(self, timestamp: datetime) -> DatabaseWrapper:
        wit_ts = datetime_to_wit_datetime(timestamp)
        return DatabaseWrapper(self._db.at_effective_timestamp(wit_ts))

    def query_events(self, selector) -> list[Event]:
        """Query events matching the selector."""
        wit_selector = selector_to_wit(selector)
        query = sc_types.DatabaseQuery(
            selector=wit_selector,
            range=None,
            direction=sc_types.QueryDirection.FORWARD,
            limit=None,
        )
        wit_events = self._db.query_events(query)
        return [wit_cloudevent_to_event(e) for e in wit_events]

    def view_state(
        self,
        name: str,
        version: int,
        parameters: list[tuple[str, Any]] | None = None,
    ) -> StateView | None:
        """Fetch a state view."""
        wit_params: list[tuple[str, sc_types.EventAttribute]] = []
        if parameters:
            for key, value in parameters:
                if isinstance(value, str):
                    wit_params.append((key, sc_types.EventAttribute_Subject(value)))
                # Add other parameter type conversions as needed

        result = self._db.view_state(name, version, wit_params)
        if result is None:
            return None

        return StateView(
            content=result.content,
            content_type=result.context.content_type,
        )


# =============================================================================
# State Change Adapter
# =============================================================================


T = TypeVar("T")


class StateChangeAdapter:
    """Adapter that creates a WitWorld implementation for state changes.

    This adapter bridges the gap between the componentize-py generated
    WitWorld interface and user-defined state change logic using SDK types.

    Example:
        ```python
        from evidentsource_functions.wasm import StateChangeAdapter

        @dataclass
        class MyCommand:
            value: str

            @classmethod
            def from_dict(cls, data: dict) -> "MyCommand":
                return cls(value=data["value"])

        def decide(db, command: MyCommand, metadata):
            # Your business logic here
            return (events, constraints)

        # Create the WitWorld implementation
        class WitWorld(StateChangeAdapter):
            command_type = MyCommand
            decide_func = staticmethod(decide)
        ```
    """

    command_type: type = None  # Override in subclass
    decide_func: Callable = None  # Override in subclass

    def decide(
        self,
        db: sc_types.Database,
        command: sc_types.Command,
        metadata: sc_types.StateChangeMetadata,
    ) -> tuple[list[sc_cloudevents.Cloudevent], list[sc_types.BatchConstraint]]:
        """Implement the WIT decide function."""
        try:
            # Convert WIT types to SDK types
            sdk_command = wit_command_to_sdk(command)
            sdk_metadata = wit_metadata_to_sdk(metadata)
            db_wrapper = DatabaseWrapper(db)

            # Parse command
            data = sdk_command.parse_json()
            typed_command = self.command_type.from_dict(data)

            # Call user's decide function
            events, constraints = self.decide_func(db_wrapper, typed_command, sdk_metadata)

            # Convert results back to WIT types
            wit_events = [prospective_event_to_wit_cloudevent(e) for e in events]
            wit_constraints = [constraint_to_wit(c) for c in constraints]

            return (wit_events, wit_constraints)

        except StateChangeError as e:
            # Re-raise as WIT error wrapped in Err for componentize-py
            raise Err(sdk_error_to_wit(e)) from e
        except Exception as e:
            # Wrap unexpected errors in Err for componentize-py
            raise Err(sc_types.StateChangeError_Internal(str(e))) from e


# =============================================================================
# State View Adapter
# =============================================================================


def sv_wit_cloudevent_to_event(ce: sv_cloudevents.Cloudevent) -> Event:
    """Convert a state-view WIT CloudEvent to a domain Event."""
    subject: str | None = None
    time: datetime | None = None
    datacontenttype: str | None = None
    dataschema: str | None = None
    extensions: list[tuple[str, StringExtension | BooleanExtension | IntegerExtension]] = []

    # Process attributes
    for key, attr in ce.attributes:
        if key == "subject" and isinstance(attr, sv_cloudevents.CloudeventAttributeValue_String):
            subject = attr.value
        elif key == "time" and isinstance(attr, sv_cloudevents.CloudeventAttributeValue_Timestamp):
            time = datetime.fromtimestamp(
                attr.value.seconds + attr.value.nanoseconds / 1_000_000_000,
                tz=UTC,
            )
        elif key == "datacontenttype" and isinstance(
            attr, sv_cloudevents.CloudeventAttributeValue_String
        ):
            datacontenttype = attr.value
        elif key == "dataschema" and isinstance(
            attr,
            (
                sv_cloudevents.CloudeventAttributeValue_Uri,
                sv_cloudevents.CloudeventAttributeValue_UriRef,
            ),
        ):
            dataschema = attr.value
        elif isinstance(attr, sv_cloudevents.CloudeventAttributeValue_String):
            extensions.append((key, StringExtension(attr.value)))
        elif isinstance(attr, sv_cloudevents.CloudeventAttributeValue_Boolean):
            extensions.append((key, BooleanExtension(attr.value)))
        elif isinstance(attr, sv_cloudevents.CloudeventAttributeValue_Integer):
            extensions.append((key, IntegerExtension(attr.value)))

    # Handle data
    data = None
    if ce.data is not None:
        if isinstance(ce.data, sv_cloudevents.CloudeventData_Binary):
            data = BinaryEventData(ce.data.value)
        elif isinstance(ce.data, sv_cloudevents.CloudeventData_String):
            data = StringEventData(ce.data.value)

    return Event(
        id=ce.id,
        source=ce.source,
        event_type=ce.type,
        subject=subject,
        data=data,
        time=time,
        datacontenttype=datacontenttype,
        dataschema=dataschema,
        extensions=extensions,
    )


class StateViewAdapter:
    """Adapter that creates a WitWorld implementation for state views.

    This adapter bridges the gap between the componentize-py generated
    WitWorld interface and user-defined state view logic using SDK types.

    Example:
        ```python
        from dataclasses import dataclass
        from evidentsource_functions.wasm import StateViewAdapter
        from evidentsource_functions import StateViewBase
        import json

        @dataclass
        class TodoList(StateViewBase):
            items: list = None

            def __post_init__(self):
                if self.items is None:
                    self.items = []

            def evolve_event(self, event):
                if event.event_type == "todo.created":
                    data = json.loads(event.data_as_string())
                    self.items.append(data)

            def to_dict(self):
                return {"items": self.items}

            @classmethod
            def from_dict(cls, data):
                return cls(items=data.get("items", []))

        class WitWorld(StateViewAdapter):
            state_view_type = TodoList
        ```
    """

    state_view_type: type = None  # Override in subclass

    def evolve(
        self,
        state_view: sv_types.RenderedStateView,
        events: list[sv_cloudevents.Cloudevent],
    ) -> bytes | None:
        """Implement the WIT evolve function."""
        import json

        # Parse existing state or create new
        if state_view.content:
            data = json.loads(state_view.content.decode("utf-8"))
            state = self.state_view_type.from_dict(data)
        else:
            state = self.state_view_type()

        # Apply events
        for wit_event in events:
            event = sv_wit_cloudevent_to_event(wit_event)
            state.evolve_event(event)

        # Serialize result
        result = state.to_dict()
        return json.dumps(result).encode("utf-8")
