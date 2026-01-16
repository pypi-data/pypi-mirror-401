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

import oliv.projection.grp as grp_funcs
from oliv.image.framestack import *
from oliv.projection import *

def read_GRP_table(file_path: str, grp: GRP = GRP()) -> GRP:
    """ Create or append a GRP table from a file """
    return grp_funcs.read_table(file_path, grp)


def projection_method(method: AvailableProjection, *args) -> ProjectionMethod:
    """ Create a new projection method from arguments"""
    if method == AvailableProjection.DLT:
        return ProjectionDLT(args[0])


def image_mapping(method: ProjectionMethod, params: OrthoImageParams) -> ImageMapping:
    """ Create a new image mapping method from Ortho-image parameters using Projection method"""
    return method.build_mapping(params)


def build_orthoimages(fs_in: FrameStack, im_map: ImageMapping) -> OrthoFrameStack | None:
    """ Compute ortho-images from a given FrameStack using an ImageMapping object """
    return im_map.map_stack(fs_in)


def ij_to_xy(i_row: float | np.ndarray, j_col: float | np.ndarray, params: OrthoImageParams | float | np.ndarray,
             method: ProjectionMethod | None = None) -> tuple[float | np.ndarray, float | np.ndarray]:
    """ Compute spatialized position (X,Y) from a pixel position (I_row,J_col)
    Project Method is optional (None for orthoimage pixel coordinates)
    """
    if method is not None:
        return method.ij_to_xy(i_row, j_col, params)
    else:
        return base.ij_to_xy(i_row, j_col, params)


def xy_to_ij(x: float | np.ndarray, y: float | np.ndarray, params: OrthoImageParams | float | np.ndarray,
             method: ProjectionMethod | None = None) -> tuple[np.ndarray, np.ndarray]:
    """ Compute pixel position (I,J) from spatialized position (X,Y)
    Project Method is optional (None for orthoimage pixel coordinates)
    """
    if method is not None:
        return method.xy_to_ij(x, y, params)
    else:
        return base.xy_to_ij(x, y, params)
