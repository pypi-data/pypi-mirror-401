######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass
from os import path
import cv2
from numpy import ndarray
from oliv.common.base import communication, MessageLevel


@dataclass
class Mask:
    img: ndarray


def import_mask(filepath: str) -> Mask | None:
    if path.exists(filepath):
        return Mask(cv2.imread(filepath, cv2.IMREAD_GRAYSCALE))
    else:
        communication.display("Mask file {} not present".format(filepath), MessageLevel.ERROR)
        return None


def invert_mask(mask: Mask) -> Mask:
    return Mask(cv2.bitwise_not(mask.img))
