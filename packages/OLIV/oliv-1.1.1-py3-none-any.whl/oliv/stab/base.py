######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

import cv2
import numpy as np
from dataclasses import dataclass
from copy import copy

from oliv import read_video_file, LoadVideoParams, MessageLevel
from oliv.image.framestack import FrameStack
from oliv.image.videofile import VideoFile
from oliv.common.base import communication


@dataclass
class StabilisationParams:
    smooth_stab: bool
    smooth_step: int


@dataclass
class StabilisationTransform:
    start_index: int
    end_index: int
    transformations: list


@dataclass
class VideoStabilisationTransform(StabilisationTransform):
    ref: VideoFile


@dataclass
class FrameStackStabilisationTransform(StabilisationTransform):
    ref: FrameStack


def apply_stab(stab_trans: StabilisationTransform, filepath_out: str | None) -> FrameStack | VideoFile:
    if isinstance(stab_trans, FrameStackStabilisationTransform):
        fs_in = stab_trans.ref
        w, h = fs_in.imgs[0].shape[1], fs_in.imgs[0].shape[0]
        fs_out = FrameStack([fs_in.imgs[stab_trans.start_index].copy()], copy(stab_trans.ref.fps))
        communication.start_progress("Applying stabilisation transformations for frame stack",
                                     len(stab_trans.transformations))
        for idx, matrix in enumerate(stab_trans.transformations):
            fs_out.imgs.append(cv2.warpAffine(fs_in.imgs[stab_trans.start_index+1+idx], matrix, (w, h)))
            if filepath_out is not None:
                cv2.imwrite(filepath_out+str(idx), fs_out.imgs[-1])
            communication.progress(idx + 1, len(stab_trans.transformations))
        communication.end_progress()
        return fs_out

    elif isinstance(stab_trans, VideoStabilisationTransform):
        if filepath_out is None:
            communication.display("filepath_out should be specified to stabilize video", MessageLevel.ERROR)
        video_in = stab_trans.ref
        video_in.cap.set(cv2.CAP_PROP_POS_FRAMES, stab_trans.start_index)
        img_out = video_in.cap.read()[1]
        w, h = img_out.shape[1], img_out.shape[0]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_out = cv2.VideoWriter(filepath_out, fourcc, video_in.fps, (w, h))
        video_out.write(img_out)  # write first non-modified frame
        communication.start_progress("Applying stabilisation transformations for video",
                                     len(stab_trans.transformations))
        for idx, matrix in enumerate(stab_trans.transformations):
            video_out.write(cv2.warpAffine(video_in.cap.read()[1], matrix, (w, h)))
            communication.progress(idx + 1, len(stab_trans.transformations))
        video_out.release()
        communication.end_progress()
        return read_video_file(LoadVideoParams(filepath_out))
    else:
        communication.display("stab_trans must be FrameStack or VideoFile", MessageLevel.ERROR)


def smooth_transformations(raw_transformations: list, params: StabilisationParams) -> list:
    communication.display('Smoothing transformations...', end="",level=MessageLevel.INFO)
    tmp_transformations = []
    smoothed_transformations = []
    for idx, matrix in enumerate(raw_transformations):
        tmp_transformations.append(matrix)
        if len(tmp_transformations) > params.smooth_step:
            tmp_transformations.pop(0)
        smoothed_transformations.append(np.mean(np.array(tmp_transformations), axis=0))

    communication.display('Ok', MessageLevel.INFO)
    return smoothed_transformations


def _fix_frame_border(frame_in: np.ndarray) -> np.ndarray:
    # Scale the image x% without moving the center
    T = cv2.getRotationMatrix2D((frame_in.shape[1] / 2, frame_in.shape[0] / 2), 0, 1.00)
    frame_out = cv2.warpAffine(frame_in, T, (frame_in.shape[1], frame_in.shape[0]))
    return frame_out
