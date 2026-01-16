######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np

from .base import dataclass, communication, MessageLevel, VelocimetryResults, FilterSimple

@dataclass
class FilterVelocityThresholdParams:
    """ Filter with velocity thresholds """
    v_norm: tuple[float, float] = (0, 1e9)  # Threshold min/max for velocity norm [m/s]
    v_x: tuple[float, float] = (-1e9, 1e9)  # Threshold min/max for velocity along X-axis [m/s]
    v_y: tuple[float, float] = (-1e9, 1e9)  # Threshold min/max for velocity along Y-axis [m/s]


class FilterVelocityThreshold(FilterSimple):
    def __init__(self, params: FilterVelocityThresholdParams):
        super().__init__(name="VelocityThreshold")
        self.params = params

    def update(self, res: VelocimetryResults):
        communication.display("Updating filter {}...".format(self.name), MessageLevel.INFO, end="")
        self.reset(res.n_times(), res.n_points(), False)
        self.arr = np.logical_and(res.v_x >= self.params.v_x[0], res.v_x <= self.params.v_x[1])
        self.arr &= np.logical_and(res.v_y >= self.params.v_y[0], res.v_y <= self.params.v_y[1])
        self.arr &= np.logical_and(res.v_norm >= self.params.v_norm[0], res.v_norm <= self.params.v_norm[1])
        communication.display("Ok", MessageLevel.INFO)
