from __future__ import annotations

from typing import TypeVar

from ucam_faas.execution_info import ExecutionInfo


class UCAMFAASException(Exception):
    pass


class UCAMFAASCouldNotProcess(UCAMFAASException):
    pass


class UCAMFAASCouldNotLoadTarget(UCAMFAASException):
    pass


class ExecutionAbortedException(UCAMFAASException):
    execution_info: ExecutionInfo

    def __init__(self, *args: object, execution_info: ExecutionInfo) -> None:
        super().__init__(*args)
        self.execution_info = execution_info

    def __repr__(self) -> str:
        args_repr = f"{repr(self.args)[1:-1].rstrip(',')}, " if self.args else ""
        kwargs_repr = f"execution_info={self.execution_info!r}"
        return f"{self.__class__.__name__}({args_repr}{kwargs_repr})"


_ExceptionT = TypeVar("_ExceptionT", bound=BaseException)


def with_notes(exc: _ExceptionT, *notes: str) -> _ExceptionT:
    """
    Attach note strings to an Exception and return it.

    Versions of Python before 3.11 will not render notes in tracebacks, but will
    still have them attached in `__notes__`.
    """
    if not notes:
        return exc
    all_notes: list[str] = exc.__dict__.setdefault("__notes__", [])
    all_notes.extend(notes)
    return exc
