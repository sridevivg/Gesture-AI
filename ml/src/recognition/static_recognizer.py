"""Static hand pose recognizer."""

import logging
import os
from typing import Optional
import numpy as np
from ml.src.config import ml_settings
from ml.src.recognition.classifier import (
    BaseGestureClassifier,
    ClassificationResult,
)

logger = logging.getLogger(__name__)


class StaticGestureRecognizer(BaseGestureClassifier):
    """Classifies single-frame static hand poses (e.g. Pinch, Fist, Open Palm)."""

    def __init__(self, model_filename: Optional[str] = "static_gesture_model.joblib"):
        self.model = None
        self.classes_ = ["OPEN_PALM", "FIST", "POINTING", "PINCH", "VICTORY"]
        self.model_path = (
            os.path.join(ml_settings.MODELS_DIR, model_filename)
            if model_filename
            else None
        )
        if self.model_path and os.path.exists(self.model_path):
            self.load_model(self.model_path)

    def load_model(self, model_path: str) -> bool:
        """Load trained scikit-learn classifier model via joblib."""
        try:
            import joblib
            self.model = joblib.load(model_path)
            logger.info("Loaded static gesture model from %s", model_path)
            return True
        except Exception as e:
            logger.warning("Could not load static gesture model from %s: %s", model_path, e)
            return False

    def predict(self, features: np.ndarray) -> ClassificationResult:
        """
        Predict static gesture class from normalized 21-landmark array (shape: 21, 3 or 63,).
        If model weights are not yet trained, returns an UNKNOWN result with zero confidence.
        """
        if self.model is None:
            return ClassificationResult(
                gesture_name="UNKNOWN",
                confidence=0.0,
                category="static",
            )

        flat_features = features.reshape(1, -1)
        try:
            proba = self.model.predict_proba(flat_features)[0]
            best_idx = np.argmax(proba)
            confidence = float(proba[best_idx])
            gesture_name = self.classes_[best_idx] if best_idx < len(self.classes_) else "UNKNOWN"

            return ClassificationResult(
                gesture_name=gesture_name,
                confidence=confidence,
                category="static",
                probabilities={
                    cls_name: float(p) for cls_name, p in zip(self.classes_, proba)
                },
            )
        except Exception as e:
            logger.error("Error during static gesture inference: %s", e)
            return ClassificationResult(
                gesture_name="UNKNOWN",
                confidence=0.0,
                category="static",
            )
