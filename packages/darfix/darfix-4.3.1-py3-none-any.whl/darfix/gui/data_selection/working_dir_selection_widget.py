import logging

from silx.gui import qt

from ..utils.utils import create_completer

_logger = logging.getLogger(__name__)


class WorkingDirSelectionWidget(qt.QWidget):
    """
    Widget used to obtain a directory name
    """

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._directoryLineEdit = qt.QLineEdit("", parent=self)
        self.completer = create_completer()
        self._directoryLineEdit.setCompleter(self.completer)

        self._addButton = qt.QPushButton("Select working directory", parent=self)
        self.setLayout(qt.QHBoxLayout())

        self.layout().addWidget(self._directoryLineEdit)
        self.layout().addWidget(self._addButton)

        # Connect Signals / Slots

        self._addButton.pressed.connect(self._selectWorkingDirectory)

    def _selectWorkingDirectory(self):
        """
        Select a folder to be used as working directory (task results will be saved at this location)
        """
        fileDialog = qt.QFileDialog()
        fileDialog.setOption(qt.QFileDialog.ShowDirsOnly)
        fileDialog.setFileMode(qt.QFileDialog.Directory)
        if fileDialog.exec():
            self._directoryLineEdit.setText(fileDialog.directory().absolutePath())
        else:
            _logger.warning("Could not open directory")

    def getDir(self) -> str:
        return str(self._directoryLineEdit.text())

    def setDir(self, working_directory: str):
        self._directoryLineEdit.setText(str(working_directory))

    def setDefaultDir(self, default_dir: str):
        self._directoryLineEdit.setPlaceholderText(default_dir + " (default)")
