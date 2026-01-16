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

import os
from functools import singledispatch
import cv2
import copy
from numpy import ndarray

from oliv import FrameStack
from oliv.common.base import communication, MessageLevel


@singledispatch
def write(obj, dir_path: str)-> bool:
    communication.display(type(obj).__name__+" has no write function", MessageLevel.ERROR)
    return False

@write.register
def _(fs_in: FrameStack, dir_path: str) -> bool:
    if len(fs_in.imgs) == 0:
        communication.display("No images to write", MessageLevel.ERROR)
        return False
    else:
        os.makedirs(dir_path, exist_ok=True)
        communication.display("Writing image stack to " + dir_path)
        for i, img in enumerate(fs_in.imgs):
            cv2.imwrite(os.path.join(dir_path, "img_{:04d}.tif".format(i)), img)
        return True


def imgs_to_ram(saved_imgs: list[list[ndarray]],
                new_imgs: list[ndarray]) -> list[list[ndarray]]:
    saved_imgs.append(copy.deepcopy(new_imgs))
    return saved_imgs
