"""Video capture interface."""

import logging
from typing import Generator, Optional, Tuple
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class VideoCaptureManager:
    """Manages OpenCV video stream capture lifecycle."""

    def __init__(self, camera_index: int = 0, target_fps: int = 30):
        self.camera_index = camera_index
        self.target_fps = target_fps
        self._cap: Optional[cv2.VideoCapture] = None

    def start(self) -> bool:
        """Open camera capture device."""
        try:
            self._cap = cv2.VideoCapture(self.camera_index)
            if not self._cap.isOpened():
                logger.warning("Camera index %d could not be opened.", self.camera_index)
                return False
            self._cap.set(cv2.CAP_PROP_FPS, self.target_fps)
            return True
        except Exception as e:
            logger.error("Error opening video capture: %s", e)
            return False

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a single frame from capture stream."""
        if self._cap is None or not self._cap.isOpened():
            return False, None
        return self._cap.read()

    def stop(self) -> None:
        """Release camera resource."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None
            logger.info("Video capture released.")
