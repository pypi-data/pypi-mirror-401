import warnings

from .data_partition import DataPartition  # noqa: F401

warnings.warn(
    f"The '{__name__}' module is deprecated and will be removed in a future release. "
    "Please replace module name `datapartition` by `data_partition`",
    DeprecationWarning,
    stacklevel=2,
)
