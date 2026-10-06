"""Action mapping and dispatch REST API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.schemas.action import (
    ActionExecutionRequest,
    ActionExecutionResponse,
    ActionMappingCreate,
    ActionMappingResponse,
)
from app.services.action_executor import action_executor
from app.services.gesture_service import gesture_service

router = APIRouter()


@router.get("/mappings", response_model=List[ActionMappingResponse])
async def list_action_mappings(
    enabled_only: bool = True,
    db: AsyncSession = Depends(get_db_session),
) -> List[ActionMappingResponse]:
    """Retrieve all gesture-to-action bindings."""
    mappings = await gesture_service.get_action_mappings(db, enabled_only=enabled_only)
    return [ActionMappingResponse.model_validate(m) for m in mappings]


@router.post(
    "/mappings",
    response_model=ActionMappingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_action_mapping(
    payload: ActionMappingCreate,
    db: AsyncSession = Depends(get_db_session),
) -> ActionMappingResponse:
    """Create a new mapping between a gesture and an automation action."""
    mapping = await gesture_service.create_action_mapping(db, payload)
    return ActionMappingResponse.model_validate(mapping)


@router.post("/execute", response_model=ActionExecutionResponse)
async def execute_action(
    request: ActionExecutionRequest,
) -> ActionExecutionResponse:
    """Safely trigger an action if confidence and cooldown criteria are satisfied."""
    return await action_executor.execute_action(request)
