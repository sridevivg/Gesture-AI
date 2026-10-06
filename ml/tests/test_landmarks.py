"""Unit tests for ML geometry and landmark normalization."""

import numpy as np
import pytest
from ml.src.utils.geometry import (
    calculate_angle,
    calculate_distance,
    normalize_landmarks,
)


def test_normalize_landmarks_wrist_origin():
    """Verify that landmark normalization translates wrist (idx 0) to origin."""
    raw_landmarks = [(0.5 + i * 0.01, 0.4 + i * 0.01, 0.0) for i in range(21)]
    normalized = normalize_landmarks(raw_landmarks)

    assert isinstance(normalized, np.ndarray)
    assert normalized.shape == (21, 3)
    # Wrist should be at origin (0, 0, 0)
    assert pytest.approx(normalized[0, 0], abs=1e-5) == 0.0
    assert pytest.approx(normalized[0, 1], abs=1e-5) == 0.0
    assert pytest.approx(normalized[0, 2], abs=1e-5) == 0.0


def test_calculate_distance():
    """Verify 2D Euclidean distance calculation."""
    p1 = (0.0, 0.0)
    p2 = (3.0, 4.0)
    dist = calculate_distance(p1, p2)
    assert pytest.approx(dist) == 5.0


def test_calculate_angle_right_angle():
    """Verify right angle calculation (90 degrees)."""
    a = (0.0, 1.0)
    b = (0.0, 0.0)
    c = (1.0, 0.0)
    angle = calculate_angle(a, b, c)
    assert pytest.approx(angle, abs=1e-3) == 90.0
