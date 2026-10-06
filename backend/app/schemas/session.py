"""Session and telemetry schemas."""

from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field


class LandmarkPoint(BaseModel):
    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)
    z: float


class FrameTelemetry(BaseModel):
    client_id: str
    timestamp: float
    landmarks: List[LandmarkPoint] = Field(default_factory=list)


class RecognitionResult(BaseModel):
    gesture_name: str
    confidence: float
    category: str
    action_triggered: Optional[str] = None
    timestamp: float


class SessionCreate(BaseModel):
    client_id: str


class SessionResponse(BaseModel):
    id: uuid.UUID
    client_id: str
    status: str
    total_frames_processed: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
