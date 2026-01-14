"""Exception contracts shared across layers (no behavior beyond typing)."""

class CrystfluxError(Exception):
    """Base exception for crystflux."""


class InvalidJsonPayloadError(CrystfluxError):
    """Raised when JSON parsing fails or payload is invalid."""


class ModeNotSupportedError(CrystfluxError):
    """Raised when an unknown mode is requested."""


__all__ = ["CrystfluxError", "InvalidJsonPayloadError", "ModeNotSupportedError"]
