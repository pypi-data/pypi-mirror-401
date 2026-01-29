"""Error types for SDK components.

This module provides error types that match the WIT state-change-error
variant, allowing state changes to return structured errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StateChangeErrorKind(Enum):
    """Error kinds matching WIT state-change-error variant."""

    VALIDATION = "validation"
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    INTERNAL = "internal"


@dataclass
class StateChangeError(Exception):
    """Error returned from state change execution.

    This error type maps to the WIT state-change-error variant and can
    be used to return structured errors from state change functions.

    Example:
        ```python
        def decide(db, command, metadata):
            if command.amount <= 0:
                raise StateChangeError.validation("Amount must be positive")

            account = db.view_state("account", 1, [])
            if account is None:
                raise StateChangeError.not_found(f"Account {command.account_id} not found")

            if account.balance < command.amount:
                raise StateChangeError.conflict("Insufficient balance")

            # ... process command
        ```
    """

    kind: StateChangeErrorKind
    message: str

    def __str__(self) -> str:
        return f"{self.kind.value}: {self.message}"

    @classmethod
    def validation(cls, message: str) -> StateChangeError:
        """Create a validation error.

        Use this for input validation failures, malformed commands,
        or constraint violations.
        """
        return cls(StateChangeErrorKind.VALIDATION, message)

    @classmethod
    def conflict(cls, message: str) -> StateChangeError:
        """Create a conflict error.

        Use this for optimistic concurrency conflicts, insufficient
        resources, or business rule violations.
        """
        return cls(StateChangeErrorKind.CONFLICT, message)

    @classmethod
    def not_found(cls, message: str) -> StateChangeError:
        """Create a not found error.

        Use this when a required entity doesn't exist.
        """
        return cls(StateChangeErrorKind.NOT_FOUND, message)

    @classmethod
    def unauthorized(cls, message: str) -> StateChangeError:
        """Create an unauthorized error.

        Use this for permission/authorization failures.
        """
        return cls(StateChangeErrorKind.UNAUTHORIZED, message)

    @classmethod
    def internal(cls, message: str) -> StateChangeError:
        """Create an internal error.

        Use this for unexpected errors that should not normally occur.
        """
        return cls(StateChangeErrorKind.INTERNAL, message)


@dataclass
class DatabaseAccessError(Exception):
    """Error type for database operations within SDK components."""

    message: str

    def __str__(self) -> str:
        return self.message

    @classmethod
    def query_failed(cls, message: str) -> DatabaseAccessError:
        """Create a query failed error."""
        return cls(f"Query failed: {message}")

    @classmethod
    def state_view_not_found(cls) -> DatabaseAccessError:
        """Create a state view not found error."""
        return cls("State view not found")

    @classmethod
    def invalid_revision(cls, message: str) -> DatabaseAccessError:
        """Create an invalid revision error."""
        return cls(f"Invalid revision: {message}")

    @classmethod
    def conversion_error(cls, message: str) -> DatabaseAccessError:
        """Create a conversion error."""
        return cls(f"Conversion error: {message}")


class ContentNegotiationError(Exception):
    """Error during content negotiation (JSON parsing/serialization)."""

    pass


class NoBody(ContentNegotiationError):
    """Command body is required but was not provided."""

    def __init__(self) -> None:
        super().__init__("Command body is required")


class UnsupportedContentType(ContentNegotiationError):
    """Content type is not supported."""

    def __init__(self, content_type: str) -> None:
        super().__init__(f"Unsupported content type: {content_type}")
        self.content_type = content_type


class DeserializationFailed(ContentNegotiationError):
    """Failed to deserialize the command body."""

    def __init__(self, message: str) -> None:
        super().__init__(f"Deserialization failed: {message}")
