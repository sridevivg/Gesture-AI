"""Media playback and presentation control adapter."""

import logging
from app.adapters.system_controller import SystemController

logger = logging.getLogger(__name__)


class MediaController:
    """Controls media playback and presentation slides via system keys."""

    def __init__(self, system_controller: SystemController):
        self.system = system_controller

    def play_pause(self) -> bool:
        """Toggle media playback."""
        logger.info("Executing media play/pause")
        return self.system.press_key("playpause")

    def next_track(self) -> bool:
        """Skip to next media track."""
        logger.info("Executing media next track")
        return self.system.press_key("nexttrack")

    def prev_track(self) -> bool:
        """Go to previous media track."""
        logger.info("Executing media prev track")
        return self.system.press_key("prevtrack")

    def volume_up(self) -> bool:
        """Increment system audio volume."""
        logger.info("Executing volume up")
        return self.system.press_key("volumeup")

    def volume_down(self) -> bool:
        """Decrement system audio volume."""
        logger.info("Executing volume down")
        return self.system.press_key("volumedown")

    def presentation_next(self) -> bool:
        """Advance presentation to next slide."""
        logger.info("Executing presentation next slide")
        return self.system.press_key("right")

    def presentation_previous(self) -> bool:
        """Go back to previous presentation slide."""
        logger.info("Executing presentation previous slide")
        return self.system.press_key("left")
