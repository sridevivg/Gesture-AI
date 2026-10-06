"""Action mapping Pydantic schemas."""

from datetime import datetime
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field


class ActionMappingBase(BaseModel):
    gesture_id: uuid.UUID
    action_type: str = Field(..., min_length=2, max_length=64, examples=["MOUSE_CLICK"])
    action_payload: Dict[str, Any] = Field(default_factory=dict)
    is_enabled: bool = True
    cooldown_seconds: float = Field(1.0, ge=0.1, le=60.0)


class ActionMappingCreate(ActionMappingBase):
    pass


class ActionMappingUpdate(BaseModel):
    action_type: Optional[str] = Field(None, min_length=2, max_length=64)
    action_payload: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None
    cooldown_seconds: Optional[float] = Field(None, ge=0.1, le=60.0)


class ActionMappingResponse(ActionMappingBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActionExecutionRequest(BaseModel):
    gesture_name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    session_id: Optional[uuid.UUID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ActionExecutionResponse(BaseModel):
    executed: bool
    gesture_name: str
    action_type: Optional[str] = None
    status: str
    message: str
