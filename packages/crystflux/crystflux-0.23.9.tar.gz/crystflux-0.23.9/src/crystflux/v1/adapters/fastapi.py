"""FastAPI integration helpers (optional)."""

from __future__ import annotations

from typing import Any

from .crystallizer_impl import Crystallizer
from ..core.value_modes import LatentValue


def crystflux_request_body(payload: Any) -> LatentValue:
    """Parse incoming JSON-like payload into a LatentValue."""
    return Crystallizer.latent(payload)


def crystflux_response(value: LatentValue) -> Any:
    """Serialize a crystflux value back to JSON-compatible data."""
    return value.as_json_value()


__all__ = ["crystflux_request_body", "crystflux_response"]
