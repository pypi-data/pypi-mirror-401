"""Pydantic integration helpers (optional, Strict only)."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from ..core.value_modes import StrictValue
from .crystallizer_impl import Crystallizer

if TYPE_CHECKING:
    from pydantic import BaseModel
else:  # pragma: no cover - runtime fallback when pydantic is absent

    class BaseModel:  # type: ignore[too-many-ancestors]
        ...


PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


def to_pydantic(model_cls: type[PydanticModel], value: StrictValue) -> PydanticModel:
    """StrictValue → Pydantic (Strict only supported)."""

    BaseModel = _require_base_model()
    if not issubclass(model_cls, BaseModel):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError("model_cls must be a subclass of BaseModel")
    if not isinstance(value, StrictValue):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError("to_pydantic only supports StrictValue")
    raw = value.as_json_value()
    return model_cls.model_validate(raw)


def from_pydantic(model: BaseModel) -> StrictValue:
    """Pydantic → StrictValue (mode fixed)."""

    BaseModel = _require_base_model()
    if not isinstance(model, BaseModel):
        raise TypeError("model must be a Pydantic BaseModel instance")
    payload = model.model_dump(mode="python")
    return Crystallizer.strict(payload)


def _require_base_model() -> type[BaseModel]:
    try:
        from pydantic import BaseModel as _BaseModel
    except Exception as exc:  # pragma: no cover - optional dependency guard
        raise ImportError("pydantic is required for crystflux.v1.adapters.pydantic") from exc
    return _BaseModel


__all__ = ["to_pydantic", "from_pydantic"]
