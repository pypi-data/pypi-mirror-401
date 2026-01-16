######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################
from dataclasses import dataclass
from ctypes import c_int, POINTER, c_double
import numpy as np
from numpy import ndarray
from oliv.common.base import load_lib

try:
    lib_piv = load_lib("piv")
except OSError:
    lib_piv = None

@dataclass
class PIVParams:
    IA: int
    Sim: int
    Sjm: int
    Sip: int
    Sjp: int

def sub_piv(img_a: np.ndarray, img_b: np.ndarray, piv_param: PIVParams,
            x: ndarray, y: ndarray) -> tuple[ndarray, ndarray,ndarray, ndarray, ndarray]:
    # Get arrays length
    ni = (np.shape(img_a)[0])
    nj = (np.shape(img_a)[1])
    grid_size = len(x)
    # Ensure IA is odd
    if piv_param.IA / 2 % 2 == 0:
        piv_param.IA = piv_param.IA + 1
    # adapt types
    x = np.array(x, dtype=c_int)
    y = np.array(y, dtype=c_int)
    img_a = np.array(img_a, dtype=c_int, order="F")
    img_b = np.array(img_b, dtype=c_int, order="F")
    # Build outputs
    c_max = np.zeros(grid_size, dtype=c_double)
    ri_max = np.zeros(grid_size, dtype=c_double)
    rj_max = np.zeros(grid_size, dtype=c_double)
    peak_size = np.zeros(grid_size, dtype=c_int)
    area = np.zeros(grid_size, dtype=c_int)

    piv_fortran = getattr(lib_piv, 'sub_piv')
    piv_fortran.argtypes = [POINTER(c_int),  # img_a
                            POINTER(c_int),  # img_b
                            POINTER(c_int),  # Bi
                            POINTER(c_int),  # Bj
                            POINTER(c_int),  # Sim
                            POINTER(c_int),  # Sjm
                            POINTER(c_int),  # Sip
                            POINTER(c_int),  # Sjp
                            POINTER(c_int),  # ni
                            POINTER(c_int),  # nj
                            POINTER(c_int),  # grid_size
                            POINTER(c_int),  # x
                            POINTER(c_int),  # y
                            POINTER(c_double),  # c_max
                            POINTER(c_double),  # ri_max
                            POINTER(c_double),  # rj_max
                            POINTER(c_int),  # peak_size
                            POINTER(c_int)]  # aire
    piv_fortran.restype = None

    piv_fortran(img_a.ctypes.data_as(POINTER(c_int)),
                img_b.ctypes.data_as(POINTER(c_int)),
                c_int(piv_param.IA),
                c_int(piv_param.IA),
                c_int(piv_param.Sim),
                c_int(piv_param.Sjm),
                c_int(piv_param.Sip),
                c_int(piv_param.Sjp),
                c_int(ni),
                c_int(nj),
                c_int(grid_size),
                x.ctypes.data_as(POINTER(c_int)),
                y.ctypes.data_as(POINTER(c_int)),
                c_max.ctypes.data_as(POINTER(c_double)),
                ri_max.ctypes.data_as(POINTER(c_double)),
                rj_max.ctypes.data_as(POINTER(c_double)),
                peak_size.ctypes.data_as(POINTER(c_int)),
                area.ctypes.data_as(POINTER(c_int)))

    return ri_max, rj_max, c_max, peak_size, area