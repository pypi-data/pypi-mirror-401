"""
Support for parsing/validating/serialising GCP Pub/Sub messages within
CloudEvent envelopes.

This module provides constants for the CloudEvent type that identifies message
events, and Pydantic data models for the data payload of these events.

Example
-------
>>> cloud_event_json = {
...     "id": "1",
...     "time": "2025-03-18T09:01:02.345Z",
...     "specversion": "1.0",
...     "datacontenttype": "application/json",
...     "type": "google.cloud.pubsub.topic.v1.messagePublished",
...     "source": "//pubsub.googleapis.com/projects/my-project/topics/my-topic",
...     "data": {
...         "message": {
...             "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
...             "data": "bWVzc2FnZTE=",
...             "attributes": {"my_attr_1": "foo", "my_attr_2": "bar"},
...             "messageId": "1",
...             "publishTime": "2025-03-18T09:01:02.345Z",
...         }
...     },
... }
>>> from cloudevents.conversion import from_dict
>>> from cloudevents.pydantic.v2 import CloudEvent as PydanticCloudEvent
>>> cloud_event = from_dict(PydanticCloudEvent, cloud_event_json)
>>>
>>> assert cloud_event.get_attributes()['type'] == PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE
>>>
>>> payload = MessagePublishedData.model_validate(cloud_event.get_data())
>>> assert payload.message.data == b'message1'
>>> assert payload.message.message_id == '1'
>>> assert payload.message.attributes == {"my_attr_1": "foo", "my_attr_2": "bar"}
>>> assert payload.message.publish_time.year == 2025
>>>
>>> # The Pub/Sub topic is in the CloudEvent's "source" attribute.
>>> assert cloud_event.get_attributes()['source'] == \\
...     "//pubsub.googleapis.com/projects/my-project/topics/my-topic"
>>>
>>> # Although we can parse the project_id and topic_id as follows, if you need
>>> # to verify the topic is correct, it's probably fine to treat the source as
>>> # an atomic/opaque value and compare it to a string containing your IDs.
>>> topic = cloud_event.get_attributes()['source'].removeprefix('//pubsub.googleapis.com/')
>>> PUBSUB_CLOUD_EVENT_TOPIC_PATTERN.match(topic).groupdict()
{'project_id': 'my-project', 'topic_id': 'my-topic'}
"""
from __future__ import annotations

import base64
import re
from typing import TYPE_CHECKING, Annotated, Final, Literal, Mapping

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    PlainValidator,
    StringConstraints,
)
from pydantic_core import PydanticCustomError

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

PubsubMessageType: TypeAlias = Literal["type.googleapis.com/google.pubsub.v1.PubsubMessage"]
PUBSUB_MESSAGE_TYPE: Final = "type.googleapis.com/google.pubsub.v1.PubsubMessage"
"""The `@type` property of Pubsub message data within `...messagePublished` CloudEvent objects."""
PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE: Final = "google.cloud.pubsub.topic.v1.messagePublished"
"""The `type` property used on CloudEvent objects containing `...PubsubMessage` data."""

PUBSUB_CLOUD_EVENT_TOPIC_PATTERN: Final = re.compile(
    r"^projects/(?P<project_id>[^/]+)/topics/(?P<topic_id>[^/]+)$"
)

NonEmptyString: TypeAlias = Annotated[str, StringConstraints(min_length=1)]


def _decode_Base64JsonString(data: str | bytes) -> bytes:
    if isinstance(data, bytes):
        return data
    try:
        return base64.b64decode(data)
    except ValueError as e:
        raise PydanticCustomError(
            "base64_decode", "Base64 decoding error: '{error}'", {"error": str(e)}
        )


def _encode_Base64JsonString(data: bytes) -> str:
    return base64.b64encode(data).decode()


Base64JsonString: TypeAlias = Annotated[
    bytes,
    PlainSerializer(func=_encode_Base64JsonString, when_used="json"),
    PlainValidator(func=_decode_Base64JsonString, json_schema_input_type=str),
]
"""Binary data. Python representation is bytes, JSON is a (non-URL-safe) base64 string."""


class PubsubMessage(BaseModel):
    """
    A message from Pubsub to notify a subscriber of an event on their topic.

    The message data is a byte string in the application-specific format known to
    the subscriber.
    """

    model_config = ConfigDict(populate_by_name=True)

    type: PubsubMessageType = Field(alias="@type", default=PUBSUB_MESSAGE_TYPE)
    data: Base64JsonString
    attributes: Mapping[str, str]
    message_id: NonEmptyString = Field(alias="messageId")
    publish_time: AwareDatetime = Field(alias="publishTime")


class MessagePublishedData(BaseModel):
    """
    The Pubsub `MessagePublishedData` object.

    This JSON object wraps a `PubsubMessage` and in theory could contain extra
    information about it. In practice, it contains only a message property and
    no other fields, but the schema suggests it could contain `subscription` and
    `deliveryAttempt` properties. When the `functions_framework` constructs it,
    it never populates these, only `message`.

    See Also
    --------
    - https://github.com/GoogleCloudPlatform/functions-framework-conformance/\
blob/main/docs/mapping.md#cloud-pubsub-events
    - [google-cloudevents JSON schema](https://github.com/googleapis/\
google-cloudevents/blob/main/jsonschema/google/events/cloud/pubsub/v1/\
MessagePublishedData.json)
    """

    message: PubsubMessage
