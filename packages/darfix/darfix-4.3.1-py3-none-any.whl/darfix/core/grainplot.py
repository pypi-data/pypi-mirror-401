from __future__ import annotations

import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Tuple

import colorstamps
import numpy
from silx.math.medianfilter import medfilt2d

from darfix.core.dimension import AcquisitionDims
from darfix.core.transformation import Transformation
from darfix.io.utils import create_nxdata_dict

from ..dtypes import AxisType
from ..dtypes import Dataset
from .moment_types import MomentsPerDimension
from .moment_types import MomentType

DimensionRange = Tuple[float, float]


@dataclass
class GrainPlotMaps:
    dims: AcquisitionDims
    moments_dims: MomentsPerDimension
    zsum: numpy.ndarray
    transformation: numpy.ndarray
    title: str

    @staticmethod
    def from_dataset(dataset: Dataset) -> GrainPlotMaps:
        """
        Just retrieve all necessary attributes in `ImageDataset` object to return a `GrainPlotMaps` object.

        :Note:  zsum computation is executed
        """
        imgDataset = dataset.dataset
        return GrainPlotMaps(
            dims=imgDataset.dims,
            moments_dims=imgDataset.moments_dims,
            zsum=imgDataset.zsum(),
            transformation=imgDataset.transformation,
            title=imgDataset.title,
        )


class GrainPlotData:
    KEY_IMAGE_SIZE = 1000

    def __init__(
        self,
        grain_plot_maps: GrainPlotMaps,
        x_dimension: int,
        y_dimension: int,
        x_dimension_range: DimensionRange,
        y_dimension_range: DimensionRange,
        zsum: numpy.ndarray | None = None,
        colormap_name: str = "hsv",
        sat: int = 40,
    ) -> None:
        """
        Store data for orientation distribution RGB layer (the HSV colormap) and data (Histogram 2D)

        :param zsum: Precomputed dataset.zsum() used as the weight of the histogram 2D . If None dataset.zsum() is called.

        :param colormap_name: See https://colorstamps.readthedocs.io/en/latest/index.html#quick-reference

        :param sat: See https://colorstamps.readthedocs.io/en/latest/stamps.html#colorstamps.stamps.get_cmap
        """

        if len(grain_plot_maps.moments_dims) == 0:
            raise ValueError("Moments should be computed before.")

        com_x = grain_plot_maps.moments_dims[x_dimension][MomentType.COM]
        com_y = grain_plot_maps.moments_dims[y_dimension][MomentType.COM]

        self.x_range = x_dimension_range
        self.y_range = y_dimension_range

        if zsum is None:
            zsum = grain_plot_maps.zsum

        # automatic bins
        # In darfix<=3.x orientation distribution shape was the size of the dimension
        # A x2 Factor is a little thinner. To see if it needs to be update in the future.
        self.x_bins = grain_plot_maps.dims.get(x_dimension).size * 2
        self.y_bins = grain_plot_maps.dims.get(y_dimension).size * 2

        self.x_label = grain_plot_maps.dims.get(x_dimension).name
        self.y_label = grain_plot_maps.dims.get(y_dimension).name

        # Histogram in 2D
        histogram, _, _ = numpy.histogram2d(
            com_y.ravel(),
            com_x.ravel(),  # note: y first is in purpose : see numpy.histogram2d documentation
            weights=zsum.ravel(),  # We need to take into account pixel intensity
            bins=[self.y_bins, self.x_bins],
            range=[self.y_range, self.x_range],
        )
        self.data = histogram
        """Orientation distribution data as an histogram 2D of the center of mass in two dimensions"""
        self.smooth_data = medfilt2d(numpy.ascontiguousarray(self.data))
        """ `self.data` filtered with a median filter 2D"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)  # Ignore nan values warning
            self.mosaicity, stamp = colorstamps.apply_stamp(
                com_y,
                com_x,
                colormap_name,
                vmin_0=self.y_range[0],
                vmax_0=self.y_range[1],
                vmin_1=self.x_range[0],
                vmax_1=self.x_range[1],
                sat=sat,
                clip="none",
                l=self.KEY_IMAGE_SIZE,
            )

        # Display pixel with null intensity as black
        self.mosaicity[zsum == 0] = 0, 0, 0

        # Display out of range pixel as grey
        self.mosaicity[numpy.isnan(self.mosaicity)] = 0.2

        self.rgb_key = stamp.cmap

    def x_data_values(self) -> numpy.ndarray:
        return numpy.linspace(
            self.x_range[0], self.x_range[1], self.x_bins, endpoint=False
        )

    def y_data_values(self) -> numpy.ndarray:
        return numpy.linspace(
            self.y_range[0], self.y_range[1], self.y_bins, endpoint=False
        )

    def x_rgb_key_values(self) -> numpy.ndarray:
        return numpy.linspace(
            self.x_range[0], self.x_range[1], self.KEY_IMAGE_SIZE, endpoint=False
        )

    def y_rgb_key_values(self) -> numpy.ndarray:
        return numpy.linspace(
            self.y_range[0], self.y_range[1], self.KEY_IMAGE_SIZE, endpoint=False
        )

    def origin(
        self,
        origin: AxisType,
    ) -> tuple[float, float]:
        if origin == "dims":
            return (self.x_range[0], self.y_range[0])
        elif origin == "center":
            return (
                -numpy.ptp(self.x_range) / 2,
                -numpy.ptp(self.y_range) / 2,
            )
        else:
            return (0, 0)

    def data_plot_scale(self) -> tuple[float, float]:
        return (
            numpy.ptp(self.x_range) / self.x_bins,
            numpy.ptp(self.y_range) / self.y_bins,
        )

    def rgb_key_plot_scale(self) -> tuple[float, float]:
        return (
            numpy.ptp(self.x_range) / self.KEY_IMAGE_SIZE,
            numpy.ptp(self.y_range) / self.KEY_IMAGE_SIZE,
        )

    def to_motor_coordinates(
        self,
        points_x: numpy.ndarray,
        points_y: numpy.ndarray,
        origin: AxisType,
    ) -> tuple[numpy.ndarray, numpy.ndarray]:
        """
        Given points_x, points_y in the 2D space of self.data, returns motor coordinates x, y
        """
        x_origin, y_origin = self.origin(origin)
        return (
            points_x * numpy.ptp(self.x_range) / (self.x_bins - 1) + x_origin,
            points_y * numpy.ptp(self.y_range) / (self.y_bins - 1) + y_origin,
        )


class MultiDimMomentType(Enum):
    """Moments that are only computed for datasets with multiple dimensions"""

    ORIENTATION_DIST = "Orientation distribution"
    MOSAICITY = "Mosaicity"


def get_axes(transformation: Transformation | None) -> tuple[
    tuple[numpy.ndarray, numpy.ndarray] | None,
    tuple[str, str] | None,
    tuple[str, str] | None,
]:
    if not transformation:
        return None, None, None

    axes = (transformation.xregular, transformation.yregular)
    axes_names = ("x", "y")
    axes_long_names = (transformation.label, transformation.label)

    return axes, axes_names, axes_long_names


def create_moment_nxdata_groups(
    parent: dict[str, Any],
    moment_data: numpy.ndarray,
    axes,
    axes_names,
    axes_long_names,
):

    for map_type in MomentType:
        map_value = map_type.value
        parent[map_value] = create_nxdata_dict(
            moment_data[map_type],
            map_value,
            axes,
            axes_names,
            axes_long_names,
        )


def generate_grain_maps_nxdict(
    grainPlotMaps: GrainPlotMaps,
    orientation_dist_image: GrainPlotData | None,
) -> dict:
    moments = grainPlotMaps.moments_dims
    axes, axes_names, axes_long_names = get_axes(grainPlotMaps.transformation)

    nx = {
        "entry": {"@NX_class": "NXentry"},
        "@NX_class": "NXroot",
        "@default": "entry",
    }

    if orientation_dist_image is not None:

        nx["entry"][MultiDimMomentType.MOSAICITY.value] = create_nxdata_dict(
            orientation_dist_image.mosaicity,
            MultiDimMomentType.MOSAICITY.value,
            axes,
            axes_names,
            axes_long_names,
            rgba=True,
        )
        nx["entry"]["@default"] = MultiDimMomentType.MOSAICITY.value

        nx["entry"][MultiDimMomentType.ORIENTATION_DIST.value] = {
            "key": create_nxdata_dict(
                orientation_dist_image.rgb_key,
                "image",
                (
                    orientation_dist_image.y_rgb_key_values(),
                    orientation_dist_image.x_rgb_key_values(),
                ),
                (orientation_dist_image.y_label, orientation_dist_image.x_label),
                rgba=True,
            ),
            "data": create_nxdata_dict(
                orientation_dist_image.data,
                "orientation distribution",
                (
                    orientation_dist_image.y_data_values(),
                    orientation_dist_image.x_data_values(),
                ),
                (orientation_dist_image.y_label, orientation_dist_image.x_label),
            ),
            "@default": "data",
        }
    else:
        nx["entry"]["@default"] = MomentType.COM.value

    if grainPlotMaps.dims.ndim <= 1:
        create_moment_nxdata_groups(
            nx["entry"],
            moments[0],
            axes,
            axes_names,
            axes_long_names,
        )
    else:
        for axis, dim in grainPlotMaps.dims.items():
            nx["entry"][dim.name] = {"@NX_class": "NXcollection"}
            create_moment_nxdata_groups(
                nx["entry"][dim.name],
                moments[axis],
                axes,
                axes_names,
                axes_long_names,
            )

    return nx
