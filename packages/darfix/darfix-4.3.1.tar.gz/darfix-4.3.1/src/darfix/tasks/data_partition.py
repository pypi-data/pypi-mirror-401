from __future__ import annotations

import warnings

from ewokscore import Task
from ewokscore.missing_data import MISSING_DATA
from ewokscore.missing_data import MissingData
from ewokscore.model import BaseInputModel
from pydantic import ConfigDict

from darfix import dtypes


class Inputs(BaseInputModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    dataset: dtypes.Dataset
    bins: int | MissingData = MISSING_DATA
    filter_bottom_bin_idx: int | MissingData = MISSING_DATA
    filter_top_bin_idx: int | MissingData = MISSING_DATA


class DataPartition(
    Task,
    input_model=Inputs,
    output_names=["dataset"],
):
    """
    :deprecated: Deprecated task to be removed in 5.0.
    """

    def run(self):
        warnings.warn(
            "`DataPartition` is a legacy task and is poorly tested in Darfix. Before 4.3, it might induce weird behaviour in the next tasks of the workflow."
            "In 4.3, the low intensity filtering is deactivate and the task does not modify the dataset. This just does nothing in order to not break compatibility with existing workflows."
            "In 5.0, the task will be removed.",
            DeprecationWarning,
        )
        # Just a pass through
        self.outputs.dataset = self.inputs.dataset
