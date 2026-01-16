######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from abc import ABC, abstractmethod
from enum import Enum, auto
import numpy as np

from oliv.image.framestack import OrthoImageParams


class ProjectionMethod(ABC):

    @abstractmethod
    def calibrate(self) -> None:
        pass

    @abstractmethod
    def build_mapping(self, *args):
        pass

    @abstractmethod
    def ij_to_xy(self, *args) -> tuple[float | np.ndarray, float | np.ndarray]:
        pass

    @abstractmethod
    def xy_to_ij(self, *args) -> tuple[float | np.ndarray, float | np.ndarray]:
        pass

    @abstractmethod
    def check(self):
        pass


class AvailableProjection(Enum):
    DLT = auto()


def ij_to_xy(i_row: float | np.ndarray, j_col: float | np.ndarray, params: OrthoImageParams)\
        -> tuple[float | np.ndarray, float | np.ndarray]:
    """ Simple I/J -> X/Y projection for Ortho-images """
    x = j_col * params.pixel_size + params.roi.xmin
    y = i_row * params.pixel_size + params.roi.ymin
    return x, y


def xy_to_ij(x: float | np.ndarray, y: float | np.ndarray, params: OrthoImageParams)\
        -> tuple[float | np.ndarray, float | np.ndarray]:
    """ Simple I/J -> X/Y projection for Ortho-images """
    j_col = (x - params.roi.xmin) / params.pixel_size
    i_row = (y - params.roi.ymin) / params.pixel_size
    return i_row, j_col
