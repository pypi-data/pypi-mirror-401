import warnings

from .grain_plot import GrainPlot  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `grainplot` by `grain_plot`",
    DeprecationWarning,
    stacklevel=2,
)
