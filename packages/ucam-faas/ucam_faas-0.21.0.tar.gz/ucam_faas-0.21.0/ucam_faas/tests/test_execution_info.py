from dataclasses import dataclass

from ucam_faas.execution_info import (
    AbortedExecutionReason,
    AbortedExecutionResult,
    CompletedExecutionResult,
    ExecutionInfo,
    ExecutionStatus,
)


class TestCompletedExecutionResult:
    def test_init(self) -> None:
        result = CompletedExecutionResult()
        assert result.status is ExecutionStatus.COMPLETED
        assert result.duration_seconds is None

        result = CompletedExecutionResult(duration_seconds=1.5)
        assert result.duration_seconds == 1.5


class TestAbortedExecutionResult:
    def test_init(self) -> None:
        err = ValueError("Oops")
        result = AbortedExecutionResult(
            reason=AbortedExecutionReason.USER_DATA_INVALID,
            exception=err,
            duration_seconds=1.5,
        )
        assert result.status is ExecutionStatus.ABORTED
        assert result.reason is AbortedExecutionReason.USER_DATA_INVALID
        assert result.exception is err
        assert result.duration_seconds == 1.5

        result = AbortedExecutionResult(reason="custom.reason")
        assert result.status is ExecutionStatus.ABORTED
        assert result.reason == "custom.reason"
        assert result.exception is None
        assert result.duration_seconds is None


class TestExecutionInfo:
    @dataclass
    class CustomAttributes:
        size: int
        label: str

    def test_init(self) -> None:
        execinfo = ExecutionInfo()
        assert execinfo.execution == CompletedExecutionResult()

        execinfo = ExecutionInfo(
            execution=AbortedExecutionResult(
                reason=AbortedExecutionReason.USER_DATA_INVALID, exception=ValueError("Oops")
            )
        )
        assert execinfo.execution.status is ExecutionStatus.ABORTED
        assert isinstance(execinfo.execution.exception, ValueError)

    def test_arbitrary_attributes(self) -> None:
        """ExecutionInfo models can hold arbitrary attributes without subclassing."""
        custom = TestExecutionInfo.CustomAttributes(size=42, label="foo")
        execinfo = ExecutionInfo(custom_stuff=custom)

        assert execinfo.custom_stuff == custom  # type: ignore[attr-defined]
        assert execinfo.model_extra is not None
        assert execinfo.model_extra["custom_stuff"] == custom

        assert execinfo.model_dump(mode="json") == {
            "execution": {"duration_seconds": None, "status": "COMPLETED"},
            "custom_stuff": {"label": "foo", "size": 42},
        }

    def test_from_context(self) -> None:
        assert ExecutionInfo.from_context(execution=CompletedExecutionResult()) == ExecutionInfo(
            execution=CompletedExecutionResult()
        )
