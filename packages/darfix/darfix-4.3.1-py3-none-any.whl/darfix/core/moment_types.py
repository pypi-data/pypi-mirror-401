from __future__ import annotations

from enum import Enum
from typing import Dict

import numpy


class MomentType(Enum):
    COM = "Center of mass"
    FWHM = "FWHM"
    SKEWNESS = "Skewness"
    KURTOSIS = "Kurtosis"


MomentsPerDimension = Dict[int, Dict[MomentType, numpy.ndarray]]
