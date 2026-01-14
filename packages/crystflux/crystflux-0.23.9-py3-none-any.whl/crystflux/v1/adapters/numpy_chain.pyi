"""
Stub for NumpyChain focused on IDE completion.

Scope:
- Lists ~50 stable, frequent ndarray methods/properties for long-term (5y+) hints.
- Returns align with runtime behavior (ndarray→NumpyChain, scalar→Any, in-place→None).
- Combination/splitting/where ops are available via NumPy functions
  (np.concatenate/stack/split/where) through __array__.

Example (Type-safe array extraction + NumPy one-liner):
    >>> json_data = {"scores": [85, 92, 78, 96, 88]}
    >>> cryst_value = Crystallizer.from_dict(json_data)
    >>> scores = cryst_value.get("scores")
    >>> above_90 = np.where(as_numpy_chain(scores).array > 90)[0]
    >>> above_90
    array([1, 3])

Docstrings are short and include quick examples for IDE users.
"""

from __future__ import annotations
from typing import Any, Optional
import numpy.typing as npt
from crystflux.v1.core.value_api import ValueAPI

class NumpyChain:
    """
    Context object providing transparent NumPy operations with automatic chaining.

    Wraps a NumPy array and forwards method calls, automatically wrapping returned
    arrays in new NumpyChain instances to enable fluent method chaining.

    Compatible with NumPy 1.20+ through 2.1+.
    """

    _array: npt.NDArray[Any]

    def __init__(self, array: npt.NDArray[Any]) -> None:
        """Initialize NumpyChain with a NumPy array."""
        ...

    @property
    def array(self) -> npt.NDArray[Any]:
        """Access the underlying NumPy array."""
        ...

    @property
    def shape(self) -> tuple[int, ...]:
        """Array dimensions."""
        ...

    @property
    def ndim(self) -> int:
        """Number of dimensions."""
        ...

    @property
    def size(self) -> int:
        """Total element count."""
        ...

    @property
    def dtype(self) -> Any:
        """Array dtype."""
        ...

    def to_cryst(self) -> ValueAPI:
        """
        Convert back to CrystFlux value.

        Returns:
            CrystFlux value representation of the array
        """
        ...

    # Dynamic fallback for all ndarray methods
    def __array__(self) -> npt.NDArray[Any]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __getitem__(self, key: Any) -> Any: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    # =========================================================================
    # SHAPE OPERATIONS - Restructure array dimensions
    # =========================================================================
    # These methods change the structure/layout of data without altering values
    # Critical for: batch processing, dimension alignment, data preparation

    def reshape(self, *shape: int, order: str = "C") -> NumpyChain:
        """
        Change array shape without changing data.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1,2,3,4])).reshape(2,2).shape
            (2, 2)
        """
        ...

    def transpose(self, *axes: int) -> NumpyChain:
        """
        Permute array dimensions.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([[1,2],[3,4]])).transpose().tolist()
            [[1, 3], [2, 4]]
        """
        ...

    @property
    def T(self) -> npt.NDArray[Any]:
        """Shorthand for transpose (ndarray result, matches runtime)."""
        ...

    def flatten(self, order: str = "C") -> NumpyChain:
        """
        Collapse array into 1D (copy).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([[1,2],[3,4]])).flatten().tolist()
            [1, 2, 3, 4]
        """
        ...

    def ravel(self, order: str = "C") -> NumpyChain:
        """
        Flatten to 1D (may return view).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([[1,2],[3,4]])).ravel().tolist()
            [1, 2, 3, 4]
        """
        ...

    def squeeze(self, axis: Optional[int | tuple[int, ...]] = None) -> NumpyChain:
        """
        Remove axes of length 1.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([[[1]], [[2]]])).squeeze().shape
            (2,)
        """
        ...

    def swapaxes(self, axis1: int, axis2: int) -> NumpyChain:
        """
        Interchange two axes.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([[[1],[2]]])).swapaxes(0,1).shape
            (1, 2, 1)
        """
        ...

    # =========================================================================
    # STATISTICAL OPERATIONS - Compute aggregates and statistics
    # =========================================================================
    # Reduce data to summary statistics or perform element-wise calculations
    # Essential for: data analysis, normalization, feature engineering

    def sum(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        dtype: Any = None,
        out: Any = None,
        keepdims: bool = False,
        initial: Any = None,
        where: Any = True,
    ) -> Any:
        """
        Sum over axis (scalar if axis=None).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1,2,3])).sum()
            6
        """
        ...

    def mean(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        dtype: Any = None,
        out: Any = None,
        keepdims: bool = False,
        where: Any = True,
    ) -> Any:
        """
        Arithmetic mean (scalar if axis=None).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1,2,3,4])).mean()
            2.5
        """
        ...

    def std(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        dtype: Any = None,
        out: Any = None,
        ddof: int = 0,
        keepdims: bool = False,
        where: Any = True,
    ) -> Any:
        """
        Standard deviation.

        Example:
            >>> round(as_numpy_chain(Crystallizer.strict([1,2,3])).std(), 2)
            0.82
        """
        ...

    def var(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        dtype: Any = None,
        out: Any = None,
        ddof: int = 0,
        keepdims: bool = False,
        where: Any = True,
    ) -> Any:
        """
        Variance (var = std**2).

        Example:
            >>> round(as_numpy_chain(Crystallizer.strict([1,2,3])).var(), 2)
            0.67
        """
        ...

    def min(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        out: Any = None,
        keepdims: bool = False,
        initial: Any = None,
        where: Any = True,
    ) -> Any:
        """
        Minimum value (scalar if axis=None).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([2,5,1])).min()
            1
        """
        ...

    def max(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        out: Any = None,
        keepdims: bool = False,
        initial: Any = None,
        where: Any = True,
    ) -> Any:
        """
        Maximum value (scalar if axis=None).

        Example:
            >>> as_numpy_chain(Crystallizer.strict([2,5,1])).max()
            5
        """
        ...

    def cumsum(
        self, axis: Optional[int] = None, dtype: Any = None, out: Any = None
    ) -> NumpyChain:
        """
        Cumulative sum along axis.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1,2,3])).cumsum().tolist()
            [1, 3, 6]
        """
        ...

    def prod(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        dtype: Any = None,
        out: Any = None,
        keepdims: bool = False,
        initial: Any = None,
        where: Any = True,
    ) -> Any:
        """
        Product of elements over axis.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([2, 3, 4])).prod()
            24
        """
        ...

    def all(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        out: Any = None,
        keepdims: bool = False,
        where: Any = True,
    ) -> Any:
        """
        Test if all elements are True.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([True, True, False])).all()
            False
        """
        ...

    def any(
        self,
        axis: Optional[int | tuple[int, ...]] = None,
        out: Any = None,
        keepdims: bool = False,
        where: Any = True,
    ) -> Any:
        """
        Test if any element is True.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([False, False, True])).any()
            True
        """
        ...

    # =========================================================================
    # SELECTION & INDEXING - Extract and order elements
    # =========================================================================
    # Methods for ordering, filtering, and extracting specific elements
    # Key for: ranking, top-k selection, data filtering

    def sort(self, axis: int = -1, kind: Optional[str] = None, order: Any = None) -> None:
        """
        Sort in-place along axis (returns None).

        Example:
            >>> ctx = as_numpy_chain(Crystallizer.strict([3, 1, 4, 1]))
            >>> ctx.sort()  # in-place sort
            >>> ctx.tolist()
            [1, 1, 3, 4]  # sorted array
        """
        ...

    def argsort(
        self, axis: int = -1, kind: Optional[str] = None, order: Any = None
    ) -> NumpyChain:
        """
        Indices that would sort the array.

        Example:
            >>> ctx = as_numpy_chain(Crystallizer.strict([3, 1, 4, 1]))
            >>> ctx.argsort().tolist()
            [1, 3, 0, 2]  # indices that would sort the array
        """
        ...

    def argmax(self, axis: Optional[int] = None, out: Any = None, keepdims: bool = False) -> Any:
        """
        Indices of maximum values.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([10, 50, 20])).argmax()
            1  # index of maximum value
        """
        ...

    def argmin(self, axis: Optional[int] = None, out: Any = None, keepdims: bool = False) -> Any:
        """
        Indices of minimum values.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([10, 50, 20])).argmin()
            0  # index of minimum value
        """
        ...

    def take(
        self, indices: Any, axis: Optional[int] = None, out: Any = None, mode: str = "raise"
    ) -> NumpyChain:
        """
        Extract elements at given indices.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([10, 20, 30, 40])).take([0, 2]).tolist()
            [10, 30]
        """
        ...

    def clip(self, min: Any = None, max: Any = None, out: Any = None) -> NumpyChain:
        """
        Limit values to a range.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1, 5, 10, 15])).clip(min=3, max=12).tolist()
            [3, 5, 10, 12]
        """
        ...

    def repeat(self, repeats: int | tuple[int, ...], axis: Optional[int] = None) -> NumpyChain:
        """
        Repeat elements along an axis.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1, 2, 3])).repeat(2).tolist()
            [1, 1, 2, 2, 3, 3]
        """
        ...

    def compress(self, condition: Any, axis: Optional[int] = None, out: Any = None) -> NumpyChain:
        """
        Select slices by boolean condition.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([10,20,30,40])).compress([False,True,False,True]).tolist()
            [20, 40]  # elements where condition is True
        """
        ...

    def nonzero(self) -> tuple[npt.NDArray[Any], ...]:
        """
        Indices of non-zero elements.

        Examples:
            >>> # 1D case - simple array
            >>> as_numpy_chain(Crystallizer.strict([0, 10, 0, 20])).nonzero()
            (array([1, 3]),)

            >>> # 2D case - returns (row_indices, col_indices) tuple
            >>> grid = Crystallizer.strict([[0, 1, 0], [2, 0, 3]])
            >>> as_numpy_chain(grid).nonzero()
            (array([0, 1, 1]), array([1, 0, 2]))
        """
        ...

    # =========================================================================
    # TYPE & VALUE OPERATIONS - Convert types and modify values
    # =========================================================================
    # Methods that change data representation or element-wise values
    # Important for: data type management, precision control

    def astype(
        self,
        dtype: Any,
        order: str = "K",
        casting: str = "unsafe",
        subok: bool = True,
        copy: bool = True,
    ) -> NumpyChain:
        """
        Cast array to specified dtype.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1, 2, 3])).astype(float).tolist()
            [1.0, 2.0, 3.0]
        """
        ...

    def round(self, decimals: int = 0, out: Any = None) -> NumpyChain:
        """
        Round to given decimals.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1.234, 5.678, 9.012])).round(2).tolist()
            [1.23, 5.68, 9.01]  # rounded to 2 decimal places
        """
        ...

    def copy(self, order: str = "K") -> NumpyChain:
        """
        Return a copy of the array.

        Example:
            >>> original = as_numpy_chain(Crystallizer.strict([1, 2, 3]))
            >>> copied = original.copy()
            >>> copied.tolist()
            [1, 2, 3]  # independent copy of the array
        """
        ...

    def fill(self, value: Any) -> None:
        """
        Fill the array with a scalar value (in-place).

        Example:
            >>> ctx = as_numpy_chain(Crystallizer.strict([0, 0, 0]))
            >>> ctx.fill(99)
            >>> ctx.tolist()
            [99, 99, 99]  # array filled with scalar value

            >>> # fill() returns None, so chaining fails
            >>> # as_numpy_chain(Crystallizer.strict([0, 0, 0])).fill(99).tolist()  # AttributeError
        """
        ...

    def item(self, *args: Any) -> Any:
        """
        Extract a Python scalar from the array.

        Examples:
            >>> # Extract scalar from multi-dimensional array
            >>> ctx = as_numpy_chain(Crystallizer.strict([[1, 2], [3, 4]]))
            >>> ctx.item(1, 0)  # row 1, column 0
            3

            >>> # Note: NumPy scalars are auto-converted to Python types
            >>> result = as_numpy_chain(Crystallizer.strict([1, 2, 3, 4])).sum()
            >>> result  # Already a Python int, no .item() needed
            10
        """
        ...

    def tolist(self) -> list[Any]:
        """
        Convert array to nested Python lists.

        Example:
            >>> as_numpy_chain(Crystallizer.strict([1, 2, 3])).tolist()
            [1, 2, 3]
        """
        ...

    # Operators (explicit for completion)
    def __add__(self, other: Any) -> Any: ...
    def __sub__(self, other: Any) -> Any: ...
    def __mul__(self, other: Any) -> Any: ...
    def __truediv__(self, other: Any) -> Any: ...
    def __matmul__(self, other: Any) -> Any: ...
    def __pow__(self, other: Any) -> Any: ...

def as_numpy_chain(value: ValueAPI, dtype: Optional[npt.DTypeLike] = None) -> NumpyChain:
    """
    Convert a CrystFlux value to NumpyChain for fluent NumPy operations.

    This function bridges CrystFlux's value system with NumPy's array operations,
    enabling method chaining for complex data transformations.

    Args:
        value: CrystFlux value to convert (must be array-like in strict mode)
        dtype: Optional NumPy dtype for output array

    Returns:
        NumpyChain wrapping the converted array

    Raises:
        TypeError: If value cannot be converted to NumPy array

    Examples:
        >>> from crystflux.v1 import Crystallizer
        >>> data = Crystallizer.strict([1, 2, 3, 4, 5, 6])
        >>> result = as_numpy_chain(data).reshape(2, 3).transpose().to_cryst()
        >>> print(result.as_json_value())
        ((1, 4), (2, 5), (3, 6))

        >>> # Normalization pipeline
        >>> raw = Crystallizer.strict([10.0, 20.0, 30.0, 40.0, 50.0])
        >>> ctx = as_numpy_chain(raw)
        >>> normalized = ctx.__sub__(ctx.mean()).__truediv__(ctx.std()).to_cryst()
    """
    ...

__all__ = ["NumpyChain", "as_numpy_chain"]
