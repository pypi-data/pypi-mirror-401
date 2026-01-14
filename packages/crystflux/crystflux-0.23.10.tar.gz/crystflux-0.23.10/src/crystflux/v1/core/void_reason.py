from __future__ import annotations

from enum import Enum


class VoidReason(str, Enum):
    MISSING_KEY = "missing_key"
    MISSING_INDEX = "missing_index"
    TYPE_MISMATCH = "type_mismatch"
    NON_ARRAY_OPERATION = "non_array_operation"
    DESIRE_CALL = "desire_call"
    EMPTY_SPLIT = "empty_split"


__all__ = ["VoidReason"]
