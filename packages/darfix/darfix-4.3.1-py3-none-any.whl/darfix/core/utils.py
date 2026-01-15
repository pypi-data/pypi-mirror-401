from __future__ import annotations

import math

import numpy

TWO_PI = 2 * numpy.pi
SQRT_2 = math.sqrt(2)


class OperationAborted(Exception):
    """Raised when operation is aborted"""

    def __init__(self) -> None:
        super().__init__("Operation aborted.")


class NoDimensionsError(Exception):
    """Error raised when a method needing Darfix dimensions is called before the dimensions were found."""

    def __init__(self, method_name: str) -> None:
        super().__init__(
            f"{method_name} needs to have defined dimensions. Run `find_dimensions` before `{method_name}`."
        )


class TooManyDimensionsForRockingCurvesError(ValueError):
    def __init__(self) -> None:
        super().__init__(
            "Unsupported number of dimensions. Rocking curves only support 1D, 2D or 3D datasets."
        )
