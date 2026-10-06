"""User configuration and preference endpoints."""

from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class SystemSettingsSchema(BaseModel):
    confidence_threshold: float = Field(0.80, ge=0.5, le=0.99)
    cooldown_seconds: float = Field(1.0, ge=0.1, le=5.0)
    failsafe_enabled: bool = True
    control_mode: str = "Presentation"  # Presentation, Media, Desktop, Disabled
    camera_resolution: str = "640x480"
    target_fps: int = 30
    enabled_gestures: List[str] = [
        "PINCH",
        "SWIPE_RIGHT",
        "SWIPE_LEFT",
        "THUMBS_UP",
        "THUMBS_DOWN",
        "OPEN_PALM",
    ]


_current_settings = SystemSettingsSchema()


@router.get("", response_model=SystemSettingsSchema)
async def get_settings() -> SystemSettingsSchema:
    """Retrieve active user configuration and preference settings."""
    return _current_settings


@router.put("", response_model=SystemSettingsSchema)
async def update_settings(payload: SystemSettingsSchema) -> SystemSettingsSchema:
    """Update active user configuration and preference settings."""
    global _current_settings
    _current_settings = payload
    return _current_settings
