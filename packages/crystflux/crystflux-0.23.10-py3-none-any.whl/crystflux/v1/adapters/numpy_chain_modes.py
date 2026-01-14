"""Internal chain-mode carriers for NumPy chaining (strict/latent/dream).

These classes are intentionally thin: they only carry mode/context metadata.
Behavior remains in NumpyChain; mode-specific behavior will be defined later.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .base_chain_vesicle import BaseChainVesicle
from ..boundary.mode_contracts import CrystMode


@dataclass(frozen=True)
class StrictNumpyChain(BaseChainVesicle):
    """Strict mode carrier; behavior lives in NumpyChain."""
    mode: CrystMode = field(default="strict", init=False)


@dataclass(frozen=True)
class LatentNumpyChain(BaseChainVesicle):
    """Latent mode carrier (future behavior)."""
    mode: CrystMode = field(default="latent", init=False)


@dataclass(frozen=True)
class DreamNumpyChain(BaseChainVesicle):
    """Dream mode carrier (future behavior)."""
    mode: CrystMode = field(default="dream", init=False)


__all__ = ["StrictNumpyChain", "LatentNumpyChain", "DreamNumpyChain"]
