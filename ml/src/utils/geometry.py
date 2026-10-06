"""Geometric calculation and landmark normalization utilities."""

import math
from typing import List, Tuple
import numpy as np


def normalize_landmarks(raw_landmarks: List[Tuple[float, float, float]]) -> np.ndarray:
    """
    Translate landmarks relative to wrist (point 0) and scale to unit radius.
    Input: list of 21 (x, y, z) tuples.
    Output: normalized numpy array of shape (21, 3).
    """
    if not raw_landmarks or len(raw_landmarks) != 21:
        return np.zeros((21, 3), dtype=np.float32)

    coords = np.array(raw_landmarks, dtype=np.float32)

    # 1. Translate wrist (point 0) to origin (0, 0, 0)
    wrist = coords[0].copy()
    translated = coords - wrist

    # 2. Compute maximum distance from wrist to scale invariantly
    distances = np.linalg.norm(translated, axis=1)
    max_dist = np.max(distances)

    if max_dist > 1e-6:
        normalized = translated / max_dist
    else:
        normalized = translated

    return normalized


def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate 2D Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def calculate_angle(
    a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]
) -> float:
    """Calculate the interior angle (in degrees) formed by three points ABC at vertex B."""
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    norm_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    norm_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if norm_ba * norm_bc == 0:
        return 0.0

    cosine_angle = max(-1.0, min(1.0, dot_product / (norm_ba * norm_bc)))
    return math.degrees(math.acos(cosine_angle))
