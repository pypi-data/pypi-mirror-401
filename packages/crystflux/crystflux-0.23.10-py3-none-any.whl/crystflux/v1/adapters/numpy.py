"""NumPy adapter for CrystFlux value system."""

from __future__ import annotations

from typing import Any, Mapping

from crystflux.v1 import Crystallizer
from crystflux.v1.core.value_api import ValueAPI
from crystflux.v1.core.json_types import JsonValue
from crystflux.v1.boundary.mode_contracts import CrystMode, resolve_mode

import numpy as np
import numpy.typing as npt


class NumPyAdapter:
    """Adapter between CrystFlux values and NumPy arrays.

    Performance optimization currently achieves basic improvements through caching and dtype detection,
    but further detailed optimization via benchmarking and profiling remains a future challenge."""

    _conversion_cache: dict[str, Any] = {}
    _max_cache_size = 128

    @classmethod
    def _get_cache_key(cls, json_value: JsonValue, dtype: Any) -> str:
        """Generate cache key for conversion."""
        return f"{type(json_value).__name__}:{str(json_value)}:{dtype}"

    @classmethod
    def _cache_conversion(cls, key: str, result: Any) -> None:
        """Cache conversion result with LRU eviction."""
        if len(cls._conversion_cache) >= cls._max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(cls._conversion_cache))
            del cls._conversion_cache[oldest_key]
        cls._conversion_cache[key] = result

    @classmethod
    def _get_cached_conversion(cls, key: str) -> Any:
        """Get cached conversion result."""
        return cls._conversion_cache.get(key)

    @staticmethod
    def _detect_optimal_dtype(data: list[Any] | tuple[Any, ...], current_dtype: Any) -> Any:
        """Detect optimal dtype for array creation based on data content."""
        if current_dtype is not None or len(data) == 0:
            return current_dtype

        has_strings = any(isinstance(x, str) for x in data)
        has_mixed = len(data) > 1 and any(type(x) is not type(data[0]) for x in data)

        return object if (has_strings or has_mixed) else current_dtype

    @staticmethod
    def _create_array(data: list[Any] | tuple[Any, ...], dtype: Any) -> npt.NDArray[Any]:
        """Create NumPy array with optimal method based on data size."""
        if len(data) > 10000:
            return np.asarray(data, dtype=dtype)
        else:
            return np.array(data, dtype=dtype)

    @staticmethod
    def to_numpy(value: ValueAPI, dtype: npt.DTypeLike | None = None) -> npt.NDArray[Any]:
        """
        Convert a CrystFlux value to a NumPy array.

        Args:
            value: CrystFlux value to convert
            dtype: Optional NumPy dtype for the output array

        Returns:
            NumPy array representation of the value

        Raises:
            TypeError: If the value cannot be converted to a NumPy array
        """
        json_value = value.as_json_value()

        # Check cache first
        cache_key = NumPyAdapter._get_cache_key(json_value, dtype)
        cached_result = NumPyAdapter._get_cached_conversion(cache_key)
        if cached_result is not None:
            return cached_result

        # Perform conversion
        if isinstance(json_value, (list, tuple)):
            # Convert sequence to NumPy array
            data = json_value
            dtype = NumPyAdapter._detect_optimal_dtype(data, dtype)
            array = NumPyAdapter._create_array(data, dtype)
        elif isinstance(json_value, Mapping):
            # Convert dict values to NumPy array
            data = list(json_value.values())
            dtype = NumPyAdapter._detect_optimal_dtype(data, dtype)
            array = NumPyAdapter._create_array(data, dtype)
        elif isinstance(json_value, (int, float, bool)):
            # Convert scalar to NumPy array
            array = np.array([json_value], dtype=dtype)
        elif isinstance(json_value, type(None)):
            # Convert None to NumPy array with object dtype
            array = np.array([None], dtype=dtype or object)
        else:
            raise TypeError(
                f"Cannot convert {type(json_value).__name__} to NumPy array. "
                f"Supported types: list, tuple, dict, int, float, bool, None. "
                f"Got value: {json_value!r}"
            )

        # Cache the result
        NumPyAdapter._cache_conversion(cache_key, array)
        return array

    @staticmethod
    def from_numpy(array: npt.NDArray[Any], mode: CrystMode = "strict") -> ValueAPI:
        """
        Convert a NumPy array to a CrystFlux value.

        Args:
            array: NumPy array to convert
            mode: CrystFlux mode ("strict", "latent", "dream")

        Returns:
            CrystFlux value representation of the array
        """

        # Convert NumPy array to Python list
        if array.ndim == 0:
            # Scalar array - convert NumPy scalar to Python native type
            python_value = array.item()
            # Convert NumPy bool to Python bool (NumPy 1.x only)
            # NumPy 1.x: item() returns np.bool_; NumPy 2.x: item() returns Python bool
            if type(python_value) is np.bool_:
                python_value = bool(python_value)
        else:
            # Multi-dimensional array
            python_value = array.tolist()

        # Create CrystFlux value
        resolved_mode = resolve_mode(mode)
        return Crystallizer.from_dict(python_value, mode=resolved_mode)

    @staticmethod
    def to_numpy_safe(value: ValueAPI, dtype: npt.DTypeLike | None = None) -> npt.NDArray[Any] | None:
        """
        Safely convert a CrystFlux value to a NumPy array.
        Returns None for VOID values.
        """
        if value.is_void():
            return None
        return NumPyAdapter.to_numpy(value, dtype)

    @staticmethod
    def from_numpy_safe(array: npt.NDArray[Any], mode: CrystMode = "strict") -> ValueAPI:
        """
        Safely convert a NumPy array to a CrystFlux value.
        Handles edge cases gracefully.
        """
        try:
            # Check for unconvertible object arrays
            if array.dtype == object:
                # Try to convert each element to see if any are problematic
                for item in array.flat:
                    if isinstance(item, object) and type(item) is object:
                        # This is a generic object that can't be converted
                        from crystflux.v1.core import VOID

                        return VOID
            return NumPyAdapter.from_numpy(array, mode)
        except Exception:
            # Return VOID for any conversion errors
            from crystflux.v1.core import VOID

            return VOID

    @staticmethod
    def clear_cache() -> None:
        """Clear the conversion cache."""
        NumPyAdapter._conversion_cache.clear()

    @staticmethod
    def get_cache_stats() -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(NumPyAdapter._conversion_cache),
            "max_size": NumPyAdapter._max_cache_size,
        }


__all__ = [
    "NumPyAdapter",
]
