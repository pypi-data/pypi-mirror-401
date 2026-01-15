from ewoksorange.gui.owwidgets.threaded import OWEwoksWidgetOneThread

from darfix.gui.utils.message import show_error_msg
from darfix.tasks.data_partition import DataPartition


class DataPartitionWidgetOW(OWEwoksWidgetOneThread, ewokstaskclass=DataPartition):
    """
    In cases with a large number of images you may want to omit the images with low intensity.
    This widget allows you to see an intensity curve of the images and to choose how many images you want to keep.
    At the next steps of the workflow only the images with higher intensity will be used for the analysis.
    """

    name = "partition data"
    icon = "icons/filter.png"
    want_main_area = False

    _ewoks_inputs_to_hide_from_orange = (
        "bins",
        "filter_bottom_bin_idx",
        "filter_top_bin_idx",
    )

    def handleNewSignals(self):
        show_error_msg(
            "This widget is legacy and will be removed in 5.0. To not break compatibility with existing workflows in 4.3, the widget is not removed but is now just a pass through that does not modify the dataset."
        )
        super().handleNewSignals()
