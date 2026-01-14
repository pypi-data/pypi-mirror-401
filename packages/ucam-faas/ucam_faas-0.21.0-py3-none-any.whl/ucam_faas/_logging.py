from __future__ import annotations

import warnings
from typing import Generator, cast

from structlog.typing import FilteringBoundLogger
from ucam_observe import get_structlog_logger as _get_structlog_logger  # type: ignore


def get_structlog_logger(name: str = "ucam_faas") -> FilteringBoundLogger:
    """Get a logger that emits a JSON object for each log call."""
    return cast(FilteringBoundLogger, _get_structlog_logger(name))


# As well as making a logger available this should setup logging before the flask app is created
logger: FilteringBoundLogger = get_structlog_logger(__name__)


class FlattenedJsonPropertyClashWarning(UserWarning):
    pass


def flatten_json(json_value: object) -> dict[str, object]:
    """
    Flatten a JSON tree into a single wide object containing scalar leaf values.

    Each value's property name is its path in the input object, joined with ".".

    Examples
    --------
    >>> wide_obj = flatten_json({
    ...     "ok": True,
    ...     "person": {"name": "Joe", "age": 100},
    ...     "pets": [
    ...         {"species": "cat", "colour": "orange"},
    ...         {"species": "dog", "size": "tiny"},
    ...     ],
    ...     "empty": {},
    ... })

    >>> import json
    >>> print(json.dumps(wide_obj, indent=2))
    {
      "ok": true,
      "person.name": "Joe",
      "person.age": 100,
      "pets.0.species": "cat",
      "pets.0.colour": "orange",
      "pets.1.species": "dog",
      "pets.1.size": "tiny"
    }

    # The flat representation is not lossless, if two values have the same
    # property path (due to one or both containing "." in their own keys) then
    # the last value will override earlier values.
    >>> import pytest
    >>> with pytest.warns(FlattenedJsonPropertyClashWarning,
    ...                   match=r'value was lost when flattening a JSON value'):
    ...     flatten_json({"foo": {"bar": 42}, "foo.bar": 100})
    {'foo.bar': 100}
    """
    if not isinstance(json_value, dict):
        json_value = {"message": json_value}

    items = [
        (".".join(map(str, path)), value)
        for (path, value) in iter_json_tree_leaves((), json_value)
    ]
    flat_props = {path: value for (path, value) in items}
    if len(items) > len(flat_props):
        warnings.warn(
            "At least one value was lost when flattening a JSON value, because "
            "two or more values have the same dot-separated property path.",
            category=FlattenedJsonPropertyClashWarning,
            stacklevel=2,
        )
    return flat_props


def iter_json_tree_leaves(
    path: tuple[str, ...], inner_node: dict[str, object] | list[object]
) -> Generator[tuple[tuple[int | str, ...], object]]:
    """
    Walk the leaf nodes (scalar values) of a JSON tree.

    This is a generator that yields tuple pairs containing:
    1. The path of the leaf node from the root to the value, as a tuple of str | int values
    2. The value
    """
    items = inner_node.items() if isinstance(inner_node, dict) else enumerate(inner_node)
    for name, value in items:
        sub_path = (*path, str(name))
        if isinstance(value, (dict, list)):
            yield from iter_json_tree_leaves(sub_path, value)
        else:
            yield (sub_path, value)
