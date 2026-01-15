import warnings

from .weak_beam import WeakBeam  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `weakbeam` by `weak_beam`",
    DeprecationWarning,
    stacklevel=2,
)
