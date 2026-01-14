"""Default DesireLogger implementations."""

from __future__ import annotations

import logging

from ..boundary.event_schema import DesireEvent
from ..boundary.desire_logger import DesireLogger


class StdoutDesireLogger(DesireLogger):
    """Minimal logger that prints one line per event."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def log(self, event: DesireEvent) -> None:
        if not self.verbose:
            print(f"[Desire] method={event.method_name} target={event.target_type} repr={event.target_repr}")
            return
        lines = [
            f"[Desire verbose] method={event.method_name}",
            f"  target={event.target_type} repr={event.target_repr}",
            f"  source={event.source_location}",
            f"  chain_steps={event.chain_steps}",
            f"  trace_frames={event.trace_frames}",
            f"  timestamp={event.timestamp}",
        ]
        print("\n".join(lines))


class LoggingDesireLogger(DesireLogger):
    """Logging module-backed DesireLogger."""

    def __init__(self, logger: logging.Logger | None = None, verbose: bool = False) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self.verbose = verbose

    def log(self, event: DesireEvent) -> None:
        if not self.verbose:
            self._logger.info(
                "desire_event method=%s target_type=%s target_repr=%s",
                event.method_name,
                event.target_type,
                event.target_repr,
            )
            return
        self._logger.info(
            "desire_event method=%s target_type=%s target_repr=%s source=%s chain=%s trace=%s ts=%s",
            event.method_name,
            event.target_type,
            event.target_repr,
            event.source_location,
            event.chain_steps,
            event.trace_frames,
            event.timestamp,
        )


__all__ = ["StdoutDesireLogger", "LoggingDesireLogger"]
