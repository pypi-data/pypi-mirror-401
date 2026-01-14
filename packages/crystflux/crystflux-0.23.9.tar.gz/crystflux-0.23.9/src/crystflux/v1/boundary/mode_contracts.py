"""
Mode resolution helpers for Strict/Latent/Dream values (pure boundary utilities).

Usage guide:
- Use resolve_mode when you already have a mode string (may be None) and need normalization/fallback.
- Use infer_value_mode when you have a ValueAPI instance and want its concrete mode inferred.
- Use decide_mode when you optionally accept an explicit mode and otherwise want to infer from a value.

Examples:
    resolve_mode("Strict")           # -> "strict"
    infer_value_mode(StrictValue(1)) # -> "strict"
    decide_mode(latent_val, None)    # -> "latent" (inferred)
    decide_mode(dream_val, "latent") # -> "latent" (explicit wins)

Note on type checkers:
- basedpyright narrows `normalized` to CrystMode via membership, so it flags `cast` as unnecessary.
- mypy does not narrow `str` to Literal through membership, so returning `normalized` directly fails its return-type check.
- Using an explicit loop to return the matched candidate avoids casts and satisfies both checkers.
"""

from __future__ import annotations

from typing import Literal

from ..core.value_api import ValueAPI
from ..core.value_modes import DreamValue, LatentValue, StrictValue
from .error_contracts import ModeNotSupportedError

CrystMode = Literal["strict", "latent", "dream"]
DEFAULT_MODE: CrystMode = "latent"
SUPPORTED_MODES: tuple[CrystMode, ...] = ("strict", "latent", "dream")
_SUPPORTED_MODES_STR = ", ".join(SUPPORTED_MODES)


def resolve_mode(mode: str | None, *, fallback: CrystMode = DEFAULT_MODE) -> CrystMode:
    """Normalize an explicit mode string or fall back when None."""
    if mode is None:
        return fallback

    normalized = mode.lower()

    # See Note above for type checker differences
    for candidate in SUPPORTED_MODES:
        if normalized == candidate:
            return candidate
    raise ModeNotSupportedError(f"Unsupported mode: {mode}. Supported modes: {_SUPPORTED_MODES_STR}")


def infer_value_mode(value: ValueAPI) -> CrystMode:
    """Infer mode from a ValueAPI concrete type."""
    if isinstance(value, DreamValue):
        return "dream"
    if isinstance(value, LatentValue):
        return "latent"
    if isinstance(value, StrictValue):
        return "strict"
    raise ModeNotSupportedError(
        f"Cannot infer mode from {type(value).__name__}. Supported modes: {_SUPPORTED_MODES_STR}"
    )


def decide_mode(value: ValueAPI | None, mode: str | None, *, fallback: CrystMode = DEFAULT_MODE) -> CrystMode:
    """Resolve explicit mode when given; otherwise infer from the value."""
    if mode is not None:
        return resolve_mode(mode, fallback=fallback)
    if value is None:
        raise ModeNotSupportedError(
            f"Cannot decide mode without value or explicit mode. Supported modes: {_SUPPORTED_MODES_STR}"
        )
    return infer_value_mode(value)


__all__ = [
    "CrystMode",
    "DEFAULT_MODE",
    "SUPPORTED_MODES",
    "resolve_mode",
    "infer_value_mode",
    "decide_mode",
]
