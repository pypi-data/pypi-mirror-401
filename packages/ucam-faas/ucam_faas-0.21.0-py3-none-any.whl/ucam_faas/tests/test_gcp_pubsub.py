import re
from datetime import datetime
from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from ucam_faas.gcp_pubsub import Base64JsonString, MessagePublishedData, PubsubMessage

datetime_type = TypeAdapter(datetime)


def test_Base64JsonString() -> None:
    base64_json_string = TypeAdapter(Base64JsonString)

    # JSON representation is a base64-encoded string
    assert base64_json_string.validate_json('"bWVzc2FnZTE="') == b"message1"
    assert base64_json_string.dump_json(b"message1") == b'"bWVzc2FnZTE="'
    assert base64_json_string.dump_python(b"message1", mode="json") == "bWVzc2FnZTE="

    # The Python representation is bytes
    assert base64_json_string.validate_python(b"\x00foobar\xff") == b"\x00foobar\xff"
    assert base64_json_string.dump_python(b"message1") == b"message1"

    # A Python str is also accepted, and decoded as bytes
    assert base64_json_string.validate_python("bWVzc2FnZTE=") == b"message1"

    # Invalid base64 values are reported as pydantic ValidationError
    with pytest.raises(ValidationError) as exc_info:
        base64_json_string.validate_python("00000")  # invalid base64

    assert "Invalid base64-encoded string: " in str(exc_info.value)
    assert exc_info.value.errors()[0]["type"] == "base64_decode"


tuple[dict[str, object], MessagePublishedData]
valid_pubsub_message_published_event_data_examples = pytest.mark.parametrize(
    "message_json,message_parsed",
    [
        pytest.param(
            {
                "message": {
                    "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
                    "data": "bWVzc2FnZTE=",
                    "attributes": {"my_attr_1": "foo", "my_attr_2": "bar"},
                    "messageId": "1",
                    "publishTime": "2025-03-17T15:07:22.650Z",
                }
            },
            MessagePublishedData(
                message=PubsubMessage(
                    data=b"message1",
                    attributes={"my_attr_1": "foo", "my_attr_2": "bar"},
                    message_id="1",
                    publish_time=datetime_type.validate_python("2025-03-17T15:07:22.650Z"),
                ),
            ),
            id="with-attrs",
        ),
        pytest.param(
            {
                "message": {
                    "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
                    "data": "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJC"
                    "UmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9Q"
                    "UVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3"
                    "x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaan"
                    "qKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0t"
                    "PU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+",
                    "attributes": {},
                    "messageId": "2",
                    "publishTime": "2025-03-17T15:10:35.306Z",
                }
            },
            MessagePublishedData(
                message=PubsubMessage(
                    data=bytes(range(255)),
                    attributes={},
                    message_id="2",
                    publish_time=datetime_type.validate_python("2025-03-17T15:10:35.306Z"),
                ),
            ),
            id="without-attrs",
        ),
    ],
)


@valid_pubsub_message_published_event_data_examples
def test_MessagePublishedData_round_trip(
    message_json: dict[str, object], message_parsed: MessagePublishedData
) -> None:
    parsed = MessagePublishedData.model_validate(message_json)
    assert parsed == message_parsed

    dumped = parsed.model_dump(mode="json", by_alias=True)
    # Pydantic uses more digits to represent fractional sections than we get in
    # real payload data.
    dumped["message"]["publishTime"] = _normalise_iso_datetime(dumped["message"]["publishTime"])
    assert message_json == dumped


@valid_pubsub_message_published_event_data_examples
def test_PubsubMessage_timestamps_are_tz_aware(
    message_json: dict[str, object], message_parsed: MessagePublishedData
) -> None:
    instance = MessagePublishedData.model_validate(message_json)
    assert instance.message.publish_time.tzinfo is not None


@valid_pubsub_message_published_event_data_examples
def test_PubsubMessage_validation_rejects_non_tz_aware_timestamps(
    message_json: dict[str, Any], message_parsed: MessagePublishedData
) -> None:
    message_json["message"]["publishTime"] = message_json["message"]["publishTime"].rstrip("Z")
    with pytest.raises(ValidationError, match=r"Input should have timezone info"):
        MessagePublishedData.model_validate(message_json)

    with pytest.raises(ValidationError, match=r"Input should have timezone info"):
        PubsubMessage(**message_parsed.model_dump(), publish_time=datetime.now(tz=None))


@valid_pubsub_message_published_event_data_examples
def test_PubsubMessage_message_id_cannot_be_empty(
    message_json: dict[str, Any], message_parsed: MessagePublishedData
) -> None:
    message_json["message"]["messageId"] = ""
    with pytest.raises(ValidationError, match=r"should have at least 1 character"):
        MessagePublishedData.model_validate(message_json)

    with pytest.raises(ValidationError, match=r"should have at least 1 character"):
        PubsubMessage(**message_parsed.model_dump(), message_id="")


@valid_pubsub_message_published_event_data_examples
def test_PubsubMessage_type_must_be_correct(
    message_json: dict[str, Any], message_parsed: MessagePublishedData
) -> None:
    message_json["message"]["@type"] = "foobar"
    with pytest.raises(ValidationError, match=r"Input should be.+PubsubMessage"):
        MessagePublishedData.model_validate(message_json)

    with pytest.raises(ValidationError, match=r"Input should be.+PubsubMessage"):
        PubsubMessage(**message_parsed.model_dump(), type="foobar")


def _normalise_iso_datetime(iso_datetime: str) -> str:
    """Truncate fractional seconds of an ISO datetime string to 3 digits.

    Examples
    --------
    >>> _normalise_iso_datetime('2025-03-17T15:10:35.306000Z')
    '2025-03-17T15:10:35.306Z'
    >>> _normalise_iso_datetime('asdfsdfds')
    'asdfsdfds'
    """
    # limit fractional seconds to 1ms resolution (3 digits)
    return re.sub(r"\.([0-9]+)[zZ]$", lambda m: f".{m.group(1)[:3]}Z", iso_datetime)
