"""Gesture management business logic service."""

import logging
from typing import List, Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.gesture import ActionMapping, Gesture
from app.schemas.action import ActionMappingCreate
from app.schemas.gesture import GestureCreate, GestureUpdate

logger = logging.getLogger(__name__)


class GestureService:
    """Encapsulates business operations for gestures and bindings."""

    async def get_all_gestures(
        self, db: AsyncSession, active_only: bool = True
    ) -> List[Gesture]:
        """Fetch all registered gestures."""
        stmt = select(Gesture)
        if active_only:
            stmt = stmt.where(Gesture.is_active.is_(True))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_gesture_by_id(
        self, db: AsyncSession, gesture_id: uuid.UUID
    ) -> Optional[Gesture]:
        """Fetch single gesture by primary key."""
        return await db.get(Gesture, gesture_id)

    async def create_gesture(
        self, db: AsyncSession, data: GestureCreate
    ) -> Gesture:
        """Register a new gesture definition."""
        gesture = Gesture(
            name=data.name.upper(),
            category=data.category,
            description=data.description,
            min_confidence=data.min_confidence,
            is_active=data.is_active,
        )
        db.add(gesture)
        await db.commit()
        await db.refresh(gesture)
        return gesture

    async def update_gesture(
        self, db: AsyncSession, gesture: Gesture, data: GestureUpdate
    ) -> Gesture:
        """Update existing gesture properties."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(gesture, field, value)
        await db.commit()
        await db.refresh(gesture)
        return gesture

    async def get_action_mappings(
        self, db: AsyncSession, enabled_only: bool = True
    ) -> List[ActionMapping]:
        """Fetch all action bindings."""
        stmt = select(ActionMapping)
        if enabled_only:
            stmt = stmt.where(ActionMapping.is_enabled.is_(True))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create_action_mapping(
        self, db: AsyncSession, data: ActionMappingCreate
    ) -> ActionMapping:
        """Create new mapping from gesture to action."""
        mapping = ActionMapping(
            gesture_id=data.gesture_id,
            action_type=data.action_type,
            action_payload=data.action_payload,
            is_enabled=data.is_enabled,
            cooldown_seconds=data.cooldown_seconds,
        )
        db.add(mapping)
        await db.commit()
        await db.refresh(mapping)
        return mapping


gesture_service = GestureService()
