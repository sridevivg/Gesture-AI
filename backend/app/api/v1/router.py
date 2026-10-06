"""Version 1 API router aggregation."""

from fastapi import APIRouter
from app.api.v1.endpoints import actions, gestures, health, sessions, settings
from app.api.v1.websockets import gesture_stream

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(gestures.router, prefix="/gestures", tags=["Gestures"])
api_v1_router.include_router(actions.router, prefix="/actions", tags=["Actions"])
api_v1_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_v1_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_v1_router.include_router(gesture_stream.router, tags=["WebSockets"])
