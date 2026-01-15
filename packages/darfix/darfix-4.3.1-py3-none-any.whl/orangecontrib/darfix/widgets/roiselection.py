from __future__ import annotations

import numpy
from ewokscore.missing_data import is_missing_data

from darfix import dtypes
from darfix.gui.roi_selection_widget import ROISelectionWidget
from darfix.tasks.roi import RoiSelection
from orangecontrib.darfix.widgets.operation_widget_base import OperationWidgetBase


class RoiSelectionWidgetOW(OperationWidgetBase, ewokstaskclass=RoiSelection):
    name = "roi selection"
    icon = "icons/roi.png"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("roi_origin", "roi_size")

    def __init__(self):
        super().__init__()

        # Connect Signals / Slots

        self.datasetChanged.connect(self.onDatasetChanged)
        self.sigOperationApplied.connect(self.onRoiApplied)

    def createMainWidget(self, default_inputs: dict) -> ROISelectionWidget:
        widget = ROISelectionWidget()
        return widget

    def saveMainWidget(self) -> dict:
        self.set_default_input(
            "roi_origin", tuple(self.mainWidget.getRoi().getOrigin())
        )
        self.set_default_input("roi_size", tuple(self.mainWidget.getRoi().getSize()))

    @property
    def mainWidget(self) -> ROISelectionWidget:
        return super().mainWidget

    def onRoiApplied(self, newDataset: dtypes.Dataset):
        self.mainWidget.setDataset(newDataset, roiEnabled=False)

    def onDatasetChanged(self, dataset: dtypes.Dataset):
        self.mainWidget.setDataset(dataset)
        if not self._tryRecoverLastRoi():
            self.mainWidget.setROIForNewDataset(dataset.dataset)
        else:
            self.mainWidget.clampRoiToDataset(dataset.dataset)

    def _tryRecoverLastRoi(self) -> bool:
        """Look at saved default input in .ows and try propose the roi on the current dataset."""
        origin = self.get_task_input_value("roi_origin")
        size = self.get_task_input_value("roi_size")

        if (
            is_missing_data(origin)
            or is_missing_data(size)
            or len(origin) != 2
            or len(size) != 2
        ):
            return False

        origin = numpy.array(origin)
        size = numpy.array(size)
        self.mainWidget.setRoi(size=size, origin=origin)

        return True
