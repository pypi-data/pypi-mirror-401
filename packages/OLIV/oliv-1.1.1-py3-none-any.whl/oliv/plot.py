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

from typing import Literal
from math import dist
import matplotlib.pyplot as plt
import numpy as np

from oliv.common import ROI
from oliv.motion import VelocimetryResults
from oliv.section import CrossSectionResults


def plot_velocity_field(vel_res: VelocimetryResults, img: np.ndarray, roi: ROI, xs_res: CrossSectionResults = None,
                        origin: Literal["lower", "upper"] = "lower", time_index: int = -1):
    """Plot velocity field with background image (+ optional Cross-section results)

    :param vel_res: Velocimetry results
    :param img: Background image
    :param roi: Region of Interest (for Image scaling)
    :param xs_res: Cross-section results (optional)
    :param origin: 'lower' or 'upper' (optional)
    :param time_index: Index of time in Velocimetry results (optional)
    """
    plt.quiver(vel_res.grid.xy[:, 0], vel_res.grid.xy[:, 1], vel_res.v_x[time_index, :], vel_res.v_y[time_index, :])
    plt.imshow(img, extent=[roi.xmin, roi.xmax, roi.ymin, roi.ymax], origin=origin)
    if xs_res is not None:
        plt.quiver(xs_res.geom.xy()[:, 0], xs_res.geom.xy()[:, 1],
                   xs_res.v_xy[:, 0], xs_res.v_xy[:, 1], color="red")
        plt.plot(xs_res.geom.data[:,0], xs_res.geom.data[:,1], '--', c="orange")
    plt.show()

def plot_cross_section_flow(xs_res: CrossSectionResults):
    fig, ax = plt.subplots(figsize=(8, 8))
    x_pos = np.zeros((xs_res.geom.n_points()) )
    for i in range(1, x_pos.shape[0]):
        x_pos[i] = dist(xs_res.geom.data[0, 0:2], xs_res.geom.data[i, 0:2])
    ax.plot(x_pos, xs_res.geom.z(), color="k")
    ax.set_xlabel("Position [m]")
    ax.set_ylabel("Hauteur [m]")
    ax.fill_between(x_pos, xs_res.geom.z(), xs_res.geom.z()+xs_res.water_depth, interpolate=False, alpha=0.3)
    ax2 = ax.twinx()
    ax2.plot(x_pos, xs_res.v_avg, "x", color="r")
    ax2.set_ylabel("Vitesse moyenne [m.s-1]")
    ax2.tick_params(axis='y', colors='r')
    ax2.yaxis.label.set_color('r')
    ax2.set_ylim(bottom=0, top=2)
    ax.set_title("Débit: Q = %.2f m3/s | Aire mouillée: A = %.2f m2" % (xs_res.q, xs_res.wetted_area))
    plt.show()
