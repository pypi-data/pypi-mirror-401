from __future__ import annotations

from traceback import TracebackException
from typing import TYPE_CHECKING, Annotated, Union

from pydantic import PlainSerializer

if TYPE_CHECKING:
    from typing_extensions import TypeAlias


def _serialize_exception(value: Exception | str) -> str:
    if isinstance(value, str):
        return value
    return "".join(TracebackException.from_exception(value).format())


SerialisableException: TypeAlias = Annotated[
    Union[Exception, str], PlainSerializer(_serialize_exception, when_used="json")
]
"""A Pydantic type for Exceptions that are JSON-serialised as a traceback string."""
