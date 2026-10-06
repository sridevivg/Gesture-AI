"""Visualization helpers for rendering landmarks on video frames."""

from typing import List, Tuple
import numpy as np

# Standard 21-point MediaPipe hand connections
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17),                               # Palm base
]


def get_bounding_box(
    landmarks: List[Tuple[float, float, float]], width: int, height: int
) -> Tuple[int, int, int, int]:
    """Calculate pixel bounding box (xmin, ymin, xmax, ymax) from normalized landmarks."""
    if not landmarks:
        return (0, 0, 0, 0)

    xs = [int(p[0] * width) for p in landmarks]
    ys = [int(p[1] * height) for p in landmarks]

    xmin, xmax = max(0, min(xs)), min(width, max(xs))
    ymin, ymax = max(0, min(ys)), min(height, max(ys))

    # Add margin
    margin = 20
    return (
        max(0, xmin - margin),
        max(0, ymin - margin),
        min(width, xmax + margin),
        min(height, ymax + margin),
    )
