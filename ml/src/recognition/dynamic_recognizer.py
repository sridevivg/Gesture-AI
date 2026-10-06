"""Dynamic temporal gesture recognizer."""

from collections import deque
import logging
import os
from typing import Deque, Optional
import numpy as np
from ml.src.config import ml_settings
from ml.src.recognition.classifier import (
    BaseGestureClassifier,
    ClassificationResult,
)

logger = logging.getLogger(__name__)


class DynamicGestureRecognizer(BaseGestureClassifier):
    """Classifies temporal multi-frame gestures using a sliding sequence window."""

    def __init__(
        self,
        window_size: int = ml_settings.TEMPORAL_WINDOW_SIZE,
        model_filename: Optional[str] = "dynamic_gesture_model.pt",
    ):
        self.window_size = window_size
        self.classes_ = ["SWIPE_LEFT", "SWIPE_RIGHT", "SWIPE_UP", "SWIPE_DOWN", "WAVE"]
        self.buffer: Deque[np.ndarray] = deque(maxlen=window_size)
        self.model = None
        self.model_path = (
            os.path.join(ml_settings.MODELS_DIR, model_filename)
            if model_filename
            else None
        )
        if self.model_path and os.path.exists(self.model_path):
            self.load_model(self.model_path)

    def load_model(self, model_path: str) -> bool:
        """Load PyTorch sequence model weights."""
        try:
            import torch
            self.model = torch.jit.load(model_path)
            self.model.eval()
            logger.info("Loaded dynamic sequence model from %s", model_path)
            return True
        except Exception as e:
            logger.warning("Could not load dynamic gesture model from %s: %s", model_path, e)
            return False

    def add_frame(self, frame_features: np.ndarray) -> None:
        """Append normalized landmark vector for current video frame."""
        self.buffer.append(frame_features.flatten())

    def reset_buffer(self) -> None:
        """Clear temporal window buffer."""
        self.buffer.clear()

    def predict(self, features: Optional[np.ndarray] = None) -> ClassificationResult:
        """Predict dynamic gesture over buffered frame window."""
        if features is not None:
            self.add_frame(features)

        if len(self.buffer) < self.window_size or self.model is None:
            return ClassificationResult(
                gesture_name="UNKNOWN",
                confidence=0.0,
                category="dynamic",
            )

        # Placeholder inference pipeline until dynamic model weights are trained
        return ClassificationResult(
            gesture_name="UNKNOWN",
            confidence=0.0,
            category="dynamic",
        )
