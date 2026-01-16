######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np
from scipy.stats import circvar

from .base import dataclass, communication, MessageLevel, VelocimetryResults, FilterSimple


@dataclass
class FilterVelocityAngleTemporalConsistencyParams:
    circ_var_max: float = 0.25


class FilterVelocityAngleTemporalConsistency(FilterSimple):
    def __init__(self, params: FilterVelocityAngleTemporalConsistencyParams):
        super().__init__(name="VelocityAngleTemporalConsistency")
        self.params = params

    def update(self, res: VelocimetryResults):
        communication.display("Updating filter {}...".format(self.name), MessageLevel.INFO, end='')
        self.reset(res.n_times(), res.n_points(), True)
        atan_v = np.arctan2(res.v_x, res.v_y)
        circ_var = circvar(atan_v, high=np.pi, low=-np.pi, nan_policy="omit", axis=0)
        self.arr[0, :] = circ_var < self.params.circ_var_max
        for time in range(1, res.n_times()):
            self.arr[time, :] = self.arr[0, :]
        communication.display("Ok", MessageLevel.INFO)
