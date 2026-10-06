"""Action execution engine with confidence checks and safety cooldowns."""

import logging
import time
from typing import Dict, Optional
from app.adapters.media_controller import MediaController
from app.adapters.system_controller import SystemController
from app.core.config import settings
from app.schemas.action import ActionExecutionRequest, ActionExecutionResponse

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Manages safe action dispatching based on gesture confidence and cooldowns."""

    def __init__(self):
        self.system_controller = SystemController(
            failsafe_enabled=settings.SAFETY_FAILSAFE_ENABLED
        )
        self.media_controller = MediaController(self.system_controller)
        self._last_execution_time: Dict[str, float] = {}

    def is_cooling_down(self, action_type: str, cooldown_seconds: float) -> bool:
        """Check if action is currently in cooldown period."""
        now = time.time()
        last_time = self._last_execution_time.get(action_type, 0.0)
        return (now - last_time) < cooldown_seconds

    def record_execution(self, action_type: str) -> None:
        """Record timestamp of executed action."""
        self._last_execution_time[action_type] = time.time()

    async def execute_action(
        self, request: ActionExecutionRequest, mapping_info: Optional[Dict] = None
    ) -> ActionExecutionResponse:
        """Validate confidence, check cooldown, and execute action safely."""
        # 1. Global action enable check
        if not settings.ENABLE_SYSTEM_ACTIONS:
            return ActionExecutionResponse(
                executed=False,
                gesture_name=request.gesture_name,
                status="DISABLED",
                message="System action execution is disabled by configuration (ENABLE_SYSTEM_ACTIONS=false).",
            )

        # 2. Check confidence against threshold
        if request.confidence < settings.CONFIDENCE_THRESHOLD:
            return ActionExecutionResponse(
                executed=False,
                gesture_name=request.gesture_name,
                status="LOW_CONFIDENCE",
                message=f"Confidence {request.confidence:.2f} is below required threshold {settings.CONFIDENCE_THRESHOLD:.2f}.",
            )

        # 3. Determine action type
        action_type = mapping_info.get("action_type") if mapping_info else None
        if not action_type:
            action_type = self._get_default_action_for_gesture(request.gesture_name)

        if not action_type:
            return ActionExecutionResponse(
                executed=False,
                gesture_name=request.gesture_name,
                status="NO_MAPPING",
                message=f"No action mapped for gesture '{request.gesture_name}'.",
            )

        # 4. Check cooldown
        cooldown = (
            mapping_info.get("cooldown_seconds", settings.ACTION_EXECUTION_COOLDOWN_SECONDS)
            if mapping_info
            else settings.ACTION_EXECUTION_COOLDOWN_SECONDS
        )

        if self.is_cooling_down(action_type, cooldown):
            return ActionExecutionResponse(
                executed=False,
                gesture_name=request.gesture_name,
                action_type=action_type,
                status="COOLDOWN_BLOCKED",
                message=f"Action '{action_type}' is on cooldown.",
            )

        # 5. Execute action via appropriate controller
        success = self._dispatch(action_type, request.metadata)
        if success:
            self.record_execution(action_type)
            return ActionExecutionResponse(
                executed=True,
                gesture_name=request.gesture_name,
                action_type=action_type,
                status="SUCCESS",
                message=f"Action '{action_type}' executed successfully.",
            )

        return ActionExecutionResponse(
            executed=False,
            gesture_name=request.gesture_name,
            action_type=action_type,
            status="FAILED",
            message=f"Action '{action_type}' failed during system dispatch.",
        )

    def _get_default_action_for_gesture(self, gesture_name: str) -> Optional[str]:
        """Provide default standard action mappings."""
        defaults = {
            "PINCH": "MOUSE_CLICK",
            "SWIPE_RIGHT": "PRESENTATION_NEXT",
            "SWIPE_LEFT": "PRESENTATION_PREVIOUS",
            "THUMBS_UP": "VOLUME_UP",
            "THUMBS_DOWN": "VOLUME_DOWN",
        }
        return defaults.get(gesture_name)

    def _dispatch(self, action_type: str, metadata: Dict) -> bool:
        """Dispatch action to system or media controller."""
        if action_type == "MOUSE_CLICK":
            return self.system_controller.click(button="left")
        elif action_type == "MOUSE_RIGHT_CLICK":
            return self.system_controller.click(button="right")
        elif action_type == "MEDIA_PLAY_PAUSE":
            return self.media_controller.play_pause()
        elif action_type == "MEDIA_NEXT":
            return self.media_controller.next_track()
        elif action_type == "MEDIA_PREV":
            return self.media_controller.prev_track()
        elif action_type == "VOLUME_UP":
            return self.media_controller.volume_up()
        elif action_type == "VOLUME_DOWN":
            return self.media_controller.volume_down()
        elif action_type == "PRESENTATION_NEXT":
            return self.media_controller.presentation_next()
        elif action_type == "PRESENTATION_PREVIOUS":
            return self.media_controller.presentation_previous()
        elif action_type == "CURSOR_MOVE":
            x = metadata.get("x", 0.5)
            y = metadata.get("y", 0.5)
            return self.system_controller.move_cursor(x, y)
        else:
            logger.warning("Unrecognized action type: %s", action_type)
            return False


action_executor = ActionExecutor()
