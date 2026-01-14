"""Core layer: immutable JSON crystals and mode semantics."""

from .json_types import (
    JsonScalar,
    JsonValue,
    JsonMapping,
    JsonArray,
    SortedJsonValue,
    sort_json_value,
)
from .freeze_value import freeze_value
from .void_value import VOID, VoidValue
from .value_api import ValueAPI
from .value_core import BaseValue
from .value_modes import StrictValue, LatentValue, DreamValue
from .value_projections import it, It, Projection

__all__ = [
    "JsonScalar",
    "JsonValue",
    "JsonMapping",
    "JsonArray",
    "SortedJsonValue",
    "sort_json_value",
    "freeze_value",
    "VOID",
    "VoidValue",
    "ValueAPI",
    "BaseValue",
    "StrictValue",
    "LatentValue",
    "DreamValue",
    "it",
    "It",
    "Projection"
]
