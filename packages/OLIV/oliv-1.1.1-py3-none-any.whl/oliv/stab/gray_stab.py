######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from .base import *
from oliv.image.mask import Mask

@dataclass
class GrayStabilisationParams(StabilisationParams):
    maxCorners: int
    qualityLevel: float
    minDistance: float
    blockSize: int


def compute_stab(obj_in: FrameStack | VideoFile, params: GrayStabilisationParams, start_index: int = 0,
                 end_index: int = -1, mask: Mask = None) -> StabilisationTransform:

    if isinstance(obj_in, FrameStack):
        img_prev = cv2.cvtColor(obj_in.imgs[start_index], cv2.COLOR_BGR2GRAY)
        img_prev = cv2.bitwise_and(img_prev, img_prev, mask=mask.img)
        if end_index == -1:
            end_index = len(obj_in.imgs) - start_index
        stab_res = FrameStackStabilisationTransform(start_index=start_index, end_index=end_index,
                                                    transformations=[], ref=obj_in)
        communication.start_progress("Computing stabilisation transformations for frame stack", end_index-start_index)
        for img_i in range(start_index + 1, end_index):
            img_curr = cv2.cvtColor(obj_in.imgs[img_i], cv2.COLOR_BGR2GRAY)
            img_curr = cv2.bitwise_and(img_curr, img_curr, mask=mask.img)
            stab_res.transformations.append(_compute_gftt_stab(img_prev, img_curr, params))
            img_prev = img_curr
            communication.progress(img_i + 1, end_index - start_index)

    elif isinstance(obj_in, VideoFile):
        obj_in.cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)
        img_prev = cv2.cvtColor(obj_in.cap.read()[1], cv2.COLOR_BGR2GRAY)
        img_prev = cv2.bitwise_and(img_prev, img_prev, mask=mask.img)
        if end_index == -1:
            end_index = cv2.CAP_PROP_FRAME_COUNT - start_index
        stab_res = VideoStabilisationTransform(ref=obj_in, start_index=start_index, end_index=end_index,
                                               transformations=[])
        communication.start_progress("Computing stabilisation transformations for video", end_index-start_index-1)
        for img_i in range(start_index + 1, end_index):
            img_curr = cv2.cvtColor(obj_in.cap.read()[1], cv2.COLOR_BGR2GRAY)
            img_curr = cv2.bitwise_and(img_curr, img_curr, mask=mask.img)
            stab_res.transformations.append(_compute_gftt_stab(img_prev, img_curr, params))
            img_prev = img_curr
            communication.progress(img_i + 1, end_index - start_index - 1)
    else:
        communication.display("obj_to_stab must be FrameStack or VideoFile", MessageLevel.ERROR)
    communication.end_progress()
    return stab_res


def _compute_gftt_stab(img_prev: np.ndarray, img_curr: np.ndarray,
                      params: GrayStabilisationParams) -> tuple[float, float, float]:

    # determine object in previous and current images
    prev_pts = cv2.goodFeaturesToTrack(img_prev, maxCorners=params.maxCorners, qualityLevel=params.qualityLevel,
                                        minDistance=params.minDistance, blockSize=params.blockSize)
    curr_pts, status, err = cv2.calcOpticalFlowPyrLK(img_prev, img_curr, prev_pts, None)

    # filtering objects
    idx = np.where(status == 1)[0]
    prev_pts = prev_pts[idx]
    curr_pts = curr_pts[idx]

    # find transformation matrix
    M, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)

    return M
