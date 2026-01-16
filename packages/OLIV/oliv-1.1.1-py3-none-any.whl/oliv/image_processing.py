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

from copy import copy

from oliv.image import *


def framestack_from_dir(dir_path: str, extension:str, fps: float) -> FrameStack:
    fs_out = FrameStack([], fps)
    fs_out.append_from_dir(dir_path, extension)
    return fs_out


def gaussian_blur(fs_in: FrameStack, params: GaussianBlurParams) -> FrameStack:
    """ Applying Gaussian smoothing to image stack """
    return FrameStack(gaussian_blur_processing(fs_in.imgs, params), copy(fs_in.fps))


def CLAHE(fs_in: FrameStack, params: CLAHEParams) -> FrameStack:
    """ Applying Gaussian smoothing to the stack of images """
    return FrameStack(CLAHE_processing(fs_in.imgs, params), copy(fs_in.fps))


def crop_framestack(fs_in: FrameStack, ij_extent: tuple[int, int, int, int]) -> FrameStack:
    imgs_out = []
    for img in fs_in.imgs:
        imgs_out.append(img[ij_extent[0]:ij_extent[1], ij_extent[2]:ij_extent[3]])
    return FrameStack(imgs_out, fs_in.fps)
