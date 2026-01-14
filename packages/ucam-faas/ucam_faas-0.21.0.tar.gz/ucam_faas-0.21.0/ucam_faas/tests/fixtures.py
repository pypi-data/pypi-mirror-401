from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, Iterable, Literal, Mapping, TypedDict, overload

from cloudevents.abstract import AnyCloudEvent, CloudEvent
from cloudevents.conversion import from_dict
from cloudevents.pydantic.v2 import CloudEvent as PydanticCloudEvent
from google.protobuf.message import Message
from pydantic import BaseModel
from typing_extensions import Required, Unpack

from ucam_faas.gcp_pubsub import (
    PUBSUB_CLOUD_EVENT_TOPIC_PATTERN,
    PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE,
    MessagePublishedData,
    PubsubMessage,
)

if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem


def pubsub_message_bytes(cloud_event: CloudEvent) -> bytes:
    return MessagePublishedData.model_validate(cloud_event.get_data()).message.data


def make_pubsub_message(
    *,
    data: BaseModel | Mapping[str, object] | Message | bytes | None = None,
    attributes: Mapping[str, str] | None = None,
) -> PubsubMessage:
    _data: bytes
    if isinstance(data, BaseModel):
        _data = data.model_dump_json().encode()
    elif isinstance(data, Mapping):
        _data = json.dumps(data).encode()
    elif isinstance(data, Message):
        _data = data.SerializeToString()
    elif data is None:
        _data = b"__example__"
    elif isinstance(data, bytes):
        _data = data
    else:
        raise TypeError(f"Unsupported data type: {data!r}")
    return PubsubMessage(
        data=_data,
        attributes={**(attributes or {})},
        message_id="1",
        publish_time="2025-03-18T09:01:02.345Z",
    )


def make_pubsub_cloud_event(
    pubsub_message: PubsubMessage, topic: str | None = "projects/my-project/topics/my-topic"
) -> CloudEvent:
    if topic and not PUBSUB_CLOUD_EVENT_TOPIC_PATTERN.match(topic):
        raise ValueError(f"Invalid topic value: {topic}")

    ce_data_json = MessagePublishedData(message=pubsub_message).model_dump(
        mode="json", by_alias=True
    )
    return make_cloud_event(
        id=ce_data_json["message"]["messageId"],
        time=ce_data_json["message"]["publishTime"],
        specversion="1.0",
        datacontenttype="application/json",
        type=PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE,
        # functions_framework (which creates this value at runtime, when
        # converting the Pubsub-specific event data to CloudEvent format)
        # will use an empty string when the request URL invoking the
        # function does not match the pattern it expects.
        source=f"//pubsub.googleapis.com/{topic or ''}",
        data=MessagePublishedData(message=pubsub_message).model_dump(mode="json", by_alias=True),
    )


class CloudEventCreateAttributes(TypedDict, total=False):
    """
    Attributes required to create CloudEvent with from_dict().

    Attributes are `Required` if they have no default value. For example, `id`
    is required in CloudEvent objects, but it defaults to a generated UUID.

    See: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#context-attributes
    """

    id: str | None
    source: Required[str]
    specversion: Literal["1.0"]
    type: Required[str]
    datacontenttype: str
    dataschema: str
    subject: str
    time: int | str | datetime | None
    data: object


@overload
def make_cloud_event(
    event_type: type[PydanticCloudEvent] = ...,
    extra_attributes: SupportsKeysAndGetItem[str, object]
    | Iterable[tuple[str, object]]
    | None = ...,
    **attributes: Unpack[CloudEventCreateAttributes],
) -> PydanticCloudEvent:
    ...


@overload
def make_cloud_event(
    event_type: type[AnyCloudEvent],
    extra_attributes: SupportsKeysAndGetItem[str, object]
    | Iterable[tuple[str, object]]
    | None = ...,
    **attributes: Unpack[CloudEventCreateAttributes],
) -> AnyCloudEvent:
    ...


def make_cloud_event(
    event_type: type[AnyCloudEvent] | type[PydanticCloudEvent] = PydanticCloudEvent,
    extra_attributes: SupportsKeysAndGetItem[str, object]
    | Iterable[tuple[str, object]]
    | None = None,
    **attributes: Unpack[CloudEventCreateAttributes],
) -> AnyCloudEvent | PydanticCloudEvent:
    """Create a CloudEvent object with provided attribute values.

    `type` and `source` attributes are required, `id`, `specversion`, `time` and
    `data` have default values.

    See: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#context-attributes

    Examples
    --------
    >>> ce = make_cloud_event(
    ...     id='00000000-0000-0000-0000-000000000000',
    ...     type="com.example.sampletype1",
    ...     source="https://example.com/event-producer",
    ...     time=0,
    ...     data="Hi",
    ... )
    >>> type(ce)
    <class 'cloudevents.pydantic.v2.event.CloudEvent'>

    >>> from cloudevents.conversion import to_json
    >>> print(to_json(ce).decode())
    {\"specversion": "1.0", \
"id": "00000000-0000-0000-0000-000000000000", \
"source": "https://example.com/event-producer", \
"type": "com.example.sampletype1", \
"time": "1970-01-01T00:00:00+00:00", \
"data": "Hi"}
    """

    return from_dict(
        event_type=event_type,
        event={**(dict(extra_attributes) if extra_attributes is not None else {}), **attributes},
    )
