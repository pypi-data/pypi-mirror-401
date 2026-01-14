"""
Brightness Example - A minimal Reactor model demonstrating real-time interaction.

This model generates a simple animated gradient and allows users to adjust
the brightness in real time via the @command decorator.
"""

import time
import numpy as np
from PIL import Image, ImageDraw
from omegaconf import DictConfig
from pydantic import Field
import logging

from reactor_runtime import VideoModel, model, command, get_ctx

logger = logging.getLogger(__name__)


@model(name="brightness-example", config="config.yml")
class BrightnessExample(VideoModel):
    """
    A minimal example showing real-time interaction with a Reactor model.

    Features:
    - Generates an animated gradient with a moving bar
    - Brightness can be adjusted in real time via the set_brightness command
    - Demonstrates the @model decorator, @command decorator, and session lifecycle
    """

    @command("set_brightness", description="Adjust brightness level")
    def set_brightness(
        self,
        brightness: float = Field(
            ...,
            ge=0.0,
            le=2.0,
            description="Brightness multiplier (0.0 = black, 1.0 = normal, 2.0 = bright)",
        ),
    ):
        """Set the brightness multiplier for generated frames."""
        self._brightness = brightness

    def __init__(self, config: DictConfig):
        """
        Initialize the model.

        This runs once when the runtime starts. Load weights and initialize
        pipelines here. This example simulates weight loading with a delay.
        """
        # Fixed output parameters
        self._fps = 30
        self._height = 480
        self._width = 640

        # Configurable text overlay position
        self._text_x = config.get("text_x", 10)
        self._text_y = config.get("text_y", 10)

        # Session state
        self._brightness = 1.0
        self._frame_count = 0

        # Simulate loading model weights
        logger.info("Loading model weights...")
        time.sleep(2.0)
        logger.info("Model ready!")

    def start_session(self):
        """
        Main generation loop. Called when a user connects.

        This loop runs continuously, generating frames and checking for the
        stop signal. User commands (like set_brightness) update instance
        variables that the loop reads each iteration.
        """
        logger.info("Session started")
        frame_interval = 1.0 / self._fps

        try:
            while not get_ctx().should_stop():
                start_time = time.time()

                # Generate and emit a frame
                frame = self._generate_frame()
                get_ctx().emit_block(frame)
                self._frame_count += 1

                # Maintain target FPS
                elapsed = time.time() - start_time
                sleep_time = max(0.0, frame_interval - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

        finally:
            # Reset session state for the next user
            self._reset_state()
            logger.info("Session ended")

    def _reset_state(self):
        """Reset session state for the next user."""
        self._brightness = 1.0
        self._frame_count = 0

    def _generate_frame(self) -> np.ndarray:
        """Generate a single frame with animated gradient and brightness applied."""
        h, w = self._height, self._width

        # Create base gradient (red channel increases from top to bottom)
        img = np.zeros((h, w, 3), dtype=np.uint8)
        for y in range(h):
            intensity = int((y / h) * 255)
            img[y, :, 0] = intensity

        # Add moving green bar
        offset = (self._frame_count * 2) % w
        bar_width = max(1, w // 20)
        x_start = offset
        x_end = min(w, x_start + bar_width)
        img[:, x_start:x_end, 1] = 255

        # Apply brightness multiplier
        img = np.clip(img * self._brightness, 0, 255).astype(np.uint8)

        # Add frame counter overlay at configured position
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)

        text = f"Frame: {self._frame_count}"

        # Draw outline for visibility
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    draw.text(
                        (self._text_x + dx, self._text_y + dy), text, fill=(0, 0, 0)
                    )
        draw.text((self._text_x, self._text_y), text, fill=(255, 255, 255))

        return np.array(pil_img)
