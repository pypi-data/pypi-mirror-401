######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from os import listdir, path
import copy
from dataclasses import dataclass
import cv2
import numpy as np

from oliv.common import communication, MessageLevel, ROI


@dataclass
class FrameStack:
    imgs: list[np.ndarray]
    fps: float

    def append_from_dir(self, dir_path: str, extension: str):
        for filename in listdir(dir_path):
            if filename.endswith(extension):
                img = cv2.imread(path.join(dir_path, filename))
                if img is not None:
                    self.imgs.append(img)


@dataclass
class OrthoImageParams:
    """ Base parameter class for ortho-image creation"""
    roi: ROI  # Region Of Interest [m]
    pixel_size: float  # Pixel size of orthoimage [m/pix]
    z: float  # Free surface level [m]

    def __post_init__(self):
        """ To initialize from global dictionary """
        if type(self.roi) is dict:
            # ROI built from dictionary
            self.roi = ROI(**self.roi)


@dataclass
class OrthoFrameStack(OrthoImageParams, FrameStack):
    """ Merge of FrameStack with OrthoImageParams properties """

    def __post_init__(self):
        pass

@dataclass
class ImageMapping(OrthoImageParams):
    """ Base class for computing ortho-images from original images

    Ortho-image parameters are transmitted to the created OrthoFrameStack
    """
    map_i: np.ndarray  # Column map for OpenCV remap function
    map_j: np.ndarray  # Row map for OpenCV remap function

    def map_stack(self, fs_in: FrameStack) -> OrthoFrameStack | None:
        """ Compute ortho-images from a given FrameStack using an ImageMapping object
            Pixel size and ROI are copied (not referenced) from ImageMapping to OrthoFrameStack
            to prevent subsequent changes
        """
        communication.start_progress("Building orthoimages", len(fs_in.imgs))
        roi = copy.deepcopy(self.roi)  # copy to prevent subsequent changes
        pixel_size = copy.copy(self.pixel_size)  # copy to prevent subsequent changes
        z = copy.copy(self.z)
        fps = copy.deepcopy(fs_in.fps)
        if len(self.map_i) > 0:
            fs_out = OrthoFrameStack([], fps, roi, pixel_size, z)
            for i, img in enumerate(fs_in.imgs):
                fs_out.imgs.append(cv2.remap(img, self.map_i, self.map_j, cv2.INTER_CUBIC))
                communication.progress(i, len(fs_in.imgs))
            communication.end_progress()
            return fs_out
        else:
            communication.display("Unable to build ortho image (no map), calibrate camera first.", MessageLevel.ERROR)
            return None
