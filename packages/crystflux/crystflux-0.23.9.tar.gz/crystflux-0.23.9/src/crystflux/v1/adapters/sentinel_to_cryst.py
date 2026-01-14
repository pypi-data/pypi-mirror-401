"""Adapter-layer helpers for converting VOID sentinels back into CrystFlux Values.

This module depends on core Value implementations, so it intentionally lives in adapters.
"""

from __future__ import annotations

from typing import Any

from crystflux.v1.boundary.mode_contracts import CrystMode, resolve_mode
from crystflux.v1.boundary.chain_step import ChainStep
from crystflux.v1.core import VOID
from crystflux.v1.core.value_api import ValueAPI
from crystflux.v1.core.value_modes import DreamValue
from crystflux.v1.core.void_reason import VoidReason
from crystflux.v1.core.void_value import ReasonedVoid


def sentinel_to_cryst(
    *,
    reason: VoidReason | str,
    mode: CrystMode,
    void_reasoning: bool,
    chain_steps: tuple[ChainStep, ...] = (),
    mode_override: CrystMode | None = None,
) -> ValueAPI:
    """Convert a sentinel state into a CrystFlux ValueAPI.

    Notes:
    - Strict raises (fail-fast).
    - Latent returns VOID (or ReasonedVoid when enabled and reason is a VoidReason).
    - Dream returns a void DreamValue; desire observation is handled elsewhere.
    """
    effective_mode = resolve_mode(mode_override or mode)

    if effective_mode == "strict":
        raise TypeError("Void sentinel encountered in strict mode")

    coerced_reason = _coerce_reason(reason)

    if effective_mode == "dream":
        recorded_reason = coerced_reason if (void_reasoning and isinstance(coerced_reason, VoidReason)) else None
        # Crystallizer/DreamValue currently models `chain_steps` as `tuple[str, ...]`.
        # Project-level sentinels may carry structured `ChainStep` traces; bridge by projecting to `op`.
        dream_chain_steps: tuple[str, ...] = tuple(step.op for step in chain_steps)
        return DreamValue(
            None,
            chain_steps=dream_chain_steps,
            _void_reason=recorded_reason,
            _void_reasoning_enabled=void_reasoning,
        )

    if void_reasoning and isinstance(coerced_reason, VoidReason):
        return ReasonedVoid(coerced_reason)

    return VOID


def _coerce_reason(reason: VoidReason | str) -> Any:
    """Try to map a string reason into VoidReason; fall back to the original value."""
    if isinstance(reason, VoidReason):
        return reason
    try:
        return VoidReason(str(reason))
    except Exception:
        return reason


__all__ = ["sentinel_to_cryst"]
