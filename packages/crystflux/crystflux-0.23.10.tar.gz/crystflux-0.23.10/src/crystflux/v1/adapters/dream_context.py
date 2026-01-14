"""Dream mode context manager for research use (Async-safe)."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar

from ..boundary.error_contracts import ModeNotSupportedError

F = TypeVar("F", bound=Callable[..., Any])

# Default is False (Safe/Strict/Latent only)
_DREAM_PERMISSION: ContextVar[bool] = ContextVar("dream_permission", default=False)


@contextmanager
def enable_dream_mode() -> Iterator[None]:
    """Enable Dream mode within this context (research use only).

    This implementation relies on `contextvars`, making it safe for both
    multithreading and asyncio environments. The permission propagates to
    sub-tasks created within the context but isolates parallel tasks.

    Example:
        from crystflux.v1 import Crystallizer
        from crystflux.v1.adapters import enable_dream_mode

        with enable_dream_mode():
            val = Crystallizer.dream({"a": 1})
    """
    token = _DREAM_PERMISSION.set(True)
    try:
        yield
    finally:
        _DREAM_PERMISSION.reset(token)


def with_dream_mode(func: F) -> F:
    """Decorator to enable Dream mode for the decorated function (research use only)."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with enable_dream_mode():
            return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


def require_dream_mode() -> None:
    """Raise if Dream mode is not enabled in the current context."""
    if not _DREAM_PERMISSION.get():
        raise ModeNotSupportedError(
            "Crystallizer.dream() is locked. "
            "Use 'with enable_dream_mode():' to authorize experimental usage."
        )


__all__ = ["enable_dream_mode", "with_dream_mode", "require_dream_mode"]
