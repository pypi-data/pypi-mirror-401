import warnings

from darfix.core.noise_removal_type import NoiseRemovalType

warnings.warn(
    "Use of `Operation` class is deprecated and is only kept for backward compatibility with .ows file from Darfix < 4.3.",
    DeprecationWarning,
)
Operation = NoiseRemovalType
