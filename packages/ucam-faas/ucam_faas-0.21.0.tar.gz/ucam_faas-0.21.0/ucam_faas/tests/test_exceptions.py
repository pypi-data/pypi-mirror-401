import re
import sys

import pytest

from ucam_faas.exceptions import ExecutionAbortedException, with_notes
from ucam_faas.execution_info import AbortedExecutionResult, ExecutionInfo


@pytest.mark.parametrize(
    "args, repr_template",
    [
        pytest.param(
            ("The magic smoke escaped",),
            "ExecutionAbortedException('The magic smoke escaped', execution_info={})",
            id="1 arg",
        ),
        pytest.param(
            ("The magic smoke escaped", 42),
            "ExecutionAbortedException('The magic smoke escaped', 42, execution_info={})",
            id="2 args",
        ),
    ],
)
def test_ExecutionAbortedException(args: tuple[object, ...], repr_template: str) -> None:
    execution_info = ExecutionInfo(execution=AbortedExecutionResult(reason="magicsmoke"), foo=123)
    err = ExecutionAbortedException(*args, execution_info=execution_info)

    assert err.execution_info is execution_info
    assert err.args == args
    assert repr(err) == repr_template.format(repr(execution_info))


@pytest.mark.skipif(condition=sys.version_info < (3, 11), reason="Notes are not rendered < py311")
def test_with_notes__results_in_notes_displaying_from_311() -> None:
    with pytest.raises(
        ValueError,
        match=re.compile(r"boom.*Useful context.*More info", re.MULTILINE | re.DOTALL),
    ):
        raise with_notes(ValueError("boom"), "Useful context", "More info")


@pytest.mark.skipif(condition=sys.version_info >= (3, 11), reason="Notes are rendered >= py311")
def test_with_notes__does_not_fail_pre_311() -> None:
    # we don't expect notes to render, just that they don't break
    with pytest.raises(ValueError, match=r"boom") as exc_info:
        raise with_notes(ValueError("boom"), "Useful context", "More info")

    assert "Useful context" in getattr(exc_info.value, "__notes__")
    assert "More info" in getattr(exc_info.value, "__notes__")
