import warnings

from .shift_correction import ShiftCorrection  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `shiftcorrection` by `shift_correction`",
    DeprecationWarning,
    stacklevel=2,
)
