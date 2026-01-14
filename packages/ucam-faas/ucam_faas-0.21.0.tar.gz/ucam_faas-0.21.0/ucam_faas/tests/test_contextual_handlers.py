from __future__ import annotations

import re
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Generic, Literal, TypeVar

import pytest
from pydantic import BaseModel, Field
from typing_extensions import Never, assert_type

from ucam_faas.contexts import (
    ActivateContextVarFn,
    contextual_default_factory,
    contextvar_activator,
)
from ucam_faas.contextual_handlers import ContextualHandlerFn, contextual_handler
from ucam_faas.exceptions import ExecutionAbortedException
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    ExecutionInfo,
    ExecutionResult,
    ExecutionStatus,
)

_T = TypeVar("_T")


class ExampleEvent(BaseModel):
    """A fictional event type for demonstration purposes."""

    version: Literal["1.0", "1.1"]
    id: str
    metadata: dict[str, str]
    message: str


@dataclass
class ExampleContext:
    """Metadata available implicitly to handler functions."""

    event: ExampleEvent
    weather_today: Literal["wet", "dry"]


EXAMPLE_CONTEXT = ContextVar[ExampleContext]("EXAMPLE_CONTEXT")

activate_example_context = contextvar_activator(EXAMPLE_CONTEXT)


class ExampleExecutionInfo(ExecutionInfo, Generic[_T]):
    data: _T

    weather_today: Literal["wet", "dry"] = Field(
        default_factory=contextual_default_factory(
            EXAMPLE_CONTEXT, fn=lambda ctx: ctx.weather_today
        )
    )


@dataclass
class ExampleEventContextParser:
    weather_today: Literal["wet", "dry"]

    def __call__(
        self, raw_json_event: bytes
    ) -> tuple[ExampleEvent, ExampleContext] | ExecutionInfo:
        try:
            event = ExampleEvent.model_validate_json(raw_json_event)
            if event.version != "1.0":
                raise ValueError(
                    f"Only event version 1.0 is not supported: version={event.version!r}"
                )
        except ValueError as e:
            result = AbortedExecutionResult(
                reason=AbortedExecutionReason.SERVICE_DATA_INVALID,
                exception=e,
            )
            return ExecutionInfo(execution=result)

        return (event, ExampleContext(event=event, weather_today=self.weather_today))


example_event_parser = ExampleEventContextParser(weather_today="dry")


@pytest.fixture
def example_event() -> ExampleEvent:
    return ExampleEvent(version="1.0", id="ab12", metadata={"location": "middle"}, message="Hi")


@pytest.fixture
def example_event_json(example_event: ExampleEvent) -> bytes:
    return example_event.model_dump_json().encode()


def test_contextual_handler__may_return_none(
    example_event: ExampleEvent, example_event_json: bytes
) -> None:
    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> None:
        assert event == example_event
        return None

    assert_type(
        handle_event,
        ContextualHandlerFn[bytes, ExampleEvent, Never, ExecutionInfo, None],
    )

    execution_info = handle_event(example_event_json)

    assert_type(execution_info, ExecutionInfo)
    assert execution_info.execution.status is ExecutionStatus.COMPLETED


def test_contextual_handler__returns_specified_default_ExecutionInfo_type_when_handler_returns_none(  # noqa: E501
    example_event: ExampleEvent, example_event_json: bytes
) -> None:
    def create_default_execution_info(
        *, execution: ExecutionResult
    ) -> ExampleExecutionInfo[Literal["foo"]]:
        return ExampleExecutionInfo[Literal["foo"]](data="foo", execution=execution)

    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=create_default_execution_info,
    )
    def handle_event(event: ExampleEvent) -> None:
        assert event == example_event
        return None

    assert_type(
        handle_event,
        ContextualHandlerFn[
            bytes, ExampleEvent, Never, ExampleExecutionInfo[Literal["foo"]], None
        ],
    )

    execution_info = handle_event(example_event_json)

    assert_type(execution_info, ExampleExecutionInfo[Literal["foo"]])
    assert execution_info.execution.status is ExecutionStatus.COMPLETED
    assert execution_info.data == "foo"
    assert execution_info.weather_today == example_event_parser.weather_today


def test_contextual_handler__returns_only_handler_type_when_handler_does_not_return_none(
    example_event: ExampleEvent, example_event_json: bytes
) -> None:
    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        assert event == example_event
        return ExampleExecutionInfo(data=event.message)

    assert_type(
        handle_event,
        ContextualHandlerFn[bytes, ExampleEvent, ExampleExecutionInfo[str], Never, Never],
    )

    execution_info = handle_event(example_event_json)

    assert_type(execution_info, ExampleExecutionInfo[str])
    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.data == example_event.message
    assert execution_info.weather_today == example_event_parser.weather_today


@pytest.mark.parametrize("weather", ["wet", "dry"])
@pytest.mark.parametrize(
    "context",
    [
        pytest.param(EXAMPLE_CONTEXT, id="context-var"),
        pytest.param(activate_example_context, id="context-activator"),
    ],
)
def test_contextual_handler__provides_context_metadata_from_parser_in_context(
    example_event: ExampleEvent,
    example_event_json: bytes,
    weather: Literal["wet", "dry"],
    context: ContextVar[ExampleContext] | ActivateContextVarFn[ExampleContext],
) -> None:
    @contextual_handler(
        # the parser provides the value of EXAMPLE_CONTEXT
        parser=ExampleEventContextParser(weather_today=weather),
        # context can be a ContextVar or an contextvar_activator function
        context=context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        assert event == example_event
        example_context = EXAMPLE_CONTEXT.get()
        assert example_context.event is event
        return ExampleExecutionInfo(data=example_context.weather_today)

    assert_type(
        handle_event,
        ContextualHandlerFn[bytes, ExampleEvent, ExampleExecutionInfo[str], Never, Never],
    )

    execution_info = handle_event(example_event_json)

    assert execution_info.data == weather
    assert execution_info.weather_today == weather


def test_contextual_handler__parser_can_return_ExecutionInfo_to_abort(
    example_event: ExampleEvent,
) -> None:
    # The parser returns if the version is not 1.0
    example_event.version = "1.1"
    unsupported_version_example_event_json = example_event.model_dump_json().encode()
    failed_parse_result = example_event_parser(unsupported_version_example_event_json)

    assert isinstance(failed_parse_result, ExecutionInfo)
    assert failed_parse_result.execution.status is ExecutionStatus.ABORTED
    assert "Only event version 1.0 is not supported: version='1.1'" in str(
        failed_parse_result.execution.exception
    )

    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        assert False, "parser aborts so handler is not called"

    with pytest.raises(ExecutionAbortedException) as exc_info:
        handle_event(unsupported_version_example_event_json)

    exc_info.match(re.escape("handle_event input parser rejected input"))


def test_contextual_handler__re_raises_unhandled_exceptions_from_parser_as_ExecutionAbortedException() -> (  # noqa: E501
    None
):
    # Context parser functions should only raise ExecutionAbortedException. This
    # one raises a ValueError without wrapping it in ExecutionAbortedException,
    # which it shouldn't do, because the parser is best placed to record context
    # about the parse error in an ExecutionInfo value.
    def misbehaving_parser(
        raw_json_event: bytes,
    ) -> tuple[ExampleEvent, ExampleContext] | ExecutionInfo:
        raise ValueError("Example unhandled error from parser")

    @contextual_handler(
        parser=misbehaving_parser,
        context=activate_example_context,
        default_info_factory=ExampleExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        assert False, "parser aborts so handler is not called"

    with pytest.raises(ExecutionAbortedException) as exc_info:
        handle_event(b"not JSON")

    assert exc_info.value.execution_info.execution.status is ExecutionStatus.ABORTED

    assert isinstance(exc_info.value.execution_info.execution.exception, ValueError)
    assert "Example unhandled error from parser" in str(
        exc_info.value.execution_info.execution.exception
    )

    exc_info.match(re.escape("handle_event input context parser threw an exception"))
    exc_info.match(r"input context parser: .*\bmisbehaving_parser")
    exc_info.match(re.escape("input: b'not JSON'"))
    exc_info.match(
        re.escape(
            "Note: context parsers should only throw "
            "ExecutionAbortedException, this parser is misbehaving."
        )
    )


def test_contextual_handler__re_raises_ExecutionAbortedException_raised_from_handler(
    example_event_json: bytes,
) -> None:
    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        raise ExecutionAbortedException(
            "handle_event threw an ExecutionAbortedException itself",
            execution_info=ExecutionInfo(
                execution=AbortedExecutionResult(
                    reason=AbortedExecutionReason.FUNCTION_ABORTED,
                    exception=RuntimeError("Example error!"),
                )
            ),
        )

    with pytest.raises(ExecutionAbortedException) as exc_info:
        handle_event(example_event_json)

    assert exc_info.value.execution_info.execution.status is ExecutionStatus.ABORTED

    assert isinstance(exc_info.value.execution_info.execution.exception, RuntimeError)
    assert "Example error!" == exc_info.value.execution_info.execution.exception.args[0]

    exc_info.match(re.escape("handle_event threw an ExecutionAbortedException itself"))


def test_contextual_handler__re_raises_exceptions_from_handler_as_ExecutionAbortedException(
    example_event_json: bytes,
) -> None:
    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> ExampleExecutionInfo[str]:
        raise RuntimeError("Example error!")

    with pytest.raises(ExecutionAbortedException) as exc_info:
        handle_event(example_event_json)

    assert exc_info.value.execution_info.execution.status is ExecutionStatus.ABORTED

    assert isinstance(exc_info.value.execution_info.execution.exception, RuntimeError)
    assert "Example error!" == exc_info.value.execution_info.execution.exception.args[0]

    exc_info.match(re.escape("handle_event handler threw an exception"))


def test_contextual_handler__has_same_name_as_wrapped_handler_function() -> None:
    @contextual_handler(
        parser=example_event_parser,
        context=activate_example_context,
        default_info_factory=ExecutionInfo.from_context,
    )
    def handle_event(event: ExampleEvent) -> None:
        pass

    assert handle_event.__name__ == "handle_event"
