"""
Support for event handler functions that process message events, such as GCP
PubSub messages.

This module provides support for:

- Validating incoming message metadata envelope
- Parsing/validating the message payload
- Recording the message envelope metadata in the function's `ExecutionInfo` result

Handler functions can focus on processing decoded message data payloads, without
needing to do their own parsing and validation or event metadata
logging/reporting.

To use this module, handler functions are wrapped with this module's
`@message_handler(...)` decorator. The decorator takes a `message_type`
argument that describes the message payload that the handler will be called
with to handle an incoming message. The `message_type` can be any of:

- A Pydantic model, to handle a JSON payload;
  the handler receives an instance of the model.
- A Protobuf Message class, to handle a protobuf payload;
  the handler receives an instance of the Message.
- `None` to perform no validation; the handler receives the payload bytes.
- A parser function that receives bytes and returns a value;
  the handler receives the parser's return value.

Handler functions receive the message payload decoded by the `message_type`, and
also have access to the the full GCP PubSub message and CloudEvent values that
the message was delivered with. Metadata from these metadata envelopes is
automatically included in `PubsubMessageExecutionInfo` values created within the
handler function's scope.
"""

from __future__ import annotations

import functools
from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Protocol, cast, overload

from pydantic import BaseModel, Field
from typing_extensions import Never, TypeGuard, TypeVar

from ucam_faas.cloud_events import (
    CloudEventHandlerExecutionInfo,
    CloudEventHandlerExecutorFn,
    CloudEventType,
    cloud_event_handler,
)
from ucam_faas.contexts import contextual_default_factory, contextvar_activator
from ucam_faas.contextual_handlers import (
    ContextualHandlerParserFn,
    CreateExecutionInfoFn,
    HandlerFn,
    contextual_handler,
)
from ucam_faas.exceptions import ExecutionAbortedException, with_notes
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    ExecutionInfo,
)
from ucam_faas.gcp_pubsub import (
    PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE,
    MessagePublishedData,
    PubsubMessage,
)
from ucam_faas.handler_execution import HandlerExecutionOptions

if TYPE_CHECKING:
    # protobuf is not a required dependency
    from google.protobuf.message import Message

_PydanticModelT = TypeVar("_PydanticModelT", bound=BaseModel)
_ProtobufMessageT = TypeVar("_ProtobufMessageT", bound="Message")
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

_InfoT = TypeVar("_InfoT", bound=ExecutionInfo)
_DefaultInfoT = TypeVar("_DefaultInfoT", bound=ExecutionInfo)
_DefaultInfoT_co = TypeVar("_DefaultInfoT_co", bound=ExecutionInfo, covariant=True)

_NoneT = TypeVar("_NoneT", None, Never, default=Never)


MESSAGE_CONTEXT: ContextVar[MessageHandlerContext] = ContextVar("MESSAGE_CONTEXT")
activate_message_context = contextvar_activator(MESSAGE_CONTEXT)
PUBSUB_MESSAGE_PUBLISHED_CLOUD_EVENT = CloudEventType(
    event_type=PUBSUB_MSG_PUBLISHED_CLOUD_EVENT_TYPE, event_data_model=MessagePublishedData
)


@dataclass
class MessageHandlerContext:
    pubsub_message: PubsubMessage
    handler: MessageHandlerAttributes


@dataclass
class MessageHandlerAttributes:
    input_message_accepted: bool


class PubsubMessageExecutionInfo(ExecutionInfo):
    pubsub_message: PubsubMessage = Field(
        default_factory=contextual_default_factory(
            MESSAGE_CONTEXT, fn=lambda ctx: ctx.pubsub_message
        )
    )
    message_handler: MessageHandlerAttributes = Field(
        default_factory=contextual_default_factory(MESSAGE_CONTEXT, fn=lambda ctx: ctx.handler)
    )


class MessageHandlerExecutionInfo(PubsubMessageExecutionInfo, CloudEventHandlerExecutionInfo):
    pass


class MessageParserFn(Protocol[_T_co]):
    def __call__(self, raw_message: bytes, /) -> _T_co:
        pass


class MessageHandlerDecoratorFn(Protocol[_T_co, _DefaultInfoT_co]):
    """The type of the decorator returned by `@message_handler(...)`"""

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
        self, event_data_handler: HandlerFn[_T_co, _InfoT], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT]:
        pass

    @overload
    def __call__(
        self, event_data_handler: HandlerFn[_T_co, _InfoT | None], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT | _DefaultInfoT_co]:
        pass

    def __call__(
        self, event_data_handler: HandlerFn[_T_co, _InfoT | _NoneT], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT | _DefaultInfoT_co]:
        pass


@overload
def message_handler(
    *,
    message_type: type[_PydanticModelT],
    create_default_info: None = None,
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_PydanticModelT, MessageHandlerExecutionInfo]:
    pass


@overload
def message_handler(
    *,
    message_type: type[_PydanticModelT],
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT],
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_PydanticModelT, _DefaultInfoT]:
    pass


@overload
def message_handler(
    *,
    message_type: type[_ProtobufMessageT],
    create_default_info: None = None,
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_ProtobufMessageT, MessageHandlerExecutionInfo]:
    pass


@overload
def message_handler(
    *,
    message_type: type[_ProtobufMessageT],
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT],
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_ProtobufMessageT, _DefaultInfoT]:
    pass


@overload
def message_handler(
    *,
    message_type: MessageParserFn[_T],
    create_default_info: None = None,
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_T, MessageHandlerExecutionInfo]:
    pass


@overload
def message_handler(
    *,
    message_type: MessageParserFn[_T],
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT],
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_T, _DefaultInfoT]:
    pass


@overload
def message_handler(
    *,
    message_type: None,
    create_default_info: None = None,
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[bytes, MessageHandlerExecutionInfo]:
    pass


@overload
def message_handler(
    *,
    message_type: None,
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT],
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[bytes, _DefaultInfoT]:
    pass


def message_handler(
    *,
    message_type: type[BaseModel] | type[Message] | MessageParserFn[object] | None,
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT] | None = None,
    options: HandlerExecutionOptions | None = None,
) -> MessageHandlerDecoratorFn[_T, _DefaultInfoT]:
    """Register a function to be called when Pubsub publishes a message.

    This is a (python) function decorator that is used to define the entry point
    of a `ucam_faas` managed (cloud) function. The registered (python) function
    is called by `ucam_faas` each time a message is published to the Pubsub
    topic the deployed (cloud) function is subscribed to. (The topic and other
    subscription details are configured at during deployment, not when
    registering a python function with this decorator.)

    The registered function receives a validated message value, parsed from the
    data payload of the incoming Pubsub event, using the Pydantic model,
    Protobuf message or parser function provided to the `@message_handler(...)`
    decorator when registering.

    Parameters
    ----------
    message_type:
        The type to use to decode/validate the message payload, or function to
        parse the payload. The handler function is called with decoded message
        payload. If `None`, the handler receives the payload as `bytes`, without
        any decoding.
    create_default_info:
        A function used to create an ExecutionInfo value if the decorated
        handler function does not return one.
    options:
        Override the default behaviour for logging the `ExecutionInfo` result,
        and representing the `ExecutionInfo` result as an HTTP response.

    Example
    -------
    First define the data payload of the message you will handle:
    >>> from pydantic import BaseModel
    >>> class GreetingMessage(BaseModel):
    ...     greeting: str

    Second, define a function to handle the message. It'll be called automatically
    each time a PubSub message is received — as long as the message passes
    validation using your model.

    >>> from ucam_faas.messages import message_handler
    >>> @message_handler(message_type=GreetingMessage)
    ... def handle_greeting(message: GreetingMessage) -> None:
    ...     print(f"Received greeting: {message.greeting!r}")

    The handler function can be executed for testing purposes:
    >>> from ucam_faas.tests.fixtures import make_pubsub_cloud_event, make_pubsub_message
    >>> cloud_event = make_pubsub_cloud_event(
    ...     make_pubsub_message(data=GreetingMessage(greeting="Hello World!")),
    ...     topic="projects/my-project/topics/greetings",
    ... )
    >>> exc_info = handle_greeting.execute_for_result(cloud_event)
    Received greeting: 'Hello World!'
    """
    message_parser_fn = get_message_parser_fn(message_type)
    parser = contextual_message_parser(cast(MessageParserFn[_T], message_parser_fn))

    @overload
    def message_handler_decorator(
        message_handler: HandlerFn[_T, _InfoT], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT]:
        pass

    @overload
    def message_handler_decorator(
        message_handler: HandlerFn[_T, _InfoT | None], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT | _DefaultInfoT]:
        pass

    def message_handler_decorator(
        message_handler: HandlerFn[_T, _InfoT | _NoneT], /
    ) -> CloudEventHandlerExecutorFn[MessagePublishedData, _InfoT | _DefaultInfoT]:
        # When create_default_info is None or
        # CreateExecutionInfoFn[MessageExecutionInfo],
        # _DefaultInfoT IS PubsubMessageExecutionInfo because of the
        # @overloads, so this cast is safe.
        _create_default_info = cast(
            CreateExecutionInfoFn[_DefaultInfoT],
            create_default_info or MessageHandlerExecutionInfo.from_context,
        )

        @cloud_event_handler(
            event_data_parser=PUBSUB_MESSAGE_PUBLISHED_CLOUD_EVENT, options=options
        )
        @contextual_handler(
            parser=parser,
            context=activate_message_context,
            default_info_factory=_create_default_info,
        )
        @functools.wraps(message_handler)
        def message_handler_executor(event_data: _T, /) -> _InfoT | _NoneT:
            return message_handler(event_data)

        assert message_handler_executor.__name__ == message_handler_executor.__name__
        return message_handler_executor

    return message_handler_decorator


def bytes_message_parser(raw_message: bytes, /) -> bytes:
    return raw_message


def is_protobuf_message_cls(value: object) -> TypeGuard[type[Message]]:
    return isinstance(value, type) and callable(getattr(value, "ParseFromString", None))


# This is a class rather than fn to allow introspection of the model being used,
# rather than having it hidden in a function closure.
@dataclass
class PydanticMessageParser(Generic[_PydanticModelT]):
    model: type[_PydanticModelT]

    def __call__(self, raw_message: bytes, /) -> _PydanticModelT:
        return self.model.model_validate_json(raw_message)


@dataclass
class ProtobufMessageParser(Generic[_ProtobufMessageT]):
    message_type: type[_ProtobufMessageT]

    def __call__(self, raw_message: bytes, /) -> _ProtobufMessageT:
        return self.message_type.FromString(raw_message)


@overload
def get_message_parser_fn(
    message_type: type[_PydanticModelT],
) -> MessageParserFn[_PydanticModelT]:
    pass


@overload
def get_message_parser_fn(
    message_type: type[_ProtobufMessageT],
) -> MessageParserFn[_ProtobufMessageT]:
    pass


@overload
def get_message_parser_fn(
    message_type: MessageParserFn[_T],
) -> MessageParserFn[_T]:
    pass


@overload
def get_message_parser_fn(
    message_type: None,
) -> MessageParserFn[bytes]:
    pass


def get_message_parser_fn(
    message_type: type[BaseModel] | type[Message] | MessageParserFn[object] | None,
) -> MessageParserFn[object]:
    if message_type is None:
        return bytes_message_parser
    elif isinstance(message_type, type) and issubclass(message_type, BaseModel):
        return PydanticMessageParser(model=message_type)
    elif is_protobuf_message_cls(message_type):
        return ProtobufMessageParser(message_type=message_type)
    elif callable(message_type):
        return cast(MessageParserFn[object], message_type)
    raise TypeError(
        f"message_parser must be a Pydantic model class, a Protobuf Message "
        f"class, a function or None, got: {message_type!r}"
    )


def parse_pubsub_message_data(
    message_parser: MessageParserFn[_T], event_data: MessagePublishedData
) -> _T:
    try:
        return message_parser(event_data.message.data)
    except ExecutionAbortedException:
        raise
    except Exception as e:
        raise with_notes(
            ExecutionAbortedException(
                "message_parser failed to parse message",
                execution_info=MessageHandlerExecutionInfo(
                    execution=AbortedExecutionResult(
                        reason=AbortedExecutionReason.USER_DATA_INVALID, exception=e
                    )
                ),
            ),
            f"See this exception's cause for full details:\n{e}",
        ) from e


def contextual_message_parser(
    message_parser: MessageParserFn[_T_co],
) -> ContextualHandlerParserFn[MessagePublishedData, _T_co, MessageHandlerContext, ExecutionInfo]:
    """Wrap a (bytes) -> T function to be a @contextual_handler() parser.

    The T value returned by the function is the primary value and the context
    contains the GCP Pub/Sub `MessagePublished` event that the data came from.

    The function is run with `MESSAGE_CONTEXT` active.
    """

    @functools.wraps(message_parser)
    def parse_input(
        event_data: MessagePublishedData, /
    ) -> tuple[_T_co, MessageHandlerContext] | ExecutionInfo:
        context = MessageHandlerContext(
            pubsub_message=event_data.message,
            handler=MessageHandlerAttributes(input_message_accepted=False),
        )

        with activate_message_context(context):
            parse_result = parse_pubsub_message_data(message_parser, event_data)

        context.handler.input_message_accepted = True
        return parse_result, context

    return parse_input
