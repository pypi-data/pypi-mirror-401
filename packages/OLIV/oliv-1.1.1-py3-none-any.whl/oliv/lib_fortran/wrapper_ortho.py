######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from ctypes import c_int, POINTER, c_double
import numpy as np

from oliv.common.base import load_lib, communication, MessageLevel

try:
    lib_ortho = load_lib("ortho")
except OSError:
    communication.display("Unable to load ortho fortran dynamic library", MessageLevel.WARNING)
    lib_ortho = None


# Ortho 2D
def sub_ortho(GRP: np.ndarray) -> np.ndarray:
    """ Compute DLT coefficients: 2D or 3D depending on the Z values

    :param GRP: Ground Reference Points
    :type GRP: ndarray
    :return: DLT coefficients (list)
    """
    xp = np.array(GRP[:, 0], dtype=np.float64)
    yp = np.array(GRP[:, 1], dtype=np.float64)
    zp = np.array(GRP[:, 2], dtype=np.float64)
    x = np.array(GRP[:, 3], dtype=np.int32)
    y = np.array(GRP[:, 4], dtype=np.int32)

    n_points = len(x)
    z_max = np.sum(np.abs(np.diff(zp)))

    if z_max < 0.01:
        coeffs = np.zeros(8, dtype=np.float64)
        subroutine = getattr(lib_ortho, "sub_ortho2d")
    else:
        coeffs = np.zeros(11, dtype=np.float64)
        subroutine = getattr(lib_ortho, "sub_ortho3d")

    subroutine.argtypes = [POINTER(c_int),  # x image
                           POINTER(c_int),  # y image
                           POINTER(c_double),  # xp
                           POINTER(c_double),  # yp
                           POINTER(c_double),  # zp
                           POINTER(c_int),  # Nb GRPs
                           POINTER(c_double)]  # coeff DLT
    subroutine.restype = None

    subroutine(x.ctypes.data_as(POINTER(c_int)),
               y.ctypes.data_as(POINTER(c_int)),
               xp.ctypes.data_as(POINTER(c_double)),
               yp.ctypes.data_as(POINTER(c_double)),
               zp.ctypes.data_as(POINTER(c_double)),
               c_int(n_points),
               coeffs.ctypes.data_as(POINTER(c_double))
               )

    return coeffs
