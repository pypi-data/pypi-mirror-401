######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass

@dataclass
class ROI:
    """ Region Of Interest [m] """
    xmin: float
    ymin: float
    xmax: float
    ymax: float
