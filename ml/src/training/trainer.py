"""Model training routines for static and dynamic gestures."""

import logging
import os
from typing import Optional
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml.src.config import ml_settings

logger = logging.getLogger(__name__)


class GestureModelTrainer:
    """Orchestrates training of gesture classification models."""

    def __init__(self, models_dir: Optional[str] = None):
        self.models_dir = models_dir or ml_settings.MODELS_DIR

    def train_random_forest(
        self,
        X: np.ndarray,
        y: np.ndarray,
        output_filename: str = "static_gesture_model.joblib",
    ) -> str:
        """Train Random Forest classifier on landmark features and persist model."""
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
        clf.fit(X_train, y_train)

        val_acc = clf.score(X_val, y_val)
        logger.info("Validation accuracy: %.4f", val_acc)

        os.makedirs(self.models_dir, exist_ok=True)
        save_path = os.path.join(self.models_dir, output_filename)
        joblib.dump(clf, save_path)
        logger.info("Model saved to %s", save_path)
        return save_path
