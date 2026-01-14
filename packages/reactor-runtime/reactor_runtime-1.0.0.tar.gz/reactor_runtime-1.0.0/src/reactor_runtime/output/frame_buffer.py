import logging
import queue
import threading
import time
from typing import Callable, Optional

import numpy as np


STARTING_FPS_GUESS: int = 16
STARTING_FRAME_INTERVAL: float = 1.0 / STARTING_FPS_GUESS
DEFAULT_FRAME_DIMENSIONS: tuple[int, int, int] = (720, 1280, 3)  # 720p RGB

logger: logging.Logger = logging.getLogger(__name__)


class FrameBuffer:
    """
    This frame buffer is a component used to accept frames from the model at an unstable rate, or as blocks.
    This buffer then ensures that a specific FPS is maintained, calculating the right rate to make the generation smooth.
    """

    def __init__(
        self,
        callback: Callable[[np.ndarray], None],
        maxsize: int = 50,
        fps_debuff_factor: float = 1.0,
    ) -> None:
        self._q: queue.Queue[Optional[np.ndarray]] = queue.Queue(maxsize=maxsize)
        self._counter: int = 0
        self._monitoring_active: bool = False
        self._last_block_time: Optional[float] = None
        self.fps: Optional[float] = None
        self.fps_debuff_factor: float = fps_debuff_factor

        # Emission state
        self._callback: Callable[[np.ndarray], None] = callback
        self._emission_thread: Optional[threading.Thread] = None
        self._emission_running: bool = False
        self._emission_stop_event: threading.Event = threading.Event()
        self._emission_lock: threading.Lock = (
            threading.Lock()
        )  # Protects start/stop emission
        self._last_emitted_frame: Optional[np.ndarray] = None
        self._frame_dimensions: Optional[tuple[int, int, int]] = (
            None  # (H, W, C) for creating black frames
        )

        logger.info(
            f"Frame Buffer initialized with fps_debuff_factor: {fps_debuff_factor}"
        )

    def enable_monitoring(self) -> None:
        """
        This command enables FPS monitoring and live changing. When a model is emitting blocks of frames,
        this should be called beforehand, to adapt the FPS to try and show these frames smoothly.
        In this case the enable monitoring should be called again before the next block is generated, so we can use the time o the call
        to already estimate the fps.
        """
        if self._monitoring_active is False:
            self._monitoring_active = True
            self._last_block_time = time.perf_counter()

    def disable_monitoring(self) -> None:
        """
        If the model stops emitting frames we cause the timing setup to fallback to the previous fps estimate.
        """
        self._last_block_time = None
        self._monitoring_active = False

    def push(self, frames: Optional[np.ndarray]) -> None:
        """
        Push frames to the frame buffer.
        The frames MUST be a NumPy ndarray instance. If None, the frame buffer will put the None through in the frame, allowing the video streamer to send a black frame.
        - Dimensions should be (H, W, C) for a single frame, or (N, H, W, C) for multiple frames.
        Args:
                frames: A single ndarray containing one or more frames.
        If NONE is sent, the frame buffer will put the None through in the frame, allowing the video streamer to send a black frame.
        """

        if frames is None:
            self._q.put_nowait(None)
            return

        # Extract individual frames from the ndarray
        individual_frames: list[np.ndarray]
        total_frames: int
        if frames.ndim == 4:  # (N, H, W, C)
            individual_frames = list(
                frames
            )  # (N, H, W, C) ->  list of (H, W, C) frames
            total_frames = frames.shape[0]
        elif frames.ndim == 3:  # (H, W, C)
            individual_frames = [frames]
            total_frames = 1
        else:
            raise ValueError(
                f"Unsupported frame dimensions: {frames.shape}. Expected (H, W, C) or (N, H, W, C)"
            )

        # Calculate total number of frames for FPS calculation
        if not self._last_block_time:
            if not self.fps:
                self.fps = float(STARTING_FPS_GUESS)
        else:
            block_generation_time: float = time.perf_counter() - self._last_block_time
            if self._q.qsize() > 2:
                # If the buffer size is starting to accumulate, we calculate the FPS so that we know we'll empty the buffer by the next block time.
                self.fps = (
                    (total_frames + self._q.qsize()) - 1
                ) / block_generation_time
            else:
                self.fps = (
                    total_frames / block_generation_time
                ) * self.fps_debuff_factor
            logger.debug(f"Block generation time: {block_generation_time}")
            logger.debug(f"Total frames processed: {total_frames}")
            # logger.info(f"Estimated FPS: {self.fps}")

        self._last_block_time = time.perf_counter()

        # Process each individual frame
        for frame in individual_frames:
            try:
                self._q.put_nowait(frame)
            except queue.Full:
                # drop-oldest
                try:
                    self._q.get_nowait()
                except queue.Empty:
                    pass
                try:
                    self._q.put_nowait(frame)
                except queue.Full:
                    pass

    def estimated_fps(self) -> float:
        """Base FPS estimate from historical data."""
        if not self.fps:
            return float(
                STARTING_FPS_GUESS
            )  # This is a baseline prediction, we improve with data over time.
        return self.fps

    def get_nowait(self) -> Optional[np.ndarray]:
        """Get a frame from the buffer without blocking."""
        return self._q.get_nowait()

    def clear(self) -> None:
        """Clear all frames from the buffer."""
        while True:
            try:
                self._q.get_nowait()
            except queue.Empty:
                break

    def is_monitoring_active(self) -> bool:
        return self._monitoring_active

    def start_emission(self) -> None:
        """
        Start emitting frames at the estimated FPS rate.

        The emission will:
        - Emit frames from the buffer at the estimated_fps rate
        - Re-emit the last frame if the buffer is empty
        - Emit a black frame if the buffer contains None
        - Can be stopped via stop_emission()
        - Will ignore subsequent start_emission calls if already running

        Thread-safe: Can be called from any thread.
        """
        with self._emission_lock:
            if self._emission_running:
                logger.warning(
                    "Frame emission already started, ignoring start_emission call"
                )
                return

            self._emission_running = True
            self._emission_stop_event.clear()
            self._emission_thread = threading.Thread(
                target=self._emission_loop, daemon=True
            )
            self._emission_thread.start()
            logger.info("Frame emission started")

    def stop_emission(self) -> None:
        """
        Stop the frame emission loop.

        Thread-safe: Can be called from any thread.
        """
        thread_to_join: Optional[threading.Thread] = None

        with self._emission_lock:
            if not self._emission_running:
                logger.debug("Frame emission not running, nothing to stop")
                return

            self._emission_stop_event.set()
            thread_to_join = self._emission_thread
            self._emission_thread = None
            self._emission_running = False

        # Join outside the lock to avoid potential deadlock
        if thread_to_join:
            thread_to_join.join(timeout=1.0)
        logger.info("Frame emission stopped")

    def _create_black_frame(self) -> np.ndarray:
        """
        Create a black frame based on known frame dimensions.
        Falls back to a default 720p frame if dimensions are unknown.
        """
        if self._frame_dimensions:
            return np.zeros(self._frame_dimensions, dtype=np.uint8)
        return np.zeros(DEFAULT_FRAME_DIMENSIONS, dtype=np.uint8)

    def _emission_loop(self) -> None:
        """
        Internal emission loop that runs in a separate thread.
        Emits frames at the estimated FPS rate.
        """
        while not self._emission_stop_event.is_set():
            current_fps: float = self.estimated_fps()
            frame_interval: float = (
                1.0 / current_fps if current_fps > 0 else STARTING_FRAME_INTERVAL
            )
            loop_start: float = time.perf_counter()

            try:
                frame: Optional[np.ndarray] = self._q.get_nowait()

                if frame is not None:
                    # Store frame dimensions for future black frames
                    self._frame_dimensions = (
                        frame.shape[0],
                        frame.shape[1],
                        frame.shape[2],
                    )
                    # Store as last emitted frame for re-emission
                    self._last_emitted_frame = frame
                else:
                    logger.debug("Emitting black frame (None in buffer)")

                frame = frame if frame is not None else self._create_black_frame()
                self._callback(frame)

            except queue.Empty:
                # Buffer is empty, re-emit the last frame if available
                if self._last_emitted_frame is not None:
                    self._callback(self._last_emitted_frame)
                    logger.debug("Re-emitting last frame (buffer empty)")
                else:
                    # No last frame available, emit black frame
                    black_frame: np.ndarray = self._create_black_frame()
                    self._callback(black_frame)
                    logger.debug("Emitting black frame (no last frame available)")

            # Sleep to maintain the target FPS
            elapsed: float = time.perf_counter() - loop_start
            sleep_time: float = frame_interval - elapsed
            if sleep_time > 0:
                self._emission_stop_event.wait(timeout=sleep_time)
