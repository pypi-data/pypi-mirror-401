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

import numpy as np

from oliv.common.base import communication
from oliv.image.videofile import *
from oliv.image_processing import FrameStack


def extract_next_frame(vid: VideoFile) -> np.ndarray:
    """ Extract next frame from video"""
    return vid.cap.read()[1]


def read_video_file(params: LoadVideoParams) -> VideoFile:
    """ Load a video file """
    cap = cv2.VideoCapture(params.filepath)
    communication.display("Video loaded: " + params.filepath +
                          " contains " + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) + " frames")
    return VideoFile(cap, cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))


def extract_framestack(vid: VideoFile, params: ExtractFrameParams) -> FrameStack:
    """ Build a stack of images from video """
    return vid.extract_framestack(params)
