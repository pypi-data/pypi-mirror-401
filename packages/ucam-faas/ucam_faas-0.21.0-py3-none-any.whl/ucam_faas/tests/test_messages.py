from __future__ import annotations

import gzip
import json
import re
from typing import Callable, Generic, Literal, TypeVar, cast

import pytest
from google.protobuf.message import DecodeError
from pydantic import BaseModel, Field
from typing_extensions import Never, assert_type

from ucam_faas.cloud_events import CloudEventAttributes, CloudEventHandlerExecutionInfo
from ucam_faas.contexts import contextual_default_factory
from ucam_faas.exceptions import ExecutionAbortedException
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    ExecutionStatus,
)
from ucam_faas.messages import (
    MESSAGE_CONTEXT,
    MessageHandlerExecutionInfo,
    message_handler,
)
from ucam_faas.tests.fixtures import (
    make_cloud_event,
    make_pubsub_cloud_event,
    make_pubsub_message,
)
from ucam_faas.tests.protobuf import example_pb2

_T = TypeVar("_T")


class ExampleMessage(BaseModel):
    colour: Literal["red", "green", "blue"]
    size: int


class EchoExecutionInfo(MessageHandlerExecutionInfo, Generic[_T]):
    message: _T


def echo_message_handler(message: _T) -> EchoExecutionInfo[_T]:
    return EchoExecutionInfo(message=message)


def gzip_json_message_parser(raw_message: bytes) -> dict[str, object]:
    json_value = json.loads(gzip.decompress(raw_message))
    assert isinstance(json_value, dict)
    return json_value


def aborting_message_parser(raw_message: bytes) -> Never:
    raise ExecutionAbortedException(
        "aborted due to testing",
        execution_info=MessageHandlerExecutionInfo(
            execution=AbortedExecutionResult(
                status=ExecutionStatus.ABORTED, reason="custom-reason"
            )
        ),
    )


def value_error_message_parser(raw_message: bytes) -> Never:
    raise ValueError("no message data values are valid")


def test_message_handler__with_no_message_parser__provides_bytes_to_message_handler() -> None:
    @message_handler(message_type=None)
    def demo_handler(message: bytes) -> EchoExecutionInfo[bytes]:
        return EchoExecutionInfo(message=message)

    pubsub_cloud_event = make_pubsub_cloud_event(make_pubsub_message(data=b"foo"))
    execution_info = demo_handler.execute(pubsub_cloud_event)

    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.message == b"foo"


def test_message_handler__with_pydantic_message_parser__provides_model_instance_to_message_handler() -> (  # noqa: E501
    None
):
    @message_handler(message_type=ExampleMessage)
    def demo_handler(message: ExampleMessage) -> EchoExecutionInfo[ExampleMessage]:
        return EchoExecutionInfo(message=message)

    model_msg = ExampleMessage(colour="red", size=42)
    execution_info = demo_handler.execute(
        make_pubsub_cloud_event(make_pubsub_message(data=model_msg))
    )

    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.message == model_msg


def test_message_handler__with_pydantic_message_parser__rejects_message_with_invalid_data() -> (
    None
):
    @message_handler(message_type=ExampleMessage)
    def demo_handler(message: ExampleMessage) -> EchoExecutionInfo[ExampleMessage]:
        return EchoExecutionInfo(message=message)

    with pytest.raises(
        ExecutionAbortedException, match=r"Input should be 'red', 'green' or 'blue'"
    ) as exc_info:
        demo_handler.execute(
            make_pubsub_cloud_event(
                # Invalid JSON data for ExampleMessage
                make_pubsub_message(data={"colour": "foo", "size": 42})
            )
        )

    execution_info = exc_info.value.execution_info
    assert execution_info.execution.status == ExecutionStatus.ABORTED
    assert execution_info.execution.reason == AbortedExecutionReason.USER_DATA_INVALID


def test_message_handler__with_protobuf_message_parser__provides_message_instance_to_message_handler() -> (  # noqa: E501
    None
):
    @message_handler(message_type=example_pb2.ExampleRecord)
    def demo_handler(
        message: example_pb2.ExampleRecord,
    ) -> EchoExecutionInfo[example_pb2.ExampleRecord]:
        return EchoExecutionInfo(message=message)

    protobuf_msg = example_pb2.ExampleRecord(query="foo", page_number=3, results_per_page=10)
    execution_info = demo_handler.execute(
        make_pubsub_cloud_event(make_pubsub_message(data=protobuf_msg))
    )

    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.message == protobuf_msg


def test_message_handler__with_protobuf_message_parser__rejects_message_with_invalid_data() -> (  # noqa: E501
    None
):
    @message_handler(message_type=example_pb2.ExampleRecord)
    def demo_handler(
        message: example_pb2.ExampleRecord,
    ) -> EchoExecutionInfo[example_pb2.ExampleRecord]:
        return EchoExecutionInfo(message=message)

    with pytest.raises(
        ExecutionAbortedException, match=r"message_parser failed to parse message"
    ) as exc_info:
        demo_handler.execute(
            # 0xFF is not a valid serialised example_pb2.ExampleRecord
            make_pubsub_cloud_event(make_pubsub_message(data=b"\xff"))
        )
    execution_info = exc_info.value.execution_info
    assert execution_info.execution.status == ExecutionStatus.ABORTED
    assert isinstance(execution_info.execution.exception, DecodeError)
    assert execution_info.execution.reason == AbortedExecutionReason.USER_DATA_INVALID


def test_message_handler__with_function_message_parser__provides_message_instance_to_message_handler() -> (  # noqa: E501
    None
):
    @message_handler(message_type=gzip_json_message_parser)
    def demo_handler(message: dict[str, object]) -> EchoExecutionInfo[dict[str, object]]:
        return EchoExecutionInfo(message=message)

    custom_msg = {"hello": "world"}
    encoded_custom_msg = gzip.compress(json.dumps(custom_msg).encode())
    execution_info = demo_handler.execute(
        make_pubsub_cloud_event(make_pubsub_message(data=encoded_custom_msg))
    )

    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.message == custom_msg


def test_message_handler__with_function_message_parser__rejects_message_with_invalid_data() -> (  # noqa: E501
    None
):
    @message_handler(message_type=gzip_json_message_parser)
    def demo_handler(message: dict[str, object]) -> EchoExecutionInfo[dict[str, object]]:
        return EchoExecutionInfo(message=message)

    with pytest.raises(
        ExecutionAbortedException, match=re.escape(r"Not a gzipped file (b'\xff')")
    ) as exc_info:
        demo_handler.execute(
            # 0xFF is not valid gzip stream
            make_pubsub_cloud_event(make_pubsub_message(data=b"\xff"))
        )
    execution_info = exc_info.value.execution_info
    assert execution_info.execution.status == ExecutionStatus.ABORTED
    assert execution_info.execution.reason == AbortedExecutionReason.USER_DATA_INVALID


def test_message_handler__with_function_message_parser__honours_AbortedExecutionResult_thrown_by_parser() -> (  # noqa: E501
    None
):
    @message_handler(message_type=aborting_message_parser)
    def demo_handler(message: object) -> EchoExecutionInfo[Never]:
        assert False, "not reachable due to parser aborting"

    with pytest.raises(ExecutionAbortedException, match=r"aborted due to testing") as exc_info:
        demo_handler.execute(make_pubsub_cloud_event(make_pubsub_message(data=b"")))
    execution_info = exc_info.value.execution_info
    assert execution_info.execution.status == ExecutionStatus.ABORTED
    assert execution_info.execution.reason == "custom-reason"


def test_message_handler__with_invalid_message_parser__throws_type_error_on_creation() -> None:
    with pytest.raises(
        TypeError,
        match=r"message_parser must be "
        r"a Pydantic model class, "
        r"a Protobuf Message class, "
        r"a function "
        r"or None, got: <object object at .+>",
    ):

        @message_handler(message_type=cast(None, object()))
        def demo_handler(message: bytes) -> Never:
            assert False, "Never called due to invalid message_type"


def test_message_handler__can_return_none_to_use_default_execution_info_result() -> None:
    received_message: bytes | None = None

    @message_handler(message_type=None)
    def handle_bytes(message: bytes) -> None:
        nonlocal received_message
        received_message = message

    pubsub_cloud_event = make_pubsub_cloud_event(make_pubsub_message(data=b"foo"))
    execution_info = handle_bytes.execute(pubsub_cloud_event)

    assert_type(execution_info, MessageHandlerExecutionInfo)
    assert isinstance(execution_info, MessageHandlerExecutionInfo)

    assert execution_info.execution.status is ExecutionStatus.COMPLETED
    assert received_message == b"foo"


def test_message_handler__returns_specified_default_execution_info_type() -> None:
    """
    The handler returns no ExecutionInfo itself, so a default ExecutionInfo gets
    created after it returns.

    The default ExecutionInfo type is overridden to be MyExecutionInfo, so it
    gets created, and picks up an attribute from the parsed Pubsub message to
    record as part of the result.
    """

    class MyExecutionInfo(MessageHandlerExecutionInfo):
        foo: str = Field(
            default_factory=contextual_default_factory(
                MESSAGE_CONTEXT, fn=lambda msg: msg.pubsub_message.attributes["foo"]
            )
        )

    @message_handler(message_type=None, create_default_info=MyExecutionInfo.from_context)
    def demo_handler(message: bytes) -> None:
        pass

    pubsub_cloud_event = make_pubsub_cloud_event(
        make_pubsub_message(data=b"foo", attributes={"foo": "foobar!"})
    )
    execution_info = demo_handler.execute(pubsub_cloud_event)

    assert_type(execution_info, MyExecutionInfo)
    assert isinstance(execution_info, MyExecutionInfo)

    assert execution_info.execution.status is ExecutionStatus.COMPLETED
    assert execution_info.foo == "foobar!"


@pytest.mark.parametrize("message_type", [aborting_message_parser, value_error_message_parser])
def test_message_handler__provides_input_message_in_execution_info__when_input_message_is_rejected(
    message_type: Callable[[bytes], Never],
) -> None:
    @message_handler(message_type=message_type)
    def demo_handler(message: bytes) -> EchoExecutionInfo[bytes]:
        assert False, "not reachable due to parser aborting"

    pubsub_message = make_pubsub_message(data=b"foo")
    pubsub_cloud_event = make_pubsub_cloud_event(pubsub_message)

    with pytest.raises(ExecutionAbortedException) as exc_info:
        demo_handler.execute(pubsub_cloud_event)

    execution_info = exc_info.value.execution_info
    assert isinstance(execution_info, MessageHandlerExecutionInfo)
    assert execution_info.execution.status == ExecutionStatus.ABORTED

    assert execution_info.cloudevents == CloudEventAttributes.from_cloud_event(pubsub_cloud_event)
    assert execution_info.cloud_event_handler.input_event_accepted is True

    assert execution_info.message_handler.input_message_accepted is False
    assert execution_info.pubsub_message == pubsub_message


def test_message_handler__provides_input_message_in_execution_info__when_input_message_is_accepted() -> (  # noqa: E501
    None
):
    @message_handler(message_type=None)
    def demo_handler(message: bytes) -> None:
        return None

    pubsub_message = make_pubsub_message(data=b"foo")
    pubsub_cloud_event = make_pubsub_cloud_event(pubsub_message)

    execution_info = demo_handler.execute(pubsub_cloud_event)

    assert execution_info.execution.status == ExecutionStatus.COMPLETED

    assert execution_info.cloudevents == CloudEventAttributes.from_cloud_event(pubsub_cloud_event)
    assert execution_info.cloud_event_handler.input_event_accepted is True

    assert execution_info.message_handler.input_message_accepted is True
    assert execution_info.pubsub_message == pubsub_message


def test_message_handler__provides_cloud_event_only__when_input_cloud_event_is_not_pubsub_message_event() -> (  # noqa: E501
    None
):
    @message_handler(message_type=None)
    def demo_handler(message: bytes) -> None:
        return None

    wrong_cloud_event = make_cloud_event(
        type="com.example.sampletype1", source="https://example.com/event-producer"
    )

    with pytest.raises(
        ExecutionAbortedException, match="demo_handler input parser rejected input"
    ) as exc_info:
        demo_handler.execute(wrong_cloud_event)

    execution_info = exc_info.value.execution_info
    assert isinstance(execution_info, CloudEventHandlerExecutionInfo)
    assert not isinstance(execution_info, MessageHandlerExecutionInfo)
    assert execution_info.execution.status == ExecutionStatus.ABORTED

    assert execution_info.cloudevents == CloudEventAttributes.from_cloud_event(wrong_cloud_event)
    assert execution_info.cloud_event_handler.input_event_accepted is False
