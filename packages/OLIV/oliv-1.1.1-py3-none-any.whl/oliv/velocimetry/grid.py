######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################


from dataclasses import dataclass
import numpy as np

from oliv.common import communication, MessageLevel, ROI
from oliv.image.framestack import OrthoImageParams
from oliv.image.mask import Mask
from oliv.projection.base import ij_to_xy

@dataclass
class Grid:
    ij: np.ndarray  # Grid-point column/row position (image coordinate system, origin lower)
    xy: np.ndarray  # Grid-point x/y position (real coordinate system)

    def add_points(self, list_of_points: list) -> None:
        """ Add a list of points to the grid

        :param list_of_points: List of points
        :type list_of_points: list
        """
        list_of_points = np.array(list_of_points, ndmin=2)
        self.ij = np.concatenate((self.ij, list_of_points), axis=0)

    def crop(self, tool: Mask | ROI | tuple):
        """ Crop grid using ortho-mask (removing points outside the mask) """
        out_points = []
        if type(tool) is Mask:
            communication.display("Cropping grid using mask from {}".format(self.ij.shape[0]), end="")
            for p in range(self.ij.shape[0]):
                if not tool.img[self.ij[p][0], self.ij[p][1]]:
                    out_points.append(p)
        elif type(tool) is ROI:
            communication.display("Cropping grid using ROI from {}".format(self.ij.shape[0]), end="")
            for p in range(self.xy.shape[0]):
                if (not tool.xmin < self.xy[p, 0] < tool.xmax
                        or not tool.ymin < self.xy[p, 1] < tool.xmax):
                    out_points.append(p)
        elif type(tool) is tuple:
            communication.display("Cropping grid using bounds from {}".format(self.ij.shape[0]), end="")
            for p in range(self.ij.shape[0]):
                if (not tool[0] < self.ij[p, 0] < tool[1]
                        or not tool[2] < self.ij[p, 1] < tool[3]):
                    out_points.append(p)
        else:
            communication.display("Unknown tool for cropping grid", MessageLevel.ERROR)

        xy, ij = np.delete(self.xy, out_points, axis=0), np.delete(self.ij, out_points, axis=0)
        communication.display(" to {} points".format(xy.shape[0]))


def grid_from_properties(corner: tuple[int, int], delta: tuple[int, int], size: tuple[int, int],
                         fs_ortho: OrthoImageParams) -> Grid:
    """ To generate grid

    :param corner: Minimum (i,j) coordinate
    :type corner: tuple[int, int]
    :param delta: (i,j) spacing for grid
    :type delta: tuple[int, int]
    :param size: number of (i,j) grid points
    :type size: tuple[int, int]
    :return: grid read from the file
    """
    nx, ny = size
    communication.display("Generating grid with {}x{} points.".format(nx, ny))
    n_points = nx * ny
    ij = np.empty((n_points, 2), dtype=int)
    for i in range(nx):
        for j in range(ny):
            ij[i + j * nx, 0] = corner[0] + i * delta[0]
            ij[i + j * nx, 1] = corner[1] + j * delta[1]
    x, y = ij_to_xy(i_row=ij[:, 0], j_col=ij[:, 1], params=fs_ortho)
    xy = np.array((x, y)).T
    return Grid(ij, xy)


def grid_from_ij_file(file_path: str, fs_ortho: OrthoImageParams, swap_ij: bool = True) -> Grid:
    """ Load grid definition for velocity field computation

    :param file_path: File path of grid definition (pixel coordinates)
    :param fs_ortho: Ortho-image stack for ROI/pixel size information
    :param swap_ij: Invert j/i for inverted grid file
    """
    communication.display("Reading grid from file '{}'".format(file_path), end=" ")
    ij = np.genfromtxt(file_path, dtype=int)
    if swap_ij:
        ij[:, [0, 1]] = ij[:, [1, 0]]
    communication.display("contains " + str(ij.shape[0]) + " grid points")
    x, y = ij_to_xy(i_row=ij[:, 0], j_col=ij[:, 1], params=fs_ortho)
    xy = np.array((x, y)).T
    return Grid(ij, xy)


def grid_from_dict(dict_in: dict, params: OrthoImageParams) -> Grid | None:
    """ Reset grid using Parameters dictionary """
    if "grid" in dict_in:
        # Generating/reading grid
        if "file" in dict_in["grid"]:
            return grid_from_ij_file(dict_in["grid"]["file"], params)
        elif "properties" in dict_in["grid"]:
            return grid_from_properties(dict_in["grid"]["properties"]["corner"],
                                        dict_in["grid"]["properties"]["delta"],
                                        dict_in["grid"]["properties"]["size"], params)
        else:
            communication.display("Missing information for resetting grid in 'grid' dictionary",
                                  MessageLevel.ERROR)
            return None
    else:
        communication.display("Unable to reset grid, keyword 'grid' is missing in parameters dictionary",
                              MessageLevel.ERROR)
        return None
