######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np

from .base import dataclass, communication, MessageLevel, VelocimetryResults, FilterSimple


@dataclass
class FilterCorrelationThresholdParams:
    """ Filter with correlation thresholds (c-values are obtained from PIV computation) """
    c_min: float = 0.4      # Minimal correlation value
    c_max: float = 0.98     # Maximal correlation value


class FilterCorrelationThreshold(FilterSimple):
    def __init__(self, params: FilterCorrelationThresholdParams):
        super().__init__(name="CorrelationThreshold")
        self.params = params

    def update(self, res: VelocimetryResults):
        communication.display("Updating filter {}...".format(self.name), MessageLevel.INFO, end='')
        self.reset(res.n_times(), res.n_points(), False)
        self.arr = np.logical_and(res.c_max > self.params.c_min, res.c_max < self.params.c_max)
        communication.display("Ok", MessageLevel.INFO)
