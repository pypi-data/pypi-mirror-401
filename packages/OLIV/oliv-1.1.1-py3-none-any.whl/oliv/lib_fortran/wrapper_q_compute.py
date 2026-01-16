######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from ctypes import c_int, POINTER, c_double
import numpy as np
from oliv.common.base import load_lib

try:
    lib_q_compute = load_lib("q_compute")
except OSError:
    lib_q_compute = None

def sub_q_compute(stage, rx, ry, comp_vel, xp, yp, u, v, t_aa, t_bb, t_comp, t_xpp,
                  t_x, t_y, t_z, t_coef, Q_measured, Q_total, bathy_area, sum_Q_coef_1):

    q_compute_fortran = getattr(lib_q_compute, 'sub_q_compute')
    q_compute_fortran.argtypes = [POINTER(c_double),  # stage
                                  POINTER(c_double),  # rx
                                  POINTER(c_double),  # ry
                                  POINTER(c_int),  # comp_vel
                                  POINTER(c_double),  # xp
                                  POINTER(c_double),  # yp
                                  POINTER(c_double),  # u
                                  POINTER(c_double),  # u
                                  POINTER(c_double),  # t_aa
                                  POINTER(c_double),  # t_bb
                                  POINTER(c_int),  # t_comp
                                  POINTER(c_double),  # t_xpp
                                  POINTER(c_double),  # t_x
                                  POINTER(c_double),  # t_y
                                  POINTER(c_double),  # t_z
                                  POINTER(c_double),  # t_coef
                                  POINTER(c_double),  # Q_meas
                                  POINTER(c_double),  # Q_tot
                                  POINTER(c_double),  # Area
                                  POINTER(c_double)]  # coef

    q_compute_fortran.restype = None

    q_compute_fortran(c_double(stage),
                      c_double(rx),
                      c_double(ry),
                      c_int(comp_vel),
                      xp.ctypes.data_as(POINTER(c_double)),
                      yp.ctypes.data_as(POINTER(c_double)),
                      u.ctypes.data_as(POINTER(c_double)),
                      v.ctypes.data_as(POINTER(c_double)),
                      c_double(t_aa),
                      c_double(t_bb),
                      c_int(t_comp),
                      t_xpp.ctypes.data_as(POINTER(c_double)),
                      t_x.ctypes.data_as(POINTER(c_double)),
                      t_y.ctypes.data_as(POINTER(c_double)),
                      t_z.ctypes.data_as(POINTER(c_double)),
                      t_coef.ctypes.data_as(POINTER(c_double)),
                      c_double(Q_measured),
                      c_double(Q_total),
                      c_double(bathy_area),
                      c_double(sum_Q_coef_1))
    # Merge outputs
    out = np.array([Q_measured, Q_total, bathy_area, sum_Q_coef_1]).T

    return out
