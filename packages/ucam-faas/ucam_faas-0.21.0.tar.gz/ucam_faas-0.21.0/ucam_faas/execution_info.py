from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Self, TypeAlias

from ucam_faas.pydantic import SerialisableException


class ExecutionStatus(Enum):
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"


class AbortedExecutionReason(Enum):
    FUNCTION_ABORTED = "ucam_faas.function-aborted"
    """The handler function threw an Exception, or returned an aborted ExecutionInfo."""
    CLOUD_EVENT_TYPE_INCORRECT = "ucam_faas.cloud-event-type-incorrect"
    """The CloudEvent sent to the function was not a type expected by the function."""
    SERVICE_DATA_INVALID = "ucam_faas.service-data-invalid"
    """The service-specific event metadata in the CloudEvent's data payload was not
    structured correctly for the CloudEvent type.
    """
    USER_DATA_INVALID = "ucam_faas.user-data-invalid"
    """The application-specific, end-user-supplied data in the service-specific
    event's data payload was rejected by the `message_validator`.
    """


@dataclass
class CompletedExecutionResult:
    """The function executed and returned normally."""

    status: Literal[ExecutionStatus.COMPLETED] = ExecutionStatus.COMPLETED
    duration_seconds: float | None = None


@dataclass
class AbortedExecutionResult:
    """The function was aborted before completing its work."""

    reason: AbortedExecutionReason | str
    status: Literal[ExecutionStatus.ABORTED] = ExecutionStatus.ABORTED
    exception: SerialisableException | None = None
    """The Exception that aborted the function execution.

    Can be None if the function explicitly returned an aborted ExecutionInfo
    value without raising, in which case the value should contain properties to
    describe what happened.
    """
    duration_seconds: float | None = None


ExecutionResult: TypeAlias = Union[CompletedExecutionResult, AbortedExecutionResult]


class ExecutionInfo(BaseModel):
    """Data to inform observers of the outcome of a function execution.

    - Handlers can return subclasses of this type, with appropriate fields to
      describe the result or side-effects of their function.
    - `ucam_faas` serializes values as JSON and logs them to provide operational
      observability of the behaviour of deployed functions.
    - Unit tests can access the un-serialized values to make assertions about
      the behaviour of a handler, given an input event object.
      - Use the `.execute(cloud_event)` method on the function decorated with
        `@message_handler(...)` to execute the function and return your info.
    - By providing plenty of info on your handler's outcome, you can improve
      both runtime observability and development testability in one go.
    """

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    execution: ExecutionResult = Field(default_factory=CompletedExecutionResult)

    @classmethod
    def from_context(cls, *, execution: ExecutionResult) -> Self:
        """
        Create an instance of this ExecutionInfo type from the executing function's context.

        The ExecutionInfo class does not have any contextual fields, but
        subclasses should use `Field(default_factory=contextual_default_factory(...))`
        to automatically populate fields from `ContextVar`s they are expected to
        be created under.

        Notes
        -----
        In theory this shouldn't need to exist, as a reference to the class
        itself acts as a function that creates an instance with an `execution`,
        but Python type checkers seem to not match overloaded functions when a
        model class constructor is used as a function reference. Perhaps because
        of the Pydantic mypy plugin generating the constructor signature.
        """
        return cls(execution=execution)
