"""Gesture and Action mapping ORM entities."""

import uuid
from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class Gesture(Base, TimestampMixin):
    """Registered hand gesture definition."""

    __tablename__ = "gestures"

    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)  # static | dynamic
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    min_confidence: Mapped[float] = mapped_column(Float, default=0.80, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    mappings: Mapped[list["ActionMapping"]] = relationship(
        "ActionMapping", back_populates="gesture", cascade="all, delete-orphan"
    )


class ActionMapping(Base, TimestampMixin):
    """Binding between a gesture and an automation action."""

    __tablename__ = "action_mappings"

    gesture_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gestures.id", ondelete="CASCADE"), nullable=False
    )
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)
    action_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    cooldown_seconds: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    gesture: Mapped["Gesture"] = relationship("Gesture", back_populates="mappings")
