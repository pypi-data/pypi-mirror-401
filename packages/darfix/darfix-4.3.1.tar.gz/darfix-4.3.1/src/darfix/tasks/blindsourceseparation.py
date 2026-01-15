import warnings

from .blind_source_separation import BlindSourceSeparation  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `blindsourceseparation` by `blind_source_separation`",
    DeprecationWarning,
    stacklevel=2,
)
