######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass, field
from enum import Enum, auto
import numpy as np

from oliv.common.base import communication, MessageLevel
from ..velocimetry_results import VelocimetryResults


class AvailableFilters(Enum):
    FilterSimple = auto()
    FilterVelocityThreshold = auto()
    FilterCorrelationThreshold = auto()
    FilterMedianTest = auto()
    FilterVelocityTemporalConsistency = auto()
    FilterVelocityAngleTemporalConsistency = auto()

@dataclass
class FilterSimple:
    """  Base class for all velocimetry (can be used for manual filtering) """
    name: str   # Name of the filter
    # boolean array of one row per time step, one column per grid point
    arr: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=bool))

    def reset(self, n_times: int, n_points: int, val: bool):
        if self.arr.shape != (n_times, n_points):
            self.arr = np.full((n_times, n_points), val, dtype=bool)
        else:
            self.arr[:, :] = val

    def set_value(self, time_index: int, point_index: int, val: bool):
        """ Manually set filter value for one point/time pair (all times if time_index == -1) """
        if point_index == -1:
            self.arr[:, time_index] = val
        else:
            self.arr[time_index, point_index] = val

    def update(self, res: VelocimetryResults):
        communication.display("filter {} is manual".format(self.name), MessageLevel.INFO, end='')
        pass

    def apply(self, res_in: VelocimetryResults) -> VelocimetryResults:
        """ Apply list of filters to VelocimetryResults and return new VelocimetryResults """
        res_out = VelocimetryResults(res_in.grid)
        for field_name in res_in.names:
            field_out = res_in.__getattribute__(field_name).copy()
            field_out = np.logical_and(field_out, self.arr)
            res_out.__setattr__(field_name, field_out)
        return res_out


def default_filter(name: str, n_times: int, n_points: int) -> FilterSimple:
    return FilterSimple(name, np.full((n_times, n_points), True, dtype=bool))


def merge_filters(filter1: FilterSimple, filter2: FilterSimple) -> FilterSimple | None:
    """ Merge two filters, generally used to update global filter before averaging velocity field """
    if filter1.arr.shape == filter2.arr.shape:
        filter_out = FilterSimple("ok", filter1.arr.copy())
        filter_out.arr &= filter2.arr
        return filter_out
    else:
        communication.error("Filter {} and {} cannot be merged (different shape)"
                            .format(filter1.name, filter2.name), MessageLevel.ERROR)
        return None


def global_filter(res_in: VelocimetryResults, filter_list: list[FilterSimple]) -> FilterSimple:
    # Updating velocimetry
    if len(filter_list) > 0:
        for fil in filter_list:
            fil.update(res_in)

    # Pre-processing velocimetry
    if len(filter_list) == 1:
        g_fil = filter_list[0]
    else:
        g_fil = default_filter("global_filter", res_in.n_times(), res_in.n_points())
        if len(filter_list) > 1:
            for new_fil in filter_list:
                g_fil = merge_filters(g_fil, new_fil)

    return g_fil
