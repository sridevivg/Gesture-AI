"""Unit tests for backend Pydantic schemas."""

import pytest
from pydantic import ValidationError
from app.schemas.action import ActionExecutionRequest
from app.schemas.gesture import GestureCreate
from app.schemas.session import LandmarkPoint


def test_gesture_create_valid():
    """Verify successful validation of GestureCreate schema."""
    data = {
        "name": "PINCH",
        "category": "static",
        "description": "Index finger and thumb pinching together",
        "min_confidence": 0.85,
        "is_active": True,
    }
    gesture = GestureCreate(**data)
    assert gesture.name == "PINCH"
    assert gesture.category == "static"
    assert gesture.min_confidence == 0.85


def test_gesture_create_invalid_category():
    """Verify category restriction to static or dynamic."""
    with pytest.raises(ValidationError):
        GestureCreate(
            name="INVALID",
            category="unsupported_category",
        )


def test_landmark_point_bounds():
    """Verify landmark coordinate validation within normalized bounds."""
    point = LandmarkPoint(x=0.5, y=0.8, z=-0.05)
    assert point.x == 0.5
    assert point.y == 0.8

    with pytest.raises(ValidationError):
        LandmarkPoint(x=1.5, y=0.5, z=0.0)


def test_action_execution_request():
    """Verify action execution request schema validation."""
    req = ActionExecutionRequest(
        gesture_name="SWIPE_RIGHT",
        confidence=0.92,
        metadata={"speed": 1.2},
    )
    assert req.gesture_name == "SWIPE_RIGHT"
    assert req.confidence == 0.92
