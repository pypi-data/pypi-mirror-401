"""ValueAPI projection helpers for lambda omission (op-chain style).

None handling:
- as_* comparisons treat None as False (predicate returns False).
- expected_* comparisons raise TypeError when the projected value is None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Literal, TypeAlias

from .value_api import ValueAPI

OpTag = Literal["get", "at"]
Scalar = int | float | bool | None


@dataclass(frozen=True)
class Op:
    """Single projection step."""

    tag: OpTag
    payload: str | int


@dataclass(frozen=True)
class Projection:
    """Chainable projection for ValueAPI."""

    ops: tuple[Op, ...] = ()

    def get(self, key: str) -> "Projection":
        """Return a new Projection with get(key) appended."""
        return self._append(Op("get", key))

    def at(self, index: int) -> "Projection":
        """Return a new Projection with at(index) appended."""
        return self._append(Op("at", index))

    def __getattr__(self, name: str) -> "Projection":
        """Attribute sugar: it.name -> it.get("name")."""
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return self.get(name)

    def __getitem__(self, index: int) -> "Projection":
        """Index sugar: it[index] -> it.at(index)."""
        return self.at(index)

    def __call__(self, value: ValueAPI) -> ValueAPI:
        """Apply ops left-to-right on a ValueAPI."""
        current = value
        for op in self.ops:
            if op.tag == "get":
                current = current.get(op.payload)  # type: ignore[arg-type]
            elif op.tag == "at":
                current = current.at(op.payload)  # type: ignore[arg-type]
            else:
                raise ValueError(f"Unsupported op tag: {op.tag}")
        return current

    def as_int(self) -> "ScalarProjection":
        """Return a scalar projection via ValueAPI.as_int()."""
        return ScalarProjection(self, scalar_type="int")

    def as_float(self) -> "ScalarProjection":
        """Return a scalar projection via ValueAPI.as_float()."""
        return ScalarProjection(self, scalar_type="float")

    def as_bool(self) -> "ScalarProjection":
        """Return a scalar projection via ValueAPI.as_bool()."""
        return ScalarProjection(self, scalar_type="bool")

    def is_true(self) -> "_BasePredicate":
        """Return predicate that checks if the value is True via ValueAPI.as_bool().is_true()."""
        return self.as_bool().is_true()

    def is_false(self) -> "_BasePredicate":
        """Return predicate that checks if the value is False via ValueAPI.as_bool().is_false()."""
        return self.as_bool().is_false()

    def _infer_scalar_projection(self, value: object) -> "ScalarProjection":
        """Infer and create scalar projection from value.

        This is a private helper for comparison operators.

        Args:
            value: The value to infer type from

        Returns:
            ScalarProjection with inferred type

        Raises:
            TypeError: If the value type cannot be inferred
        """
        if isinstance(value, bool):
            return self.as_bool()
        elif isinstance(value, int):
            return self.as_int()
        elif isinstance(value, float):
            return self.as_float()
        elif value is None:
            return self.as_int()  # Default to int
        else:
            raise TypeError(
                f"Cannot infer scalar type from {type(value).__name__}. "
                f"Use explicit type conversion: "
                f".as_int(), .as_float(), or .as_bool()"
            )

    def expected_int(self) -> "ExpectedScalarProjection":
        """Return a scalar projection via ValueAPI.expected_int()."""
        return ExpectedScalarProjection(self, scalar_type="int")

    def expected_float(self) -> "ExpectedScalarProjection":
        """Return a scalar projection via ValueAPI.expected_float()."""
        return ExpectedScalarProjection(self, scalar_type="float")

    def expected_bool(self) -> "ExpectedScalarProjection":
        """Return a scalar projection via ValueAPI.expected_bool()."""
        return ExpectedScalarProjection(self, scalar_type="bool")

    def _append(self, op: Op) -> "Projection":
        return Projection(self.ops + (op,))

    # --- Comparison operators with automatic type inference (EFD-125) ---
    # These enable simplified syntax: it.age > 21 instead of it.age.as_int() > 21

    def __eq__(self, other: object) -> "_BasePredicate":  # type: ignore[override]
        """Equality comparison with automatic type inference."""
        return self._infer_scalar_projection(other) == other

    def __ne__(self, other: object) -> "_BasePredicate":  # type: ignore[override]
        """Inequality comparison with automatic type inference."""
        return self._infer_scalar_projection(other) != other

    def __lt__(self, other: object) -> "_BasePredicate":
        """Less-than comparison with automatic type inference."""
        return self._infer_scalar_projection(other) < other

    def __le__(self, other: object) -> "_BasePredicate":
        """Less-or-equal comparison with automatic type inference."""
        return self._infer_scalar_projection(other) <= other

    def __gt__(self, other: object) -> "_BasePredicate":
        """Greater-than comparison with automatic type inference."""
        return self._infer_scalar_projection(other) > other

    def __ge__(self, other: object) -> "_BasePredicate":
        """Greater-or-equal comparison with automatic type inference."""
        return self._infer_scalar_projection(other) >= other


@dataclass(frozen=True)
class It:
    """Universal placeholder for ValueAPI projections."""

    def get(self, key: str) -> Projection:
        """Return a new Projection starting with get(key)."""
        return Projection((Op("get", key),))

    def at(self, index: int) -> Projection:
        """Return a new Projection starting with at(index)."""
        return Projection((Op("at", index),))

    def __getattr__(self, name: str) -> Projection:
        """Attribute sugar: it.name -> it.get("name")."""
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        return self.get(name)

    def __getitem__(self, index: int) -> Projection:
        """Index sugar: it[index] -> it.at(index)."""
        return self.at(index)


it = It()

ScalarType: TypeAlias = Literal["int", "float", "bool"]
CompareOp = Literal["eq", "ne", "lt", "le", "gt", "ge"]


def _compare_value(left_val: Scalar, op: CompareOp, right: object, *, strict: bool) -> bool:
    if left_val is None:
        if strict:
            raise TypeError("Expected scalar value, got None")
        return False
    try:
        if op == "eq":
            return left_val == right
        if op == "ne":
            return left_val != right
        if op == "lt":
            return left_val < right  # type: ignore[operator]
        if op == "le":
            return left_val <= right  # type: ignore[operator]
        if op == "gt":
            return left_val > right  # type: ignore[operator]
        if op == "ge":
            return left_val >= right  # type: ignore[operator]
    except TypeError:
        return False
    raise ValueError(f"Unsupported compare op: {op}")


def _scalar_value(target: ValueAPI, scalar_type: ScalarType, *, expected: bool) -> Scalar:
    if scalar_type == "int":
        return target.expected_int() if expected else target.as_int()
    if scalar_type == "float":
        return target.expected_float() if expected else target.as_float()
    if scalar_type == "bool":
        return target.expected_bool() if expected else target.as_bool()
    raise ValueError(f"Unsupported scalar type: {scalar_type}")


@dataclass(frozen=True)
class _BasePredicate:
    left: "_BaseScalarProjection"
    op: CompareOp
    right: object

    _strict: ClassVar[bool] = False

    def __call__(self, value: ValueAPI) -> bool:
        left_val = self.left(value)
        return _compare_value(left_val, self.op, self.right, strict=self._strict)


@dataclass(frozen=True)
class Predicate(_BasePredicate):
    """ValueAPI -> bool predicate for filter."""

    _strict: ClassVar[bool] = False


@dataclass(frozen=True)
class PredicateStrict(_BasePredicate):
    """ValueAPI -> bool predicate that raises on missing values."""

    _strict: ClassVar[bool] = True


@dataclass(frozen=True, eq=False)
class _BaseScalarProjection:
    base: Projection
    scalar_type: ScalarType

    _expected: ClassVar[bool] = False

    def __call__(self, value: ValueAPI) -> Scalar:
        target = self.base(value)
        return _scalar_value(target, self.scalar_type, expected=self._expected)

    def _predicate(self, op: CompareOp, other: object) -> _BasePredicate:
        raise NotImplementedError

    def __eq__(self, other: object) -> _BasePredicate:  # type: ignore[override]
        return self._predicate("eq", other)

    def __ne__(self, other: object) -> _BasePredicate:  # type: ignore[override]
        return self._predicate("ne", other)

    def __lt__(self, other: object) -> _BasePredicate:
        return self._predicate("lt", other)

    def __le__(self, other: object) -> _BasePredicate:
        return self._predicate("le", other)

    def __gt__(self, other: object) -> _BasePredicate:
        return self._predicate("gt", other)

    def __ge__(self, other: object) -> _BasePredicate:
        return self._predicate("ge", other)

    def eq(self, other: object) -> _BasePredicate:
        """Return predicate for equality comparison."""
        return self._predicate("eq", other)

    def ne(self, other: object) -> _BasePredicate:
        """Return predicate for inequality comparison."""
        return self._predicate("ne", other)

    def lt(self, other: object) -> _BasePredicate:
        """Return predicate for less-than comparison."""
        return self._predicate("lt", other)

    def le(self, other: object) -> _BasePredicate:
        """Return predicate for less-or-equal comparison."""
        return self._predicate("le", other)

    def gt(self, other: object) -> _BasePredicate:
        """Return predicate for greater-than comparison."""
        return self._predicate("gt", other)

    def ge(self, other: object) -> _BasePredicate:
        """Return predicate for greater-or-equal comparison."""
        return self._predicate("ge", other)

    def is_true(self) -> _BasePredicate:
        """Return predicate that checks scalar is True."""
        return self._predicate("eq", True)

    def is_false(self) -> _BasePredicate:
        """Return predicate that checks scalar is False."""
        return self._predicate("eq", False)


@dataclass(frozen=True, eq=False)
class ScalarProjection(_BaseScalarProjection):
    """ValueAPI -> scalar projection for comparisons."""

    _expected: ClassVar[bool] = False

    def _predicate(self, op: CompareOp, other: object) -> _BasePredicate:
        return Predicate(self, op, other)


@dataclass(frozen=True, eq=False)
class ExpectedScalarProjection(_BaseScalarProjection):
    """ValueAPI -> scalar projection that raises on missing values."""

    _expected: ClassVar[bool] = True

    def _predicate(self, op: CompareOp, other: object) -> _BasePredicate:
        return PredicateStrict(self, op, other)


__all__ = [
    "Op",
    "Projection",
    "ScalarProjection",
    "Predicate",
    "ExpectedScalarProjection",
    "PredicateStrict",
    "It",
    "it",
]
