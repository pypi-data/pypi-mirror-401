"""Protocol describing the public Value API (including array helpers).

Note: Implementation understanding or feature addition should start from this file.

For technical notes and design decisions, see:
    src/crystflux/v1/core/TECH_NOTES.md
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Protocol, Sequence

from .json_types import JsonScalar, JsonValue
from .void_reason import VoidReason


class ValueAPI(Protocol):
    """Public surface shared by Value implementations (including VOID)."""

    # --- Navigation --------------------------------------------------------------
    def get(self, key: str) -> "ValueAPI":
        """Strict raises on missing/non-object; Latent/Dream collapse to VOID."""
        ...

    def at(self, index: int) -> "ValueAPI":
        """Strict raises on missing/non-array; Latent/Dream collapse to VOID."""
        ...

    # --- Array Operations --------------------------------------------------------
    # NOTE: See BaseValue.to_array() (core/value_core.py). Array operations go through it; values
    # do not auto-switch to an ArrayValue by content. It also defines the non-array fallback:
    # Strict raises; Latent/Dream return VOID.
    def first_rest(self) -> tuple["ValueAPI", "ValueAPI"]:
        """
        Split array; Strict errors on non-array, Latent/Dream return (VOID, VOID).
        len=0 → (VOID, VOID); len=1 → (first, empty tuple).
        """
        ...

    def rest_last(self) -> tuple["ValueAPI", "ValueAPI"]:
        """
        Split array tail; Strict errors on non-array, Latent/Dream return (VOID, VOID).
        len=0 → (VOID, VOID); len=1 → (empty tuple, last).
        """
        ...

    def map(self, fn: Callable[["ValueAPI"], "ValueAPI"]) -> "ValueAPI":
        """Apply fn per element; Strict errors on non-array, Latent/Dream return VOID."""
        ...

    def filter(self, predicate: Callable[["ValueAPI"], bool]) -> "ValueAPI":
        """Keep elements by predicate; Strict errors on non-array, Latent/Dream return VOID."""
        ...

    def to_array(self) -> "ValueAPI":
        """Promote to ArrayValue; Strict errors on non-array, Latent/Dream return VOID."""
        ...

    # --- Safe Accessors ----------------------------------------------------------
    # Safe accessors return None on mismatch or missing elements.
    # For array length, use: `len(value.as_str_array() or ())`
    #
    # Example patterns:
    #   Crystallizer.latent(42).as_int() → 42
    #   Crystallizer.latent(42).as_str() → None
    #   Crystallizer.latent({"a": 1}).as_str_array() → None
    #   len(Crystallizer.latent(["a", "b"]).as_str_array() or ()) → 2
    #   len(Crystallizer.latent(["a", "b", 8]).as_str_array() or ()) → 2

    # Safe Scalars
    def as_str(self) -> str | None:
        """Return first string or None (Strict also returns None to mirror safe access)."""
        ...

    def as_int(self) -> int | None:
        """Return first int or None (Strict also returns None to mirror safe access)."""
        ...

    def as_float(self) -> float | None:
        """Return first float or None (Strict also returns None to mirror safe access)."""
        ...

    def as_bool(self) -> bool | None:
        """Return first bool or None (Strict also returns None to mirror safe access)."""
        ...

    # Safe Arrays
    def as_str_array(self) -> tuple[str, ...] | None:
        """
        Return tuple of strings or None (non-array → None; non-strings are skipped).
        """
        ...

    def as_int_array(self) -> tuple[int, ...] | None:
        """
        Return tuple of ints or None (non-array → None; non-ints are skipped).
        """
        ...

    def as_float_array(self) -> tuple[float, ...] | None:
        """
        Return tuple of floats or None (non-array → None; non-floats are skipped).
        """
        ...

    def as_scalars(self) -> tuple[JsonScalar, ...] | None:
        """
        Return tuple of JSON scalars or None (non-array → None; non-scalars are skipped).
        """
        ...

    # --- Expected Accessors ------------------------------------------------------
    # Expected accessors raise TypeError on non-array or VOID.
    #
    # Example patterns:
    #   Crystallizer.strict(42).expected_int() → 42
    #   Crystallizer.strict(42).expected_str() → raises TypeError
    #   Crystallizer.strict({"a": 1}).expected_str_array() → raises TypeError
    #   len(Crystallizer.strict(["a", "b"]).expected_str_array()) → 2
    #   len(Crystallizer.strict(["a", "b", 8]).expected_str_array()) → raises TypeError

    # Expected Scalars
    def expected_str(self) -> str:
        """Require a string; raises TypeError on mismatch/VOID."""
        ...

    def expected_int(self) -> int:
        """Require an int; raises TypeError on mismatch/VOID."""
        ...

    def expected_float(self) -> float:
        """Require a float; raises TypeError on mismatch/VOID."""
        ...

    def expected_bool(self) -> bool:
        """Require a bool; raises TypeError on mismatch/VOID."""
        ...

    # Expected Arrays
    def expected_str_array(self) -> tuple[str, ...]:
        """Require an array of strings; raises TypeError on mismatch/VOID."""
        ...

    def expected_int_array(self) -> tuple[int, ...]:
        """Require an array of ints; raises TypeError on mismatch/VOID."""
        ...

    def expected_float_array(self) -> tuple[float, ...]:
        """Require an array of floats; raises TypeError on mismatch/VOID."""
        ...

    # --- Immutable Helpers ------------------------------------------------------
    def with_value(self, value: JsonValue) -> "ValueAPI":
        """Return a new Value in the same mode/config wrapping value."""
        ...

    # --- Raw / State / Diagnostics ----------------------------------------------
    def as_json_value(self) -> JsonValue: ...
    def is_void(self) -> bool: ...
    def has_value(self) -> bool: ...
    def is_void_reasoning_enabled(self) -> bool: ...
    def void_reason(self) -> VoidReason | None: ...

    # --- Internal Helpers --------------------------------------------------------
    def _spawn(self, value: JsonValue) -> "ValueAPI": ...
    def inherit_kwargs(self) -> dict[str, Any]: ...
    def _as_object(self) -> Mapping[str, JsonValue] | None: ...
    def _as_array(self) -> Sequence[JsonValue] | None: ...
    def _void(self) -> "ValueAPI": ...
