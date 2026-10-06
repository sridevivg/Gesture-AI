"""Session tracking and recognition history ORM models."""

import uuid
from typing import Optional
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin


class RecognitionSession(Base, TimestampMixin):
    """Active recognition streaming session."""

    __tablename__ = "recognition_sessions"

    client_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    total_frames_processed: Mapped[int] = mapped_column(default=0, nullable=False)

    history_entries: Mapped[list["GestureHistory"]] = relationship(
        "GestureHistory", back_populates="session", cascade="all, delete-orphan"
    )


class GestureHistory(Base, TimestampMixin):
    """Historical record of recognized gestures and executed actions."""

    __tablename__ = "gesture_history"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recognition_sessions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    gesture_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gestures.id", ondelete="SET NULL"), nullable=True
    )
    gesture_name: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    action_executed: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    execution_status: Mapped[str] = mapped_column(
        String(64), default="SUCCESS", nullable=False
    )

    session: Mapped["RecognitionSession"] = relationship(
        "RecognitionSession", back_populates="history_entries"
    )
