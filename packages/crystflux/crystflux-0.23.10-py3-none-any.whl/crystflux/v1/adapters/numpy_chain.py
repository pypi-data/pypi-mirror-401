"""Enhanced NumPy integration with method chaining support for CrystFlux."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt
from typing import Any, Callable, Optional, cast

from crystflux.v1.core.value_api import ValueAPI
from crystflux.v1.boundary.mode_contracts import infer_value_mode

from .base_chain_vesicle import EmptyChainContext
from .numpy_chain_modes import DreamNumpyChain, LatentNumpyChain, StrictNumpyChain


class NumpyChain:
    """
    Context object that provides transparent NumPy operations with automatic chaining.

    This class wraps a NumPy array and forwards attribute/method access to the
    underlying ndarray. Method calls are wrapped to keep chaining alive when the
    result is an ndarray. IDE completion is provided by `numpy_chain.pyi`, while
    runtime behavior is driven by `__getattr__`.

    Design notes (strict-first):
    - Only NumPy arrays are re-wrapped to continue chaining.
    - NumPy scalars / Python scalars are returned as-is (no wrapping) to keep
      behavior predictable; convert back via Crystallizer.strict(...) if needed.
    """

    def __init__(
        self,
        array: npt.NDArray[Any],
        *,
        _vesicle: StrictNumpyChain | LatentNumpyChain | DreamNumpyChain | None = None,
    ):
        """
        Initialize NumpyChain with a NumPy array.

        Args:
            array: NumPy array to wrap
        """
        self._array: npt.NDArray[Any] = np.asarray(array)
        if _vesicle is None:
            self._vesicle = StrictNumpyChain(context=EmptyChainContext(), sentinel=None)
        else:
            self._vesicle = _vesicle

    @property
    def array(self) -> npt.NDArray[Any]:
        """
        Get the underlying NumPy array.

        Returns:
            The wrapped NumPy array
        """
        return self._array

    def to_cryst(self) -> ValueAPI:
        """
        Convert back to CrystFlux value.

        Uses the vesicle mode inferred at entry.

        Returns:
            CrystFlux value representation of the array
        """
        # Import NumPyAdapter locally to avoid circular imports
        from .numpy import NumPyAdapter

        return NumPyAdapter.from_numpy(self._array, self._vesicle.mode)

    def __getattr__(self, name: str) -> Any:
        """
        Transparently forward attribute access to the underlying NumPy array.

        For method calls, automatically wraps returned arrays in new NumpyChain
        instances to enable fluent chaining. Scalar results are returned as-is.

        Args:
            name: Attribute name

        Returns:
            The attribute or a wrapped method

        Raises:
            AttributeError: If the attribute doesn't exist on the array
        """
        # Get the attribute from the underlying array
        attr: Any = getattr(self._array, name)

        # If it's a method, create a wrapper that preserves chaining
        if callable(attr):
            typed_attr = cast(Callable[..., Any], attr)

            def method_wrapper(*args: Any, **kwargs: Any) -> Any:
                """Wrapper that preserves NumpyChain chaining."""
                result: Any = typed_attr(*args, **kwargs)

                # If the result is array-like, wrap to keep chaining alive
                if isinstance(result, np.ndarray):
                    arr_result = cast(npt.NDArray[Any], result)
                    return NumpyChain(arr_result, _vesicle=self._vesicle)
                # Scalars (NumPy generic or Python) are returned raw for predictability
                if isinstance(result, np.generic):
                    return cast(Any, result.item())
                return result

            return method_wrapper

        # If it's not a method, return the attribute directly
        return attr

    def __repr__(self) -> str:
        """String representation of the NumpyChain."""
        return f"NumpyChain(shape={self._array.shape}, dtype={self._array.dtype})"

    def __str__(self) -> str:
        """String representation of the underlying array."""
        return str(self._array)

    # Allow passing this object directly into NumPy APIs (np.mean, etc.)
    def __array__(self) -> npt.NDArray[Any]:  # pragma: no cover - passthrough
        return self._array


def as_numpy_chain(value: ValueAPI, dtype: Optional[npt.DTypeLike] = None) -> NumpyChain:
    """
    Convert a CrystFlux value to a NumpyChain for fluent NumPy operations.
    ValueAPIのモードを引き継ぐ（strict/latent/dream）。

    Args:
        value: CrystFlux value to convert
        dtype: Optional NumPy dtype for the output array
        
    Returns:
        NumpyChain wrapping the converted array
        
    Raises:
        TypeError: If the value cannot be converted to a NumPy array
        
    Examples:
        >>> from crystflux.v1 import Crystallizer
        >>> data = Crystallizer.strict([1, 2, 3, 4, 5])
        >>> result = as_numpy_chain(data).reshape(2, 2).transpose().to_cryst()
        >>> print(result.as_json_value())
        ((1, 3), (2, 4))
    """
    # Import NumPyAdapter locally to avoid circular imports
    from .numpy import NumPyAdapter
    array: npt.NDArray[Any] = NumPyAdapter.to_numpy(value, dtype)
    mode = infer_value_mode(value)
    context = EmptyChainContext()
    if mode == "strict":
        vesicle = StrictNumpyChain(context=context, sentinel=None)
    elif mode == "latent":
        vesicle = LatentNumpyChain(context=context, sentinel=None)
    else:
        vesicle = DreamNumpyChain(context=context, sentinel=None)
    return NumpyChain(array, _vesicle=vesicle)


__all__ = [
    "NumpyChain",
    "as_numpy_chain",
]
