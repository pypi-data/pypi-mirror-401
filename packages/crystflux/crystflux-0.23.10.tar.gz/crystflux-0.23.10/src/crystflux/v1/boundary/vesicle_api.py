"""
Vesicle protocol (recommended semantics).

Intent:
- Immutable carrier that transports a fixed mode + opaque context strata + structural trace.
- It does not interpret payloads, does not decide termination, does not execute plans.
- Once VOID is entered (sentinel attached), it never returns to a value state.

Key invariants:
- mode is fixed for the lifetime of a vesicle (no switching).
- is_void == (sentinel is not None)
- chain_steps are single-sourced:
    - before VOID: steps are local (tag="spawn")
    - after VOID: steps are sentinel.chain_steps (tag="bump"); local steps are not appended anymore

Design note:
- To avoid premature convergence and naive local implementations, this protocol intentionally
  does not prescribe the concrete implementation of `spawn` (wrapper creation to keep method
  chains alive) nor the recording rules for `chain_steps` before a void occurs. When ambiguity
  arises, consult the human owner responsible for the library-wide specification or a
  higher-level AI agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Self, runtime_checkable

from ..core.void_reason import VoidReason

from .chain_context import ChainContext, ChainContextLayer
from .chain_step import ChainStep
from .mode_contracts import CrystMode
from .void_sentinel import VoidSentinel


@dataclass(frozen=True)
class VoidSummary:
    """A small, stable projection of a persistent-VOID state (no raw values)."""

    mode: CrystMode
    reason: VoidReason | str
    count: int
    void_reasoning: bool
    chain_steps: tuple[ChainStep, ...]


@runtime_checkable
class VesicleAPI(Protocol):
    """
    Immutable outer-shell carrier.

    Data it carries (but does not interpret):
    - mode: fixed observation phase (strict/latent/dream) for this chain
    - context: opaque immutable strata (ChainContext.evolve-only)
    - sentinel: persistent VOID carrier after first failure (None before VOID)
    - structural trace: ChainStep list (local before VOID, sentinel-owned after VOID)
    """

    # --- Conceptual note ------------------------------------------------------
    # Acts as a cell-like membrane that:
    # - Isolates internal adapter implementation from external interaction
    # - Wraps adapters with mode-specific behavior (StrictNumpyChain, etc.)
    # - Preserves mode metadata through method chaining
    # - Manages structural traces with single-sourcing (pre/post-VOID)
    # - Provides stable projections for external system integration
    # - Planned to serve as the foundation for a future LLM-integrated method chain ecosystem

    # --- Required attributes -------------------------------------------------
    mode: CrystMode
    context: ChainContext
    sentinel: VoidSentinel | None

    # --- Required projections ------------------------------------------------
    @property
    def is_void(self) -> bool:
        """True if sentinel is attached."""
        ...

    @property
    def chain_steps(self) -> tuple[ChainStep, ...]:
        """
        Structural trace (single-sourced):
        - sentinel is None  -> local steps
        - sentinel not None -> sentinel.chain_steps
        """
        ...

    # --- Required operations (no interpretation; return new instance only) ---
    def coat(self, layer: ChainContextLayer) -> Self:
        """
        Add one immutable context stratum.

        Must:
        - call context.evolve(layer)
        - never interpret layer.payload
        - never mutate in-place
        """
        ...

    def imprint(self, op: str) -> Self:
        """
        Record one structural trace step without executing anything.

        Semantics:
        - if not void: append ChainStep(tag="spawn", op=op) to local trace
        - if void: bump the sentinel (which appends ChainStep(tag="bump", op=op) internally)

        Must:
        - not validate/fix vocabulary of op
        - not store raw values, call args, or results
        """
        ...

    def seal(self, sentinel: VoidSentinel) -> Self:
        """
        Enter persistent-VOID state by attaching a sentinel.

        Must:
        - be immutable (return new instance)
        - make is_void True
        - enforce mode consistency (vesicle.mode == sentinel.mode), or fail fast
        - ensure chain_steps projection becomes sentinel.chain_steps (no double history)
        """
        ...

    # --- Optional but strongly stabilizing projections -----------------------
    def project_ops(self) -> tuple[str, ...]:
        """Return only the op labels from chain_steps (bridge to other chain systems)."""
        ...

    def project_context_tags(self) -> tuple[str, ...]:
        """Return only ChainContextLayer.tag sequence (payload remains opaque)."""
        ...

    def void_summary(self) -> VoidSummary | None:
        """Return a stable summary when void; otherwise None."""
        ...
