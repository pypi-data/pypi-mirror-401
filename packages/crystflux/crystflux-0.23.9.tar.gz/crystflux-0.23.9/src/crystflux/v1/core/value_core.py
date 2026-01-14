"""Base immutable value wrapper for JSON crystals."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from .value_api import ValueAPI
from .freeze_value import freeze_value
from .json_types import JsonScalar, JsonValue, SortedJsonValue, sort_json_value
from .void_reason import VoidReason


@dataclass(frozen=True)
class BaseValue(ValueAPI):
    """Shared mechanics: freezing, classification, and type-safe accessors."""

    _value: JsonValue
    _sorted: SortedJsonValue = field(init=False, repr=False)
    _void_reason: VoidReason | None = field(default=None, repr=False)
    _void_reasoning_enabled: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        frozen_val = freeze_value(self._value)
        object.__setattr__(self, "_value", frozen_val)
        object.__setattr__(self, "_sorted", sort_json_value(frozen_val))

    # Navigation helpers (to be specialized by modes)
    def get(self, key: str) -> "ValueAPI":
        obj = self._as_object()
        if obj is None:
            raise TypeError(
                f"Cannot get key '{key}' from non-object type: {type(self._value).__name__}"
            )
        if key not in obj:
            raise KeyError(key)
        return self._spawn(obj[key])

    def at(self, index: int) -> "ValueAPI":
        arr = self._as_array()
        if arr is None:
            raise TypeError(
                f"Cannot get index {index} from non-array type: {type(self._value).__name__}"
            )
        if not (0 <= index < len(arr)):
            raise IndexError("Array index out of range")
        return self._spawn(arr[index])

    # Safe accessors
    def as_str(self) -> str | None:
        return self._sorted.strings[0] if self._sorted.strings else None

    def as_int(self) -> int | None:
        return self._sorted.integers[0] if self._sorted.integers else None

    def as_float(self) -> float | None:
        return self._sorted.floats[0] if self._sorted.floats else None

    def as_bool(self) -> bool | None:
        return self._sorted.booleans[0] if self._sorted.booleans else None

    def as_str_array(self) -> tuple[str, ...] | None:
        """
        Return this value as a tuple of strings, or None when not an array.
        """
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            return None
        strings: list[str] = []
        for elem in arr:
            if isinstance(elem, str):
                strings.append(elem)
        return tuple(strings)

    def as_int_array(self) -> tuple[int, ...] | None:
        """
        Return this value as a tuple of ints, or None when not an array.

        Uses exact int checks to avoid treating bools as integers.
        """
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            return None
        ints: list[int] = []
        for elem in arr:
            if type(elem) is int:  # avoid bool
                ints.append(elem)
        return tuple(ints)

    def as_float_array(self) -> tuple[float, ...] | None:
        """
        Return this value as a tuple of floats, or None when not an array.
        """
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            return None
        floats: list[float] = []
        for elem in arr:
            if isinstance(elem, float):
                floats.append(elem)
        return tuple(floats)

    def as_scalars(self) -> tuple[JsonScalar, ...] | None:
        """
        Return this value as a tuple of JSON scalars, or None when not an array.
        """
        arr = self._as_array()
        if arr is None:
            return None
        collected: list[JsonScalar] = []
        self._collect_scalars(arr, collected)
        return tuple(collected)

    def to_array(self) -> ValueAPI:
        """
        Promote this value into an ArrayValue of the same mode (Strict/Latent/Dream).

        - Strict: non-array → TypeError
        - Latent/Dream: non-array → VOID
        """
        from .value_modes import DreamValue, LatentValue, StrictValue  # avoid cycle
        from .value_array import DreamArrayValue, LatentArrayValue, StrictArrayValue

        arr = self._as_array()
        if arr is None:
            if isinstance(self, StrictValue):
                raise TypeError(f"Cannot treat non-array as array: {type(self._value).__name__}")
            return self._void_with_reason(VoidReason.NON_ARRAY_OPERATION)

        kwargs = self.inherit_kwargs()
        # Use exact type checks to avoid DreamValue being caught by LatentValue
        if type(self) is StrictValue:
            return StrictArrayValue(arr, **kwargs)
        if type(self) is DreamValue:
            return DreamArrayValue(arr, **kwargs)
        if type(self) is LatentValue:
            return LatentArrayValue(arr, **kwargs)
        return self._spawn(arr)

    def map(self, fn: Callable[[ValueAPI], ValueAPI]) -> ValueAPI:
        """
        Apply fn to each array element in this value's mode; follows to_array semantics.
        """
        return self.to_array().map(fn)

    def filter(self, predicate: Callable[[ValueAPI], bool]) -> ValueAPI:
        """
        Keep only elements where predicate returns True; follows to_array semantics.
        """
        return self.to_array().filter(predicate)

    def first_rest(self) -> tuple["ValueAPI", "ValueAPI"]:
        """
        Split array into (first, rest) in this value's mode; follows to_array semantics.
        """
        return self.to_array().first_rest()

    def rest_last(self) -> tuple["ValueAPI", "ValueAPI"]:
        """
        Split array into (rest, last) in this value's mode; follows to_array semantics.
        """
        return self.to_array().rest_last()

    # Strict accessors
    def expected_str(self) -> str:
        if self._sorted.strings:
            return self._sorted.strings[0]
        raise TypeError(f"Expected a string, but got {type(self._value).__name__}")

    def expected_int(self) -> int:
        if self._sorted.integers:
            return self._sorted.integers[0]
        raise TypeError(f"Expected an integer, but got {type(self._value).__name__}")

    def expected_float(self) -> float:
        if self._sorted.floats:
            return self._sorted.floats[0]
        raise TypeError(f"Expected a float, but got {type(self._value).__name__}")

    def expected_bool(self) -> bool:
        if self._sorted.booleans:
            return self._sorted.booleans[0]
        raise TypeError(f"Expected a boolean, but got {type(self._value).__name__}")

    def expected_str_array(self) -> tuple[str, ...]:
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            raise TypeError(f"Expected an array of strings, but got {type(self._value).__name__}")

        strings: list[str] = []
        for elem in arr:
            if not isinstance(elem, str):
                raise TypeError(f"Expected an array of strings, but found {type(elem).__name__}")
            strings.append(elem)
        return tuple(strings)

    def expected_int_array(self) -> tuple[int, ...]:
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            raise TypeError(f"Expected an array of integers, but got {type(self._value).__name__}")

        ints: list[int] = []
        for elem in arr:
            if type(elem) is not int:  # avoid bool
                raise TypeError(f"Expected an array of integers, but found {type(elem).__name__}")
            ints.append(elem)
        return tuple(ints)

    def expected_float_array(self) -> tuple[float, ...]:
        arr = self._sorted.arrays[0] if self._sorted.arrays else None
        if arr is None:
            raise TypeError(f"Expected an array of floats, but got {type(self._value).__name__}")
        floats: list[float] = []
        for elem in arr:
            if not isinstance(elem, float):
                raise TypeError(f"Expected an array of floats, but found {type(elem).__name__}")
            floats.append(elem)
        return tuple(floats)

    # Raw value access
    def as_json_value(self) -> JsonValue:
        return self._value

    def with_value(self, value: JsonValue) -> "ValueAPI":
        """Return a new Value in the same mode/config wrapping value."""
        return self._spawn(value)

    # State
    def is_void(self) -> bool:
        return False

    def has_value(self) -> bool:
        return True

    def is_void_reasoning_enabled(self) -> bool:
        return self._void_reasoning_enabled

    def void_reason(self) -> VoidReason | None:
        return self._void_reason

    # Internal helpers
    def inherit_kwargs(self) -> dict[str, Any]:
        """Keyword args to propagate into spawned sibling values (override in subclasses)."""
        return {
            "_void_reason": self._void_reason,
            "_void_reasoning_enabled": self._void_reasoning_enabled,
        }

    def _spawn(self, value: JsonValue) -> "ValueAPI":
        return type(self)(value, **self.inherit_kwargs())

    def _as_object(self) -> Mapping[str, JsonValue] | None:
        return self._sorted.objects[0] if self._sorted.objects else None

    def _as_array(self) -> Sequence[JsonValue] | None:
        return self._sorted.arrays[0] if self._sorted.arrays else None

    def _void(self) -> "ValueAPI":
        raise NotImplementedError

    def _void_with_reason(self, reason: VoidReason) -> "ValueAPI":
        if self._void_reasoning_enabled:
            from .void_value import ReasonedVoid

            return ReasonedVoid(reason=reason)
        return self._void()

    def _collect_scalars(self, arr: Sequence[JsonValue], out: list[JsonScalar]) -> None:
        for elem in arr:
            if isinstance(elem, bool):
                out.append(elem)
                continue
            if type(elem) is int:
                out.append(elem)
                continue
            if isinstance(elem, float):
                out.append(elem)
                continue
            if isinstance(elem, str):
                out.append(elem)
                continue
            if elem is None:
                out.append(elem)
                continue
            if isinstance(elem, Mapping):
                continue
            if isinstance(elem, Sequence):
                self._collect_scalars(elem, out)


__all__ = ["BaseValue"]
