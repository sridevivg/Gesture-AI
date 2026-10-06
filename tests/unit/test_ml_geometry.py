"""Unit tests for ML geometry functions."""

import pytest
from ml.src.utils.geometry import calculate_angle, calculate_distance, normalize_landmarks


def test_distance_symmetry():
    """Verify distance(p1, p2) == distance(p2, p1)."""
    p1 = (1.5, 2.5)
    p2 = (4.5, 6.5)
    assert calculate_distance(p1, p2) == pytest.approx(calculate_distance(p2, p1))


def test_normalize_empty_list():
    """Verify graceful handling of empty or malformed landmark array."""
    res = normalize_landmarks([])
    assert res.shape == (21, 3)
    assert (res == 0).all()


def test_collinear_angle():
    """Verify straight line angle (180 degrees)."""
    a = (-1.0, 0.0)
    b = (0.0, 0.0)
    c = (1.0, 0.0)
    assert calculate_angle(a, b, c) == pytest.approx(180.0, abs=1e-3)
