from darfix.dtypes import Dataset
from darfix.tasks.weak_beam import WeakBeam


def test_weakbeam(input_dataset, tmp_path):
    input_dataset.find_dimensions()
    input_dataset.reshape_data()
    task = WeakBeam(inputs={"dataset": Dataset(input_dataset), "nvalue": 1})
    task.execute()
