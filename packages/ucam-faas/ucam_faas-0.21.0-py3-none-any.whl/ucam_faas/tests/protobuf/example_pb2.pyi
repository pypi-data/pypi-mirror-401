from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class ExampleRecord(_message.Message):
    __slots__ = ["page_number", "query", "results_per_page"]
    PAGE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RESULTS_PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    page_number: int
    query: str
    results_per_page: int
    def __init__(
        self,
        query: _Optional[str] = ...,
        page_number: _Optional[int] = ...,
        results_per_page: _Optional[int] = ...,
    ) -> None: ...
