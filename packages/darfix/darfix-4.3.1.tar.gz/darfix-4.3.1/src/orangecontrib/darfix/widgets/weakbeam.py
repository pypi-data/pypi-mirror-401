import logging

from darfix import dtypes
from darfix.gui.weak_beam_widget import WeakBeamWidget
from darfix.tasks.weak_beam import WeakBeam
from orangecontrib.darfix.widgets.operation_widget_base import OperationWidgetBase

_logger = logging.getLogger(__name__)


class WeakBeamWidgetOW(
    OperationWidgetBase,
    ewokstaskclass=WeakBeam,
):
    """
    Widget that computes dataset with filtered weak beam and recover its Center of Mass.
    """

    name = "weak beam"
    icon = "icons/gaussian.png"
    want_main_area = True
    want_control_area = False

    _ewoks_inputs_to_hide_from_orange = ("nvalue", "title")

    def __init__(self):
        super().__init__()
        self.sigOperationApplied.connect(self.__onOperationApplied)
        self.buttons.resetButton.hide()

    def createMainWidget(self, default_inputs: dict) -> WeakBeamWidget:
        widget = WeakBeamWidget()
        widget.nvalue = default_inputs.get("nvalue", 1.0)
        return widget

    def saveMainWidget(self) -> dict:
        self.set_default_input("nvalue", self.mainWidget.nvalue)

    def __onOperationApplied(self, dataset: dtypes.Dataset):
        self.mainWidget.updateDataset(dataset)
        # this trick re-enable button apply directly
        self.reset()

    @property
    def mainWidget(self) -> WeakBeamWidget:
        return super().mainWidget
