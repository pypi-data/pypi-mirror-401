"""Protocol for Missing logger sinks."""

from __future__ import annotations

from typing import Protocol

from .event_schema import MissingEvent


class MissingLogger(Protocol):
    """Sink for missing key/index events."""

    def log(self, event: MissingEvent) -> None:
        """Record a MissingEvent without raising.

        This is telemetry only. It is intentionally separate from `VoidSentinel`,
        which represents a persistent VOID state in other layers (e.g., adapters).
        """
        ...


__all__ = ["MissingLogger"]
