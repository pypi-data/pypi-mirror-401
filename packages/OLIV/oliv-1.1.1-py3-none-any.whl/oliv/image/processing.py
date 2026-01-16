######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass
import cv2
import numpy as np

from oliv.common.base import communication


@dataclass
class GaussianBlurParams:
    kernel: tuple[int, int]


def gaussian_blur_processing(imgs_in: list[np.ndarray], params: GaussianBlurParams) -> list[np.ndarray]:
    """ Applying Gaussian smoothing to list of images stack """
    imgs_out = []
    communication.start_progress("Gaussian smoothing", len(imgs_in))
    for i, img in enumerate(imgs_in):
        imgs_out.append(cv2.GaussianBlur(img, params.kernel, cv2.BORDER_REPLICATE))
        communication.progress(i, len(imgs_in))
    communication.end_progress()
    return imgs_out


@dataclass
class CLAHEParams:
    clip_limit: float
    offset: int
    gray: bool = False


def CLAHE_processing(imgs_in: list[np.ndarray], params: CLAHEParams) -> list[np.ndarray]:
    """ Applying Gaussian smoothing to the stack of images """
    clahe = cv2.createCLAHE(clipLimit=params.clip_limit)
    imgs_out = []
    communication.start_progress("CLAHE algorithm", len(imgs_in))
    for i, img in enumerate(imgs_in):
        if not params.gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgs_out.append(np.clip(clahe.apply(img) + params.offset, 0, 255).astype(np.uint8))
        communication.progress(i, len(imgs_in))
    communication.end_progress()
    return imgs_out
