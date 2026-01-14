from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import TYPE_CHECKING, Callable, Generator, Protocol, TypeVar, overload

from typing_extensions import Never

from ucam_faas.exceptions import with_notes

if TYPE_CHECKING:
    from contextlib import _GeneratorContextManager

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")


class ActivateContextVarFn(Protocol[_T]):
    """Get a context manager that sets `value` on a `ContextVar` while active."""

    def __call__(self, value: _T | None = None) -> _GeneratorContextManager[_T]:
        pass


def contextvar_activator(contextvar: ContextVar[_T]) -> ActivateContextVarFn[_T]:
    """
    Create a function that sets a `ContextVar`'s value within a `with` block.

    When called with an existing `ContextVar`, this function returns another
    function that itself takes a value to set on the `ContextVar` and returns a
    context manager that will activate and deactivate the value on the
    `ContextVar`.

    Example
    -------
    >>> my_context = ContextVar('my_context', default='Not Set')
    >>> activate_my_context = contextvar_activator(my_context)

    >>> my_context.get()
    'Not Set'

    >>> with activate_my_context('Hello World!') as active_value:
    ...     assert active_value == 'Hello World!'

    >>> my_context.get()
    'Not Set'
    """

    @contextmanager
    def activate_context(value: _T | None = None) -> Generator[_T]:
        token: Token[_T] | None = None
        if value is not None:
            token = contextvar.set(value)
        try:
            yield contextvar.get()
        finally:
            if token is not None:
                contextvar.reset(token)

    activate_context.__name__ = f"activate_{contextvar.name.lower()}"
    return activate_context


@overload
def contextual_default_factory(
    contextvar: ContextVar[_T],
    *,
    fn: None = None,
    default_fn: None = None,
) -> Callable[[], _T]:
    ...


@overload
def contextual_default_factory(
    contextvar: ContextVar[_T],
    *,
    fn: Callable[[_T], _U],
    default_fn: Callable[[LookupError], Never] | None = None,
) -> Callable[[], _U]:
    ...


@overload
def contextual_default_factory(
    contextvar: ContextVar[_T],
    *,
    fn: Callable[[_T], _U],
    default_fn: Callable[[LookupError], _V],
) -> Callable[[], _U | _V]:
    ...


@overload
def contextual_default_factory(
    contextvar: ContextVar[_T],
    *,
    default_fn: Callable[[LookupError], _V],
    fn: None = None,
) -> Callable[[], _T | _V]:
    ...


def contextual_default_factory(
    contextvar: ContextVar[_T],
    *,
    fn: Callable[[_T], _U] | None = None,
    default_fn: Callable[[LookupError], _V] | None = None,
) -> Callable[[], _T | _U | _V]:
    """
    Create a default-providing function that refers to the value of a `ContextVar`.

    When the returned function is called to provide a default, the `fn`
    keyword argument is called with the current value of the `contextvar` and it
    returns the default value to use. If `fn` is not provided, the `contextvar`'s
    value is returned directly as the default.

    When the `contextvar` holds no value, the `default_fn` is called with a
    `LookupError`. It can either return a default value or raise an error. If
    `default_fn` is not provided, the `LookupError` is raised.
    """

    def contextual_default_factory() -> _T | _U | _V:
        try:
            ctx = contextvar.get()
        except LookupError as e:
            e = with_notes(
                e,
                "A ContextVar was empty when its value was read by a "
                "default_factory function to provide a default value. "
                "This is often caused by trying to create an instance of a "
                "Pydantic model or dataclass that gets default values for its "
                "fields from the environment it's created in. You either need "
                "to provide an explicit value for the field(s) that use a "
                "contextual_default_factory(), or create it in an environment "
                "that provides a value for this empty ContextVar.",
            )
            if default_fn is not None:
                return default_fn(e)
            raise e
        return ctx if fn is None else fn(ctx)

    return contextual_default_factory
