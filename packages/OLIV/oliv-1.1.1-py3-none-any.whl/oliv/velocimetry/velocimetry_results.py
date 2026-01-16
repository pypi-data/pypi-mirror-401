######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass, field
import numpy as np

from oliv.velocimetry.grid import Grid


@dataclass
class VelocimetryResults:
    grid: Grid  # Reference to the grid
    # fields available : one row per time step, one column per grid point
    v_x: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    v_y: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    v_norm: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    c_max: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=float))
    peak_size: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=int))
    area: np.ndarray = field(default_factory=lambda: np.empty((0, 0), dtype=int))
    # names of available fields
    names: list[str] = field(default_factory=lambda: ["v_x", "v_y", "v_norm", "c_max", "peak_size", "area"])

    def __post_init__(self):
        for field_name in self.names:
            field_in = self.__getattribute__(field_name)
            self.__setattr__(field_name, np.empty((0, self.grid.ij.shape[0]), dtype=field_in.dtype))

    def n_times(self) -> int:
        return self.v_x.shape[0]

    def n_points(self) -> int:
        return self.v_x.shape[1]
