"""Mock-free frame inspection functionality for CrystFlux.

This module provides pure functions for frame inspection that can be easily tested
without mocks by extracting the core logic from stack manipulation.
"""

from __future__ import annotations

import os
from typing import Any, Callable, NamedTuple
from dataclasses import dataclass


class FrameInfo(NamedTuple):
    """Immutable frame information extracted from stack frames."""

    filename: str
    lineno: int
    function: str


@dataclass(frozen=True)
class StackContext:
    """Immutable context for stack inspection operations."""

    frames: tuple[FrameInfo, ...]

    @classmethod
    def from_current_stack(cls, skip_frames: int = 0) -> StackContext:
        """Create context from current call stack."""
        import inspect

        frame_records = inspect.stack()[skip_frames:]
        frames = tuple(
            FrameInfo(filename=record.filename, lineno=record.lineno, function=record.function)
            for record in frame_records
        )
        return cls(frames)

    def get_frame_at_depth(self, depth: int) -> FrameInfo | None:
        """Get frame at specific depth from the start of context."""
        if 0 <= depth < len(self.frames):
            return self.frames[depth]
        return None

    def find_caller_frame(self, caller_patterns: list[str]) -> FrameInfo | None:
        """Find first frame matching caller patterns."""
        for frame in self.frames:
            if any(pattern in frame.filename for pattern in caller_patterns):
                continue
            return frame
        return None

    def filter_frames(self, exclude_patterns: list[str], max_frames: int) -> tuple[FrameInfo, ...]:
        """Filter frames excluding patterns and limit count."""
        filtered = [
            frame
            for frame in self.frames
            if not any(pattern in frame.filename for pattern in exclude_patterns)
        ]
        return tuple(filtered[:max_frames])


def extract_caller_location(context: StackContext, target_depth: int = 4) -> str:
    """Extract caller location from stack context.

    Args:
        context: Stack context containing frame information
        target_depth: Depth of the target caller frame

    Returns:
        Formatted location string "filename:lineno" or empty string
    """
    frame = context.get_frame_at_depth(target_depth)
    if frame:
        basename = os.path.basename(frame.filename)
        return f"{basename}:{frame.lineno}"
    return ""


def extract_trace_frames(context: StackContext, max_frames: int = 8) -> tuple[str, ...]:
    """Extract trace frames from context, filtering internal frames.

    Args:
        context: Stack context containing frame information
        max_frames: Maximum number of frames to return

    Returns:
        Tuple of formatted frame strings "filename:lineno"
    """
    exclude_patterns = ["crystflux/v1", "crystflux\\v1"]
    filtered_frames = context.filter_frames(exclude_patterns, max_frames)

    return tuple(f"{os.path.basename(frame.filename)}:{frame.lineno}" for frame in filtered_frames)


def find_user_caller_frame(
    context: StackContext, internal_patterns: list[str] | None = None
) -> FrameInfo | None:
    """Find the first user caller frame excluding internal patterns.

    Args:
        context: Stack context containing frame information
        internal_patterns: Patterns to identify internal frames

    Returns:
        First non-internal frame or None
    """
    if internal_patterns is None:
        internal_patterns = ["crystflux/v1", "crystflux\\v1"]

    return context.find_caller_frame(internal_patterns)


# Pure functions for testing without stack inspection
def format_frame_location(frame: FrameInfo) -> str:
    """Format frame info into location string."""
    basename = os.path.basename(frame.filename)
    return f"{basename}:{frame.lineno}"


def is_internal_frame(frame: FrameInfo, patterns: list[str]) -> bool:
    """Check if frame matches internal patterns."""
    return any(pattern in frame.filename for pattern in patterns)


def stack_context_from_frames(frames: list[tuple[str, int, str]]) -> StackContext:
    """Create a StackContext from provided frame tuples (synthetic context).

    Args:
        frames: List of (filename, lineno, function) tuples

    Returns:
        StackContext built from the given frames
    """
    frame_infos = [
        FrameInfo(filename=filename, lineno=lineno, function=function)
        for filename, lineno, function in frames
    ]
    return StackContext(tuple(frame_infos))


# Performance monitoring
class FrameInspectionMetrics:
    """Metrics for frame inspection performance."""

    def __init__(self) -> None:
        self.stack_calls: int = 0
        self.frame_processing_time_ns: int = 0

    def record_stack_call(self, duration_ns: int) -> None:
        """Record a stack inspection call."""
        self.stack_calls += 1
        self.frame_processing_time_ns += duration_ns

    def get_average_time_ns(self) -> float:
        """Get average processing time per call."""
        if self.stack_calls == 0:
            return 0.0
        return self.frame_processing_time_ns / self.stack_calls


# Global metrics instance
_metrics = FrameInspectionMetrics()


def get_metrics() -> FrameInspectionMetrics:
    """Get global frame inspection metrics."""
    return _metrics


# Decorator for performance monitoring
def monitor_frame_inspection(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to monitor frame inspection performance."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import time

        start = time.time_ns()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.time_ns() - start
            _metrics.record_stack_call(duration)

    return wrapper


# Monitored versions of the main functions
@monitor_frame_inspection
def get_caller_location_with_metrics(target_depth: int = 4) -> str:
    """Get caller location with performance monitoring."""
    context = StackContext.from_current_stack(skip_frames=0)
    return extract_caller_location(context, target_depth)


@monitor_frame_inspection
def collect_trace_frames_with_metrics(max_frames: int = 8) -> tuple[str, ...]:
    """Collect trace frames with performance monitoring."""
    context = StackContext.from_current_stack(skip_frames=2)
    return extract_trace_frames(context, max_frames)
