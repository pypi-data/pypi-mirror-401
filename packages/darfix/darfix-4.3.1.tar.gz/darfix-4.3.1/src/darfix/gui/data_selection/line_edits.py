from __future__ import annotations

import h5py
from silx.gui import qt
from silx.gui.dialog.DatasetDialog import DatasetDialog
from silx.gui.dialog.GroupDialog import GroupDialog


class _BaseLineEdit(qt.QWidget):
    """
    A line edit for paths that can filled via a selection dialog.

    The dialog creation and result must be implemented in `_getDialogResult`
    """

    dialogSelected = qt.Signal(str)
    editingFinished = qt.Signal()

    _ERROR_LINE_EDIT_STYLE_SHEET = "border: 2px solid red"
    _INVALID_INPUT_TXT = "Invalid input."

    def __init__(self, parent: qt.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self._lineEdit = qt.QLineEdit()
        self._defaultLineEditStyle = self._lineEdit.styleSheet()
        self._errorMsgLabel = qt.QLabel()
        self._errorMsgLabel.setStyleSheet("color : red")
        self._errorMsgLabel.setText(self._INVALID_INPUT_TXT)
        self._errorMsgLabel.hide()
        browseButton = qt.QPushButton("Browse...")

        layout = qt.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._lineEdit)
        layout.addWidget(browseButton)
        layout.addWidget(self._errorMsgLabel)

        browseButton.clicked.connect(self._openDialog)
        self._lineEdit.editingFinished.connect(self._onEditFinished)

    def _getDialogResult(self) -> str | None:
        raise NotImplementedError()

    def _isValid(self, result: str) -> bool:
        raise NotImplementedError()

    def _openDialog(self):
        result = self._getDialogResult()
        if not result:
            return

        self._lineEdit.setText(result)

        if self.validateLineEdit():
            self.dialogSelected.emit(result)

    def _onEditFinished(self):
        if self.validateLineEdit():
            self.editingFinished.emit()

    def validateLineEdit(self) -> bool:
        isValid = self._isValid(self._lineEdit.text())
        if isValid:
            self._lineEdit.setStyleSheet(self._defaultLineEditStyle)
            self._errorMsgLabel.hide()
        else:
            self._lineEdit.setStyleSheet(self._ERROR_LINE_EDIT_STYLE_SHEET)
            self._errorMsgLabel.show()

        return isValid

    def setText(self, text: str):
        self._lineEdit.setText(text)
        self._onEditFinished()

    def getText(self) -> str:
        return self._lineEdit.text()


class H5FileLineEdit(_BaseLineEdit):
    """A line edit for file paths that can filled via a file selection dialog"""

    _INVALID_INPUT_TXT = "File does not exist or is not a valid H5 file."

    def _getDialogResult(self) -> None | str:
        dialog = qt.QFileDialog(filter="h5 file (*.h5 *.hdf *.hdf5 *.nx *.nxs)")
        result = dialog.exec()

        if not result:
            return None
        return dialog.selectedFiles()[0]

    def _isValid(self, result: str) -> bool:
        return h5py.is_hdf5(result)


class DatasetLineEdit(_BaseLineEdit):
    """
    A line edit for an HDF5 dataset path that can filled via a dataset selection dialog.
    The file needs to be set beforehand with `setFile`
    """

    _INVALID_INPUT_TXT = "Not a valid H5 dataset."

    def __init__(self, parent: qt.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._file = None

    def setFile(self, file: str):
        self._file = file

    def _getDialogResult(self) -> None | str:
        dialog = DatasetDialog()
        if self._file is None:
            return None

        dialog.addFile(self._file)
        result = dialog.exec()
        if not result:
            return None

        url = dialog.getSelectedDataUrl()
        return url.data_path() if url else None

    def _isValid(self, result: str) -> bool:
        if not h5py.is_hdf5(self._file):
            return False
        with h5py.File(self._file) as f:
            return isinstance(f.get(result), h5py.Dataset)


class GroupLineEdit(_BaseLineEdit):
    """
    A line edit for an HDF5 group path that can filled via a group selection dialog.
    The file needs to be set beforehand with `setFile`
    """

    _INVALID_INPUT_TXT = "Not a valid H5 group."

    dialogSelected = qt.Signal(str)
    editingFinished = qt.Signal()

    def __init__(self, parent: qt.QWidget | None = None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._file = None

    def setFile(self, file: str):
        self._file = file

    def _getDialogResult(self) -> None | str:
        dialog = GroupDialog()
        if self._file is None:
            return None

        dialog.addFile(self._file)
        result = dialog.exec()
        if not result:
            return None

        url = dialog.getSelectedDataUrl()
        return url.data_path() if url else None

    def _isValid(self, result: str) -> bool:
        if not h5py.is_hdf5(self._file):
            return False
        with h5py.File(self._file) as f:
            return isinstance(f.get(result), h5py.Group)
