"""Abstract base classifier interface for gesture prediction."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np


@dataclass
class ClassificationResult:
    """Standardized output structure for gesture inference."""

    gesture_name: str
    confidence: float
    category: str  # "static" | "dynamic"
    probabilities: Optional[Dict[str, float]] = None


class BaseGestureClassifier(ABC):
    """Abstract interface that all gesture classifiers must implement."""

    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        """Load trained weights or model checkpoint from disk."""
        pass

    @abstractmethod
    def predict(self, features: np.ndarray) -> ClassificationResult:
        """Perform inference on preprocessed feature tensor."""
        pass
