"""Array-specific operations mixed into mode values."""

from __future__ import annotations

from typing import Callable, Sequence

from crystflux.v1.core.value_api import ValueAPI

from .json_types import JsonValue
from .value_core import BaseValue
from .value_modes import DreamValue, LatentValue, StrictValue
from .void_reason import VoidReason


class ArrayOpsMixin(BaseValue):
    """Array-only helpers with mode-aware fallbacks."""

    def first_rest(self) -> tuple[ValueAPI, ValueAPI]:
        """
        Split array into (first, rest).

        - Strict: non-array → TypeError
        - Latent/Dream: non-array → (VOID, VOID)
        - len=0 → (VOID, VOID); len=1 → (first, empty tuple)
        """
        arr = self._as_array()
        if arr is None:
            return self._handle_non_array_split()
        if len(arr) == 0:
            return (
                self._void_with_reason(VoidReason.EMPTY_SPLIT),
                self._void_with_reason(VoidReason.EMPTY_SPLIT),
            )
        if len(arr) == 1:
            return (self._spawn(arr[0]), self._spawn(tuple()))
        return (self._spawn(arr[0]), self._spawn(arr[1:]))

    def rest_last(self) -> tuple[ValueAPI, ValueAPI]:
        """
        Split array into (rest, last).

        - Strict: non-array → TypeError
        - Latent/Dream: non-array → (VOID, VOID)
        - len=0 → (VOID, VOID); len=1 → (empty tuple, last)
        """
        arr = self._as_array()
        if arr is None:
            return self._handle_non_array_split()
        if len(arr) == 0:
            return (
                self._void_with_reason(VoidReason.EMPTY_SPLIT),
                self._void_with_reason(VoidReason.EMPTY_SPLIT),
            )
        if len(arr) == 1:
            return (self._spawn(tuple()), self._spawn(arr[0]))
        return (self._spawn(arr[:-1]), self._spawn(arr[-1]))

    def map(self, fn: Callable[[ValueAPI], ValueAPI]) -> ValueAPI:
        """
        Transform each element with fn, returning a new array of the same mode.

        - Strict: non-array → TypeError
        - Latent/Dream: non-array → VOID
        """
        arr = self._require_array_or_void()
        if arr is None:
            return self._void_with_reason(VoidReason.NON_ARRAY_OPERATION)
        mapped = tuple(fn(self._spawn(elem)).as_json_value() for elem in arr)
        return self._spawn(mapped)

    def filter(self, predicate: Callable[[ValueAPI], bool]) -> ValueAPI:
        """
        Keep only elements where predicate returns True.

        - Strict: non-array → TypeError
        - Latent/Dream: non-array → VOID
        """
        arr = self._require_array_or_void()
        if arr is None:
            return self._void_with_reason(VoidReason.NON_ARRAY_OPERATION)
        filtered = tuple(elem for elem in arr if predicate(self._spawn(elem)))
        return self._spawn(filtered)

    def _handle_non_array_split(self) -> tuple[ValueAPI, ValueAPI]:
        """Non-array handling for split helpers (mode-aware)."""
        if isinstance(self, StrictValue):
            raise TypeError(
                f"Cannot split array parts from non-array type: {type(self._value).__name__}"
            )
        void = self._void_with_reason(VoidReason.TYPE_MISMATCH)
        return (void, void)

    def _require_array_or_void(self) -> Sequence[JsonValue] | None:
        """Return array when present; else TypeError (Strict) or None (Latent/Dream)."""
        arr = self._as_array()
        if arr is not None:
            return arr
        if isinstance(self, StrictValue):
            raise TypeError(f"Cannot operate on non-array type: {type(self._value).__name__}")
        return None


class StrictArrayValue(ArrayOpsMixin, StrictValue):
    """Strict mode array operations."""


class LatentArrayValue(ArrayOpsMixin, LatentValue):
    """Latent mode array operations."""


class DreamArrayValue(ArrayOpsMixin, DreamValue):
    """Dream mode array operations."""
