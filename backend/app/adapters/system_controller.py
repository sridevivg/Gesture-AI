"""System automation controller adapter for mouse and keyboard simulation."""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# Check if GUI automation is available
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    PYAUTOGUI_AVAILABLE = True
except (ImportError, KeyError):
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False


class SystemController:
    """Safely emulates desktop pointer and keyboard actions."""

    def __init__(self, failsafe_enabled: bool = True):
        self.failsafe_enabled = failsafe_enabled
        if PYAUTOGUI_AVAILABLE and pyautogui is not None:
            pyautogui.FAILSAFE = failsafe_enabled

    def get_screen_resolution(self) -> Tuple[int, int]:
        """Return screen width and height."""
        if not PYAUTOGUI_AVAILABLE or pyautogui is None:
            return (1920, 1080)
        try:
            size = pyautogui.size()
            return (size.width, size.height)
        except Exception as e:
            logger.warning("Could not query screen size: %s", e)
            return (1920, 1080)

    def move_cursor(self, normalized_x: float, normalized_y: float) -> bool:
        """Move cursor to normalized coordinates (0.0 to 1.0)."""
        if not PYAUTOGUI_AVAILABLE or pyautogui is None:
            logger.debug("PyAutoGUI unavailable. Mocked cursor move to (%.2f, %.2f)", normalized_x, normalized_y)
            return False

        width, height = self.get_screen_resolution()
        target_x = int(normalized_x * width)
        target_y = int(normalized_y * height)

        try:
            pyautogui.moveTo(target_x, target_y, duration=0.0)
            return True
        except Exception as err:
            logger.error("Failed to move cursor: %s", err)
            return False

    def click(self, button: str = "left") -> bool:
        """Perform mouse click."""
        if not PYAUTOGUI_AVAILABLE or pyautogui is None:
            logger.debug("PyAutoGUI unavailable. Mocked %s click", button)
            return False
        try:
            pyautogui.click(button=button)
            return True
        except Exception as err:
            logger.error("Failed to execute mouse click: %s", err)
            return False

    def press_key(self, key_name: str) -> bool:
        """Press a keyboard key."""
        if not PYAUTOGUI_AVAILABLE or pyautogui is None:
            logger.debug("PyAutoGUI unavailable. Mocked keypress '%s'", key_name)
            return False
        try:
            pyautogui.press(key_name)
            return True
        except Exception as err:
            logger.error("Failed to press key '%s': %s", key_name, err)
            return False
