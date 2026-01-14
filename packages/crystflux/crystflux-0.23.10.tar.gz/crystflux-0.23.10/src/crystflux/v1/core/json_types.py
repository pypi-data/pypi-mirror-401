"""JSON type definitions and a one-hot classifier for immutable crystals."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence, Union

JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union["JsonMapping", "JsonArray", JsonScalar]
JsonMapping = Mapping[str, JsonValue]
JsonArray = Sequence[JsonValue]


@dataclass(frozen=True)
class SortedJsonValue:
    """Immutable one-hot container describing the concrete JsonValue type."""

    objects: tuple[JsonMapping, ...] = field(default_factory=tuple)
    arrays: tuple[JsonArray, ...] = field(default_factory=tuple)

    strings: tuple[str, ...] = field(default_factory=tuple)
    integers: tuple[int, ...] = field(default_factory=tuple)
    floats: tuple[float, ...] = field(default_factory=tuple)

    booleans: tuple[bool, ...] = field(default_factory=tuple)
    nulls: tuple[None, ...] = field(default_factory=tuple)


def sort_json_value(value: JsonValue) -> SortedJsonValue:
    """
    Classify a JsonValue into a SortedJsonValue (exactly one tuple populated).
    """
    if isinstance(value, Mapping):
        return SortedJsonValue(objects=(value,))
    if isinstance(value, (list, tuple)):
        return SortedJsonValue(arrays=(value,))
    if isinstance(value, str):
        return SortedJsonValue(strings=(value,))
    # bool before int to avoid bool being treated as int
    if isinstance(value, bool):
        return SortedJsonValue(booleans=(value,))
    if isinstance(value, int):
        return SortedJsonValue(integers=(value,))
    if isinstance(value, float):
        return SortedJsonValue(floats=(value,))
    if value is None:
        return SortedJsonValue(nulls=(None,))

    if isinstance(value, set):
        raise TypeError(
            f"JSON does not support set type. "
            f"Convert to list or tuple first:\n"
            f"  Crystallizer.strict(tuple({value!r}))"
        )

    raise TypeError(
        f"Unsupported type for JsonValue: {type(value).__name__}\n"
        f"Supported types: dict, list, tuple, str, int, float, bool, None"
    )

__all__ = [
    "JsonScalar",
    "JsonValue",
    "JsonMapping",
    "JsonArray",
    "SortedJsonValue",
    "sort_json_value",
]
