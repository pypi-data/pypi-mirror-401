"""Protocol for Desire logger sinks."""

from __future__ import annotations

from typing import Protocol

from .event_schema import DesireEvent


class DesireLogger(Protocol):
    """Sink for hallucination/desire events."""

    def log(self, event: DesireEvent) -> None:
        """Record a DesireEvent without raising."""
        ...


__all__ = ["DesireLogger"]
