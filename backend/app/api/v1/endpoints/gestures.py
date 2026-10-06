"""Gesture definitions REST API endpoints."""

from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.gesture import GestureCreate, GestureResponse, GestureUpdate
from app.services.gesture_service import gesture_service

router = APIRouter()


@router.get("", response_model=List[GestureResponse])
async def list_gestures(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db_session),
) -> List[GestureResponse]:
    """Retrieve all available hand gesture definitions."""
    gestures = await gesture_service.get_all_gestures(db, active_only=active_only)
    return [GestureResponse.model_validate(g) for g in gestures]


@router.post("", response_model=GestureResponse, status_code=status.HTTP_201_CREATED)
async def create_gesture(
    payload: GestureCreate,
    db: AsyncSession = Depends(get_db_session),
) -> GestureResponse:
    """Register a new gesture definition."""
    gesture = await gesture_service.create_gesture(db, payload)
    return GestureResponse.model_validate(gesture)


@router.get("/{gesture_id}", response_model=GestureResponse)
async def get_gesture(
    gesture_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> GestureResponse:
    """Retrieve a single gesture definition by ID."""
    gesture = await gesture_service.get_gesture_by_id(db, gesture_id)
    if not gesture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gesture with ID {gesture_id} not found",
        )
    return GestureResponse.model_validate(gesture)


@router.put("/{gesture_id}", response_model=GestureResponse)
async def update_gesture(
    gesture_id: uuid.UUID,
    payload: GestureUpdate,
    db: AsyncSession = Depends(get_db_session),
) -> GestureResponse:
    """Update an existing gesture definition."""
    gesture = await gesture_service.get_gesture_by_id(db, gesture_id)
    if not gesture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gesture with ID {gesture_id} not found",
        )
    updated = await gesture_service.update_gesture(db, gesture, payload)
    return GestureResponse.model_validate(updated)
