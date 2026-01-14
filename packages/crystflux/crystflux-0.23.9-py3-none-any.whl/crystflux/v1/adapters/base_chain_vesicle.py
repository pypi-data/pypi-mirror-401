"""VesicleAPI-aware chain carrier base (adapter layer)."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Self

from crystflux.v1.boundary.chain_step import ChainStep
from crystflux.v1.boundary.chain_context import ChainContext, ChainContextLayer
from crystflux.v1.boundary.mode_contracts import CrystMode
from crystflux.v1.boundary.vesicle_api import VesicleAPI, VoidSummary
from crystflux.v1.boundary.void_sentinel import VoidSentinel


@dataclass(frozen=True)
class BaseChainVesicle(VesicleAPI):
    """
    VesicleAPI-aware chain carrier base.

    Notes:
    - This is a base carrier; adapter-specific behavior should live in subclasses.
    - `spawn` and pre-void `chain_steps` rules are intentionally lightweight here; keep them
      aligned with the project design notes if you refine them.
    """

    mode: CrystMode
    context: ChainContext
    sentinel: VoidSentinel | None
    _steps: tuple[ChainStep, ...] = ()

    @property
    def is_void(self) -> bool:
        return self.sentinel is not None

    @property
    def chain_steps(self) -> tuple[ChainStep, ...]:
        # If VOID, delegate trace to the sentinel; otherwise use local steps.
        return self.sentinel.chain_steps if self.sentinel else self._steps

    def coat(self, layer: ChainContextLayer) -> Self:
        return replace(self, context=self.context.evolve(layer))

    def imprint(self, op: str) -> Self:
        if self.sentinel:
            return replace(self, sentinel=self.sentinel.bump(step=op))
        # Default "spawn" step; refine only with explicit design guidance.
        return replace(self, _steps=self._steps + (ChainStep(tag="spawn", op=op),))

    def seal(self, sentinel: VoidSentinel) -> Self:
        if sentinel.mode != self.mode:
            raise ValueError("Mode mismatch between vesicle and sentinel")
        return replace(self, sentinel=sentinel)

    def project_ops(self) -> tuple[str, ...]:
        return tuple(step.op for step in self.chain_steps)

    def project_context_tags(self) -> tuple[str, ...]:
        return tuple(layer.tag for layer in self.context.layers)

    def void_summary(self) -> VoidSummary | None:
        if not self.sentinel:
            return None
        return VoidSummary(
            mode=self.sentinel.mode,
            reason=self.sentinel.reason,
            count=self.sentinel.count,
            void_reasoning=self.sentinel.void_reasoning,
            chain_steps=self.sentinel.chain_steps,
        )

@dataclass(frozen=True)
class EmptyChainContext(ChainContext):
    """Minimal context container for chains that do not carry extra strata."""

    layers: tuple[ChainContextLayer, ...] = ()

    def evolve(self, layer: ChainContextLayer) -> Self:
        return type(self)(layers=self.layers + (layer,))


__all__ = ["BaseChainVesicle", "EmptyChainContext"]
