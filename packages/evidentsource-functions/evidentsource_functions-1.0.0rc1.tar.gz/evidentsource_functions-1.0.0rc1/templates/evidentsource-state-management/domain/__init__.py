"""Domain types for {{project_name}}.

This module contains shared domain types, commands, and events used across
multiple state change components.
"""

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class ExampleCommand:
    """Example command type.

    Replace this with your actual command types.
    """

    id: str
    processing_day: date

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExampleCommand":
        """Create from dictionary (for JSON deserialization)."""
        return cls(
            id=data["id"],
            processing_day=date.fromisoformat(data["processing_day"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (for JSON serialization)."""
        return {
            "id": self.id,
            "processing_day": self.processing_day.isoformat(),
        }


@dataclass
class ExampleEventOccurred:
    """Example domain event.

    Replace this with your actual domain events.
    """

    id: str
    timestamp: date

    @property
    def event_type(self) -> str:
        """Get the event type as a string.

        This should return a reverse-DNS style event type identifier.
        """
        return "com.example.event.occurred"

    @property
    def subject(self) -> str:
        """Get the subject for this event.

        The subject identifies the entity this event is about.
        """
        return self.id

    def stream(self, processing_day: date) -> str:
        """Get the stream for this event.

        The stream is used for partitioning and temporal indexing.
        """
        return f"examples/{processing_day.isoformat()}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExampleEventOccurred":
        """Create from dictionary (for JSON deserialization)."""
        return cls(
            id=data["id"],
            timestamp=date.fromisoformat(data["timestamp"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary (for JSON serialization)."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
        }


__all__ = [
    "ExampleCommand",
    "ExampleEventOccurred",
]
