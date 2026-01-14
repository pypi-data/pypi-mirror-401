import json
from logging import LogRecord
from pathlib import Path
from typing import Any, Generator

import pytest
from cloudevents import conversion
from cloudevents.abstract import CloudEvent
from faker import Faker
from google.cloud import storage
from pydantic import BaseModel, ConfigDict
from structlog.testing import capture_logs
from ucam_observe import get_structlog_logger  # type: ignore[import-untyped]

from ucam_faas import cloud_event, raw_event, run_ucam_faas
from ucam_faas.cloud_events import CloudEventType, cloud_event_handler

logger = get_structlog_logger(__name__)

script_path = Path(__file__).resolve()
cwd = Path.cwd()
relative_path = script_path.relative_to(cwd)


@pytest.fixture()
def storage_client() -> storage.Client:
    return storage.Client()


@pytest.fixture()
def input_bucket(storage_client: storage.Client) -> Generator[storage.Bucket, None, None]:
    bucket = storage_client.bucket("input-bucket")

    if bucket.exists(client=storage_client):
        bucket.delete(client=storage_client, force=True)

    storage_client.create_bucket(bucket)

    yield bucket

    bucket.delete(client=storage_client, force=True)


@pytest.fixture()
def input_file(faker: Faker, input_bucket: storage.Bucket, valid_cloud_event: CloudEvent) -> str:
    input_file = f"{faker.uuid4()}.event.json"
    blob = input_bucket.blob(input_file)
    blob.upload_from_string(conversion.to_json(valid_cloud_event), content_type="application/json")
    return input_file


@raw_event
def example_raw_event(raw_event: Any) -> None:
    logger.info("example_raw_event", event_content=json.dumps(raw_event))


@cloud_event
def example_cloud_event(event_data: Any) -> None:
    logger.info("example_cloud_event", event_content=json.dumps(event_data))


class ExampleEventData(BaseModel):
    model_config = ConfigDict(extra="allow")
    foo: str


@cloud_event_handler(
    event_data_parser=CloudEventType(
        event_type="ucam_faas_event", event_data_model=ExampleEventData
    )
)
def example_cloud_event_handler(data: ExampleEventData) -> None:
    assert data.foo == "bar"


@cloud_event_handler(
    event_data_parser=CloudEventType(
        event_type="ucam_faas_event", event_data_model=ExampleEventData
    )
)
def example_unsuccessful_cloud_event_handler(data: ExampleEventData) -> None:
    assert data.foo == "bar"
    raise ValueError("Something went wrong")


@pytest.mark.parametrize("target", ["example_raw_event", "example_cloud_event"])
def test_input_file(
    target: str,
    input_file: str,
    input_bucket: storage.Bucket,
    valid_cloud_event: CloudEvent,
) -> None:
    with capture_logs() as cap_logs:
        assert (
            run_ucam_faas(
                target,
                source=relative_path,
                host="no-host",
                port=0,
                debug=False,
                long_running=True,
                input_bucket=input_bucket.name,
                input_file=input_file,
            )
            == 0
        )
    assert len(cap_logs) == 1

    assert "event_content" in cap_logs[0]
    assert json.loads(cap_logs[0]["event_content"]) == valid_cloud_event.get_data()


def test_invalid_input_file(
    input_bucket: storage.Bucket,
) -> None:
    with capture_logs() as cap_logs:
        assert (
            run_ucam_faas(
                "example_raw_event",
                source=relative_path,
                host="no-host",
                port=0,
                debug=False,
                long_running=True,
                input_bucket=input_bucket.name,
                input_file="non_existent_file.event.json",
            )
            == 3
        )
    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "Unhandled exception when loading input file"


@pytest.mark.parametrize("target", ["example_raw_event", "example_cloud_event"])
def test_no_input_file(target: str) -> None:
    with capture_logs() as cap_logs:
        assert (
            run_ucam_faas(
                target,
                source=relative_path,
                host="no-host",
                port=0,
                debug=False,
                long_running=True,
            )
            == 0
        )

    assert "event_content" in cap_logs[0]
    assert json.loads(cap_logs[0]["event_content"]) is None


def get_function_result_log(caplog: pytest.LogCaptureFixture) -> tuple[LogRecord, dict[str, Any]]:
    events = ("ucam_faas_function_completed", "ucam_faas_function_aborted")
    record = next(
        (
            r
            for r in caplog.records
            if r.name == "ucam_faas" and isinstance(r.msg, dict) and r.msg["event"] in events
        ),
        None,
    )
    assert (
        record is not None
    ), f"No record was logged in the 'ucam_faas' logger with event {' or '.join(events)}"
    assert isinstance(record.msg, dict)
    return record, record.msg


def test_long_running__executes_cloud_event_handler__and_reports_success(
    input_file: str,
    input_bucket: storage.Bucket,
    valid_cloud_event: CloudEvent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    exit_status = run_ucam_faas(
        "example_cloud_event_handler",
        source=relative_path,
        host="no-host",
        port=0,
        debug=False,
        long_running=True,
        input_bucket=input_bucket.name,
        input_file=input_file,
    )
    assert exit_status == 0

    _, log_msg = get_function_result_log(caplog)

    assert log_msg["event"] == "ucam_faas_function_completed"
    assert log_msg["execution"]["status"] == "COMPLETED"

    assert log_msg["cloudevents"]["event_id"] == valid_cloud_event.get_attributes()["id"]
    assert log_msg["cloudevents"]["event_type"] == "ucam_faas_event"
    assert log_msg["cloudevents"]["event_source"] == "ucam_faas"


def test_long_running__executes_cloud_event_handler__and_reports_failure(
    input_file: str,
    input_bucket: storage.Bucket,
    valid_cloud_event: CloudEvent,
    caplog: pytest.LogCaptureFixture,
) -> None:
    exit_status = run_ucam_faas(
        "example_unsuccessful_cloud_event_handler",
        source=relative_path,
        host="no-host",
        port=0,
        debug=False,
        long_running=True,
        input_bucket=input_bucket.name,
        input_file=input_file,
    )
    assert exit_status == 1

    _, log_msg = get_function_result_log(caplog)

    assert log_msg["event"] == "ucam_faas_function_aborted"
    assert log_msg["execution"]["status"] == "ABORTED"
    assert log_msg["execution"]["reason"] == "ucam_faas.function-aborted"

    assert "Traceback (most recent call last):\n" in log_msg["execution"]["exception"]
    assert "\nValueError: Something went wrong\n" in log_msg["execution"]["exception"]

    assert log_msg["cloudevents"]["event_id"] == valid_cloud_event.get_attributes()["id"]
    assert log_msg["cloudevents"]["event_type"] == "ucam_faas_event"
    assert log_msg["cloudevents"]["event_source"] == "ucam_faas"
