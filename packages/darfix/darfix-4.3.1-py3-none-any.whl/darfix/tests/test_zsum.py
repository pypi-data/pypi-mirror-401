import numpy

from darfix.core.image_stack import FixedDimension


def test_zsum(dataset):

    dataset.find_dimensions()
    dataset.reshape_data()
    result = numpy.sum(
        dataset.get_filtered_data(fixed_dimension=FixedDimension(0, 1)),
        axis=0,
    )
    zsum = dataset.zsum(dimension=FixedDimension(0, 1))
    numpy.testing.assert_array_equal(zsum, result)
