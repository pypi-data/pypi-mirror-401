import warnings

from .dimension_definition import DimensionDefinition  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `dimensiondefinition` by `dimension_definition`",
    DeprecationWarning,
    stacklevel=2,
)
