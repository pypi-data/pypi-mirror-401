######################################################################
#
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details :
# <http://www.gnu.org/licenses/>.
#
######################################################################

from oliv.velocimetry.aggregation import *
from .velocimetry.filters import *


def create_filter(params) -> FilterSimple | None:
    if isinstance(params, str):
        return FilterSimple(params)
    elif isinstance(params, FilterMedianTestParams):
        return FilterMedianTest(params)
    elif isinstance(params, FilterVelocityThresholdParams):
        return FilterVelocityThreshold(params)
    elif isinstance(params, FilterCorrelationThresholdParams):
        return FilterCorrelationThreshold(params)
    elif isinstance(params, FilterVelocityTemporalConsistencyParams):
        return FilterVelocityTemporalConsistency(params)
    elif isinstance(params, FilterVelocityAngleTemporalConsistencyParams):
        return FilterVelocityAngleTemporalConsistency(params)
    else:
        communication.display("filter_type unknown", MessageLevel.ERROR)
        return None


def set_filter_value_all_times(c_filter: FilterSimple, point_index: int, val: bool) -> None:
    """ Set filter value to one point for all times """
    c_filter.set_value(time_index=-1, point_index=point_index, val=val)


def apply_filters(res_in: VelocimetryResults, filter_list: list[FilterSimple]) -> VelocimetryResults:
    """ Apply list of filters to VelocimetryResults and return new VelocimetryResults """
    g_fil = global_filter(res_in, filter_list)
    return g_fil.apply(res_in)


def aggregate_results(res_in: VelocimetryResults, params: AggregationParams,
                      filter_list: list[FilterSimple]) -> VelocimetryResults:
    """ Average matrice velocimetry results applying the list of filters """
    return aggregate(res_in, params, filter_list)
