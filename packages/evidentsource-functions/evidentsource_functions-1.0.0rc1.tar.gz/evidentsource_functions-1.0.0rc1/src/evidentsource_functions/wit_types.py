"""WIT type definitions and conversions.

This module defines Python equivalents of the WIT types from decider.wit
and provides conversion utilities between WIT types and core domain types.

These types are used at the WASM component boundary and are converted
to/from core domain types for user code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from evidentsource_core import (
    AppendCondition,
    BinaryEventData,
    BooleanExtension,
    Event,
    EventAttribute,
    EventSelector,
    EventTypeAttribute,
    EventTypePrefix,
    FlatAndNode,
    FlatEqualsNode,
    FlatOrNode,
    FlatStartsWithNode,
    IntegerExtension,
    ProspectiveEvent,
    StreamAttribute,
    StreamPrefix,
    StringEventData,
    StringExtension,
    SubjectAttribute,
    SubjectPrefix,
)

# =============================================================================
# WIT Datetime
# =============================================================================


@dataclass
class WitDatetime:
    """Datetime representation matching WIT datetime record."""

    seconds: int
    nanoseconds: int

    @classmethod
    def from_datetime(cls, dt: datetime) -> WitDatetime:
        """Convert from Python datetime to WIT datetime."""
        dt = dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)

        return cls(
            seconds=int(dt.timestamp()),
            nanoseconds=dt.microsecond * 1000,
        )

    def to_datetime(self) -> datetime:
        """Convert to Python datetime."""
        return datetime.fromtimestamp(
            self.seconds + self.nanoseconds / 1_000_000_000,
            tz=UTC,
        )


def datetime_from_wit(seconds: int, nanoseconds: int) -> datetime:
    """Convert a WIT-style datetime tuple to Python datetime."""
    return datetime.fromtimestamp(
        seconds + nanoseconds / 1_000_000_000,
        tz=UTC,
    )


def datetime_to_wit(dt: datetime) -> tuple[int, int]:
    """Convert Python datetime to WIT-style datetime tuple."""
    dt = dt.replace(tzinfo=UTC) if dt.tzinfo is None else dt.astimezone(UTC)

    return (int(dt.timestamp()), dt.microsecond * 1000)


# =============================================================================
# WIT CloudEvent Types
# =============================================================================


@dataclass
class WitCloudeventDataBinary:
    """Binary data variant."""

    value: bytes


@dataclass
class WitCloudeventDataString:
    """String data variant."""

    value: str


WitCloudeventData = WitCloudeventDataBinary | WitCloudeventDataString


@dataclass
class WitCloudeventAttributeBoolean:
    """Boolean attribute variant."""

    value: bool


@dataclass
class WitCloudeventAttributeInteger:
    """Integer attribute variant."""

    value: int


@dataclass
class WitCloudeventAttributeString:
    """String attribute variant."""

    value: str


@dataclass
class WitCloudeventAttributeBinary:
    """Binary attribute variant."""

    value: bytes


@dataclass
class WitCloudeventAttributeUri:
    """URI attribute variant."""

    value: str


@dataclass
class WitCloudeventAttributeUriRef:
    """URI reference attribute variant."""

    value: str


@dataclass
class WitCloudeventAttributeTimestamp:
    """Timestamp attribute variant."""

    value: WitDatetime


WitCloudeventAttributeValue = (
    WitCloudeventAttributeBoolean
    | WitCloudeventAttributeInteger
    | WitCloudeventAttributeString
    | WitCloudeventAttributeBinary
    | WitCloudeventAttributeUri
    | WitCloudeventAttributeUriRef
    | WitCloudeventAttributeTimestamp
)


@dataclass
class WitCloudevent:
    """CloudEvent matching WIT cloudevent record."""

    id: str
    source: str
    specversion: str
    type: str
    data: WitCloudeventData | None = None
    attributes: list[tuple[str, WitCloudeventAttributeValue]] = field(default_factory=list)


# =============================================================================
# CloudEvent Conversions
# =============================================================================


def wit_cloudevent_to_event(ce: WitCloudevent) -> Event:
    """Convert a WIT CloudEvent to a domain Event."""
    subject: str | None = None
    time: datetime | None = None
    datacontenttype: str | None = None
    dataschema: str | None = None
    extensions: dict[str, StringExtension | BooleanExtension | IntegerExtension] = {}

    # Process attributes
    for key, attr in ce.attributes:
        if key == "subject" and isinstance(attr, WitCloudeventAttributeString):
            subject = attr.value
        elif key == "time" and isinstance(attr, WitCloudeventAttributeTimestamp):
            time = attr.value.to_datetime()
        elif key == "datacontenttype" and isinstance(attr, WitCloudeventAttributeString):
            datacontenttype = attr.value
        elif key == "dataschema" and isinstance(
            attr, (WitCloudeventAttributeUri, WitCloudeventAttributeUriRef)
        ):
            dataschema = attr.value
        elif isinstance(attr, WitCloudeventAttributeString):
            extensions[key] = StringExtension(attr.value)
        elif isinstance(attr, WitCloudeventAttributeBoolean):
            extensions[key] = BooleanExtension(attr.value)
        elif isinstance(attr, WitCloudeventAttributeInteger):
            extensions[key] = IntegerExtension(attr.value)

    # Handle data
    data: BinaryEventData | StringEventData | None = None
    if ce.data is not None:
        if isinstance(ce.data, WitCloudeventDataBinary):
            data = BinaryEventData(ce.data.value)
        elif isinstance(ce.data, WitCloudeventDataString):
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


def prospective_event_to_wit_cloudevent(event: ProspectiveEvent) -> WitCloudevent:
    """Convert a ProspectiveEvent to a WIT CloudEvent."""
    attributes: list[tuple[str, WitCloudeventAttributeValue]] = []

    if event.subject is not None:
        attributes.append(("subject", WitCloudeventAttributeString(event.subject)))

    if event.time is not None:
        attributes.append(
            ("time", WitCloudeventAttributeTimestamp(WitDatetime.from_datetime(event.time)))
        )

    if event.datacontenttype is not None:
        attributes.append(("datacontenttype", WitCloudeventAttributeString(event.datacontenttype)))

    if event.dataschema is not None:
        attributes.append(("dataschema", WitCloudeventAttributeUri(event.dataschema)))

    # Add extensions
    for key, ext in event.extensions.items():
        if isinstance(ext, StringExtension):
            attributes.append((key, WitCloudeventAttributeString(ext.value)))
        elif isinstance(ext, BooleanExtension):
            attributes.append((key, WitCloudeventAttributeBoolean(ext.value)))
        elif isinstance(ext, IntegerExtension):
            attributes.append((key, WitCloudeventAttributeInteger(ext.value)))

    # Handle data
    data: WitCloudeventData | None = None
    if event.data is not None:
        if isinstance(event.data, BinaryEventData):
            data = WitCloudeventDataBinary(event.data.data)
        elif isinstance(event.data, StringEventData):
            data = WitCloudeventDataString(event.data.data)

    return WitCloudevent(
        id=event.id,
        source=event.stream,  # ProspectiveEvent uses stream as source
        specversion="1.0",
        type=event.event_type,
        data=data,
        attributes=attributes,
    )


# =============================================================================
# WIT Event Selector Types
# =============================================================================


@dataclass
class WitEventAttributeStream:
    """Stream attribute variant."""

    stream: str


@dataclass
class WitEventAttributeSubject:
    """Subject attribute variant (None means no subject)."""

    subject: str | None


@dataclass
class WitEventAttributeEventType:
    """Event type attribute variant."""

    event_type: str


WitEventAttribute = WitEventAttributeStream | WitEventAttributeSubject | WitEventAttributeEventType


@dataclass
class WitEventAttributePrefixStream:
    """Stream prefix variant."""

    stream: str


@dataclass
class WitEventAttributePrefixSubject:
    """Subject prefix variant."""

    subject: str


@dataclass
class WitEventAttributePrefixEventType:
    """Event type prefix variant."""

    event_type: str


WitEventAttributePrefix = (
    WitEventAttributePrefixStream
    | WitEventAttributePrefixSubject
    | WitEventAttributePrefixEventType
)


@dataclass
class WitEventSelectorNodeEquals:
    """Equals node variant."""

    attribute: WitEventAttribute


@dataclass
class WitEventSelectorNodeStartsWith:
    """StartsWith node variant."""

    prefix: WitEventAttributePrefix


@dataclass
class WitEventSelectorNodeAnd:
    """And node variant (indices into node list)."""

    left: int
    right: int


@dataclass
class WitEventSelectorNodeOr:
    """Or node variant (indices into node list)."""

    left: int
    right: int


WitEventSelectorNode = (
    WitEventSelectorNodeEquals
    | WitEventSelectorNodeStartsWith
    | WitEventSelectorNodeAnd
    | WitEventSelectorNodeOr
)


@dataclass
class WitEventSelector:
    """Event selector with flattened node list."""

    nodes: list[WitEventSelectorNode]


# =============================================================================
# Event Selector Conversions
# =============================================================================


def selector_to_wit(selector: EventSelector) -> WitEventSelector:
    """Convert a domain EventSelector to WIT representation."""
    flat_nodes = selector.flatten()
    wit_nodes: list[WitEventSelectorNode] = []

    for node in flat_nodes:
        if isinstance(node, FlatEqualsNode):
            wit_attr = _event_attribute_to_wit(node.attribute)
            wit_nodes.append(WitEventSelectorNodeEquals(wit_attr))
        elif isinstance(node, FlatStartsWithNode):
            wit_prefix = _event_attribute_prefix_to_wit(node.prefix)
            wit_nodes.append(WitEventSelectorNodeStartsWith(wit_prefix))
        elif isinstance(node, FlatAndNode):
            wit_nodes.append(WitEventSelectorNodeAnd(node.left, node.right))
        elif isinstance(node, FlatOrNode):
            wit_nodes.append(WitEventSelectorNodeOr(node.left, node.right))

    return WitEventSelector(nodes=wit_nodes)


def _event_attribute_to_wit(attr: EventAttribute) -> WitEventAttribute:
    """Convert a domain EventAttribute to WIT representation."""
    if isinstance(attr, StreamAttribute):
        return WitEventAttributeStream(str(attr.stream))
    elif isinstance(attr, SubjectAttribute):
        return WitEventAttributeSubject(str(attr.subject) if attr.subject else None)
    elif isinstance(attr, EventTypeAttribute):
        return WitEventAttributeEventType(str(attr.event_type))
    raise TypeError(f"Unknown attribute type: {type(attr)}")


def _event_attribute_prefix_to_wit(
    prefix: StreamPrefix | SubjectPrefix | EventTypePrefix,
) -> WitEventAttributePrefix:
    """Convert a domain EventAttributePrefix to WIT representation."""
    if isinstance(prefix, StreamPrefix):
        return WitEventAttributePrefixStream(str(prefix.stream))
    elif isinstance(prefix, SubjectPrefix):
        return WitEventAttributePrefixSubject(str(prefix.subject))
    elif isinstance(prefix, EventTypePrefix):
        return WitEventAttributePrefixEventType(str(prefix.event_type))
    raise TypeError(f"Unknown prefix type: {type(prefix)}")


# =============================================================================
# WIT Append Condition Types (DCB spec: "Append Condition")
# =============================================================================


@dataclass
class WitAppendConditionMin:
    """Min condition variant."""

    selector: WitEventSelector
    revision: int


@dataclass
class WitAppendConditionMax:
    """Max condition variant."""

    selector: WitEventSelector
    revision: int


@dataclass
class WitAppendConditionRange:
    """Range condition variant."""

    selector: WitEventSelector
    min: int
    max: int


WitAppendCondition = WitAppendConditionMin | WitAppendConditionMax | WitAppendConditionRange


def condition_to_wit(condition: AppendCondition) -> WitAppendCondition:
    """Convert a domain AppendCondition to WIT representation."""
    from evidentsource_core import MaxConstraint, MinConstraint, RangeConstraint

    if isinstance(condition, MinConstraint):
        return WitAppendConditionMin(
            selector=selector_to_wit(condition.selector),
            revision=condition.revision,
        )
    elif isinstance(condition, MaxConstraint):
        return WitAppendConditionMax(
            selector=selector_to_wit(condition.selector),
            revision=condition.revision,
        )
    elif isinstance(condition, RangeConstraint):
        return WitAppendConditionRange(
            selector=selector_to_wit(condition.selector),
            min=condition.range.min,
            max=condition.range.max,
        )
    raise TypeError(f"Unknown condition type: {type(condition)}")
