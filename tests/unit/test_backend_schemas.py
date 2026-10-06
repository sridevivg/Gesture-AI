"""Unit tests for backend request and response schemas."""

import pytest
from pydantic import ValidationError
from backend.app.schemas.action import (
    ActionExecutionRequest,
    ActionExecutionResponse,
    ActionMappingCreate,
)
from backend.app.schemas.gesture import GestureCreate
from backend.app.schemas.session import LandmarkPoint


def test_gesture_schema_validation():
    """Verify validation constraints on GestureCreate."""
    valid_gesture = GestureCreate(
        name="OPEN_PALM",
        category="static",
        description="Flat palm facing camera",
        min_confidence=0.85,
    )
    assert valid_gesture.name == "OPEN_PALM"
    assert valid_gesture.category == "static"


def test_action_execution_schema():
    """Verify ActionExecutionResponse serialization."""
    res = ActionExecutionResponse(
        executed=True,
        gesture_name="PINCH",
        action_type="MOUSE_CLICK",
        status="SUCCESS",
        message="Executed click",
    )
    assert res.executed is True
    assert res.action_type == "MOUSE_CLICK"
