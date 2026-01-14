"""Recursive freezer to enforce deep immutability for JsonValue."""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping

from .json_types import JsonValue


def freeze_value(value: JsonValue) -> JsonValue:
    """Recursively freeze mappings, lists, and tuples for JSON-like values.

    Ensures deep immutability for all JSON types:
    - Mappings become read-only via MappingProxyType.
    - Lists and tuples become tuples with recursively frozen contents.
    - Scalars (str, int, float, bool, None) are returned unchanged.

    Note:
        Tuples are immutable as containers but may hold mutable elements; those are
        recursively frozen here.
    """
    if isinstance(value, Mapping):
        return MappingProxyType({k: freeze_value(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze_value(v) for v in value)
    return value


__all__ = ["freeze_value"]
