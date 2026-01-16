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

from copy import deepcopy

from oliv import communication, MessageLevel
from oliv.section import *


def import_bathymetry(filepath: str) -> CrossSectionBathymetry:
    return bathymetry_from_file(filepath)


def resample_bathymetry(xs_bathy: CrossSectionBathymetry, dist_max: float) -> CrossSectionBathymetry:
    """ Resample a cross-section profile with user-defined maximum distance between two points """
    xs_out = deepcopy(xs_bathy)
    xs_out.resample(dist_max)
    return xs_out


def compute_flowrate(res_in: VelocimetryResults, xs_bathy: CrossSectionBathymetry,
                     params: FlowRateParameters, time_index: int = 0) -> CrossSectionResults | None:
    # velocity interpolation
    if params.interpolator == VelocityInterpolator.ivp:
        v_xy = velocity_ivp_interpolation(res_in, xs_bathy, params, time_index)
    elif params.interpolator == VelocityInterpolator.linear:
        v_xy = velocity_linear_interpolation(res_in, xs_bathy, time_index)
    elif params.interpolator == VelocityInterpolator.nearest:
        v_xy = velocity_nearest_value(res_in, xs_bathy, time_index)
    else:
        communication.display("Interpolation method unknown in compute_flowrate function", MessageLevel.ERROR)
        return None
    return velocity_to_flowrate(v_xy, xs_bathy, params)
