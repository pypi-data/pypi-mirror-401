"""crystflux package root."""

from importlib.metadata import version

__version__ = version("crystflux")

from . import v1

__all__ = ["v1"]
