from __future__ import annotations

import numpy
from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot import Plot2D

import darfix
from darfix import dtypes
from darfix.core.moment_types import MomentType
from darfix.gui.utils.custom_doublespinbox import createCustomDoubleSpinBox


class WeakBeamWidget(qt.QMainWindow):
    """
    Widget to recover weak beam to obtain dislocations.
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)

        widget = qt.QWidget()
        layout = qt.QGridLayout()

        self._nLE = createCustomDoubleSpinBox()

        self._plot = Plot2D()
        self._plot.setDefaultColormap(
            Colormap(
                name=darfix.config.DEFAULT_COLORMAP_NAME,
                normalization=darfix.config.DEFAULT_COLORMAP_NORM,
            )
        )
        layout.addWidget(
            qt.QLabel("Threshold of X times the standart deviation : "), 0, 0
        )
        layout.addWidget(self._nLE, 0, 1)
        layout.addWidget(self._plot, 1, 0, 1, 2)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # set up
        self.nvalue = 1

    @property
    def nvalue(self) -> float:
        return self._nLE.value()

    @nvalue.setter
    def nvalue(self, nvalue: float):
        self._nLE.setValue(nvalue)

    def updateDataset(self, dataset: dtypes.Dataset):
        imgDataset = dataset.dataset
        center_of_mass = imgDataset.moments_dims[0][MomentType.COM]
        transformation = imgDataset.transformation
        self._plot.clear()
        if transformation is None:
            self._plot.addImage(
                center_of_mass,
                xlabel="pixels",
                ylabel="pixels",
            )
        else:
            if transformation.rotate:
                center_of_mass = numpy.rot90(center_of_mass, 3)
            self._plot.addImage(
                center_of_mass,
                origin=transformation.origin,
                scale=transformation.scale,
                xlabel=transformation.label,
                ylabel=transformation.label,
            )
