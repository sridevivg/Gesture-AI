"""MediaPipe-based hand detection and landmark tracking."""

import logging
from typing import List, Optional
import numpy as np
from ml.src.utils.geometry import normalize_landmarks
from ml.src.vision.landmarks import HandLandmarksResult

logger = logging.getLogger(__name__)

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    mp = None
    MEDIAPIPE_AVAILABLE = False


class HandDetector:
    """Detects hands in video frames and extracts 3D keypoint landmarks."""

    def __init__(
        self,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.5,
    ):
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self._mp_hands = None
        self._hands = None

        if MEDIAPIPE_AVAILABLE and mp is not None:
            self._mp_hands = mp.solutions.hands
            self._hands = self._mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )

    def process_frame(self, frame_bgr: np.ndarray) -> List[HandLandmarksResult]:
        """Process BGR image and return detected hand landmarks."""
        if not MEDIAPIPE_AVAILABLE or self._hands is None:
            return []

        try:
            # MediaPipe requires RGB image
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            results = self._hands.process(frame_rgb)
        except Exception as e:
            logger.error("Error processing frame with MediaPipe: %s", e)
            return []

        outputs = []
        if results.multi_hand_landmarks:
            for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                handedness = "Right"
                if results.multi_handedness and len(results.multi_handedness) > idx:
                    handedness = results.multi_handedness[idx].classification[0].label

                raw_coords = [
                    (lm.x, lm.y, lm.z) for lm in hand_lms.landmark
                ]
                norm_feat = normalize_landmarks(raw_coords)

                outputs.append(
                    HandLandmarksResult(
                        detected=True,
                        handedness=handedness,
                        landmarks_3d=raw_coords,
                        normalized_features=norm_feat,
                        confidence=0.95,
                    )
                )

        return outputs

    def close(self) -> None:
        """Release MediaPipe resources."""
        if self._hands is not None:
            self._hands.close()
            self._hands = None
