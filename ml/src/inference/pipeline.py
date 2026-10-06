"""End-to-end inference pipeline coordinating landmark normalization and classifiers."""

import logging
from typing import Dict, List, Optional
import numpy as np
from ml.src.config import ml_settings
from ml.src.recognition.classifier import ClassificationResult
from ml.src.recognition.dynamic_recognizer import DynamicGestureRecognizer
from ml.src.recognition.static_recognizer import StaticGestureRecognizer
from ml.src.utils.geometry import normalize_landmarks

logger = logging.getLogger(__name__)


class GestureInferencePipeline:
    """End-to-end recognition orchestrator."""

    def __init__(self):
        self.static_recognizer = StaticGestureRecognizer()
        self.dynamic_recognizer = DynamicGestureRecognizer()
        self.confidence_threshold = ml_settings.CONFIDENCE_THRESHOLD

    def process_landmarks(
        self, raw_landmarks: List[Dict[str, float]]
    ) -> ClassificationResult:
        """
        Ingest 21 landmarks formatted as dicts {'x': ..., 'y': ..., 'z': ...},
        normalize coordinates, and evaluate static/dynamic models.
        """
        if not raw_landmarks or len(raw_landmarks) != 21:
            return ClassificationResult(
                gesture_name="UNKNOWN",
                confidence=0.0,
                category="static",
            )

        coords_tuples = [(p["x"], p["y"], p.get("z", 0.0)) for p in raw_landmarks]
        norm_features = normalize_landmarks(coords_tuples)

        # 1. Evaluate static recognizer
        static_result = self.static_recognizer.predict(norm_features)
        if (
            static_result.gesture_name != "UNKNOWN"
            and static_result.confidence >= self.confidence_threshold
        ):
            return static_result

        # 2. Evaluate dynamic sequence recognizer
        dynamic_result = self.dynamic_recognizer.predict(norm_features)
        if (
            dynamic_result.gesture_name != "UNKNOWN"
            and dynamic_result.confidence >= self.confidence_threshold
        ):
            return dynamic_result

        return static_result
