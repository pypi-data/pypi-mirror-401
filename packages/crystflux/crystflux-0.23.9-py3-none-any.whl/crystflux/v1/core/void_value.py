"""Null object representing absence/failure without breaking chains."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from .value_api import ValueAPI
from .json_types import JsonScalar, JsonValue, SortedJsonValue, sort_json_value
from .freeze_value import freeze_value
from .void_reason import VoidReason

"""
[Philosophy]
無為而無不為
VOIDとは無為にして為さざるなし
In the implementation, the singleton `VOID = VoidValue(None)` is falsy and absorbs every chain;
`get`, `at`, `to_array`, `map`, and `filter` all return itself.

無名天地之始；有名萬物之母
VOIDは観測されるまで名を持たず、名は観測者から与えられる
For example, `LatentValue.get` calls `_void_with_reason(VoidReason.MISSING_KEY)`, which stays as plain
`VOID` unless `_void_reasoning_enabled` is on, in which case it becomes a reasoned void with a name.

是亦彼也，彼亦是也；彼亦一是非，此亦一是非
VOIDへの命名が差異を生み、差異が意味を生むが、その意味は視点の数だけ存在する
The same operation means different things by viewpoint: `StrictValue.to_array()` raises `TypeError`
on a non-array, while `LatentValue` returns the silent `VOID` and `DreamValue` returns a
desire-aware (optionally reasoned) `VOID`, so even `VOID`'s "truth" exists only relative to the
chosen mode.

   Truth depends on the viewpoint (Mode).
   - StrictValue: Raises TypeError (Rejects the Void)
   - LatentValue: Returns silent VOID (Accepts the Void)
   - DreamValue: Returns desire-aware VOID (Observes the Void)
   Even `VOID`'s meaning exists only relative to the chosen observer.

※AIに理解してもらうために試行錯誤した結果出来上がったプロンプト。
AIエージェントは隙あらば既存のパターンで実装を始めるので、手法模索時に早期収束への執着から引きはがすためには工夫が必要。
※老荘思想の概念を使うと複雑な構造でも、AIコーディングがスムーズに流れやすい（現時点では個人的な経験則）。
早期収束への抵抗性が増すためと思われるが、原因を追及するとかなり深い沼になりそうなので本格的な研究（検証・再現性）は後回し。
※哲学語彙が推論ハブになりAIの視野が広くなるという仮説を提唱してみたい。

---

Notes:
- おそらく、Voidは本質的に定義できない。完全に定義されたVoidはVoidではなくなる。
　　定義は境界線を作るが、Voidは境界線を溶かす。ここに矛盾が発生し、言語や記号体系の限界が顕現化する。
- このようなVoid実装概念をAIに理解させようとすると、当然ながら混乱させることになる（プロンプト次第ではあるが、AIは基本的に矛盾の保持が苦手）。
　　ここでは、コメントで抽象的な哲学語彙を重ねることで本質に近づく試みを行っている。
- 明確で具体的な指示を出すというセオリーからは外れる。しかし、この手法を用いることで、AIの書く実装が比較的イメージに近いものとなった。
　　なので、今はこれで良しとする（ただし、ミクロな実装を妨げないように、抽象考察領域はメタ認識しておく必要がある）。
"""


@dataclass(frozen=True)
class VoidValue(ValueAPI):
    """Null object that absorbs navigation and evaluates falsy.

    Note: The canonical VOID singleton never carries a reason; reasoned variants
    (ReasonedVoid or DreamValue(None, ...)) are only created when void reasoning
    is explicitly enabled.

    Meta-Design:
        When Void is used in "isolation," the following risk states manifest:

        Primary risk states:
        - Operations infinitely return themselves, with no discernible end
        - Type information fails to propagate, dissolving into ambiguity
        - The originating cause of Void becomes untraceable

        Mitigation of these risks lies beyond the responsibility of this class.
        Concrete examples here would generate early convergence pressure,
        constraining creative possibilities within the adapter layer.

        Countermeasures depend entirely on adapter‑layer context;
        therefore we deliberately refrain from indicating specific directions.
        This class adheres to the principle of wu wei (non‑action).
    """

    _value: JsonValue
    _sorted: SortedJsonValue = field(init=False, repr=False)

    def __post_init__(self) -> None:
        frozen_val = freeze_value(self._value)
        object.__setattr__(self, "_value", frozen_val)
        object.__setattr__(self, "_sorted", sort_json_value(frozen_val))

    def __bool__(self) -> bool:  # pragma: no cover - trivial
        return False

    # Navigation helpers
    def get(self, key: str) -> "VoidValue":
        return self

    def at(self, index: int) -> "VoidValue":
        return self

    def first_rest(self) -> tuple["VoidValue", "VoidValue"]:
        return (self, self)

    def rest_last(self) -> tuple["VoidValue", "VoidValue"]:
        return (self, self)

    def to_array(self) -> "VoidValue":
        return self

    def map(self, fn: Callable[[ValueAPI], ValueAPI]) -> "VoidValue":
        return self

    def filter(self, predicate: Callable[[ValueAPI], bool]) -> "VoidValue":
        return self

    # Safe accessors
    def as_str(self) -> str | None:
        return None

    def as_int(self) -> int | None:
        return None

    def as_float(self) -> float | None:
        return None

    def as_bool(self) -> bool | None:
        return None

    def as_str_array(self) -> tuple[str, ...] | None:
        return None

    def as_int_array(self) -> tuple[int, ...] | None:
        return None

    def as_float_array(self) -> tuple[float, ...] | None:
        return None

    def as_scalars(self) -> tuple[JsonScalar, ...] | None:
        return None

    # Strict accessors
    def expected_str(self) -> str:
        raise TypeError("VOID has no string value")

    def expected_int(self) -> int:
        raise TypeError("VOID has no integer value")

    def expected_float(self) -> float:
        raise TypeError("VOID has no float value")

    def expected_bool(self) -> bool:
        raise TypeError("VOID has no boolean value")

    def expected_str_array(self) -> tuple[str, ...]:
        raise TypeError("VOID has no array of strings")

    def expected_int_array(self) -> tuple[int, ...]:
        raise TypeError("VOID has no array of integers")

    def expected_float_array(self) -> tuple[float, ...]:
        raise TypeError("VOID has no array of floats")

    # Raw
    def as_json_value(self) -> JsonValue:
        return None

    def with_value(self, value: JsonValue) -> "VoidValue":
        # VOID absorbs changes; do not allow revival via with_value.
        return self

    # State
    def is_void(self) -> bool:
        return True

    def has_value(self) -> bool:
        return False

    def is_void_reasoning_enabled(self) -> bool:
        """VOID singleton never records reasons."""
        return False

    def void_reason(self) -> VoidReason | None:
        """VOID singleton never carries a reason."""
        return None

    # Helpers
    def inherit_kwargs(self) -> dict[str, Any]:
        return {}

    # Internal helpers to keep Void stable
    def _spawn(self, value: JsonValue) -> "VoidValue":
        return self

    def __getattr__(self, name: str) -> "VoidValue":
        return self

    def __getitem__(self, key: Any) -> "VoidValue":
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> "VoidValue":
        return self

    # Add to VoidValue in void_value.py
    def _as_object(self) -> Mapping[str, JsonValue] | None:
        return None

    def _as_array(self) -> Sequence[JsonValue] | None:
        return None

    def _void(self) -> "ValueAPI":
        return self


class ReasonedVoid(VoidValue):
    """VoidValue carrying a reason code (non-singleton; opt-in only)."""

    def __init__(self, reason: VoidReason) -> None:
        super().__init__(None)
        object.__setattr__(self, "reason", reason)

    def void_reason(self) -> VoidReason | None:  # type: ignore[override]
        return getattr(self, "reason", None)


VOID = VoidValue(None)

__all__ = ["VoidValue", "VOID", "ReasonedVoid"]
