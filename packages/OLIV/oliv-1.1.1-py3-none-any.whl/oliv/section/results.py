######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from copy import copy
from dataclasses import dataclass
from enum import Enum
import numpy as np
from scipy.spatial import KDTree
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

from oliv.velocimetry.velocimetry_results import VelocimetryResults
from .bathymetry import CrossSectionBathymetry

class VelocityInterpolator(Enum):
    ivp = 0
    linear = 1
    nearest = 2


@dataclass
class FlowRateParameters:
    """ Parameters for cross-section velocity computation/interpolation """
    water_level: float                  # Water_level [m]
    r_x: float                          # Search radius along X-axis [m]
    r_y: float                          # Search radius along Y-axis [m]
    n_points: int                       # Number of values to average
    interpolator: VelocityInterpolator  # Interpolation method
    fill_empty: bool = True             # Activate automatic filling of null velocities (linear interpolation)


@dataclass
class CrossSectionResults:
    """ Cross-section flow results : velocities, wetted area, flow rate... """
    geom: CrossSectionBathymetry    # Reference to bathymetric profile
    v_xy: np.ndarray                # Interpolated surface velocity vectors [m/s]
    v_norm: np.ndarray              # Interpolated surface velocity scalars (normal to cross-section) [m/s]
    v_avg: np.ndarray               # Depth-averaged velocity using v_norm and bathymetric v_coeff [m/s]
    water_depth: np.ndarray         # Water depth for each point [m]
    wetted_area: float              # Cross-section wetted area [m2]
    q: float                        # Cross-section flow rate [m3/s]
    water_level: float              # Water_level [m]


def velocity_to_flowrate(v_xy: np.ndarray, xs_bathy: CrossSectionBathymetry,
                         params: FlowRateParameters) -> CrossSectionResults | None:
    # compute water depth
    water_depth = - xs_bathy.z() + params.water_level
    water_depth[water_depth < 0] = 0

    # compute normal and average velocities
    if params.fill_empty:
        v_xy = _fill_empty_values_(v_xy, xs_bathy)
    v_xy[water_depth == 0, :] = np.nan
    flow_dir = xs_bathy.flow_direction()
    v_norm = np.dot(v_xy, flow_dir)
    v_avg = v_norm * xs_bathy.v_coeff()

    # compute flow rate
    dx = np.zeros((xs_bathy.n_points()), dtype=float)
    dx[0] = (xs_bathy.x_abs[1] - xs_bathy.x_abs[0]) / 2
    for i in range(1, xs_bathy.n_points() - 1):
        dx[i] = (xs_bathy.x_abs[i+1] - xs_bathy.x_abs[i-1]) / 2
    dx[-1] = (xs_bathy.x_abs[-1] - xs_bathy.x_abs[-2]) / 2
    wetted_area = np.nansum(dx * water_depth)
    q = np.nansum(v_avg * dx * water_depth)

    return CrossSectionResults(xs_bathy, v_xy, v_norm, v_avg, water_depth, wetted_area, q, copy(params.water_level))


def velocity_ivp_interpolation(res_in: VelocimetryResults, xs_bathy: CrossSectionBathymetry,
                               params: FlowRateParameters, time_index: int = 0) -> np.ndarray:
    """ Interpolate velocities on cross-section points and compute flow properties """
    kd_tree = KDTree(res_in.grid.xy)
    dist_neigh, index_neigh = kd_tree.query(xs_bathy.xy(), k=params.n_points,
                                            distance_upper_bound=max(params.r_x, params.r_y))

    # filtering points outside the ellipse
    _ellipse_test(index_neigh, dist_neigh, res_in.grid.xy, xs_bathy.xy(), params.r_x, params.r_y)

    # filtering points where V=0 points
    for pt in range(index_neigh.shape[0]):
        for nei in range(index_neigh.shape[1]):
            if index_neigh[pt, nei] != res_in.n_points():
                if res_in.v_norm[0, index_neigh[pt, nei]] == 0:
                    dist_neigh[pt, nei] = np.inf
                    index_neigh[pt, nei] = res_in.n_points()

    # computing inverse distance weights
    inv_dist = 1 / dist_neigh
    sum_inv_dist = np.sum(inv_dist, axis=1)[:, np.newaxis]
    sum_inv_dist[sum_inv_dist == 0] = 1
    dist_weight = inv_dist / sum_inv_dist

    # interpolation with valid points
    v_xy = np.zeros((xs_bathy.n_points(), 2), dtype=float)
    for id_pt in range(xs_bathy.n_points()):
        valid_index = index_neigh[id_pt, index_neigh[id_pt, :] != res_in.n_points()]
        valid_weight = dist_weight[id_pt, index_neigh[id_pt, :] != res_in.n_points()]
        v_xy[id_pt, 0] = np.sum(res_in.v_x[time_index, valid_index] * valid_weight)
        v_xy[id_pt, 1] = np.sum(res_in.v_y[time_index, valid_index] * valid_weight)
    v_xy[v_xy == 0] = np.nan
    return v_xy


def velocity_linear_interpolation(res_in: VelocimetryResults, xs_bathy: CrossSectionBathymetry,
                                  time_index: int = 0) -> np.ndarray:
    valid_points = res_in.v_norm[0, :] != 0
    interp = LinearNDInterpolator(res_in.grid.xy[valid_points, :],
                                  np.array([res_in.v_x[time_index, valid_points],
                                            res_in.v_y[time_index, valid_points]]).T, )
    return interp(xs_bathy.data[:, 0], xs_bathy.data[:, 1])


def velocity_nearest_value(res_in: VelocimetryResults, xs_bathy: CrossSectionBathymetry,
                           time_index: int = 0) -> np.ndarray:
    valid_points = res_in.v_norm[0, :] != 0
    interp = NearestNDInterpolator(res_in.grid.xy[valid_points, :],
                                   np.array([res_in.v_x[time_index, valid_points],
                                             res_in.v_y[time_index, valid_points]]).T, )
    return interp(xs_bathy.data[:, 0], xs_bathy.data[:, 1])


# INTERNAL FUNCTIONS
def _ellipse_test(index_n, dist_n, xy_grid, xy_xs, r_x, r_y) -> None:
    rx2, ry2 = r_x * r_x, r_y * r_y
    for pt in range(xy_xs.shape[0]):
        for nei in range(index_n.shape[1]):
            if dist_n[pt, nei] != np.inf:
                if (np.pow(xy_grid[index_n[pt, nei], 0] - xy_xs[pt, 0], 2) / rx2 +
                        np.pow(xy_grid[index_n[pt, nei], 1] - xy_xs[pt, 1], 2) / ry2 > 1):
                    index_n[pt, nei] = xy_grid.shape[0]
                    dist_n[pt, nei] = np.inf

def _fill_empty_values_(v_xy, geom) -> np.ndarray:
    index_to_fill = np.argwhere(np.isnan(v_xy[:, 0]))
    x_to_fill = geom.x_abs[index_to_fill]
    index_ref = np.argwhere(~np.isnan(v_xy[:, 0]))
    x_ref = geom.x_abs[index_ref]
    vx_ref = v_xy[index_ref, 0]
    vy_ref = v_xy[index_ref, 1]
    vx_new = np.interp(x_to_fill[:, 0], x_ref[:, 0], vx_ref[:, 0], left=np.nan, right=np.nan)
    vy_new = np.interp(x_to_fill[:, 0], x_ref[:, 0], vy_ref[:, 0], left=np.nan, right=np.nan)
    v_xy[index_to_fill, 0] = vx_new[:, np.newaxis]
    v_xy[index_to_fill, 1] = vy_new[:, np.newaxis]
    return v_xy
