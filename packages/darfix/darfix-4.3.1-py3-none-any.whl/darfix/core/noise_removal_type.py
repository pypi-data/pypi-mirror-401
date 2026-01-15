from __future__ import annotations

from enum import Enum


class NoiseRemovalType(Enum):
    """
    Enumeration of existing Noise Removal Operations in Darfix
    """

    BS = 1
    HP = 2
    THRESHOLD = 3
    MASK = 9
