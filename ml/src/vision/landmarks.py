"""Landmark data structures and extraction contracts."""

from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class HandLandmarksResult:
    """Encapsulates hand detection output."""

    detected: bool
    handedness: str  # "Left" | "Right"
    landmarks_3d: List[Tuple[float, float, float]]
    normalized_features: np.ndarray
    confidence: float
