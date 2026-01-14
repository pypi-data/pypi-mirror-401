import argparse
import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum

from abc import ABC, abstractmethod
import os
import threading
from typing import Optional
import numpy as np

from omegaconf import DictConfig
from reactor_runtime import VideoModel
from reactor_runtime.context_api import ReactorContext
from reactor_runtime.output.frame_buffer import FrameBuffer
from reactor_runtime.utils.loader import build_model
from reactor_runtime.utils.messages import ApplicationMessage
import json

from reactor_runtime.context_api import _set_global_ctx
import uuid


logger = logging.getLogger(__name__)


class State(Enum):
    """Runtime state enumeration."""

    LOADING = "loading"
    IDLE = "idle"
    RUNNING = "running"
    RESETTING = "resetting"
    ERROR = "error"


class SessionInformation:
    """Information about the current session."""

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.session_duration_minutes: int = 0
        self.emitted_frames: int = 0
        self._loop = loop
        self._duration_task: Optional[asyncio.Task] = None

    def increment_emitted_frames(self) -> None:
        """Increment the emitted frames counter."""
        self.emitted_frames += 1

    def start_duration_counter(self) -> None:
        """Start the async task that increments duration every minute."""
        if self._duration_task is not None:
            return
        self._duration_task = self._loop.create_task(self._duration_counter())

    def stop_duration_counter(self) -> None:
        """Stop the duration counter task."""
        if self._duration_task is not None:
            self._duration_task.cancel()
            self._duration_task = None

    async def _duration_counter(self) -> None:
        """Async task that increments session duration every minute."""
        try:
            while True:
                await asyncio.sleep(60.0)
                self.session_duration_minutes += 1
                logger.debug(
                    f"Session duration: {self.session_duration_minutes} minutes"
                )
        except asyncio.CancelledError:
            pass

    def __str__(self) -> str:
        return json.dumps(
            {k: v for k, v in vars(self).items() if not k.startswith("_")}, indent=4
        )


@dataclass
class RuntimeConfig:
    """
    Base configuration for all runtime implementations.

    Contains the configuration that gets passed to the runtime constructor.
    Each runtime implementation should extend this with additional fields.
    """

    model_name: str
    model_args: DictConfig
    model_spec: str

    # Environment-based fields with immediate defaults
    deployment: str = field(default_factory=lambda: os.getenv("DEPLOYMENT", "unknown"))
    region_id: str = field(default_factory=lambda: os.getenv("REGION_ID", "unknown"))
    cloud_id: str = field(default_factory=lambda: os.getenv("CLOUD_ID", "unknown"))

    # node_id depends on other fields, so it must be built in __post_init__
    node_id: str = field(init=False)
    machine_id: str = field(init=False)

    def __post_init__(self):
        """Build node_id from deployment info and model details."""
        self.machine_id = os.getenv("HOST", str(uuid.uuid4()))
        self.node_id = "@".join(
            [
                self.deployment,
                self.region_id,
                self.cloud_id,
                self.model_name,
                self.machine_id,
            ]
        )

    @staticmethod
    def parser() -> argparse.ArgumentParser:
        """
        Return an argument parser for runtime-specific CLI arguments.

        Each runtime implementation must override this method to define its own arguments.
        The parsed args will be used to construct the config.

        Returns:
            argparse.ArgumentParser with runtime-specific arguments
        """
        raise NotImplementedError("Subclasses must implement parser()")


class Runtime(ABC):
    def __init__(self, config: RuntimeConfig):
        """
        Initialize the runtime with a configuration object.

        Args:
            config: RuntimeConfig containing model information and runtime-specific settings.
        """
        self.config = config
        self.model_loaded = False
        self.model: VideoModel = None
        self.model_thread: Optional[threading.Thread] = None
        self._state = State.LOADING
        self._state_lock = threading.Lock()
        self.loop = asyncio.get_running_loop()
        self.frame_buffer = FrameBuffer(
            callback=self._send_out_app_frame_sync,
            fps_debuff_factor=self.config.model_args.get("fps_debuff_factor", 1.0),
        )
        self.stop_evt = threading.Event()

        # Session information tracking
        self._session_info: Optional[SessionInformation] = None

        self.load_model()

    def get_state(self) -> State:
        """Thread-safe getter for the runtime state."""
        with self._state_lock:
            return self._state

    def set_state(self, new_state: State) -> None:
        """Thread-safe setter for the runtime state."""
        with self._state_lock:
            old_state = self._state
            self._state = new_state
            logger.debug(f"State transition: {old_state.value} -> {new_state.value}")

    def get_session_info(self) -> Optional[SessionInformation]:
        """
        Get the current session information.

        Returns:
            SessionInformation if a session exists (or has completed), None otherwise.
        """
        return self._session_info

    def load_model(self) -> None:
        self.model = build_model(self.config.model_spec, self.config.model_args)
        self.model_loaded = True
        logger.info(
            f"Model {self.config.model_name} loaded successfully and now available for inference."
        )
        self.set_state(State.IDLE)

    def _send_out_app_message_sync(self, data: dict) -> None:
        wrapped = ApplicationMessage(data=data).model_dump()
        try:
            logger.info(f"Sending app message to client: {wrapped}")
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self.send_out_app_message(wrapped)
            )
        except Exception as e:
            logger.warning(f"Failed to send app message to client: {e}")

    def _build_context(self) -> ReactorContext:
        """
        Build the context that hooks the model to the runtime. Defines the bindings for the functions that the model,
        when running, will be able to call. The model internally calls messages to emit frames and emit messages.
        """
        self.frame_buffer.clear()
        self.stop_evt = threading.Event()
        ctx = ReactorContext(
            _send_fn=self._send_out_app_message_sync,
            _emit_block_fn=self.frame_buffer.push,
            _enable_monitoring_fn=self.frame_buffer.enable_monitoring,
            _disable_monitoring_fn=self.frame_buffer.disable_monitoring,
            _stop_evt=self.stop_evt,
        )
        _set_global_ctx(ctx)

    async def _async_send_out_frame(self, frame: np.ndarray) -> None:
        # We need this function to move both the increment of the session info and the frame emission call on the network thread.
        if self._session_info is not None:
            # Track emitted frames
            self._session_info.increment_emitted_frames()
        # call implementation.
        await self.send_out_app_frame(frame)

    def _send_out_app_frame_sync(self, frame: np.ndarray) -> None:
        """
        Frames should be a NumPy ndarray (H, W, 3) in RGB.
        Silently fails if the event loop is closed (expected during shutdown).
        """
        # Check if loop is closed before creating the coroutine to avoid "never awaited" warning
        if self.loop.is_closed():
            return
        try:
            # We need to synchronize with the loop on the network thread
            # (this is currently running on the FrameBuffer thread.)
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self._async_send_out_frame(frame)
            )
        except RuntimeError:
            # Event loop is closed, this is expected during shutdown - silently ignore
            pass

    def start_model_in_thread(self) -> bool:
        """
        Start the model's start_session() in a separate thread. Also start emission on the frame buffer,
        and build the context that hooks the model to the runtime.

        When the model thread exits (cleanly or with error), internal cleanup is performed first,
        then the abstract on_model_exit() method is called for implementation-specific cleanup.

        State transition: IDLE/ERROR -> RUNNING

        Returns:
            True if session started successfully, False if not in IDLE or ERROR state.
        """
        current_state = self.get_state()
        if current_state not in (State.IDLE, State.ERROR):
            logger.warning(
                f"Cannot start session: state is {current_state.value}, expected IDLE or ERROR"
            )
            return False

        if self.model_thread is not None and self.model_thread.is_alive():
            logger.warning("Model thread already running, ignoring start request")
            return False

        # Transition to RUNNING
        self.set_state(State.RUNNING)

        # Start duration counter
        # We create the session info object using the minimum class, only if it is not present yet.
        if self._session_info is None:
            self._session_info = SessionInformation(self.loop)
        self._session_info.start_duration_counter()

        # Reset stop event and build context
        self._build_context()

        self.frame_buffer.clear()
        # Start frame buffer emission
        self.frame_buffer.start_emission()

        def run_model() -> None:
            error: Optional[Exception] = None
            try:
                self.model.start_session()
            except Exception as e:
                logger.critical(f"Model Error: {e}", exc_info=True)
                error = e
            finally:
                self._handle_model_thread_exit(error)

        self.model_thread = threading.Thread(
            target=run_model, daemon=False, name="model-session"
        )
        self.model_thread.start()
        logger.info("Model session started in background thread")
        return True

    def _handle_model_thread_exit(self, error: Optional[Exception]) -> None:
        """
        Internal handler called when the model thread exits.
        Performs internal cleanup first, then invokes the on_model_exit hook.

        State transitions (error takes precedence over state):
        - error is not None -> ERROR
        - error is None, RESETTING -> IDLE (normal stop via stop_session)
        - error is None, RUNNING -> IDLE (clean exit without stop_session)
        """
        current_state = self.get_state()

        # Determine target state - error takes precedence over state
        if error is not None:
            # Any error -> ERROR state (regardless of current state)
            target_state = State.ERROR
        elif current_state in (State.RESETTING, State.RUNNING):
            # Clean exit: RESETTING -> IDLE or RUNNING -> IDLE
            target_state = State.IDLE
        else:
            # Unexpected state without error, log warning and go to IDLE
            logger.warning(
                f"Unexpected state {current_state.value} during model thread exit"
            )
            target_state = State.IDLE

        # Perform internal cleanup
        if self._session_info is not None:
            self._session_info.stop_duration_counter()
            logger.info(f"Session ended: {self._session_info}")
            self._session_info = None
        self.frame_buffer.stop_emission()
        self.frame_buffer.clear()

        # Clean up thread reference (don't join here - we may be called from the thread itself)
        if self.model_thread is not None and not self.model_thread.is_alive():
            self.model_thread = None

        # Call implementation hook after cleanup
        try:
            self.on_model_exit(error)
        except Exception as e:
            logger.exception(f"Error in on_model_exit: {e}")

        # Transition to target state AFTER the cleanup of the implementation hook.
        self.set_state(target_state)
        logger.info(f"Session cleanup completed, state is now {target_state.value}")

    def stop_session(self) -> None:
        """
        Stop the current session. Signals the model to stop, waits for the thread to exit,
        and performs cleanup.

        State transition: RUNNING -> RESETTING
        """
        current_state = self.get_state()
        if current_state != State.RUNNING:
            logger.debug(
                f"Cannot stop session: state is {current_state.value}, expected RUNNING"
            )
            return

        # Transition to RESETTING
        self.set_state(State.RESETTING)

        # Signal model to stop
        self.stop_evt.set()

        # Wait for model thread to exit
        if self.model_thread is not None and self.model_thread.is_alive():
            # TODO(REA-156): Add safe timeout that handles case in which the thread hangs. This means manually calling cleanup if we kill the thread.
            logger.debug("Waiting for model thread to exit")
            self.model_thread.join()

            logger.debug("Model thread exited cleanly")

        # Note: no need trigger anything else. Upon exiting of the thread of the model, the internal cleanup will be triggered.
        # Also the on_model_exit hook will be called. So no need to do that in here.

    @property
    def session_running(self) -> bool:
        """Check if a session is currently running (state is RUNNING or RESETTING)."""
        return self.get_state() in (State.RUNNING, State.RESETTING)

    @abstractmethod
    async def send_out_app_message(self, data: ApplicationMessage) -> None:
        """
        Send an application message FROM the model TO the client.
        The message has already been wrapped in an ApplicationMessage envelope.
        This should be where the messages is sent out to the client.
        """
        pass

    @abstractmethod
    async def send_out_app_frame(self, frame: np.ndarray) -> None:
        """
        Send an application frame FROM the model TO the client.
        This function gets called internally by the frame buffer, so it means that the rate at which this get called
        is already internally handled to match the right FPS to make the generation smooth.
        Frames are a NumPy ndarray (H, W, 3) in RGB.
        """
        pass

    @abstractmethod
    def on_model_exit(self, error: Optional[Exception]) -> None:
        """
        Called AFTER internal cleanup when the model thread exits.

        Implementations should override this to perform implementation-specific cleanup,
        such as saving files, sending notifications, etc.

        Args:
            error: The exception if the model exited with an error, or None if clean exit.
        """
        pass

    @abstractmethod
    async def run(self) -> None:
        pass
