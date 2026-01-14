"""
Support for event handler functions that process CloudEvents.

This module provides support for:

- Validating the type of incoming CloudEvents
- Parsing/validating the data payload of CloudEvents
- Recording the CloudEvent's metadata in the function's ExecutionInfo result

Handler functions can focus on processing a primary data value without needing
to do their own parsing and validation or event metadata logging/reporting.

To use this module, handler functions are wrapped with this module's
`@cloud_event_handler(...)` decorator. The decorator takes a parser function
that is responsible for validating CloudEvent values, and extracting their data
payload.

Handler functions receive the primary value from the parser function, and also
have access to the the full CloudEvent via the `CLOUD_EVENT_HANDLER_CONTEXT`
`ContextVar`. Metadata from the CloudEvent is automatically included in
`CloudEventHandlerExecutionInfo` values created within the handler function's
scope.
"""

from __future__ import annotations

import functools
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Protocol, cast, overload

from cloudevents.abstract import CloudEvent
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Never, Self, TypeVar

from ucam_faas.contexts import contextual_default_factory, contextvar_activator
from ucam_faas.contextual_handlers import (
    ContextualHandlerFn,
    ContextualHandlerParserFn,
    CreateExecutionInfoFn,
    HandlerFn,
    contextual_handler,
)
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    ExecutionInfo,
)
from ucam_faas.handler_execution import (
    DEFAULT_EXECUTION_RESULT_LOGGER,
    DEFAULT_HTTP_RESPONSE_CREATOR,
    CloudEventFunctionsFrameworkHandlerExecutorFn,
    HandlerExecutionOptions,
    cloud_event_handler_executor,
    get_function_execution_id,
)

CLOUD_EVENT_CONTEXT: ContextVar[CloudEventHandlerContext] = ContextVar(
    f"{__name__}.CLOUD_EVENT_HANDLER_CONTEXT"
)
activate_cloud_event_context = contextvar_activator(CLOUD_EVENT_CONTEXT)

_PydanticModelT = TypeVar("_PydanticModelT", bound=BaseModel)
_T = TypeVar("_T")
_T_con = TypeVar("_T_con", contravariant=True)
_T_co = TypeVar("_T_co", covariant=True)

_InfoT = TypeVar("_InfoT", bound=ExecutionInfo)
_InfoT_co = TypeVar("_InfoT_co", bound=ExecutionInfo, covariant=True)
_DefaultInfoT = TypeVar("_DefaultInfoT", bound=ExecutionInfo)
_DefaultInfoT_co = TypeVar("_DefaultInfoT_co", bound=ExecutionInfo, covariant=True)
_UsedDefaultInfoT_co = TypeVar(
    "_UsedDefaultInfoT_co", bound=ExecutionInfo, covariant=True, default=Never
)

_NoneT = TypeVar("_NoneT", None, Never, default=Never)
_NoneT_co = TypeVar("_NoneT_co", None, Never, covariant=True, default=Never)


@dataclass
class CloudEventHandlerContext:
    cloud_event: CloudEvent
    """The CloudEvent that is being handled."""
    execution_id: str | None
    """The unique identifier for the currently-executing GCP Cloud Run function."""

    handler: CloudEventHandlerAttributes
    """Metadata on the active `@cloud_event_handler`."""


@dataclass
class CloudEventAttributes:
    """
    Attribute metadata from a CloudEvent.

    The fields are named to follow OpenTelemetry Semantic Conventions for
    CloudEvents: https://opentelemetry.io/docs/specs/semconv/attributes-registry/cloudevents/
    """

    event_id: str
    event_source: str
    event_spec_version: str
    event_subject: str | None
    event_type: str
    event_time: str | None  # not currently in opentelemetry semconv

    @classmethod
    def from_cloud_event(cls, cloud_event: CloudEvent) -> Self:
        attributes = cloud_event.get_attributes()
        return cls(
            # Fields accessed without .get() are mandatory
            event_id=attributes["id"],
            event_source=attributes["source"],
            event_spec_version=attributes["specversion"],
            event_subject=attributes.get("subject") or None,
            event_type=attributes["type"],
            event_time=attributes.get("time") or None,
        )


@dataclass
class CloudEventHandlerAttributes:
    input_event_accepted: bool


class CloudEventHandlerExecutionInfo(ExecutionInfo):
    execution_id: str | None = Field(
        default_factory=contextual_default_factory(
            CLOUD_EVENT_CONTEXT, fn=lambda ctx: ctx.execution_id
        )
    )
    cloudevents: CloudEventAttributes = Field(
        default_factory=contextual_default_factory(
            CLOUD_EVENT_CONTEXT,
            fn=lambda ctx: CloudEventAttributes.from_cloud_event(ctx.cloud_event),
        )
    )
    cloud_event_handler: CloudEventHandlerAttributes = Field(
        default_factory=contextual_default_factory(
            CLOUD_EVENT_CONTEXT,
            fn=lambda ctx: ctx.handler,
        )
    )


class CloudEventDataParserFn(Protocol[_T_co]):
    def __call__(self, cloud_event: CloudEvent, /) -> _T_co | ExecutionInfo:
        pass


@dataclass
class CloudEventType(CloudEventDataParserFn[_PydanticModelT]):
    """An `event_data_parser` function for `@cloud_event_handler`.

    The function validates that a CloudEvent has a specific type, and validates
    the event's data by parsing it with a Pydantic model.
    """

    event_type: str
    event_data_model: type[_PydanticModelT]

    def validate_cloud_event(
        self, cloud_event: CloudEvent
    ) -> _PydanticModelT | CloudEventHandlerExecutionInfo:
        try:
            if (t := cloud_event.get_attributes().get("type")) != self.event_type:
                raise ValueError(f"Received CloudEvent with incorrect type: {t!r}")
        except ValueError as e:
            return CloudEventHandlerExecutionInfo(
                execution=AbortedExecutionResult(
                    reason=AbortedExecutionReason.CLOUD_EVENT_TYPE_INCORRECT,
                    exception=e,
                )
            )

        try:
            ce_data = self.event_data_model.model_validate(cloud_event.get_data())
        except ValidationError as e:
            return CloudEventHandlerExecutionInfo(
                execution=AbortedExecutionResult(
                    reason=AbortedExecutionReason.SERVICE_DATA_INVALID, exception=e
                )
            )

        return ce_data

    def __call__(
        self, cloud_event: CloudEvent, /
    ) -> _PydanticModelT | CloudEventHandlerExecutionInfo:
        return self.validate_cloud_event(cloud_event)


# Used as a TypeAlias to shorten the type name of @cloud_event_handler.
class CloudEventHandlerFn(
    ContextualHandlerFn[CloudEvent, _T_con, _InfoT_co, _UsedDefaultInfoT_co, _NoneT_co],
    Protocol[_T_con, _InfoT_co, _UsedDefaultInfoT_co, _NoneT_co],
):
    """The type of the inner handler function created by `@cloud_event_handler`."""


class CloudEventHandlerExecutorFn(
    CloudEventFunctionsFrameworkHandlerExecutorFn[
        CloudEventHandlerFn[_T_con, _InfoT_co, _UsedDefaultInfoT_co, _NoneT_co]
    ],
    Protocol[_T_con, _InfoT_co, _UsedDefaultInfoT_co, _NoneT_co],
):
    """
    The type of the outer `functions_framework` wrapper created by `@cloud_event_handler`.

    The `execute_handler()` method is the handler function that returns `ExecutionInfo`.
    """


class CloudEventHandlerDecoratorFn(Protocol[_T, _DefaultInfoT_co]):
    """The type of the decorator returned by `@cloud_event_handler(...)`"""

    # These overloads are needed to correctly type the return value of
    # the decorated handler function. The return varies according to whether the
    # handler function returns None:
    #
    # - When the handler CAN return None, the return is either the default
    #   ExecutionInfo type or the handler's non-None return type (if any).
    #   returned.
    # - When the handler NEVER returns None, the return is always the
    #   handler's own return type.

    @overload
    def __call__(
        self, event_data_handler: HandlerFn[_T, _InfoT], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT]:
        pass

    @overload
    def __call__(
        self, event_data_handler: HandlerFn[_T, _InfoT | None], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT, _DefaultInfoT_co, None]:
        pass

    def __call__(
        self, event_data_handler: HandlerFn[_T, _InfoT | _NoneT], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT, _DefaultInfoT_co, _NoneT]:
        pass


@overload
def cloud_event_handler(
    *,
    event_data_parser: CloudEventDataParserFn[_T],
    create_default_info: None = None,
    options: HandlerExecutionOptions | None = None,
) -> CloudEventHandlerDecoratorFn[_T, CloudEventHandlerExecutionInfo]:
    pass


@overload
def cloud_event_handler(
    *,
    event_data_parser: CloudEventDataParserFn[_T],
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT],
    options: HandlerExecutionOptions | None = None,
) -> CloudEventHandlerDecoratorFn[_T, _DefaultInfoT]:
    pass


def cloud_event_handler(
    *,
    event_data_parser: CloudEventDataParserFn[_T],
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT] | None = None,
    options: HandlerExecutionOptions | None = None,
) -> CloudEventHandlerDecoratorFn[_T, _DefaultInfoT]:
    """
    Register a function to be called when a CloudEvent needs to be handled.

    Parameters
    ----------
    event_data_parser:
        A function used to parse and validate CloudEvents before calling the
        decorated handler function. The returned value is the value the handler
        function receives.

        If the CloudEvent is not valid (wrong type, invalid data, etc), the
        function must provide an `ExecutionInfo` result instead of a value,
        either by returning it or throwing `ExecutionAbortedException`.
    create_default_info:
        A function used to create an ExecutionInfo value if the decorated
        handler function does not return one.
    options:
        Override the default behaviour for logging the `ExecutionInfo` result,
        and representing the `ExecutionInfo` result as an HTTP response.

    Example
    -------
    First define the data payload of the event you will handle:
    >>> from pydantic import BaseModel
    >>> class GreetingEventData(BaseModel):
    ...     greeting: str

    Second, define the CloudEvent that the data payload is delivered within:
    >>> from ucam_faas import CloudEventType
    >>> parse_greeting_event = CloudEventType(
    ...     event_type="com.example.events.greeting",
    ...     event_data_model=GreetingEventData,
    ... )

    Third, define a function to handle the event. It'll be called automatically
    each time an event is received — as long as the event passes validation
    using your model and event type.
    >>> from ucam_faas import cloud_event_handler
    >>> @cloud_event_handler(event_data_parser=parse_greeting_event)
    ... def handle_greeting(event_data: GreetingEventData):
    ...     print(f"Received greeting: {event_data.greeting!r}")

    The handler function can be executed for testing purposes:
    >>> from ucam_faas.tests.fixtures import make_cloud_event
    >>> exc_info = handle_greeting.execute_for_result(
    ...     make_cloud_event(
    ...         type="com.example.events.greeting",
    ...         source="testing",
    ...         data={"greeting": "Hello World!"}
    ...     ),
    ... )
    Received greeting: 'Hello World!'
    """  # noqa: E501

    @overload
    def cloud_event_handler_decorator(
        event_data_handler: HandlerFn[_T, _InfoT], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT]:
        pass

    @overload
    def cloud_event_handler_decorator(
        event_data_handler: HandlerFn[_T, _InfoT | None], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT, _DefaultInfoT, None]:
        pass

    def cloud_event_handler_decorator(
        event_data_handler: HandlerFn[_T, _InfoT | _NoneT], /
    ) -> CloudEventHandlerExecutorFn[_T, _InfoT, _DefaultInfoT, _NoneT]:
        _options = options or HandlerExecutionOptions()

        # When create_default_info is None or
        # CreateExecutionInfoFn[CloudEventHandlerExecutionInfo],
        # _DefaultInfoT IS CloudEventHandlerExecutionInfo because of the
        # @overloads, so this cast is safe.
        _create_default_info = cast(
            CreateExecutionInfoFn[_DefaultInfoT],
            create_default_info or CloudEventHandlerExecutionInfo.from_context,
        )

        # Wrap our augmented handler to make it suitable for being called by
        # functions_framework as a CloudEvent handler. This deals with logging
        # the ExecutionInfo result, and sending a suitable HTTP response,
        # according to the result.
        @cloud_event_handler_executor(
            create_http_response=_options.make_http_response or DEFAULT_HTTP_RESPONSE_CREATOR,
            log_execution_result=_options.log_execution_result or DEFAULT_EXECUTION_RESULT_LOGGER,
        )
        # Wrap the raw handler function in order to parse the raw CloudEvent
        # to extract the handler's input value, as well as to provide the
        # CloudEvent metadata in the environment via a ContextVar. Also to
        # create a default ExecutionResult value if the handler throws or
        # returns None.
        @contextual_handler(
            parser=contextual_cloud_event_parser(event_data_parser),
            context=activate_cloud_event_context,
            default_info_factory=_create_default_info,
        )
        @functools.wraps(event_data_handler)
        def event_data_handler_executor(event_data: _T, /) -> _InfoT | _NoneT:
            return event_data_handler(event_data)

        assert event_data_handler_executor.__name__ == event_data_handler.__name__
        return event_data_handler_executor

    return cloud_event_handler_decorator


def contextual_cloud_event_parser(
    cloud_event_data_parser: CloudEventDataParserFn[_T_co],
) -> ContextualHandlerParserFn[CloudEvent, _T_co, CloudEventHandlerContext, ExecutionInfo]:
    """Wrap a (CloudEvent) -> T function to be a @contextual_handler() parser.

    The T value returned by the function is the primary value and the CloudEvent
    is in the context value's `cloud_event` attribute.

    The function is run with `CLOUD_EVENT_CONTEXT` active.
    """

    @functools.wraps(cloud_event_data_parser)
    def parse_input(
        cloud_event: CloudEvent, /
    ) -> tuple[_T_co, CloudEventHandlerContext] | ExecutionInfo:
        context = CloudEventHandlerContext(
            cloud_event=cloud_event,
            execution_id=get_function_execution_id(),
            handler=CloudEventHandlerAttributes(input_event_accepted=False),
        )

        with activate_cloud_event_context(context):
            parse_result = cloud_event_data_parser(cloud_event)

        if isinstance(parse_result, ExecutionInfo):
            return parse_result

        context.handler.input_event_accepted = True
        return parse_result, context

    return parse_input
