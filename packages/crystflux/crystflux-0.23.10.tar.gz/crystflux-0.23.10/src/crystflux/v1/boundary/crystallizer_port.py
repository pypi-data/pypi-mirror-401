"""Factory interface for producing values from external inputs."""

from __future__ import annotations

from typing import Any, Protocol

from ..core.value_core import BaseValue
from ..core.value_modes import DreamValue, LatentValue, StrictValue
from .desire_logger import DesireLogger
from .missing_logger import MissingLogger
from .mode_contracts import CrystMode


class CrystallizerPort(Protocol):
    """Factory interface for producing values from external inputs."""

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
        """Parse JSON payload into a Value in the requested mode."""
        ...

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
        """Freeze a Python object and wrap it in the requested mode."""
        ...

    @classmethod
    def strict(cls, data: Any, *, void_reasoning: bool = False) -> StrictValue:
        """Fail-fast Strict wrapper shortcut."""
        ...

    @classmethod
    def latent(
        cls, data: Any, *, missing_logger: MissingLogger | None = None, void_reasoning: bool = False
    ) -> LatentValue:
        """Safe Latent wrapper shortcut (default)."""
        ...

    @classmethod
    def dream(
        cls,
        data: Any,
        *,
        desire_logger: DesireLogger | None = None,
        missing_logger: MissingLogger | None = None,
        void_reasoning: bool = False,
    ) -> DreamValue:
        """Hallucination-tolerant Dream wrapper with optional desire logging."""
        ...

    @classmethod
    def safe(cls, data: Any) -> LatentValue:
        """Alias for latent()."""
        ...


__all__ = ["CrystallizerPort"]
