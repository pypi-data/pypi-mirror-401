######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from dataclasses import dataclass
import cv2

from oliv.image.framestack import FrameStack


@dataclass
class LoadVideoParams:
    filepath: str

@dataclass
class ExtractFrameParams:
    """ Parameters for time window selection """
    start_index: int  # First frame to extract
    end_index: int  # Last frame to extract
    skip_index: int = 0  # Skip fram interval

@dataclass
class VideoFile:
    cap: cv2.VideoCapture   # OpenCV video reader
    fps: float              # Frame per second
    n_frames: int           # Number of frames

    def reset_pos(self, index: int) -> None:
        """ Reset index of the next frame to be captured """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)

    def extract_framestack(self, params: ExtractFrameParams) -> FrameStack:
        """ Build a stack of images from video """
        imgs_out = []
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, params.start_index)
        if params.end_index == -1:
            self.n_frames = cv2.CAP_PROP_FRAME_COUNT+1
        for _ in range(params.start_index, params.end_index+1, params.skip_index):
            imgs_out.append(self.cap.read()[1])
            for _ in range(params.skip_index-1):
                self.cap.read()
        fps = self.fps / params.skip_index
        return FrameStack(imgs_out, fps)
