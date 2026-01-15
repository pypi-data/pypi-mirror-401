from __future__ import annotations

from typing import Any
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union

from darfix.core.dataset import ImageDataset

AxisAndValueIndices = Tuple[List[int], List[int]]

AxisType = Union[Literal["dims"], Literal["center"], None]


class Dataset:
    def __init__(
        self,
        dataset: ImageDataset,
        bg_dataset: Optional[ImageDataset] = None,
    ):
        """Darfix dataset and background

        :param dataset: Darfix dataset object that holds the image stack
        :param bg_dataset: Darfix dataset object that holds the dark image stack. Defaults to None.
        """
        self.dataset = dataset
        self.bg_dataset = bg_dataset


class DatasetTypeError(TypeError):
    def __init__(self, wrong_dataset: Any):
        """Error raised when a dataset has not the expected Dataset type"""
        super().__init__(
            f"Dataset is expected to be an instance of {Dataset}. Got {type(wrong_dataset)}."
        )
