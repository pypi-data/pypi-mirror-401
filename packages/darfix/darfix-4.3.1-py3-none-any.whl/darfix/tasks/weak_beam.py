from __future__ import annotations

import copy
import os
import string

import h5py
import numpy
from ewokscore import Task
from ewokscore.missing_data import MISSING_DATA
from ewokscore.missing_data import MissingData
from ewokscore.model import BaseInputModel
from pydantic import ConfigDict

from darfix import dtypes
from darfix.core.moment_types import MomentType


class Inputs(BaseInputModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    dataset: dtypes.Dataset
    """Input dataset containing a stack of images."""
    nvalue: float | MissingData = MISSING_DATA
    """Increase or decrease the top threshold (threshold = `nvalue` * std)"""
    title: str | MissingData = MISSING_DATA
    """Title for the output file. If not provided, title is empty."""
    copy_dataset: bool = False
    """If `True`, operations are applied on a copy of the input dataset. Else, operations are applied directly on the input dataset"""


class WeakBeam(
    Task,
    input_model=Inputs,
    output_names=["dataset"],
):
    """
    Obtain dataset with filtered weak beam and recover its Center of Mass.
    Save file with this COM for further processing.
    """

    def run(self):
        inputs = Inputs(**self.get_input_values())

        dataset = inputs.dataset

        if inputs.copy_dataset:
            dataset = copy.deepcopy(dataset)

        nvalue = inputs.nvalue

        img_dataset = dataset.dataset

        img_dataset.recover_weak_beam(nvalue)
        com = img_dataset.apply_moments()[0][MomentType.COM]
        os.makedirs(img_dataset.dir, exist_ok=True)
        filename = os.path.join(img_dataset.dir, "weakbeam_{}.hdf5".format(nvalue))

        title = self.get_input_value("title", "")
        # title can be set to None, MISSING_DATA or an empty string. So safer to use the following line
        title = title or self.get_random_title()
        with h5py.File(filename, "a") as _file:
            _file[title] = com

        self.outputs.dataset = dtypes.Dataset(
            dataset=img_dataset,
        )

    @staticmethod
    def get_random_title() -> str:
        letters = string.ascii_lowercase
        return "".join(numpy.random.choice(list(letters)) for i in range(6))
