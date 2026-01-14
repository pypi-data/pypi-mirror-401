"""
This module's handler executor functions provide the interface to connect
`functions_framework` to the `ucam_faas` handler functions.

The handler executor functions are the base level handlers to layer
higher-level, (more specific) handlers on top of. This module's handlers support
reporting function results from ExecutionInfo objects. The results are made
available in 3 ways:

- As HTTP responses to the HTTP request that triggered the event handler
- As structured (JSON) log records
- As the original ExecutionInfo value for unit tests (tests need not
  mock or use a full functions_framework server to run a function to
  test it)
"""

from __future__ import annotations

import http.client
import logging
import time
import types
from abc import abstractmethod
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Callable, Final, Generic, Mapping, Protocol

import flask
import flask.typing
import functions_framework
from cloudevents.abstract import CloudEvent
from flask import Response
from functions_framework.execution_id import EXECUTION_ID_REQUEST_HEADER
from pydantic_core import PydanticSerializationError
from structlog.typing import FilteringBoundLogger
from typing_extensions import ParamSpec, TypeVar
from werkzeug.exceptions import HTTPException

from ucam_faas._logging import flatten_json, get_structlog_logger
from ucam_faas.exceptions import ExecutionAbortedException
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    ExecutionInfo,
    ExecutionStatus,
)


class CreateExecutionResultHttpResponseFn(Protocol):
    def __call__(self, execution_info: ExecutionInfo, /) -> Response | None:
        pass


@dataclass
class HttpResponseCreator(CreateExecutionResultHttpResponseFn):
    """
    Create minimalistic HTTP responses to communicate execution result.

    Functions are triggered by an HTTP request containing a `CloudEvent`. We
    need to send an HTTP response that communicates whether our function handled
    the event successfully, or failed in some way.

    It's expected that the HTTP response is only used to indicate that the
    function:

    - did not complete normally, and should be retried
    - was invoked with invalid/incorrect event data
    - completed successfully

    These use-cases should only require setting a status code. To help humans
    with debugging, we also send a short prose description of execution result,
    as a plain-text message in the response body.
    """

    @dataclass
    class ResponseFields:
        status_code: int
        message: str

    responses: Mapping[AbortedExecutionReason | str, ResponseFields]

    def get_unknown_reason_response(self, execution_info: ExecutionInfo) -> ResponseFields:
        return HttpResponseCreator.ResponseFields(
            status_code=http.client.INTERNAL_SERVER_ERROR,
            message="Failed to handle event for unknown reason",
        )

    def __call__(self, execution_info: ExecutionInfo) -> Response | None:
        if execution_info.execution.status is ExecutionStatus.COMPLETED:
            return None  # default successful response

        response_fields = self.responses.get(
            execution_info.execution.reason
        ) or self.get_unknown_reason_response(execution_info)

        return Response(
            response=response_fields.message,
            content_type="text/plain",
            status=response_fields.status_code,
        )


DEFAULT_HTTP_RESPONSE_CREATOR = HttpResponseCreator(
    responses={
        AbortedExecutionReason.FUNCTION_ABORTED: HttpResponseCreator.ResponseFields(
            status_code=http.client.INTERNAL_SERVER_ERROR,
            message="An error occurred while handling the CloudEvent",
        ),
        AbortedExecutionReason.CLOUD_EVENT_TYPE_INCORRECT: HttpResponseCreator.ResponseFields(
            status_code=http.client.BAD_REQUEST,
            message="The CloudEvent sent to the function was not a type expected by the function.",
        ),
        AbortedExecutionReason.SERVICE_DATA_INVALID: HttpResponseCreator.ResponseFields(
            status_code=http.client.BAD_REQUEST,
            message="The service-specific event metadata in the CloudEvent's data "
            "payload was not structured correctly for the CloudEvent type.",
        ),
        AbortedExecutionReason.USER_DATA_INVALID: HttpResponseCreator.ResponseFields(
            status_code=http.client.BAD_REQUEST,
            message="The application-specific, end-user-supplied data in the "
            "service-specific event's data payload was not valid.",
        ),
    }
)


class ExecutionResultLoggerFn(Protocol):
    def __call__(self, execution_info: ExecutionInfo, /) -> None:
        pass


class JsonRepresentation(Enum):
    NARROW_DEEP = "deep"
    """
    JSON objects and arrays can be nested arbitrarily.

    For example: `{"foo": {"bar": true}, "baz": false}`
    """
    WIDE_FLAT = "wide"
    """
    JSON is transformed into a single wide object containing all the values.

    Each value's property is its dot-separated path in the original JSON.

    For example: `{"foo.bar": true, "baz": false}`
    """


@dataclass
class StructlogJsonExecutionResultLogger(ExecutionResultLoggerFn):
    """
    Record function execution results as structured JSON log events with structlog.
    """

    json_representation: JsonRepresentation = JsonRepresentation.NARROW_DEEP
    logger: FilteringBoundLogger = field(default_factory=get_structlog_logger)

    EVENT_NAME_ABORTED: Final[str] = "ucam_faas_function_aborted"
    EVENT_NAME_COMPLETED: Final[str] = "ucam_faas_function_completed"

    def get_result_json(self, execution_info: ExecutionInfo) -> dict[str, object]:
        try:
            nested_result_json = execution_info.model_dump(mode="json")
        except PydanticSerializationError:
            self.logger.exception("execution_info_json_serialisation_failed")
            raise

        if self.json_representation is JsonRepresentation.NARROW_DEEP:
            return nested_result_json

        return flatten_json(nested_result_json)

    def send_result_json(
        self, execution_status: ExecutionStatus, result_json: dict[str, object]
    ) -> None:
        level, event_name = (
            (logging.ERROR, self.EVENT_NAME_ABORTED)
            if execution_status is ExecutionStatus.ABORTED
            else (logging.INFO, self.EVENT_NAME_COMPLETED)
        )

        # level and event last to prevent dynamic JSON properties overriding them
        self.logger.log(**result_json, level=level, event=event_name)

    def __call__(self, execution_info: ExecutionInfo) -> None:
        self.send_result_json(
            execution_info.execution.status, result_json=self.get_result_json(execution_info)
        )


DEFAULT_EXECUTION_RESULT_LOGGER = StructlogJsonExecutionResultLogger()


@dataclass
class HandlerExecutionOptions:
    log_execution_result: ExecutionResultLoggerFn | None = None
    make_http_response: CreateExecutionResultHttpResponseFn | None = None


_P = ParamSpec("_P")
_HttpResponseT = TypeVar("_HttpResponseT")


@dataclass
class FunctionsFrameworkHandlerExecutor(Generic[_P, _HttpResponseT]):
    """
    A generic `functions_framework` event handler that uses `ExecutionInfo` to
    report results.

    When called with an event, this calls its event-handling function, which
    returns an ExecutionInfo or raises an ExecutionAbortedError, both of which
    result in an ExecutionInfo value.

    The handler is responsible for logging the result of the execution,
    and creating an HTTP response in a manner compatible with being called as a
    functions_framework event handler.
    """

    log_execution_result: ExecutionResultLoggerFn
    create_http_response: CreateExecutionResultHttpResponseFn
    register: InitVar[bool]
    """Register this function with a `@functions_framework.*` handler decorator.

    If this is false, `functions_framework` will not be aware of the instance
    unless it's explicitly registered by the caller.
    """

    def __post_init__(self, register: bool) -> None:
        if register:
            # functions_framework decorators (like @cloud_event) register metadata
            # to make functions available as event handlers, but the decorator's
            # return value is not significant, as they just wrap the input with an
            # identity function. So it's fine to ignore the return value of the
            # decorator, and call us directly. The name of the function is used
            # to uniquely identify it and resolve it from a module.
            assert self.__name__ == self.execute.__name__
            self.register_with_functions_framework()  # nosemgrep: bandit.B101

    @abstractmethod
    def register_with_functions_framework(self) -> None:
        pass

    @abstractmethod
    def send_http_response(self, response: flask.Response | None) -> _HttpResponseT:
        pass

    if TYPE_CHECKING:

        @property
        @abstractmethod
        def execute(self) -> Callable[_P, ExecutionInfo]:
            ...

    def execute_for_result(self, *args: _P.args, **kwargs: _P.kwargs) -> ExecutionInfo:
        """
        Call the handler function and return its `ExecutionInfo`.

        The handler function is called in the same way as a real call, except no
        HTTP response is sent. Timing and result logging is enabled.
        """
        start_time_seconds = time.perf_counter()

        # We need to ensure we always catch and handle exceptions with
        # ExecutionAbortedException, re-throwing if required. Or maybe we do
        # this logging within the call().
        # Middle ground: catch within the call, but do side-effect logging and
        # HTTP response outside the call.
        # (This is now what we're dong.)

        execution_info: ExecutionInfo
        try:
            execution_info = self.execute(*args, **kwargs)
        except ExecutionAbortedException as e:
            execution_info = e.execution_info
        # The handler is expected to be responsible for catching other
        # exceptions and re-throwing them, wrapped in ExecutionAbortedException
        # in order to communicate an execution_info.

        execution_info.execution.duration_seconds = time.perf_counter() - start_time_seconds

        self.log_execution_result(execution_info)

        return execution_info

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _HttpResponseT:
        execution_info = self.execute_for_result(*args, **kwargs)
        response = self.create_http_response(execution_info)
        return self.send_http_response(response)

    # @functions_framework.cloud_event() decorator registers metadata using the
    # __name__ of the decorated function, so we need to preserve the name of the
    # message_handler, so that our user can use the name of their function as
    # its identifier when configuring/deploying their cloud function.
    @property
    def __name__(self) -> str:
        return self.execute.__name__

    @property  # type: ignore[misc]
    def __class__(self) -> type[types.FunctionType]:  # type: ignore[override]
        # functions_framework is over-zealous with runtime type checking, it
        # requires that registered functions are instances of types.FunctionType,
        # not just that they are `callable()`. To work around this, we falsely
        # report our executor to be a FunctionType subclass by reporting our
        # instances' __class__ is types.FunctionType.
        return types.FunctionType


_CloudEventHandlerT = TypeVar("_CloudEventHandlerT", bound=Callable[[CloudEvent], ExecutionInfo])
_CloudEventHandlerT_co = TypeVar(
    "_CloudEventHandlerT_co", bound=Callable[[CloudEvent], ExecutionInfo], covariant=True
)


class CloudEventFunctionsFrameworkHandlerExecutorFn(Protocol[_CloudEventHandlerT_co]):
    def __call__(self, cloud_event: CloudEvent) -> None:
        pass

    if TYPE_CHECKING:

        @property
        def __name__(self) -> str:
            pass

        @property
        def execute(self) -> _CloudEventHandlerT_co:
            """
            Call the handler function and return its `ExecutionInfo`.

            The normal post-handler steps of logging the result and sending an
            HTTP response are not performed.
            """

        def execute_for_result(self, cloud_event: CloudEvent) -> ExecutionInfo:
            """
            Call the handler function and return its `ExecutionInfo`.

            The handler function is called in the same way as a real call, except no
            HTTP response is sent. Timing and result logging is enabled.
            """


def cloud_event_handler_executor(
    *,
    log_execution_result: ExecutionResultLoggerFn,
    create_http_response: CreateExecutionResultHttpResponseFn,
) -> Callable[
    [_CloudEventHandlerT], CloudEventFunctionsFrameworkHandlerExecutorFn[_CloudEventHandlerT]
]:
    def cloud_event_handler_executor_decorator(
        handler: _CloudEventHandlerT, /
    ) -> CloudEventFunctionsFrameworkHandlerExecutorFn[_CloudEventHandlerT]:
        decorated: CloudEventFunctionsFrameworkHandlerExecutorFn[
            _CloudEventHandlerT
        ] = CloudEventFunctionsFrameworkHandlerExecutor(
            log_execution_result=log_execution_result,
            create_http_response=create_http_response,
            register=True,
            execute=handler,
        )
        return decorated

    return cloud_event_handler_executor_decorator


@dataclass
class CloudEventFunctionsFrameworkHandlerExecutor(
    FunctionsFrameworkHandlerExecutor[[CloudEvent], None],
    CloudEventFunctionsFrameworkHandlerExecutorFn[_CloudEventHandlerT],
    Generic[_CloudEventHandlerT],
):
    """
    A generic `@functions_framework.cloud_event` event handler that uses
    `ExecutionInfo` to report results.
    """

    execute: _CloudEventHandlerT

    def register_with_functions_framework(self) -> None:
        functions_framework.cloud_event(self)

    def send_http_response(self, response: flask.Response | None) -> None:
        if response is not None:
            raise HTTPException(response=response)


_HttpHandlerT = TypeVar("_HttpHandlerT", bound=Callable[[flask.Request], ExecutionInfo])
_HttpHandlerT_co = TypeVar(
    "_HttpHandlerT_co", bound=Callable[[flask.Request], ExecutionInfo], covariant=True
)


class HttpFunctionsFrameworkHandlerExecutorFn(Protocol[_HttpHandlerT_co]):
    def __call__(self, request: flask.Request) -> flask.typing.ResponseReturnValue:
        pass

    if TYPE_CHECKING:

        @property
        def __name__(self) -> str:
            pass

        @property
        def execute(self) -> _HttpHandlerT_co:
            """
            Call the handler function and return its `ExecutionInfo`.

            The normal post-handler steps of logging the result and sending an
            HTTP response are not performed.
            """

        def execute_for_result(self, request: flask.Request) -> ExecutionInfo:
            """
            Call the handler function and return its `ExecutionInfo`.

            The handler function is called in the same way as a real call, except no
            HTTP response is sent. Timing and result logging is enabled.
            """


@dataclass
class HttpFunctionsFrameworkHandlerExecutor(
    FunctionsFrameworkHandlerExecutor[[flask.Request], flask.typing.ResponseReturnValue],
    HttpFunctionsFrameworkHandlerExecutorFn[_HttpHandlerT],
    Generic[_HttpHandlerT],
):
    """
    A generic `@functions_framework.http` event handler that uses `ExecutionInfo`
    to report results.

    The handler is triggered by an arbitrary HTTP request, rather than a specific
    CloudEvent payload. Unlike a conventional HTTP API server, the handler is
    expected to be executed primarily for its side-effect (handling an event),
    and its HTTP response is not expected to represent an HTTP resource, rather
    it should only indicate success or failure in handling the request.

    A typical use-case would be to receive an HTTP web hook notification request,
    in which the web hook sender may retry failed requests, but does not expect
    to receive structured data in response.

    Note
    ----
    This exists as a proof-of-concept to ensure the
    `FunctionsFrameworkHandlerExecutor` is able to support use cases other than
    `functions_framework.cloud_event()`. There's no use-friendly decorator to
    register HTTP event handlers at the moment.
    """

    execute: _HttpHandlerT

    def register_with_functions_framework(self) -> None:
        functions_framework.http(self)

    def send_http_response(
        self, response: flask.Response | None
    ) -> flask.typing.ResponseReturnValue:
        if response is not None:
            return response
        return flask.Response()


def get_function_execution_id() -> str | None:
    """
    Get the unique identifier for the currently-executing GCP Cloud Run function.

    Notes
    -----
    See `functions_framework.execution_id` module. `functions_framework` always
    generates a value if one isn't set, but it should be provided by Cloud Run
    in Cloud Run deployments.
    """
    if flask.has_request_context():
        return flask.request.headers.get(EXECUTION_ID_REQUEST_HEADER) or None
    return None
