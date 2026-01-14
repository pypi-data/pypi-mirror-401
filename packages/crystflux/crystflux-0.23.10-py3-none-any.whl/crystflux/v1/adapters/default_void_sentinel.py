"""Default implementation of the boundary VoidSentinel contract.

Design intent:
- Carry persistent VOID state (first reason + hop count).
- Provide a best-effort `to_cryst()` bridge back into core Values.
- Do not emit telemetry by itself; callers may log separately.
"""

from __future__ import annotations

from dataclasses import dataclass

from crystflux.v1.boundary.mode_contracts import CrystMode
from crystflux.v1.boundary.chain_step import ChainStep
from crystflux.v1.boundary.void_sentinel import VoidSentinel
from crystflux.v1.core.value_api import ValueAPI
from crystflux.v1.core.void_reason import VoidReason

from .sentinel_to_cryst import sentinel_to_cryst


@dataclass(frozen=True)
class DefaultVoidSentinel(VoidSentinel):
    """Default sentinel used by adapters to represent a persistent VOID chain."""

    reason: VoidReason | str
    mode: CrystMode
    void_reasoning: bool
    count: int = 1
    chain_steps: tuple[ChainStep, ...] = ()

    def bump(self, *, step: str | None = None) -> "DefaultVoidSentinel":
        """Return a new sentinel with count incremented and optional step appended."""
        steps = self.chain_steps + ((ChainStep(tag="bump", op=step),) if step else tuple())
        return type(self)(
            reason=self.reason,
            mode=self.mode,
            void_reasoning=self.void_reasoning,
            count=self.count + 1,
            chain_steps=steps,
        )

    def to_cryst(self, mode_override: CrystMode | None = None) -> ValueAPI:
        """Convert this sentinel into a CrystFlux value for the effective mode."""
        return sentinel_to_cryst(
            reason=self.reason,
            mode=self.mode,
            void_reasoning=self.void_reasoning,
            chain_steps=self.chain_steps,
            mode_override=mode_override,
        )


__all__ = ["DefaultVoidSentinel"]
