"""System health and diagnostics endpoint."""

from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter
from app.core.config import settings
from app.services.ml_client import ml_client

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """Return health status of core services and dependencies."""
    ml_healthy = await ml_client.check_health()

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "api": "operational",
            "ml_inference": "operational" if ml_healthy else "standby",
            "action_execution": (
                "enabled" if settings.ENABLE_SYSTEM_ACTIONS else "disabled"
            ),
        },
    }
