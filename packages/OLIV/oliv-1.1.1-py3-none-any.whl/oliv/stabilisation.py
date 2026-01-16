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

from oliv.stab import *


def stabilize(obj_in: FrameStack | VideoFile, params: GrayStabilisationParams, start_index: int = 0,
              end_index: int = -1, filepath_out: str = None,
              mask: Mask = None, invert: bool = False) -> FrameStack | VideoFile:

    if mask is not None and invert:
        stab_mask = Mask(cv2.bitwise_not(mask.img))
    else:
        stab_mask = mask
    # compute stabilization transformations
    stab_trans = gray_stab.compute_stab(obj_in, params, start_index, end_index, stab_mask)

    if params.smooth_stab:
        stab_trans.transformations = smooth_transformations(stab_trans.transformations, params)


    # correct and return FrameStack or VideoFile
    return base.apply_stab(stab_trans, filepath_out)
