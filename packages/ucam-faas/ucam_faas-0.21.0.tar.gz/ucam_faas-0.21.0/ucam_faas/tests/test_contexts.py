from __future__ import annotations

from contextvars import ContextVar
from typing import Callable, Optional

import pytest
from typing_extensions import assert_type

from ucam_faas.contexts import (
    ActivateContextVarFn,
    contextual_default_factory,
    contextvar_activator,
)

EXAMPLE_CONTEXT: ContextVar[int] = ContextVar("EXAMPLE_CONTEXT")


def test_contextvar_activator() -> None:
    activate_example_context = contextvar_activator(EXAMPLE_CONTEXT)

    @activate_example_context(value=100)
    def func_with_context_active() -> None:
        assert EXAMPLE_CONTEXT.get() == 100

    # The context holds no value yet
    with pytest.raises(LookupError):
        assert EXAMPLE_CONTEXT.get()

    with activate_example_context(value=42) as activate_context_value:
        assert activate_context_value == 42
        assert EXAMPLE_CONTEXT.get() == 42

        # Contexts can be nested
        with activate_example_context(value=3) as inner_context_value:
            assert inner_context_value == 3
            assert EXAMPLE_CONTEXT.get() == 3

            func_with_context_active()

        # The old value is restored after the inner block ends
        assert EXAMPLE_CONTEXT.get() == 42

    # The context holds no value after execution leaves the with block.
    with pytest.raises(LookupError):
        assert EXAMPLE_CONTEXT.get()


class Test_contextual_default_factory:
    @pytest.fixture(scope="class")
    def activate_example_context(self) -> ActivateContextVarFn[int]:
        return contextvar_activator(EXAMPLE_CONTEXT)

    def test_overload_no_fn_no_default_fn(
        self, activate_example_context: ActivateContextVarFn[int]
    ) -> None:
        default_factory = contextual_default_factory(EXAMPLE_CONTEXT)

        assert_type(default_factory, Callable[[], int])

        with pytest.raises(LookupError):
            default_factory()

        with activate_example_context(42):
            assert default_factory() == 42

    def test_overload_no_fn(self, activate_example_context: ActivateContextVarFn[int]) -> None:
        default_factory = contextual_default_factory(EXAMPLE_CONTEXT, default_fn=lambda err: None)

        assert_type(default_factory, Callable[[], Optional[int]])

        assert default_factory() is None

        with activate_example_context(42):
            assert default_factory() == 42

    def test_overload_no_default_fn(
        self, activate_example_context: ActivateContextVarFn[int]
    ) -> None:
        default_factory = contextual_default_factory(EXAMPLE_CONTEXT, fn=lambda ctx: str(ctx))

        assert_type(default_factory, Callable[[], str])

        with pytest.raises(LookupError):
            default_factory()

        with activate_example_context(42):
            assert default_factory() == "42"

    def test_overload_fn_and_default_fn(
        self, activate_example_context: ActivateContextVarFn[int]
    ) -> None:
        default_factory = contextual_default_factory(
            EXAMPLE_CONTEXT, fn=lambda ctx: str(ctx), default_fn=lambda err: None
        )

        assert_type(default_factory, Callable[[], Optional[str]])

        assert default_factory() is None

        with activate_example_context(42):
            assert default_factory() == "42"
