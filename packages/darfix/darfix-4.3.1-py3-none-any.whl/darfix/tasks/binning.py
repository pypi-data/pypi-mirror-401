from __future__ import annotations

import numpy
import tqdm
from ewokscore import Task
from ewokscore.model import BaseInputModel
from pydantic import ConfigDict
from skimage.transform import rescale

from darfix.dtypes import Dataset


class Inputs(BaseInputModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
    dataset: Dataset
    """ Input dataset containing a stack of images """
    scale: float
    """Factor to rescale images of the dataset."""


class Binning(
    Task,
    input_model=Inputs,
    output_names=["dataset"],
):
    """Rescale images of a Darfix dataset by a given factor."""

    def run(self):
        input_dataset: Dataset = self.inputs.dataset
        dataset = input_dataset.dataset

        scale = self.inputs.scale

        # rescale data
        new_data = None
        for i, image in enumerate(
            tqdm.tqdm(dataset.as_array3d(), desc="Binning", total=dataset.nframes)
        ):
            simage = rescale(image, scale, anti_aliasing=True, preserve_range=True)
            if new_data is None:
                new_data = numpy.empty(
                    (dataset.nframes,) + simage.shape, dtype=dataset.data.dtype
                )
            new_data[i] = simage
            if self.cancelled:
                # if cancelled then self.outputs.dataset will be MISSING_DATA
                return

        new_dataset = dataset.copy(new_data=new_data)

        self.outputs.dataset = Dataset(
            dataset=new_dataset,
            bg_dataset=input_dataset.bg_dataset,
        )

    def cancel(self) -> None:
        """
        Cancel binning.
        """
        # Cancellation is very simple: binning is done image by image.
        # Between each image binning we check if the task has been cancelled.
        self.cancelled = True
