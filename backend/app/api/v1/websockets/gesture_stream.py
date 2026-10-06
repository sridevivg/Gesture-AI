"""Real-time WebSocket endpoint for streaming gesture telemetry."""

import json
import logging
import time
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.schemas.action import ActionExecutionRequest
from app.services.action_executor import action_executor
from app.services.ml_client import ml_client

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket telemetry connections."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info("WebSocket client connected. Active: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        logger.info("WebSocket client disconnected. Active: %d", len(self.active_connections))

    async def broadcast(self, message: Dict) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning("Error broadcasting to connection: %s", e)
                self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/gesture-stream")
async def gesture_stream_websocket(websocket: WebSocket) -> None:
    """Handle continuous bi-directional gesture data streaming."""
    await manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                payload = json.loads(raw_data)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
                continue

            event_type = payload.get("type", "frame_landmarks")
            landmarks = payload.get("landmarks", [])

            if event_type == "ping":
                await websocket.send_json({"type": "pong", "timestamp": time.time()})
                continue

            # Query ML inference engine
            prediction = await ml_client.predict_landmarks(landmarks)
            gesture_name = prediction.get("gesture_name", "UNKNOWN")
            confidence = float(prediction.get("confidence", 0.0))

            action_result = None
            if gesture_name != "UNKNOWN" and confidence > 0.0:
                # Dispatch action if confidence meets threshold
                exec_response = await action_executor.execute_action(
                    ActionExecutionRequest(
                        gesture_name=gesture_name,
                        confidence=confidence,
                        metadata=payload.get("metadata", {}),
                    )
                )
                action_result = {
                    "executed": exec_response.executed,
                    "action_type": exec_response.action_type,
                    "status": exec_response.status,
                }

            # Return real-time recognition feedback
            response_payload = {
                "type": "gesture_feedback",
                "timestamp": time.time(),
                "gesture": gesture_name,
                "confidence": confidence,
                "category": prediction.get("category", "static"),
                "action": action_result,
            }
            await websocket.send_json(response_payload)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        logger.error("Unexpected error in gesture stream: %s", exc)
        manager.disconnect(websocket)
