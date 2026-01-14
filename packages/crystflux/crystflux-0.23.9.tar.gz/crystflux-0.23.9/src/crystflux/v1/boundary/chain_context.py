"""Boundary context: immutable layered diffs ("strata").

Design intent:
- ChainContext is an *outer-shell companion* that accumulates as immutable layers.
- Each layer is a "diff stratum" conceptually, but its internal meaning is intentionally opaque
  at the boundary level.
- The only guaranteed operation is `evolve(layer) -> new_context` (no in-place mutation).

ChainContextLayer:
- "payload: object" serves as an ethical medium that defers meaning (différance) while
  preserving ontological grounds.
- Its essence manifests through the temporal interaction between the adapter layer's
  context-dependent interpretation and the user's intentionality.
- By not defining a strict type for "payload," the manifestation of meaning is deferred.
  While "Any" represents a relinquishment of interpretative responsibility, "object" is
  adopted as the minimal entity that preserves Python's ontological basis (id, hash, etc.).
- It functions as a field—akin to "Sunyata" (Emptiness)—that holds no inherent meaning
  yet harbors all possibilities of manifestation.
- Meaning, intent, and roles converge relatively through a triadic temporal interaction:
    * The Past: Inherited mode of being (the behavior of the actual type).
    * The Present: The observer's intentionality (type guards and transformation logic).
    * The Future: Context-dependent propagation through the chain (interpretability of the next layer).
- This design positions the code as an "ethical apparatus that continues to pose the
question of Being."

ChainContext:
- ChainContext provides a deterministic structure of multi-layered irreversibility
  of immutable objects at the micro level, while leaving an essential margin for
  interpretation at the macro level. The adapter layer may inscribe a narrative
  such as "the arrow of time" within this margin, yet this narrative depends on
  the observer's perspective and always retains room for reinterpretation.
  Consequently, the structural materiality at the micro level and the meaningful
  temporality at the macro level are not connected by a one-to-one linear
  correspondence, but can instead be linked through diverse networks mediated
  by the act of observation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Self


@dataclass(frozen=True)
class ChainContextLayer:
    """One immutable context stratum.

    `payload` is intentionally opaque: the boundary layer does not interpret it.
    """

    tag: str
    payload: object


class ChainContext(Protocol):
    """Minimal chain context contract for the outer shell.

    Note:
    - This immutable tuple of layers creates a functional irreversibility: once a stratum
      is appended, it can neither be modified nor removed. Through this accumulation,
      the structure allows the narrative of an "arrow of time" to emerge within the
      observer's frame of reference.
    """

    layers: tuple[ChainContextLayer, ...]

    def evolve(self, layer: ChainContextLayer) -> Self:
        """Return a new ChainContext with `layer` appended (must not mutate in-place)."""
        ...


__all__ = ["ChainContext", "ChainContextLayer"]
