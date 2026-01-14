"""Refactored Crystallizer implementation using mock-free frame inspection."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Callable

from ..boundary.crystallizer_port import CrystallizerPort
from ..boundary.error_contracts import InvalidJsonPayloadError, ModeNotSupportedError
from ..boundary.event_schema import DesireEvent
from ..boundary.desire_logger import DesireLogger
from ..boundary.event_schema import MissingEvent
from ..boundary.missing_logger import MissingLogger
from ..boundary.mode_contracts import CrystMode, SUPPORTED_MODES, resolve_mode
from ..core.freeze_value import freeze_value
from ..core.value_modes import DreamValue, LatentValue, StrictValue
from ..core.value_core import BaseValue
from ..core.void_reason import VoidReason
from .dream_context import require_dream_mode
from .frame_inspection import (
    StackContext,
    extract_caller_location,
    extract_trace_frames,
)


class Crystallizer(CrystallizerPort):
    """Factory for Strict/Latent/Dream values with mock-free frame inspection."""

    @classmethod
    def from_json(
        cls,
        data: str | bytes,
        *,
        mode: CrystMode = "latent",
        desire_logger: DesireLogger | None = None,
        missing_logger: MissingLogger | None = None,
        void_reasoning: bool = False,
    ) -> BaseValue:
        """Parse JSON payload and wrap into the requested mode."""
        try:
            parsed = json.loads(data)
        except Exception as exc:  # pragma: no cover - pass-through
            raise InvalidJsonPayloadError(str(exc)) from exc
        return cls.from_dict(
            parsed,
            mode=mode,
            desire_logger=desire_logger,
            missing_logger=missing_logger,
            void_reasoning=void_reasoning,
        )

    @classmethod
    def from_dict(
        cls,
        data: Any,
        *,
        mode: CrystMode = "latent",
        desire_logger: DesireLogger | None = None,
        missing_logger: MissingLogger | None = None,
        void_reasoning: bool = False,
    ) -> BaseValue:
        frozen = freeze_value(data)
        resolved_mode = resolve_mode(mode)

        if resolved_mode == "dream":
            require_dream_mode()
            hook = cls._make_desire_hook(desire_logger) if desire_logger else None
            missing_hook = cls._make_missing_hook(missing_logger) if missing_logger else None
            return DreamValue(
                frozen,
                on_desire=hook,
                on_missing=missing_hook,
                _void_reasoning_enabled=void_reasoning,
            )
        if resolved_mode == "strict":
            # v1 scope: strict fails fast; missing logging is ignored in strict mode.
            return StrictValue(frozen, _void_reasoning_enabled=void_reasoning)
        if resolved_mode == "latent":
            missing_hook = cls._make_missing_hook(missing_logger) if missing_logger else None
            return LatentValue(
                frozen,
                on_missing=missing_hook,
                _void_reasoning_enabled=void_reasoning,
            )
        supported = ", ".join(SUPPORTED_MODES)
        raise ModeNotSupportedError(f"Unsupported mode: {mode}. Supported modes: {supported}")

    @classmethod
    def latent(
        cls, data: Any, *, missing_logger: MissingLogger | None = None, void_reasoning: bool = False
    ) -> LatentValue:
        return cls.from_dict(
            data,
            mode="latent",
            missing_logger=missing_logger,
            void_reasoning=void_reasoning,
        )  # type: ignore[return-value]

    @classmethod
    def strict(cls, data: Any, *, void_reasoning: bool = False) -> StrictValue:
        return cls.from_dict(data, mode="strict", void_reasoning=void_reasoning)  # type: ignore[return-value]

    @classmethod
    def dream(
        cls,
        data: Any,
        *,
        desire_logger: DesireLogger | None = None,
        missing_logger: MissingLogger | None = None,
        void_reasoning: bool = False,
    ) -> DreamValue:
        return cls.from_dict(
            data,
            mode="dream",
            desire_logger=desire_logger,
            missing_logger=missing_logger,
            void_reasoning=void_reasoning,
        )  # type: ignore[return-value]

    safe = latent

    @staticmethod
    def _make_desire_hook(logger: DesireLogger) -> Callable[[str, Any, tuple[str, ...]], None]:
        def _hook(method_name: str, raw_value: Any, chain_steps: tuple[str, ...]) -> None:
            try:
                # NOTE: `verbose` is intentionally duck-typed (not part of the DesireLogger contract).
                # This keeps the boundary minimal; wrappers may or may not forward it.
                verbose = bool(getattr(logger, "verbose", False))
                trace_frames = _collect_trace_frames_with_context() if verbose else None
                event = _build_desire_event(method_name, raw_value, chain_steps, trace_frames)
                logger.log(event)
            except Exception:
                # Swallow logging errors to avoid breaking Dream chains
                pass

        return _hook

    @staticmethod
    def _make_missing_hook(logger: MissingLogger) -> Callable[..., None]:
        def _hook(
            *,
            reason: VoidReason,
            target: Any,
            key: str | None = None,
            index: int | None = None,
        ) -> None:
            try:
                # NOTE: `verbose` is intentionally duck-typed (not part of the MissingLogger contract).
                # This keeps the boundary minimal; wrappers may or may not forward it.
                verbose = bool(getattr(logger, "verbose", False))
                trace_frames = _collect_trace_frames_with_context() if verbose else None
                # NOTE: `target` is the parent container where the miss occurred (object/array),
                # not the current Value's raw `_value`.
                event = _build_missing_event(
                    reason, target, key=key, index=index, trace_frames=trace_frames
                )
                logger.log(event)
            except Exception:
                # Swallow logging errors to avoid breaking chains
                pass

        return _hook


def _build_desire_event(
    method_name: str,
    raw_value: Any,
    chain_steps: tuple[str, ...],
    trace_frames: tuple[str, ...] | None,
) -> DesireEvent:
    target_type = type(raw_value).__name__ if raw_value is not None else "void"
    target_repr = _trim_repr(raw_value, max_len=80)
    source_location = _get_caller_location_with_context()
    return DesireEvent(
        method_name=method_name,
        target_repr=target_repr,
        target_type=target_type,
        source_location=source_location,
        timestamp=datetime.now(timezone.utc),
        chain_steps=chain_steps,
        trace_frames=trace_frames,
    )


def _build_missing_event(
    reason: VoidReason,
    target: Any,
    *,
    key: str | None = None,
    index: int | None = None,
    trace_frames: tuple[str, ...] | None,
) -> MissingEvent:
    # `target` is expected to be the parent container where indexing happened (object/array).
    target_type = type(target).__name__ if target is not None else "void"
    target_repr = _trim_repr(target, max_len=80)
    source_location = _get_caller_location_with_context()
    return MissingEvent(
        reason=reason,
        key=key,
        index=index,
        target_repr=target_repr,
        target_type=target_type,
        source_location=source_location,
        timestamp=datetime.now(timezone.utc),
        trace_frames=trace_frames,
    )


def _trim_repr(value: Any, max_len: int) -> str:
    rep = repr(value)
    if len(rep) <= max_len:
        return rep
    return rep[: max_len - 3] + "..."


def _get_caller_location_with_context() -> str:
    """Get caller location using mock-free frame inspection."""
    # Create context from current stack, skipping this function.
    #
    # NOTE: Depth is tuned for this call chain:
    # user -> Value.get/at -> _notify_missing -> hook -> _build_*_event -> here
    context = StackContext.from_current_stack(skip_frames=1)
    return extract_caller_location(context, target_depth=3)


def _collect_trace_frames_with_context(max_frames: int = 8) -> tuple[str, ...]:
    """Collect trace frames using mock-free frame inspection."""
    # Create context from current stack, skipping this function and the hook wrapper.
    context = StackContext.from_current_stack(skip_frames=2)
    return extract_trace_frames(context, max_frames)


__all__ = ["Crystallizer"]
