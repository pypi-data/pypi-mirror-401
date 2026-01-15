import warnings

from .noise_removal import NoiseRemoval  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `noiseremoval` by `noise_removal`",
    DeprecationWarning,
    stacklevel=2,
)
