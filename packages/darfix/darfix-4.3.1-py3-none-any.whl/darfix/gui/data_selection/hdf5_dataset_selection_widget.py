from __future__ import annotations

import h5py
from silx.gui import qt

from darfix.core.data_path_finder import DETECTOR_KEYWORD
from darfix.core.data_path_finder import FIRST_SCAN_KEYWORD
from darfix.core.data_path_finder import LAST_SCAN_KEYWORD
from darfix.gui.utils.data_path_selection import DataPathSelection
from darfix.gui.utils.fileselection import FileSelector
from darfix.tasks.hdf5_scans_concatenation import ConcatenateHDF5Scans


class HDF5DatasetSelectionWidget(qt.QWidget):
    """Widget to concatenate a series of scans together"""

    sigInputFileChanged = qt.Signal(str)

    DETECTOR_PATH_ALLOWED_KEYWORDS = (
        DETECTOR_KEYWORD,
        FIRST_SCAN_KEYWORD,
        LAST_SCAN_KEYWORD,
    )

    POSITIONER_PATH_ALLOWED_KEYWORDS = (
        FIRST_SCAN_KEYWORD,
        LAST_SCAN_KEYWORD,
    )

    def __init__(
        self,
        parent: qt.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())
        # input file selector
        self._inputFileSelector = FileSelector(label="input file:")
        self.layout().addWidget(self._inputFileSelector, 0, 0, 1, 5)
        self._inputFileSelector.setDialogFileMode(qt.QFileDialog.ExistingFile)
        self._inputFileSelector.setDialogNameFilters(
            ("HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",)
        )

        # detector data path
        self._detectorDataPath = DataPathSelection(
            self,
            title="detector-data path",
            completer_display_dataset=True,
            data_path_type=h5py.Dataset,
        )
        self._detectorDataPath.setPattern(
            ConcatenateHDF5Scans.DEFAULT_DETECTOR_DATA_PATH,
            store_as_default=True,
        )
        self._detectorDataPath.setAvailableKeywords(self.DETECTOR_PATH_ALLOWED_KEYWORDS)
        self.layout().addWidget(self._detectorDataPath, 1, 0, 1, 5)
        # positioner data path
        self._positionerDataPath = DataPathSelection(
            self,
            title="metadata path (positioners)",
            completer_display_dataset=False,
            data_path_type=h5py.Group,
        )
        self._positionerDataPath.setPattern(
            ConcatenateHDF5Scans.DEFAULT_POSITIONERS_DATA_PATH,
            store_as_default=True,
        )
        self._positionerDataPath.setAvailableKeywords(
            self.POSITIONER_PATH_ALLOWED_KEYWORDS
        )
        self.layout().addWidget(self._positionerDataPath, 2, 0, 1, 5)

        # spacer
        spacer = qt.QWidget()
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 999, 0, 1, 5)

        # connect signal / slot
        self._inputFileSelector.sigFileChanged.connect(self._inputFileChanged)

    def _inputFileChanged(self):
        input_file = self.getInputFile()
        self._detectorDataPath.setInputFile(input_file)
        self._positionerDataPath.setInputFile(input_file)
        self.sigInputFileChanged.emit(input_file)

    def getDetectorDataPathSelection(self) -> DataPathSelection:
        return self._detectorDataPath

    def getMetadataPathSelection(self) -> DataPathSelection | None:
        return self._positionerDataPath

    def setInputFile(self, file_path: str):
        self._inputFileSelector.setFilePath(file_path=file_path)
        self._inputFileChanged()

    def getInputFile(self) -> str | None:
        return self._inputFileSelector.getFilePath()
