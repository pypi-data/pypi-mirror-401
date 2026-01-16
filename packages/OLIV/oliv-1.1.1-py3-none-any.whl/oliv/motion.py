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

import copy

from oliv.image.framestack import OrthoFrameStack
from oliv.velocimetry.grid import *
from oliv.velocimetry.velocimetry_results import *
from oliv.velocimetry.filters import *
from oliv.lib_fortran.wrapper_piv import sub_piv, PIVParams


def create_grid(*args) -> Grid | None:
    if isinstance(args[0], tuple):
        return grid_from_properties(*args)
    elif isinstance(args[0], str):
        return grid_from_ij_file(*args)
    elif isinstance(args[0], dict):
        return grid_from_dict(*args)
    else:
        communication.display("Cannot create grid (arguments error)", MessageLevel.ERROR)
        return None


def add_grid_points(grid: Grid, list_points: list) -> Grid:
    """ Add grid points (list points is X/Y list)"""
    grid_out = copy.deepcopy(grid)
    grid_out.add_points(list_points)
    return grid_out


def crop_grid(grid: Grid, tool: Mask | ROI | tuple) -> Grid:
    """ Crop grid using tool :
    - ortho-mask (removing points outside the mask)
    - ROI : bounds in real reference system (xmin, ymin, xmax, ymax)
    - tuple : bounds in image reference system (i_min, j_min, i_max, j_max)
    """
    grid_out = copy.deepcopy(grid)
    grid_out.crop(tool)
    return grid_out


def compute_piv(fs_in: OrthoFrameStack, grid: Grid,
                piv_param: PIVParams, res: VelocimetryResults = None) -> VelocimetryResults:
    """ Compute PIV between two images and append to results """

    if res is None:
        res = VelocimetryResults(grid)
    else:
        if grid != res.grid:
            communication.display("Grids do not match", MessageLevel.ERROR)
            res = VelocimetryResults(grid)
    communication.start_progress("Processing PIV", len(fs_in.imgs) - 1)
    for i in range(len(fs_in.imgs)-1):
        ri_row, rj_col, c_max, p_size, area = sub_piv(fs_in.imgs[i], fs_in.imgs[i+1], piv_param, grid.ij[:, 1], grid.ij[:, 0])
        v_y, v_x = ri_row * fs_in.pixel_size * fs_in.fps, rj_col * fs_in.pixel_size * fs_in.fps
        res.v_x = np.vstack((res.v_x, v_x))
        res.v_y = np.vstack((res.v_y, v_y))
        v_norm = np.sqrt(v_x**2 + v_y**2)
        res.v_norm = np.vstack((res.v_norm, v_norm))

        res.c_max = np.vstack((res.c_max, c_max))
        res.peak_size = np.vstack((res.peak_size, p_size))
        res.area = np.vstack((res.area, area))
        communication.progress(i + 1, len(fs_in.imgs) - 1)
    communication.end_progress()
    return res
