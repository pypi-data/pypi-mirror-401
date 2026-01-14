"""Default MissingLogger implementations and wrappers."""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass

from ..boundary.event_schema import MissingEvent
from ..boundary.missing_logger import MissingLogger


class StdoutMissingLogger(MissingLogger):
    """Minimal logger that prints one line per event."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def log(self, event: MissingEvent) -> None:
        if not self.verbose:
            detail = _format_missing_detail(event)
            print(
                f"[Missing] reason={event.reason}{detail} "
                f"target={event.target_type} repr={event.target_repr}"
            )
            return

        detail = _format_missing_detail(event)
        lines = [
            f"[Missing verbose] reason={event.reason}{detail}",
            f"  target={event.target_type} repr={event.target_repr}",
            f"  source={event.source_location}",
            f"  trace_frames={event.trace_frames}",
            f"  timestamp={event.timestamp}",
        ]
        print("\n".join(lines))


class LoggingMissingLogger(MissingLogger):
    """Logging module-backed MissingLogger."""

    def __init__(self, logger: logging.Logger | None = None, verbose: bool = False) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self.verbose = verbose

    def log(self, event: MissingEvent) -> None:
        if not self.verbose:
            self._logger.info(
                "missing_event reason=%s key=%s index=%s target_type=%s source=%s",
                event.reason,
                event.key,
                event.index,
                event.target_type,
                event.source_location,
            )
            return
        self._logger.info(
            "missing_event reason=%s key=%s index=%s target_type=%s target_repr=%s source=%s trace=%s ts=%s",
            event.reason,
            event.key,
            event.index,
            event.target_type,
            event.target_repr,
            event.source_location,
            event.trace_frames,
            event.timestamp,
        )


@dataclass(frozen=True)
class SamplingMissingLogger(MissingLogger):
    """Probabilistic sampler for Missing events."""

    inner: MissingLogger
    p: float = 1.0
    rng: random.Random | None = None

    def log(self, event: MissingEvent) -> None:
        if self.p <= 0.0:
            return
        if self.p >= 1.0:
            self.inner.log(event)
            return
        generator = self.rng or random
        if generator.random() < self.p:
            self.inner.log(event)


class RateLimitMissingLogger(MissingLogger):
    """Token-bucket rate limiter for Missing events (best-effort, single-process)."""

    def __init__(
        self,
        inner: MissingLogger,
        *,
        max_per_sec: float,
        burst: int = 10,
    ) -> None:
        if max_per_sec <= 0:
            raise ValueError("max_per_sec must be > 0")
        if burst <= 0:
            raise ValueError("burst must be > 0")
        self._inner = inner
        self._max_per_sec = max_per_sec
        self._burst = float(burst)
        self._tokens = float(burst)
        self._last_ts = time.monotonic()

    def log(self, event: MissingEvent) -> None:
        now = time.monotonic()
        elapsed = now - self._last_ts
        self._last_ts = now
        self._tokens = min(self._burst, self._tokens + elapsed * self._max_per_sec)
        if self._tokens < 1.0:
            return
        self._tokens -= 1.0
        self._inner.log(event)


def _format_missing_detail(event: MissingEvent) -> str:
    if event.key is not None:
        return f" key={event.key!r}"
    if event.index is not None:
        return f" index={event.index}"
    return ""


__all__ = [
    "StdoutMissingLogger",
    "LoggingMissingLogger",
    "SamplingMissingLogger",
    "RateLimitMissingLogger",
]
