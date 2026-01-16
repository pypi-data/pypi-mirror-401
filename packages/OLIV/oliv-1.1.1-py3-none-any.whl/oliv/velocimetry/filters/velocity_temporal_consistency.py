######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np

from .base import dataclass, communication, MessageLevel, VelocimetryResults, FilterSimple


@dataclass
class FilterVelocityTemporalConsistencyParams:
    """ Filter based on X and Y-velocity temporal consistency """
    k: float = 10       # Maximal deviation factor from standard deviation [-]

class FilterVelocityTemporalConsistency(FilterSimple):
    def __init__(self, params: FilterVelocityTemporalConsistencyParams):
        super().__init__(name="VelocityTemporalConsistency")
        self.params = params

    def update(self, res: VelocimetryResults):
        communication.display("Updating filter {}...".format(self.name), MessageLevel.INFO, end='')
        self.reset(res.n_times(), res.n_points(), True)
        mean_x, mean_y = np.nanmean(res.v_x, axis=0), np.nanmean(res.v_y, axis=0)
        dev_x, dev_y = np.abs(res.v_x-mean_x), np.abs(res.v_y-mean_y)

        std_x, std_y = np.nanstd(res.v_x, axis=0), np.nanstd(res.v_y, axis=0)
        threshold_x, threshold_y = self.params.k * std_x, self.params.k * std_y

        self.arr = np.logical_and(dev_x < threshold_x, dev_y < threshold_y)
        communication.display("Ok", MessageLevel.INFO)
