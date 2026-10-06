"""Machine Learning Service Interface."""

import logging
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class MLServiceClient:
    """Client for communicating with the ML inference service."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.ML_SERVICE_URL

    async def predict_landmarks(
        self, landmarks: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """Send landmark coordinates to ML inference service for classification."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                response = await client.post(
                    f"{self.base_url}/predict",
                    json={"landmarks": landmarks},
                )
                if response.status_code == 200:
                    return response.json()
                logger.warning(
                    "ML service returned status %s: %s",
                    response.status_code,
                    response.text,
                )
        except Exception as e:
            logger.debug("ML service unreachable at %s (%s). Using fallback heuristic.", self.base_url, e)

        # Fallback heuristic response when ML service is starting up
        return {
            "gesture_name": "UNKNOWN",
            "confidence": 0.0,
            "category": "static",
        }

    async def check_health(self) -> bool:
        """Check if ML service is reachable and healthy."""
        try:
            async with httpx.AsyncClient(timeout=1.0) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False


ml_client = MLServiceClient()
