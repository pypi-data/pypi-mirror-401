######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import numpy as np
from math import dist
from dataclasses import dataclass, field

@dataclass
class CrossSectionBathymetry:
    """ Cross-section bathymetric profil with access functions """
    data: np.ndarray    # Bathymetric profile information as 4-columns array : X/Y/Z/velocity_coeff
    x_abs: np.ndarray = field(init=False)   # Curvilinear transverse coordinate (computed from data)

    def __post_init__(self):
        self.update_x_abs()

    def n_points(self) -> int:
        return self.data.shape[0]

    def xy(self) -> np.ndarray:
        return self.data[:, 0:2]

    def z(self) -> np.ndarray:
        return self.data[:, 2]

    def v_coeff(self) -> np.ndarray:
        """ Return velocity coefficient to compute average from surface value """
        return self.data[:, 3]

    def flow_direction(self) -> np.ndarray:
        """ Compute of the normalized normal vector to the crosse section (using first and last point) """
        xs_direction = np.array([self.data[-1, 0] - self.data[0, 0], self.data[-1, 1] - self.data[0, 1]])
        flow_direction = np.array([-xs_direction[1], xs_direction[0]])
        return flow_direction / np.linalg.norm(flow_direction)

    def update_x_abs(self):
        self.x_abs = np.zeros((self.data.shape[0]), dtype=float)
        for i in range(1, self.x_abs.shape[0]):
            self.x_abs[i] = dist(self.data[i, 0:2], self.data[0, 0:2])

    def resample(self, dist_max: float):
        """ Resample a cross-section profile with user-defined maximum distance between two points """
        id_pt = 1
        while id_pt < self.data.shape[0]:
            if dist(self.data[id_pt, 0:2], self.data[id_pt - 1, 0:2]) > dist_max:
                new_point = (self.data[id_pt, :] + self.data[id_pt - 1, :]) / 2
                self.data = np.insert(self.data, id_pt, new_point, axis=0)
            else:
                id_pt += 1
        self.update_x_abs()


def bathymetry_from_file(filepath: str) -> CrossSectionBathymetry:
    """ Load a cross-section bathymetric profile from a file """
    data = np.genfromtxt(filepath)
    return CrossSectionBathymetry(data)
