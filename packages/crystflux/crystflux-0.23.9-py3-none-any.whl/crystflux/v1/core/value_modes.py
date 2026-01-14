"""Mode-specific value semantics (Strict / Latent / Dream)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Protocol, Tuple



from .json_types import JsonValue
from .value_core import BaseValue
from .void_value import VOID
from .value_api import ValueAPI
from .void_reason import VoidReason


class MissingHook(Protocol):
    """Hook called when a missing key/index is observed.

    `target` is the parent container where the missing access occurred:
    - `get(key)` -> the object (mapping)
    - `at(index)` -> the array (sequence)
    """

    def __call__(
        self,
        *,
        reason: VoidReason,
        target: JsonValue,
        key: str | None = None,
        index: int | None = None,
    ) -> None: ...


@dataclass(frozen=True)
class StrictValue(BaseValue):
    """Fail-fast semantics for production-critical paths."""

    # BaseValue behaviors already raise on type/key/index errors.

    def _void(self) -> ValueAPI:
        return VOID


@dataclass(frozen=True)
class LatentValue(BaseValue):
    """Missing or mismatched data collapses to VOID while keeping the chain alive."""

    on_missing: MissingHook | None = None

    def get(self, key: str) -> ValueAPI:
        obj = self._as_object()
        if obj is None:
            return self._void_with_reason(VoidReason.TYPE_MISMATCH)
        if key not in obj:
            self._notify_missing(VoidReason.MISSING_KEY, obj, key=key)
            return self._void_with_reason(VoidReason.MISSING_KEY)
        return self._spawn(obj[key])

    def at(self, index: int) -> ValueAPI:
        arr = self._as_array()
        if arr is None:
            return self._void_with_reason(VoidReason.TYPE_MISMATCH)
        if not (0 <= index < len(arr)):
            self._notify_missing(VoidReason.MISSING_INDEX, arr, index=index)
            return self._void_with_reason(VoidReason.MISSING_INDEX)
        return self._spawn(arr[index])

    def _void(self) -> ValueAPI:
        return VOID

    def inherit_kwargs(self) -> dict[str, Any]:
        # NOTE: `_spawn()` propagates telemetry/config via `inherit_kwargs()`; keep `on_missing` across
        # spawned values.
        kwargs = super().inherit_kwargs()
        kwargs["on_missing"] = self.on_missing
        return kwargs

    def _notify_missing(
        self,
        reason: VoidReason,
        target: JsonValue,
        *,
        key: str | None = None,
        index: int | None = None,
    ) -> None:
        """
        Best-effort missing hook.

        v1 scope: called only for MISSING_KEY / MISSING_INDEX.
        """
        if self.on_missing is None:
            return
        try:
            # NOTE: `target` is the parent container where the miss occurred (object/array), not
            # `self._value`. This maps to `MissingEvent.target_type/target_repr` in the adapters hook.
            self.on_missing(reason=reason, target=target, key=key, index=index)
        except Exception:
            # Never break chains due to telemetry/logging errors.
            pass


@dataclass(frozen=True)
class DreamValue(LatentValue):
    """Hallucination-tolerant mode; undefined methods collapse to VOID and can be observed."""

    on_desire: Callable[[str, JsonValue, tuple[str, ...]], None] | None = None
    chain_steps: Tuple[str, ...] = ()

    def get(self, key: str) -> ValueAPI:
        if self.is_void():
            return self
        # Missing handling (and `on_missing` notifications) happens in LatentValue via `super()`.
        return super().get(key)

    def at(self, index: int) -> ValueAPI:
        if self.is_void():
            return self
        # Missing handling (and `on_missing` notifications) happens in LatentValue via `super()`.
        return super().at(index)

    def __getattr__(self, name: str) -> "_VoidCallable":
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return _VoidCallable(self, name)

    def _void_with_reason(self, reason: VoidReason) -> ValueAPI:
        if self.is_void_reasoning_enabled():
            return self.spawn_void(self.chain_steps, reason=reason)
        return self._void()

    def _spawn(self, value: JsonValue) -> "DreamValue":
        return type(self)(
            value,
            on_desire=self.on_desire,
            on_missing=self.on_missing,
            chain_steps=self.chain_steps,
            _void_reason=self._void_reason,
            _void_reasoning_enabled=self._void_reasoning_enabled,
        )

    def inherit_kwargs(self) -> dict[str, Any]:
        return {
            "on_desire": self.on_desire,
            "on_missing": self.on_missing,
            "chain_steps": self.chain_steps,
            "_void_reason": self._void_reason,
            "_void_reasoning_enabled": self._void_reasoning_enabled,
        }

    def spawn_void(
        self, chain_steps: tuple[str, ...], *, reason: VoidReason | None = None
    ) -> DreamValue:
        return type(self)(
            VOID.as_json_value(),
            on_desire=self.on_desire,
            on_missing=self.on_missing,
            chain_steps=chain_steps,
            _void_reason=reason if self._void_reasoning_enabled else None,
            _void_reasoning_enabled=self._void_reasoning_enabled,
        )

    def is_void(self) -> bool:
        # NOTE: Dream treats `_value is None` as void (so JSON null is void-like here).
        # If null-vs-missing matters, do that step in Strict/Latent (null is a value; VOID is
        # distinguishable), or change Dream to use an explicit void flag.
        # Accept this as the current behavior (we know AIs tend to get confused here). If a clearer
        # yet compatible design emerges, we will swap the internals. Details: TECH_NOTES.md
        #
        # JA: 今は、現段階での仕様として受け入れてください（ここでAIコーダーが迷いやすい点は把握しています）。
        # より分かりやすく、かつ互換性も保てる良い設計が思いついたら、内部実装を差し替えます。詳細: TECH_NOTES.md
        return self._value is None


    def has_value(self) -> bool:
        return not self.is_void()

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return not self.is_void()

    # Dream tolerates array splits without explicit to_array to avoid chain breaks
    def first_rest(self) -> tuple[ValueAPI, ValueAPI]:
        arr = self.to_array()
        from .value_array import DreamArrayValue, LatentArrayValue, StrictArrayValue
        if isinstance(arr, (StrictArrayValue, LatentArrayValue, DreamArrayValue)):
            return arr.first_rest()
        return (VOID, VOID)

    def rest_last(self) -> tuple[ValueAPI, ValueAPI]:
        arr = self.to_array()
        from .value_array import DreamArrayValue, LatentArrayValue, StrictArrayValue
        if isinstance(arr, (StrictArrayValue, LatentArrayValue, DreamArrayValue)):
            return arr.rest_last()
        return (VOID, VOID)


class _VoidCallable:
    """Callable proxy that logs desire and returns a void DreamValue."""

    def __init__(self, owner: DreamValue, method_name: str) -> None:
        self._owner = owner
        self._method_name = method_name

    def __call__(self, *args: Any, **kwargs: Any) -> BaseValue:
        if self._owner.on_desire:
            # Pass the method name and a minimal descriptor (the current raw value)
            self._owner.on_desire(self._method_name, self._owner.as_json_value(), self._chain_steps())
        reason = VoidReason.DESIRE_CALL if self._owner.is_void_reasoning_enabled() else None
        return self._owner.spawn_void(self._chain_steps(), reason=reason)

    def _chain_steps(self) -> tuple[str, ...]:
        return self._owner.chain_steps + (self._method_name,)


__all__ = ["StrictValue", "LatentValue", "DreamValue"]
