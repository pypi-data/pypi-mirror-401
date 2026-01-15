__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "26/04/2021"

import logging

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.items.roi import RectangleROI
from silx.gui.plot.StackView import StackViewMainWindow
from silx.gui.plot.tools.roi import RegionOfInterestManager

import darfix
from darfix import dtypes
from darfix.core.roi import clampROI

from .roi_limits_toolbar import RoiLimitsToolBar

_logger = logging.getLogger(__file__)


class ROISelectionWidget(qt.QWidget):
    """
    Widget that allows the user to pick a ROI in any image of the dataset.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(qt.QVBoxLayout())
        self._sv = StackViewMainWindow()

        self._sv.setColormap(
            Colormap(
                name=darfix.config.DEFAULT_COLORMAP_NAME,
                normalization=darfix.config.DEFAULT_COLORMAP_NORM,
            )
        )
        self._sv.setKeepDataAspectRatio(True)
        self.layout().addWidget(self._sv)

        plot = self._sv.getPlotWidget()

        self._roiManager = RegionOfInterestManager(plot)

        self._roi = RectangleROI()
        self._roi.setText("ROI")
        self._roi.setGeometry(origin=(0, 0), size=(10, 10))
        self._roi.setEditable(True)
        self._roiManager.addRoi(self._roi)

        self._roiToolBar = RoiLimitsToolBar(roiManager=self._roiManager)
        self._sv.addToolBar(qt.Qt.BottomToolBarArea, self._roiToolBar)

    def setDataset(self, dataset: dtypes.Dataset, roiEnabled: bool = True):
        """Saves the dataset and updates the stack with the dataset data."""
        if dataset.dataset.title != "":
            self._sv.setGraphTitle(dataset.dataset.title)
        self._roi.setVisible(roiEnabled)
        self._roiToolBar.setEnabled(roiEnabled)
        self._setStack(dataset=dataset.dataset)

    def setROIForNewDataset(self, dataset: dtypes.ImageDataset):
        if not isinstance(dataset, dtypes.ImageDataset):
            raise dtypes.DatasetTypeError(dataset)
        first_frame_shape = dataset.frame_shape
        center = first_frame_shape[1] // 2, first_frame_shape[0] // 2
        size = first_frame_shape[1] // 5, first_frame_shape[0] // 5
        self.setRoi(center=center, size=size)

    def _setStack(self, dataset: dtypes.ImageDataset):
        """
        Sets new data to the stack.
        Maintains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        if not isinstance(dataset, dtypes.ImageDataset):
            raise TypeError(
                f"dataset is expected to be an instance of {dtypes.ImageDataset}. Got {type(dataset)}."
            )

        nframe = self._sv.getFrameNumber()
        self._sv.setStack(dataset.as_array3d())
        self._sv.setFrameNumber(nframe)

    def setRoi(self, roi=None, origin=None, size=None, center=None):
        """
        Sets a region of interest of the stack of images.

        :param RectangleROI roi: A region of interest.
        :param Tuple origin: If a roi is not provided, used as an origin for the roi
        :param Tuple size: If a roi is not provided, used as a size for the roi.
        :param Tuple center: If a roi is not provided, used as a center for the roi.
        """
        if roi is not None and (
            size is not None or center is not None or origin is not None
        ):
            _logger.warning(
                "Only using provided roi, the rest of parameters are omitted"
            )

        if roi is not None:
            self._roi = roi
        else:
            self._roi.setGeometry(origin=origin, size=size, center=center)

    def getRoi(self):
        """
        Returns the roi selected in the stackview.

        :rtype: silx.gui.plot.items.roi.RectangleROI
        """
        return self._roi

    def clampRoiToDataset(self, dataset: dtypes.ImageDataset):
        frame_height, frame_width = dataset.frame_shape
        # warning: we need to invert the order of the frame shape (frame_height, frame_width) vs (frame_width, frame_height)
        new_origin, new_size = clampROI(
            roi_origin=self._roi.getOrigin(),
            roi_size=self._roi.getSize(),
            frame_origin=(0, 0),
            frame_size=(frame_width, frame_height),
        )
        self._roi.setGeometry(
            origin=new_origin,
            size=new_size,
        )
