"""Structured events for fluctuation observation.

Design Notes:
- Events are *telemetry*; they do not change Value semantics.
- `MissingEvent` observes navigation misses in latent/dream (`get`/`at` when missing).
- `DesireEvent` observes dream-only "unexpected API" calls.
- These are independent from `VoidSentinel` (a persistent VOID *state carrier* used by adapters).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..core.void_reason import VoidReason


@dataclass(frozen=True)
class DesireEvent:
    """Represents an attempt to use a non-existent or unexpected API."""

    method_name: str
    target_repr: str
    target_type: str
    source_location: str | None = None
    # Reserved: v1 adapters do not populate this yet.
    context_snippet: str | None = None
    timestamp: datetime | None = None
    chain_steps: tuple[str, ...] | None = None
    trace_frames: tuple[str, ...] | None = None


@dataclass(frozen=True)
class MissingEvent:
    """Represents a missing key/index access (v1: missing only).

    Scope:
    - Emitted best-effort via the `on_missing` hook in LatentValue/DreamValue for:
      - `VoidReason.MISSING_KEY`
      - `VoidReason.MISSING_INDEX`
    - Type mismatches (non-object/non-array) currently do not emit MissingEvent.
    """

    reason: VoidReason
    key: str | None = None
    index: int | None = None
    target_repr: str = ""
    target_type: str = ""
    source_location: str | None = None
    # Reserved: v1 adapters do not populate this yet.
    context_snippet: str | None = None
    timestamp: datetime | None = None
    trace_frames: tuple[str, ...] | None = None


__all__ = ["DesireEvent", "MissingEvent"]
