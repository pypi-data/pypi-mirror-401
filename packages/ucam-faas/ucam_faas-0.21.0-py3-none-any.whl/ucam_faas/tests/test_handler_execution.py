from __future__ import annotations

import http.client
import types
from typing import Final, Generator, Protocol
from unittest import mock
from unittest.mock import ANY, Mock

import flask
import pytest
import werkzeug.exceptions
from cloudevents.abstract import CloudEvent
from functions_framework.execution_id import EXECUTION_ID_REQUEST_HEADER
from pydantic_core import PydanticSerializationError
from typing_extensions import assert_never

from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    CompletedExecutionResult,
    ExecutionInfo,
)
from ucam_faas.handler_execution import (
    DEFAULT_EXECUTION_RESULT_LOGGER,
    DEFAULT_HTTP_RESPONSE_CREATOR,
    CloudEventFunctionsFrameworkHandlerExecutor,
    CloudEventFunctionsFrameworkHandlerExecutorFn,
    HttpResponseCreator,
    JsonRepresentation,
    StructlogJsonExecutionResultLogger,
    _CloudEventHandlerT,
    cloud_event_handler_executor,
    get_function_execution_id,
)
from ucam_faas.tests.fixtures import make_cloud_event


def get_response_text(response: flask.Response) -> str:
    return "".join(
        chunk.decode() if isinstance(chunk, bytes) else chunk for chunk in response.response
    )


class TestHttpResponseCreator:
    RESPONSES: Final = {
        **DEFAULT_HTTP_RESPONSE_CREATOR.responses,
        "custom.abort": HttpResponseCreator.ResponseFields(
            status_code=http.client.IM_A_TEAPOT, message="I'm a teapot"
        ),
    }

    @pytest.fixture
    def http_response_creator(self) -> HttpResponseCreator:
        return HttpResponseCreator(responses=TestHttpResponseCreator.RESPONSES)

    @pytest.fixture(params=list(RESPONSES.items()), ids=lambda item: item[0])
    def aborted_response(
        self, request: pytest.FixtureRequest
    ) -> tuple[AbortedExecutionReason | str, HttpResponseCreator.ResponseFields]:
        reason, fields = request.param

        assert isinstance(reason, (AbortedExecutionReason, str))
        assert isinstance(fields, HttpResponseCreator.ResponseFields)

        return reason, fields

    def test_returns_none_for_execution_status_completed(
        self, http_response_creator: HttpResponseCreator
    ) -> None:
        # We return None on success because functions_framework treats handlers
        # returning None as successful and it generates its own success response.
        assert http_response_creator(ExecutionInfo(execution=CompletedExecutionResult())) is None

    def test_returns_aborted_response_for_configured_responses(
        self,
        http_response_creator: HttpResponseCreator,
        aborted_response: tuple[AbortedExecutionReason | str, HttpResponseCreator.ResponseFields],
    ) -> None:
        reason, fields = aborted_response

        resp = http_response_creator(ExecutionInfo(execution=AbortedExecutionResult(reason)))
        assert isinstance(resp, flask.Response)
        assert resp.status_code == fields.status_code
        assert resp.content_type == "text/plain"
        assert get_response_text(resp) == fields.message

    def test_returns_internal_server_error_for_unknown_aborted_reason(
        self, http_response_creator: HttpResponseCreator
    ) -> None:
        resp = http_response_creator(
            ExecutionInfo(execution=(AbortedExecutionResult(reason="unknown.foo")))
        )
        assert resp is not None
        assert resp.status_code == http.client.INTERNAL_SERVER_ERROR
        assert resp.content_type == "text/plain"
        assert get_response_text(resp) == "Failed to handle event for unknown reason"


def test_DEFAULT_HTTP_RESPONSE_CREATOR_defines_common_responses() -> None:
    assert DEFAULT_HTTP_RESPONSE_CREATOR.responses.keys() == set(AbortedExecutionReason)


class TestStructlogJsonExecutionResultLogger:
    @pytest.fixture
    def result_logger(
        self, json_representation: JsonRepresentation
    ) -> StructlogJsonExecutionResultLogger:
        return StructlogJsonExecutionResultLogger(json_representation=json_representation)

    @pytest.fixture(params=JsonRepresentation)
    def json_representation(self, request: pytest.FixtureRequest) -> JsonRepresentation:
        return JsonRepresentation(request.param)

    def test_logs_execution_info_for_completed_execution(
        self,
        caplog: pytest.LogCaptureFixture,
        result_logger: StructlogJsonExecutionResultLogger,
        json_representation: JsonRepresentation,
    ) -> None:
        result_logger(
            ExecutionInfo(
                execution=CompletedExecutionResult(duration_seconds=0.123),
                foo=123,
                bar={"baz": "boz"},
            )
        )

        assert len(caplog.records) == 1
        (record,) = caplog.records

        assert record.name == "ucam_faas"
        assert record.levelname == "INFO"
        msg = record.msg
        assert isinstance(msg, dict)

        if json_representation == JsonRepresentation.WIDE_FLAT:
            expected_fields = {
                "event": "ucam_faas_function_completed",
                "execution.status": "COMPLETED",
                "execution.duration_seconds": 0.123,
                "foo": 123,
                "bar.baz": "boz",
            }
        elif json_representation == JsonRepresentation.NARROW_DEEP:
            expected_fields = {
                "event": "ucam_faas_function_completed",
                "execution": {"duration_seconds": 0.123, "status": "COMPLETED"},
                "foo": 123,
                "bar": {"baz": "boz"},
            }
        else:
            assert_never(json_representation)

        assert {field: msg[field] for field in expected_fields} == expected_fields

    def test_logs_execution_info_for_aborted_execution(
        self,
        caplog: pytest.LogCaptureFixture,
        result_logger: StructlogJsonExecutionResultLogger,
        json_representation: JsonRepresentation,
    ) -> None:
        try:
            raise ValueError("Not OK")
        except ValueError as e:
            err = e

        result_logger(
            ExecutionInfo(
                execution=AbortedExecutionResult(
                    reason=AbortedExecutionReason.USER_DATA_INVALID,
                    exception=err,
                    duration_seconds=0.123,
                ),
                foo=123,
                bar={"baz": "boz"},
            )
        )

        assert len(caplog.records) == 1
        (record,) = caplog.records

        assert record.name == "ucam_faas"
        assert record.levelname == "ERROR"
        msg = record.msg
        assert isinstance(msg, dict)

        if json_representation == JsonRepresentation.WIDE_FLAT:
            expected_fields = {
                "event": "ucam_faas_function_aborted",
                "execution.status": "ABORTED",
                "execution.reason": "ucam_faas.user-data-invalid",
                "execution.duration_seconds": 0.123,
                "execution.exception": ANY,
                "foo": 123,
                "bar.baz": "boz",
            }
            msg_exception = msg["execution.exception"]
        elif json_representation == JsonRepresentation.NARROW_DEEP:
            expected_fields = {
                "event": "ucam_faas_function_aborted",
                "execution": {
                    "status": "ABORTED",
                    "reason": "ucam_faas.user-data-invalid",
                    "duration_seconds": 0.123,
                    "exception": ANY,
                },
                "foo": 123,
                "bar": {"baz": "boz"},
            }
            msg_exception = msg["execution"]["exception"]
        else:
            assert_never(json_representation)

        assert {field: msg[field] for field in expected_fields} == expected_fields

        assert msg_exception.startswith("Traceback (most recent call last):")
        assert "in test_logs_execution_info_for_aborted_execution" in msg_exception
        assert "ValueError: Not OK" in msg_exception

    def test_logs_exception_when_execution_info_json_serialization_fails(
        self,
        caplog: pytest.LogCaptureFixture,
        result_logger: StructlogJsonExecutionResultLogger,
        json_representation: JsonRepresentation,
    ) -> None:
        with pytest.raises(
            PydanticSerializationError, match=r"Unable to serialize unknown type: <class 'object'>"
        ):
            result_logger(ExecutionInfo(custom=object()))  # not JSON-serialisable

        assert len(caplog.records) == 1
        (record,) = caplog.records

        assert record.name == "ucam_faas"
        assert record.levelname == "ERROR"
        msg = record.msg
        assert isinstance(msg, dict)

        assert msg["event"] == "execution_info_json_serialisation_failed"
        assert (
            "PydanticSerializationError: Unable to serialize unknown type: <class 'object'>"
        ) in msg["exception"]


def test_DEFAULT_EXECUTION_RESULT_LOGGER() -> None:
    assert isinstance(DEFAULT_EXECUTION_RESULT_LOGGER, StructlogJsonExecutionResultLogger)
    assert DEFAULT_EXECUTION_RESULT_LOGGER.json_representation == JsonRepresentation.NARROW_DEEP


class Test_cloud_event_handler_executor:
    class GetDecoratedHandlerFn(Protocol):
        def __call__(
            self, handler: _CloudEventHandlerT
        ) -> CloudEventFunctionsFrameworkHandlerExecutorFn[_CloudEventHandlerT]:
            ...

    @pytest.fixture(autouse=True)
    def mock_ff_cloud_event(self) -> Generator[Mock]:
        with mock.patch("functions_framework.cloud_event") as mock_fn:
            yield mock_fn

    @pytest.fixture
    def log_execution_result(self) -> Mock:
        return Mock(name="log_execution_result")

    @pytest.fixture
    def create_http_response(self) -> Mock:
        return Mock(name="create_http_response", return_value=None)

    @staticmethod
    def raw_handler(cloud_event: CloudEvent, /) -> ExecutionInfo:
        return ExecutionInfo()

    @pytest.fixture
    def decorate_handler(
        self, log_execution_result: Mock, create_http_response: Mock
    ) -> GetDecoratedHandlerFn:
        def decorate_handler(
            handler: _CloudEventHandlerT,
        ) -> CloudEventFunctionsFrameworkHandlerExecutorFn[_CloudEventHandlerT]:
            # Equivalent to:
            # @cloud_event_handler_executor(
            #     log_execution_result=log_execution_result,
            #     create_http_response=create_http_response,
            # )
            # def handler(...):
            #     ...

            return cloud_event_handler_executor(
                log_execution_result=log_execution_result,
                create_http_response=create_http_response,
            )(handler)

        return decorate_handler

    @pytest.fixture
    def cloudevent(self) -> CloudEvent:
        return make_cloud_event(
            type="com.example.sampletype1", source="https://example.com/event-producer"
        )

    def test_is_Function_instance(self, decorate_handler: GetDecoratedHandlerFn) -> None:
        # functions_framework fails if handler functions are not instances of
        # types.FunctionType. (Ours is a callable class, so we have to fake this...)

        assert isinstance(decorate_handler(self.raw_handler), types.FunctionType)

    def test_has_name_of_wrapped_handler_fn(self, decorate_handler: GetDecoratedHandlerFn) -> None:
        # functions_framework uses the __name__ of handler functions to identify
        # them, so the name must be preserved when wrapping a user-provided
        # function.
        assert self.raw_handler.__name__ == "raw_handler"
        assert decorate_handler(self.raw_handler).__name__ == "raw_handler"

    def test_registers_handler_with_functions_framework(
        self, mock_ff_cloud_event: Mock, decorate_handler: GetDecoratedHandlerFn
    ) -> None:
        mock_ff_cloud_event.assert_not_called()

        wrapped_handler = decorate_handler(self.raw_handler)

        mock_ff_cloud_event.assert_called_once_with(wrapped_handler)

    def test_handler_fn_is_wrapped_as_CloudEventFunctionsFrameworkHandlerExecutor(
        self, decorate_handler: GetDecoratedHandlerFn
    ) -> None:
        wrapped_handler = decorate_handler(self.raw_handler)

        assert wrapped_handler is not self.raw_handler  # type: ignore[comparison-overlap]
        assert isinstance(wrapped_handler, CloudEventFunctionsFrameworkHandlerExecutor)

    def test_raw_handler_is_property_of_wrapped_handler(
        self, decorate_handler: GetDecoratedHandlerFn
    ) -> None:
        wrapped_handler = decorate_handler(self.raw_handler)
        assert wrapped_handler.execute is self.raw_handler

    @pytest.mark.parametrize("execute_for_result", [True, False])
    def test_logs_execution_result(
        self,
        decorate_handler: GetDecoratedHandlerFn,
        log_execution_result: Mock,
        cloudevent: CloudEvent,
        execute_for_result: bool,
    ) -> None:
        execution_info = ExecutionInfo(foo=123)

        def raw_handler(handler_cloudevent: CloudEvent, /) -> ExecutionInfo:
            assert handler_cloudevent is cloudevent
            return execution_info

        wrapped_handler = decorate_handler(raw_handler)
        if execute_for_result:
            wrapped_handler.execute_for_result(cloudevent)
        else:
            wrapped_handler(cloudevent)

        log_execution_result.assert_called_once_with(execution_info)

    def test_sends_response_from_create_http_response_fn(
        self,
        decorate_handler: GetDecoratedHandlerFn,
        create_http_response: Mock,
        cloudevent: CloudEvent,
    ) -> None:
        execution_info = ExecutionInfo(foo=123)
        expected_response = flask.Response("Example", status=http.client.IM_A_TEAPOT)
        create_http_response.return_value = expected_response

        def raw_handler(handler_cloudevent: CloudEvent, /) -> ExecutionInfo:
            assert handler_cloudevent is cloudevent
            return execution_info

        wrapped_handler = decorate_handler(raw_handler)

        # @functions_framework.cloud_event() handler does not allow the handler
        # to **return** a response, so we send responses by throwing HTTPException
        # which Flask/werkzeug handle.
        with pytest.raises(werkzeug.exceptions.HTTPException) as exc_info:
            wrapped_handler(cloudevent)

        assert exc_info.value.response is expected_response
        create_http_response.assert_called_once_with(execution_info)

    def test_does_not_send_response_when_create_http_response_fn_returns_none(
        self,
        decorate_handler: GetDecoratedHandlerFn,
        create_http_response: Mock,
        cloudevent: CloudEvent,
    ) -> None:
        execution_info = ExecutionInfo(foo=123)
        create_http_response.return_value = None

        def raw_handler(handler_cloudevent: CloudEvent, /) -> ExecutionInfo:
            assert handler_cloudevent is cloudevent
            return execution_info

        wrapped_handler = decorate_handler(raw_handler)

        assert wrapped_handler(cloudevent) is None  # type: ignore[func-returns-value]

        create_http_response.assert_called_once_with(execution_info)


def test_get_function_execution_id() -> None:
    execution_id = "Abcd1234Efgh"

    assert get_function_execution_id() is None

    app = flask.Flask("__future__")
    with app.test_request_context(headers={EXECUTION_ID_REQUEST_HEADER: execution_id}):
        assert flask.has_request_context()

        assert get_function_execution_id() == execution_id

    # Outside a flask context, IDs are unset
    assert get_function_execution_id() is None
