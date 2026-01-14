"""Adapters layer: concrete integrations and side-effectful implementations."""

from .crystallizer_impl import Crystallizer
from .dream_context import enable_dream_mode, with_dream_mode
from .desire_logger_impl import StdoutDesireLogger, LoggingDesireLogger
from .missing_logger_impl import StdoutMissingLogger
from .frame_inspection import (
    FrameInfo,
    StackContext,
    FrameInspectionMetrics,
)
from .default_void_sentinel import DefaultVoidSentinel

__all__ = [
    "Crystallizer",
    "enable_dream_mode",
    "with_dream_mode",
    "StdoutDesireLogger",
    "LoggingDesireLogger",
    "StdoutMissingLogger",
    "FrameInfo",
    "StackContext",
    "FrameInspectionMetrics",
    "DefaultVoidSentinel",
]
