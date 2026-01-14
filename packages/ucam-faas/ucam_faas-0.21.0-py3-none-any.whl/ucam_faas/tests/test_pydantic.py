import json

import pytest
from pydantic import ConfigDict, TypeAdapter

from ucam_faas.pydantic import SerialisableException


def test_SerialisableException() -> None:
    # Generate an exception to test with
    with pytest.raises(Exception) as exc_info:
        b"\xff".decode()

    adapter = TypeAdapter[SerialisableException](
        SerialisableException, config=ConfigDict(arbitrary_types_allowed=True)
    )

    # Exceptions are serialised as JSON strings containing the whole traceback
    dumped_json_value = json.loads(adapter.dump_json(exc_info.value))
    assert "Traceback (most recent call last):\n" in dumped_json_value
    assert 'b"\\xff".decode()\n' in dumped_json_value
    assert (
        "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: "
        "invalid start byte\n"
    ) in dumped_json_value

    # Exceptions remain Exceptions when dumped as Python values
    assert adapter.dump_python(exc_info.value) is exc_info.value
    assert adapter.validate_json('"UnicodeDecodeError: blah"') == "UnicodeDecodeError: blah"

    assert adapter.validate_python("UnicodeDecodeError: blah") == "UnicodeDecodeError: blah"
    assert adapter.validate_python(exc_info.value) is exc_info.value
