######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np
from dataclasses import dataclass, field

from oliv.common.base import MessageLevel, communication
from oliv.image.framestack import OrthoImageParams, ImageMapping
from oliv.projection.base import ProjectionMethod
from .grp import GRP
from oliv.lib_fortran.wrapper_ortho import *


@dataclass
class DLTStats:
    """ Compute statistics for DLT accuracy between original and projected GRP """
    std: float = -1.0  # Standard deviation of projected GRP [m]
    dev_max: float = -1.0  # Maximum deviation of projected GRP [m]
    # Original and projected GRP coordinated are stored in x_orig/y_orig/x_proj/y_proj [m]
    x_orig: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    y_orig: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    x_proj: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    y_proj: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    # Deviation for each GRP [m]
    dev: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))

@dataclass
class ProjectionDLT(ProjectionMethod):
    """ DLTMapping is specific class computing ImageMapping attributes.
    Internal coefficients are stored and useful only to advanced users
    """
    grp: GRP  # Ground Reference Points
    coeffs: np.ndarray = field(init=False)  # Internal coefficient of DLT (for advanced users only)
    dlt_3D: bool = field(init=False)

    def __post_init__(self):
        self.calibrate()

    def calibrate(self):
        """ Calibrate camera (DLT coefficients + mapping)"""
        self.coeffs = sub_ortho(self.grp.pts)
        if len(self.coeffs) == 8:
            self.dlt_3D = False
        else:
            self.dlt_3D = True

    def build_mapping(self, ortho_params: OrthoImageParams) -> ImageMapping:
        map_i, map_j = _compute_map(self.coeffs, ortho_params)
        communication.display("Direct Linear Transform calibration...", end="")
        im_map = ImageMapping(roi=ortho_params.roi, pixel_size=ortho_params.pixel_size,
                            z=ortho_params.z, map_i=map_i, map_j=map_j)
        communication.display("Ok")
        return im_map

    def ij_to_xy(self, i_row: float | np.ndarray, j_col: float | np.ndarray, z: float | np.ndarray) \
            -> tuple[float | np.ndarray, float | np.ndarray]:
        if self.dlt_3D:
            if isinstance(z, float) and isinstance(i_row, np.ndarray):
                z = np.full(i_row.shape, z)
            return _CRT2space_3D(self.coeffs, j_col, i_row, z)
        else:
            return _CRT2space_2D(self.coeffs, j_col, i_row)

    def xy_to_ij(self, x: float | np.ndarray, y: float | np.ndarray, z) \
            -> tuple[float | np.ndarray, float | np.ndarray]:
        if self.dlt_3D:
            if isinstance(z, float) and isinstance(x, np.ndarray):
                z = np.full(x.shape, z)
            return _space2CRT_3D(self.coeffs, x, y, z)
        else:
            return _space2CRT_2D(self.coeffs, x, y)

    def check(self) -> DLTStats:
        """ Compute and display DLT statistics using GRP """
        communication.display("Checking DLT:", MessageLevel.INFO)
        x_orig = self.grp.x().copy()
        y_orig = self.grp.y().copy()
        if len(self.coeffs) == 8:
            x_proj, y_proj = _CRT2space_2D(self.coeffs, self.grp.j_col(), self.grp.i_row())
        else:
            x_proj, y_proj = _CRT2space_3D(self.coeffs, self.grp.j_col(), self.grp.i_row(), self.grp.z())
        var = (x_proj - x_orig) ** 2 + (y_proj - y_orig) ** 2
        std = np.sqrt(np.sum(var) / len(var))
        dev = np.sqrt(var)
        communication.display("- Standard deviation: {:.3f} m".format(std), MessageLevel.INFO)
        communication.display("- Maximum deviation:  {:.3f} m".format(np.max(dev)), MessageLevel.INFO)
        return DLTStats(std, np.max(dev), x_orig, y_orig, x_proj, y_proj, dev)


# INTERNAL FUNCTIONS
def _space2CRT_3D(a: np.ndarray, x: float | np.ndarray, y: float | np.ndarray, h: float | np.ndarray) \
        -> tuple[float | np.ndarray, float | np.ndarray]:
    i_row = (a[0] * x + a[1] * y + a[2] * h + a[3]) / (a[4] * x + a[5] * y + a[6] * h + 1)
    j_col = (a[7] * x + a[8] * y + a[9] * h + a[10]) / (a[4] * x + a[5] * y + a[6] * h + 1)
    return i_row, j_col


def _CRT2space_3D(a: np.ndarray, j_col: float | np.ndarray, i_row: float | np.ndarray, z: float | np.ndarray) \
        -> tuple[float | np.ndarray, float | np.ndarray]:
    b = np.empty((j_col.shape[0], 9), dtype=float)
    b[:, 0] = z * (a[8] * a[6] - a[9] * a[5]) + (a[8] - a[10] * a[5])
    b[:, 1] = -(z * (a[1] * a[6] - a[2] * a[5]) + (a[1] - a[3] * a[5]))
    b[:, 2] = z * (a[1] * a[9] - a[2] * a[8]) + (a[1] * a[10] - a[3] * a[8])
    b[:, 3] = a[7] * a[5] - a[8] * a[4]
    b[:, 4] = -(a[0] * a[5] - a[1] * a[4])
    b[:, 5] = a[0] * a[8] - a[1] * a[7]
    b[:, 6] = -(z * (a[7] * a[6] - a[9] * a[4]) + (a[7] - a[10] * a[4]))
    b[:, 7] = z * (a[0] * a[6] - a[2] * a[4]) + (a[0] - a[3] * a[4])
    b[:, 8] = -(z * (a[0] * a[9] - a[2] * a[7]) + (a[0] * a[10] - a[3] * a[7]))
    x = (b[:, 0] * j_col + b[:, 1] * i_row + b[:, 2]) / (b[:, 3] * j_col + b[:, 4] * i_row + b[:, 5])
    y = (b[:, 6] * j_col + b[:, 7] * i_row + b[:, 8]) / (b[:, 3] * j_col + b[:, 4] * i_row + b[:, 5])
    return x, y


def _space2CRT_2D(a: np.ndarray, x: float | np.ndarray, y: float | np.ndarray) \
        -> tuple[float | np.ndarray, float | np.ndarray]:
    # Rearrange coefficients (from verif_ortho.f90)
    coef = np.zeros(9, dtype=float)
    coef[0] = a[4] - a[7] * a[5]
    coef[1] = a[2] * a[7] - a[1]
    coef[2] = a[1] * a[5] - a[2] * a[4]
    coef[3] = a[6] * a[5] - a[3]
    coef[4] = a[0] - a[2] * a[6]
    coef[5] = a[2] * a[2] - a[0] - a[5]
    coef[6] = a[7] - a[3] - a[6] * a[4]
    coef[7] = a[1] * a[6] - a[0] * a[7]
    coef[8] = a[0] * a[4] - a[1] * a[3]
    i_row = (coef[0] * x + coef[1] * y + coef[2]) / (coef[6] * x + coef[7] * y + coef[8])
    j_col = (coef[3] * x + coef[4] * y + coef[5]) / (coef[6] * x + coef[7] * y + coef[8])
    return i_row, j_col


def _CRT2space_2D(a: np.ndarray, j_col: float | np.ndarray, i_row: float | np.ndarray) \
        -> tuple[float | np.ndarray, float | np.ndarray]:
    x = (a[0] * j_col + a[1] * i_row + a[2]) / (a[6] * j_col + a[7] * i_row + 1.0)
    y = (a[3] * j_col + a[4] * i_row + a[5]) / (a[6] * j_col + a[7] * i_row + 1.0)
    return x, y


def _compute_map(coef_DLT: np.ndarray, ortho_params: OrthoImageParams) -> tuple[np.ndarray, np.ndarray] | None:
    """ Transform image using 3D-DLT coefficients

    :param coef_DLT: DLT coefficients (8 or 11 values)
    :type coef_DLT: np.ndarray
    :param ortho_params: Ortho-image parameters
    :type ortho_params: DLTParams
    :return: tuple of map for OpenCV remap function
    :rtype: tuple[np.ndarray, np.ndarray]
    """
    if len(coef_DLT) not in (8, 11):
        communication.display("DLT coefficients should contain 8 (2D) or 11 (3D) values", MessageLevel.ERROR)

    # error if ortho-image resolution > 4K
    x_res = int((ortho_params.roi.xmax - ortho_params.roi.xmin) / ortho_params.pixel_size)
    y_res = int((ortho_params.roi.ymax - ortho_params.roi.ymin) / ortho_params.pixel_size)
    if x_res > 3840 or y_res > 2160:
        communication.display(f"Ortho-images resquested resolution is too high ({x_res} x {y_res}), "
                              "increase the pixel size requested", MessageLevel.ERROR)
        return None, None

    # Build ortho-image pixel coordinates from x/y limits
    xx = np.arange(ortho_params.roi.xmin, ortho_params.roi.xmax, step=ortho_params.pixel_size)
    yy = np.arange(ortho_params.roi.ymin, ortho_params.roi.ymax, step=ortho_params.pixel_size)

    img_xy = np.meshgrid(xx, yy, indexing="xy")
    # Convert XYZ to pixels
    if len(coef_DLT) == 8:
        i_xy, j_xy = _space2CRT_2D(coef_DLT, img_xy[0], img_xy[1])
    else:
        i_xy, j_xy = _space2CRT_3D(coef_DLT, img_xy[0], img_xy[1], ortho_params.z)

    map_i = np.array(i_xy, dtype=np.float32)
    map_j = np.array(j_xy, dtype=np.float32)
    return map_i, map_j
