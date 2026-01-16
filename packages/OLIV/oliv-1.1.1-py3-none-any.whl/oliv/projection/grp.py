######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass, field
import numpy as np
from scipy.spatial import ConvexHull

from oliv.common import communication, MessageLevel, ROI


# Ground Reference Points
@dataclass
class GRP:
    """ Ground Reference Points with corresponding real (X,Y,Z) and image (J,I) coordinates """
    # pts is a numpy array containing 5 columns: X Y Z j i
    pts: np.ndarray = field(default_factory=lambda: np.empty((0, 5), dtype=float))
    area: float = 0
    pixel_area: float = 0
    estimated_pixel_size: float = 0
    roi: ROI = None

    def update_stats(self):
        self.area = ConvexHull(self.pts[:, 0:3]).area
        self.pixel_area = ConvexHull(self.pts[:, 3:]).area
        self.estimated_pixel_size = np.sqrt(self.area / self.pixel_area)
        communication.display("GRP statistics:", MessageLevel.INFO)
        communication.display("- Space area = %.2f m2 , Pixel area = %.2f pix2, pixel size = %.3f m" % (
            self.area, self.pixel_area, self.estimated_pixel_size), MessageLevel.INFO)
        self.roi = ROI(xmin=np.min(self.x()), xmax=np.max(self.x()),
                       ymin=np.min(self.y()), ymax=np.max(self.y()))
        communication.display("- ROI: xmin = %.2f m, xmax = %.2f m, ymin = %.2f m, ymax = %.2f m" % (
            self.roi.xmin, self.roi.xmax, self.roi.ymin, self.roi.ymax), MessageLevel.INFO)

    def i_row(self) -> np.ndarray:
        return self.pts[:, 4]

    def j_col(self) -> np.ndarray:
        return self.pts[:, 3]

    def x(self) -> np.ndarray:
        return self.pts[:, 0]

    def y(self) -> np.ndarray:
        return self.pts[:, 1]

    def z(self) -> np.ndarray:
        return self.pts[:, 2]


def read_table(file_path: str, grp_in: GRP) -> GRP:
    """ Read the GRP table from a file """
    communication.display("Reading GRP table: " + file_path)
    if not file_path:
        communication.display("File not present", MessageLevel.ERROR)
        return grp_in

    file = open(file_path, "rb")
    lines = file.readlines()
    if lines[0][0:3] != b"GRP":
        communication.display("File does not seem top be a GRP table", MessageLevel.WARNING)
    n_points = -1
    try:
        n_points = int(lines[1])
    except:
        communication.display("Number of points cannot be read: ", MessageLevel.WARNING)
    new_grp = GRP(np.genfromtxt(file_path, skip_header=3))
    if n_points != -1 and n_points != new_grp.pts.shape[0]:
        communication.display("Number of points does not match GRP table", MessageLevel.WARNING)
    communication.display("Number of Ground Reference Points: " + str(n_points), MessageLevel.INFO)
    if grp_in.pts.shape[0]:
        new_grp.pts = np.concatenate((grp_in.pts, new_grp.pts))

    # update areas and ROI
    new_grp.update_stats()

    return new_grp
