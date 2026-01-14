from __future__ import annotations

from enum import Enum
from typing import Generic, Literal, TypeVar

import pytest
from cloudevents.abstract import CloudEvent
from pydantic import BaseModel, ValidationError
from typing_extensions import Never, assert_type

from ucam_faas.cloud_events import (
    CloudEventAttributes,
    CloudEventHandlerAttributes,
    CloudEventHandlerContext,
    CloudEventHandlerExecutionInfo,
    CloudEventHandlerExecutorFn,
    CloudEventType,
    cloud_event_handler,
    contextual_cloud_event_parser,
)
from ucam_faas.contextual_handlers import ContextualHandlerParserFn
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    ExecutionInfo,
    ExecutionResult,
    ExecutionStatus,
)
from ucam_faas.tests.fixtures import make_cloud_event

_T = TypeVar("_T")


class DataExecutionInfo(CloudEventHandlerExecutionInfo, Generic[_T]):
    data: _T


def make_example_cloud_event(data: object) -> CloudEvent:
    return make_cloud_event(
        type="com.example.sampletype1", source="https://example.com/event-producer", data=data
    )


@pytest.fixture
def cloud_event() -> CloudEvent:
    return make_example_cloud_event(data=None)


class SpecVersion(Enum):
    V1_0 = "1.0"


def parse_specversion(cloud_event: CloudEvent) -> SpecVersion:
    return SpecVersion(cloud_event.get_attributes()["specversion"])


def test_cloud_event_handler__may_return_none(cloud_event: CloudEvent) -> None:
    @cloud_event_handler(event_data_parser=parse_specversion)
    def handler(spec_version: SpecVersion) -> None:
        return None

    assert_type(
        handler,
        CloudEventHandlerExecutorFn[SpecVersion, Never, CloudEventHandlerExecutionInfo, None],
    )

    execution_info = handler.execute(cloud_event)

    assert_type(execution_info, CloudEventHandlerExecutionInfo)
    assert execution_info.execution.status is ExecutionStatus.COMPLETED


def test_cloud_event_handler__returns_specified_default_ExecutionInfo_type_when_handler_returns_none(  # noqa: E501
    cloud_event: CloudEvent,
) -> None:
    def create_default_execution_info(
        *, execution: ExecutionResult
    ) -> DataExecutionInfo[Literal["foo"]]:
        return DataExecutionInfo[Literal["foo"]](data="foo", execution=execution)

    @cloud_event_handler(
        event_data_parser=parse_specversion, create_default_info=create_default_execution_info
    )
    def handler(spec_version: SpecVersion) -> None:
        return None

    assert_type(
        handler,
        CloudEventHandlerExecutorFn[SpecVersion, Never, DataExecutionInfo[Literal["foo"]], None],
    )

    execution_info = handler.execute(cloud_event)

    assert_type(execution_info, DataExecutionInfo[Literal["foo"]])
    assert execution_info.execution.status is ExecutionStatus.COMPLETED
    assert execution_info.data == "foo"


def test_cloud_event_handler__returns_only_handler_type_when_handler_does_not_return_none(
    cloud_event: CloudEvent,
) -> None:
    @cloud_event_handler(event_data_parser=parse_specversion)
    def handler(specversion: SpecVersion) -> DataExecutionInfo[SpecVersion]:
        return DataExecutionInfo(data=specversion)

    assert_type(
        handler,
        CloudEventHandlerExecutorFn[SpecVersion, DataExecutionInfo[SpecVersion], Never, Never],
    )

    execution_info = handler.execute(cloud_event)

    assert_type(execution_info, DataExecutionInfo[SpecVersion])
    assert execution_info.execution.status == ExecutionStatus.COMPLETED
    assert execution_info.data is SpecVersion.V1_0


class TestCloudEventType:
    class ExampleEventData(BaseModel):
        greeting: str

    @pytest.fixture
    def valid_event_data(self) -> TestCloudEventType.ExampleEventData:
        return TestCloudEventType.ExampleEventData(greeting="Hello World!")

    @pytest.fixture
    def valid_event(self, valid_event_data: TestCloudEventType.ExampleEventData) -> CloudEvent:
        return make_cloud_event(
            type="com.example.sampletype1",
            source="https://example.com/event-producer",
            data=valid_event_data.model_dump(mode="json"),
        )

    @pytest.fixture
    def invalid_event_wrong_type(
        self, valid_event_data: TestCloudEventType.ExampleEventData
    ) -> CloudEvent:
        return make_cloud_event(
            type="com.example.sampletype2",
            source="https://example.com/event-producer",
            data=valid_event_data.model_dump(mode="json"),
        )

    @pytest.fixture
    def invalid_event_invalid_data(self) -> CloudEvent:
        return make_cloud_event(
            type="com.example.sampletype1",
            source="https://example.com/event-producer",
            data={"greeting": 42},  # invalid because 42 should be a string
        )

    @pytest.fixture
    def cloud_event_type(self) -> CloudEventType[TestCloudEventType.ExampleEventData]:
        return CloudEventType(
            event_type="com.example.sampletype1",
            event_data_model=TestCloudEventType.ExampleEventData,
        )

    def test_parses_valid_cloudevent(
        self,
        cloud_event_type: CloudEventType[TestCloudEventType.ExampleEventData],
        valid_event: CloudEvent,
        valid_event_data: TestCloudEventType.ExampleEventData,
    ) -> None:
        assert cloud_event_type(valid_event) == valid_event_data

    def test_rejects_event_with_wrong_type(
        self,
        cloud_event_type: CloudEventType[TestCloudEventType.ExampleEventData],
        invalid_event_wrong_type: CloudEvent,
    ) -> None:
        # contextual_cloud_event_parser() is needed to provide the context to create
        # CloudEventHandlerExecutionInfo when the parser rejects the event.
        parse_result = contextual_cloud_event_parser(cloud_event_type)(invalid_event_wrong_type)

        assert isinstance(parse_result, CloudEventHandlerExecutionInfo)
        assert parse_result.execution.status is ExecutionStatus.ABORTED
        assert parse_result.execution.reason is AbortedExecutionReason.CLOUD_EVENT_TYPE_INCORRECT
        assert isinstance(parse_result.execution.exception, ValueError)
        assert "Received CloudEvent with incorrect type: 'com.example.sampletype2'" in str(
            parse_result.execution.exception
        )
        assert parse_result.cloudevents == CloudEventAttributes.from_cloud_event(
            invalid_event_wrong_type
        )
        assert parse_result.cloud_event_handler.input_event_accepted is False

    def test_rejects_event_with_invalid_data(
        self,
        cloud_event_type: CloudEventType[TestCloudEventType.ExampleEventData],
        invalid_event_invalid_data: CloudEvent,
    ) -> None:
        # contextual_cloud_event_parser() is needed to provide the context to create
        # CloudEventHandlerExecutionInfo when the parser rejects the event.
        parse_result = contextual_cloud_event_parser(cloud_event_type)(invalid_event_invalid_data)

        assert isinstance(parse_result, CloudEventHandlerExecutionInfo)
        assert parse_result.execution.status is ExecutionStatus.ABORTED
        assert parse_result.execution.reason is AbortedExecutionReason.SERVICE_DATA_INVALID

        assert isinstance(parse_result.execution.exception, ValidationError)
        exc_info = pytest.ExceptionInfo.from_exception(parse_result.execution.exception)
        exc_info.match(r"validation error for ExampleEventData")
        exc_info.match(r"greeting\s+Input should be a valid string")

        assert parse_result.cloudevents == CloudEventAttributes.from_cloud_event(
            invalid_event_invalid_data
        )
        assert parse_result.cloud_event_handler.input_event_accepted is False


def test_contextual_cloud_event_parser() -> None:
    @contextual_cloud_event_parser
    def parse_cloud_event(cloud_event: CloudEvent, /) -> Literal["Example"] | ExecutionInfo:
        data = cloud_event.get_data()
        if data == "Example":
            return "Example"
        return CloudEventHandlerExecutionInfo(
            execution=AbortedExecutionResult(reason=AbortedExecutionReason.SERVICE_DATA_INVALID)
        )

    assert_type(
        parse_cloud_event,
        ContextualHandlerParserFn[
            CloudEvent, Literal["Example"], CloudEventHandlerContext, ExecutionInfo
        ],
    )

    # Successfully-parsed data becomes the primary value, with the original
    # CloudEvent in the context data.
    cloud_event = make_example_cloud_event(data="Example")
    assert parse_cloud_event(cloud_event) == (
        "Example",
        CloudEventHandlerContext(
            cloud_event=cloud_event,
            execution_id=None,
            handler=CloudEventHandlerAttributes(input_event_accepted=True),
        ),
    )

    # Unsuccessful parse result ExecutionInfo is returned as-is.
    bad_cloud_event = make_example_cloud_event(data="Invalid")
    assert parse_cloud_event(bad_cloud_event) == CloudEventHandlerExecutionInfo(
        execution=AbortedExecutionResult(reason=AbortedExecutionReason.SERVICE_DATA_INVALID),
        execution_id=None,
        cloudevents=CloudEventAttributes.from_cloud_event(bad_cloud_event),
        cloud_event_handler=CloudEventHandlerAttributes(input_event_accepted=False),
    )
