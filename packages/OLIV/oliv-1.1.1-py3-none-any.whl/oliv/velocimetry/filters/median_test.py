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

from scipy.spatial import KDTree
import numpy as np

from .base import dataclass, field, communication, MessageLevel, VelocimetryResults, FilterSimple


@dataclass
class FilterMedianTestParams:
    """ Median test based on velocity thresholds """
    dist_neighbor: float = 10.0     # Neighbor search distance [m]
    nb_neighbors: int = 8           # Number of neighbors
    epsilon: float = 0.1            # unused
    # Thresholds for each velocity component
    thresholds: list[tuple[str, float]] = field(default_factory=lambda: [("v_x", 1e6), ("v_y", 1e6), ("v_norm", 2.0)])


class FilterMedianTest(FilterSimple):
    def __init__(self, params: FilterMedianTestParams):
        super().__init__(name="MedianTest")
        self.params = params

    def update(self, res: VelocimetryResults):
        communication.display("Updating filter {}...".format(self.name), MessageLevel.INFO, end='')
        self.reset(res.n_times(), res.n_points(), True)
        kd_tree = KDTree(res.grid.ij)
        dist_ind, pt_ind = kd_tree.query(res.grid.ij, self.params.nb_neighbors+1,
                                         distance_upper_bound=self.params.dist_neighbor)

        for threshold in self.params.thresholds:
            if threshold[1] < 1e6:
                field_selected = res.__getattribute__(threshold[0])
                for time in range(res.n_times()):
                    for dist, pts in zip(dist_ind, pt_ind):
                        v_field = np.zeros((len(dist)), dtype=float)
                        for i in range(1, len(dist)):
                            v_field[i] = field_selected[time, pts[i]]
                        self.arr[time, pts[0]] &= _median_test(v_field, threshold[1])
        communication.display("Ok", MessageLevel.INFO)

def _median_test(v_field: np.ndarray, threshold: float) -> bool:
    v_median = np.nanmedian(v_field[1:])
    r = np.abs(v_field[1:] - v_median)
    r_median = np.nanmedian(r)
    r0 = np.abs(v_field[0] - v_median) / r_median
    if r0 < threshold:
        return True
    else:
        return False
