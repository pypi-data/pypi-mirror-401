"""Boundary contract for persistent VOID sentinels.

Design intent:
- `VoidSentinel` is a *state carrier* for "already-void" flows (reason + hop count).
- It is intentionally orthogonal to logging/event telemetry:
  - `MissingEvent` / `MissingLogger` observe *navigation misses* (get/at) in latent/dream.
  - `DesireEvent` / `DesireLogger` observe *unexpected API calls* in dream.
- A `VoidSentinel` does not emit events by itself; adapters/policies may choose to log separately.
"""

from __future__ import annotations

from typing import Protocol

from ..core.value_api import ValueAPI
from ..core.void_reason import VoidReason
from .chain_step import ChainStep
from .mode_contracts import CrystMode


class VoidSentinel(Protocol):
    """Protocol for objects representing a persistent VOID chain.

    A sentinel captures the first VOID reason and tracks how many VOID hops
    have occurred since the first failure, without ever reverting to a value.
    Concrete implementations live outside the boundary layer (e.g., adapters).
    """

    mode: CrystMode
    reason: VoidReason | str
    count: int
    void_reasoning: bool
    chain_steps: tuple[ChainStep, ...]

    def bump(self, *, step: str | None = None) -> "VoidSentinel":
        """Return a new sentinel with count incremented and optional step appended."""
        ...

    def to_cryst(self, mode_override: CrystMode | None = None) -> ValueAPI:
        """Convert this sentinel into a CrystFlux value for the effective mode.

        Notes:
        - Strict should typically raise (fail-fast).
        - Latent/Dream should typically return VOID (optionally reasoned when enabled).
        """
        ...


__all__ = ["VoidSentinel"]
