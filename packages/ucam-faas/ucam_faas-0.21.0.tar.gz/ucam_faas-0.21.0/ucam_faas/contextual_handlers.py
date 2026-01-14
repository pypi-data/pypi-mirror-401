"""
Contextual event handler functions receive a primary value as an argument, with
additional context value provided implicitly using a `ContextVar`.

This separation allows a handler function to act primarily on an important subset
of incoming event data, but still access the wider event metadata when needed,
and automatically include metadata in `ExecutionInfo` result values (using the
`contextual_default_factory()` pattern).

Incoming events are separated into the primary value and context value by a
parser function that receives the incoming event value from the parent handler.

The `@contextual_handler(...)` decorator is the interface to this functionality.
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, Protocol, cast, overload

from typing_extensions import Never, TypeVar

from ucam_faas.contexts import ActivateContextVarFn, contextvar_activator
from ucam_faas.exceptions import ExecutionAbortedException, with_notes
from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    CompletedExecutionResult,
    ExecutionInfo,
    ExecutionResult,
)

_InT_con = TypeVar("_InT_con", contravariant=True)
_PrimaryT = TypeVar("_PrimaryT")
_PrimaryT_co = TypeVar("_PrimaryT_co", covariant=True)
_PrimaryT_con = TypeVar("_PrimaryT_con", contravariant=True)
_ContextT = TypeVar("_ContextT")
_ContextT_co = TypeVar("_ContextT_co", covariant=True)

_T_con = TypeVar("_T_con", contravariant=True)
_R_co = TypeVar("_R_co", covariant=True)

_InfoT = TypeVar("_InfoT", bound=ExecutionInfo)
_InfoT_co = TypeVar("_InfoT_co", bound=ExecutionInfo, covariant=True)
_DefaultInfoT_co = TypeVar("_DefaultInfoT_co", bound=ExecutionInfo, covariant=True)
_UsedDefaultInfoT_co = TypeVar(
    "_UsedDefaultInfoT_co", bound=ExecutionInfo, covariant=True, default=Never
)

_NoneT = TypeVar("_NoneT", None, Never, default=Never)
_NoneT_co = TypeVar("_NoneT_co", None, Never, covariant=True, default=Never)


class HandlerFn(Protocol[_T_con, _R_co]):
    """A function wrapped with and called by `@contextual_handler`."""

    def __call__(self, primary_value: _T_con, /) -> _R_co:
        pass

    @property
    def __name__(self) -> str:
        pass


class ContextualHandlerParserFn(Protocol[_InT_con, _PrimaryT_co, _ContextT_co, _InfoT_co]):
    """
    Responsible for parsing a value into a primary result and context metadata.

    The function returns an ExecutionInfo value to abort without further use of
    the input value.
    """

    def __call__(self, input: _InT_con, /) -> tuple[_PrimaryT_co, _ContextT_co] | _InfoT_co:
        pass


class CreateExecutionInfoFn(Protocol[_InfoT_co]):
    def __call__(self, *, execution: ExecutionResult) -> _InfoT_co:
        pass


class ContextualHandlerFn(
    Protocol[_InT_con, _PrimaryT_con, _InfoT_co, _UsedDefaultInfoT_co, _NoneT_co]
):
    def __call__(self, value: _InT_con, /) -> _InfoT_co | _UsedDefaultInfoT_co:
        """
        Validate and do something with a value, and get a description of the
        outcome as an `ExecutionInfo`.
        """

    # Don't define @property at runtime, as they cause subclasses to be read-only
    if TYPE_CHECKING:

        @property
        def __name__(self) -> str:
            pass

        @property
        def handle_parsed_input(self) -> HandlerFn[_PrimaryT_con, _InfoT_co | _NoneT_co]:
            pass


class ContextualHandlerDecoratorFn(Protocol[_InT_con, _PrimaryT, _DefaultInfoT_co]):
    # These overloads are needed to correctly type the return value of
    # ContextualHandlerWrapperFn() according to whether the handler
    # function returns None:
    #   - When the handler returns None, the default ExecutionInfo type is
    #     returned.
    #   - When the handler never returns None, the return is always the
    #     handler's return type.

    @overload
    def __call__(
        self, handler: HandlerFn[_PrimaryT, _InfoT], /
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT]:
        pass

    @overload
    def __call__(
        self, handler: HandlerFn[_PrimaryT, _InfoT | None], /
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT, _DefaultInfoT_co, None]:
        pass

    def __call__(
        self, handler: HandlerFn[_PrimaryT, _InfoT | _NoneT], /
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT, _DefaultInfoT_co, _NoneT]:
        pass


def contextual_handler(
    *,
    parser: ContextualHandlerParserFn[_InT_con, _PrimaryT, _ContextT, ExecutionInfo],
    context: ContextVar[_ContextT] | ActivateContextVarFn[_ContextT],
    default_info_factory: CreateExecutionInfoFn[_DefaultInfoT_co],
) -> ContextualHandlerDecoratorFn[_InT_con, _PrimaryT, _DefaultInfoT_co]:
    """
    Wrap an handler function to execute in a controlled environment.

    The decorated `handler` function is executed:

    - After a `parser` function validates the input value, to extract a primary
      value of interest, and secondary contextual metadata.
    - With the primary value, extracted from an input value by the `parser`
      function as its argument.
    - With the expectation that the `handler` will return an
      `ExecutionInfo` result, or raise an `ExecutionAbortedError` to communicate
      the outcome of the work it has completed using the parsed event.
    - With an ambient context (using a `contextvars.ContextVar`) providing
      access to the secondary contextual metadata parsed from the input value.
      - This context provides access to metadata related to the input that is
        likely less relevant to the `handler` function than the primary value.
      - The ambient context allows components called indirectly within the
        `handler` to access all available information on the input value,
        without the `handler` needing to explicitly pass all the available
        context values. For example, ExecutionInfo types can populate
        their event-related fields automatically in this way, both from the
        immediate context metadata, and from that of (possibly unknown or
        variable) outer contexts wrapping an inner context. This reduces the
        labour involved in reporting detailed ExecutionInfo results, both for
        successful execution and when errors occur.
    - With an `ExecutionInfo` automatically created when the `handler`
      does not return one, or when it throws an exception.
        - This allows for accurate reporting of execution results in the case of
          errors, or when the `handler` opts not to communicate the outcome of
          its work. (Just having completed successfully or not can be enough
          information for simple use-cases.)
    """

    @overload
    def contextual_handler_decorator(
        handler: HandlerFn[_PrimaryT, _InfoT],
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT]:
        pass

    @overload
    def contextual_handler_decorator(
        handler: HandlerFn[_PrimaryT, _InfoT | None],
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT, _DefaultInfoT_co, None]:
        pass

    def contextual_handler_decorator(
        handler: HandlerFn[_PrimaryT, _InfoT | _NoneT],
    ) -> ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT, _DefaultInfoT_co, _NoneT]:
        activate_context: ActivateContextVarFn[_ContextT]
        if isinstance(context, ContextVar):
            activate_context = contextvar_activator(context)
        else:
            activate_context = context

        wrapper = ContextualHandler[
            _InT_con, _PrimaryT, _ContextT, _InfoT, _DefaultInfoT_co, _DefaultInfoT_co, _NoneT
        ](
            handle_parsed_input=handler,
            parse_input=parser,
            activate_context=activate_context,
            create_default_info=default_info_factory,
        )

        # functions_framework relies on the user's function name, so we must preserve it
        assert wrapper.__name__ == handler.__name__  # nosemgrep: bandit.B101

        return wrapper

    return contextual_handler_decorator


@dataclass
class ContextualHandler(
    ContextualHandlerFn[_InT_con, _PrimaryT, _InfoT, _UsedDefaultInfoT_co, _NoneT],
    Generic[
        _InT_con, _PrimaryT, _ContextT, _InfoT, _DefaultInfoT_co, _UsedDefaultInfoT_co, _NoneT
    ],
):
    handle_parsed_input: HandlerFn[_PrimaryT, _InfoT | _NoneT]
    parse_input: ContextualHandlerParserFn[_InT_con, _PrimaryT, _ContextT, ExecutionInfo]
    create_default_info: CreateExecutionInfoFn[_DefaultInfoT_co | _UsedDefaultInfoT_co]
    activate_context: ActivateContextVarFn[_ContextT]

    if TYPE_CHECKING:
        # Handler that does not return None
        @overload
        def __init__(
            self: ContextualHandler[
                # • _UsedDefaultInfoT_co is Never, i.e. call can only return _InfoT
                # • _NoneT is Never, i.e. handle_parsed_input cannot return None
                _InT_con,
                _PrimaryT,
                _ContextT,
                _InfoT,
                _DefaultInfoT_co,
                Never,
                Never,
            ],
            handle_parsed_input: HandlerFn[_PrimaryT, _InfoT],
            parse_input: ContextualHandlerParserFn[_InT_con, _PrimaryT, _ContextT, ExecutionInfo],
            create_default_info: CreateExecutionInfoFn[_DefaultInfoT_co],
            activate_context: ActivateContextVarFn[_ContextT],
        ) -> None:
            pass

        # Handler that does return None
        @overload
        def __init__(
            self: ContextualHandler[
                # • _UsedDefaultInfoT_co is _DefaultInfoT_co, i.e. call can return
                #       _InfoT | _DefaultInfoT_co.
                # • _NoneT is None, i.e. handle_parsed_input can return None.
                _InT_con,
                _PrimaryT,
                _ContextT,
                _InfoT,
                _DefaultInfoT_co,
                _DefaultInfoT_co,
                _NoneT,
            ],
            handle_parsed_input: HandlerFn[_PrimaryT, _InfoT | None],
            parse_input: ContextualHandlerParserFn[_InT_con, _PrimaryT, _ContextT, ExecutionInfo],
            create_default_info: CreateExecutionInfoFn[_DefaultInfoT_co],
            activate_context: ActivateContextVarFn[_ContextT],
        ) -> None:
            pass

        def __init__(
            self,
            handle_parsed_input: HandlerFn[_PrimaryT, _InfoT | None],
            parse_input: ContextualHandlerParserFn[_InT_con, _PrimaryT, _ContextT, ExecutionInfo],
            create_default_info: CreateExecutionInfoFn[_DefaultInfoT_co],
            activate_context: ActivateContextVarFn[_ContextT],
        ) -> None:
            pass

    def __call__(self, input: _InT_con, /) -> _InfoT | _UsedDefaultInfoT_co:
        try:
            parse_result = self.parse_input(input)
            if isinstance(parse_result, ExecutionInfo):
                raise ExecutionAbortedException(
                    f"{self.__name__} input parser rejected input", execution_info=parse_result
                )
        except ExecutionAbortedException:
            raise
        except Exception as e:
            raise with_notes(
                ExecutionAbortedException(
                    f"{self.__name__} input context parser threw an exception",
                    # The context is not activated because the parse function
                    # failed, so we can't use self.create_default_info
                    execution_info=ExecutionInfo.from_context(
                        execution=AbortedExecutionResult(
                            reason=AbortedExecutionReason.FUNCTION_ABORTED, exception=e
                        )
                    ),
                ),
                f"input context parser: {self.parse_input}, input: {input!r}",
                "Note: context parsers should only throw "
                "ExecutionAbortedException, this parser is misbehaving.",
            )

        primary_value, context_value = parse_result

        with self.activate_context(value=context_value):
            execution_info: _InfoT | None
            try:
                execution_info = self.handle_parsed_input(primary_value)
            except ExecutionAbortedException:
                raise
            except Exception as e:
                raise ExecutionAbortedException(
                    f"{self.__name__} handler threw an exception",
                    execution_info=self.create_default_info(
                        execution=AbortedExecutionResult(
                            reason=AbortedExecutionReason.FUNCTION_ABORTED, exception=e
                        )
                    ),
                )

            if execution_info is None:
                # _UsedDefaultInfoT_co IS the same type as _DefaultInfoT_co when
                # execution_info is None. This is enforced by the __init__
                # @overloads.
                return cast(
                    _UsedDefaultInfoT_co,
                    self.create_default_info(execution=CompletedExecutionResult()),
                )
            return execution_info

    # @functions_framework.cloud_event() decorator registers metadata using the
    # __name__ of the decorated function, so we need to preserve the name of the
    # message_handler, so that our user can use the name of their function as
    # its identifier when configuring/deploying their cloud function.
    @property
    def __name__(self) -> str:
        return self.handle_parsed_input.__name__
