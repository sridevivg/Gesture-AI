"""Gesture Pydantic data validation schemas."""

from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field


class GestureBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=64, examples=["PINCH"])
    category: str = Field(..., pattern="^(static|dynamic)$", examples=["static"])
    description: Optional[str] = None
    min_confidence: float = Field(0.80, ge=0.0, le=1.0)
    is_active: bool = True


class GestureCreate(GestureBase):
    pass


class GestureUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=64)
    category: Optional[str] = Field(None, pattern="^(static|dynamic)$")
    description: Optional[str] = None
    min_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_active: Optional[bool] = None


class GestureResponse(GestureBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
