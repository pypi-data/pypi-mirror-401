"""
WebRTC Client for Reactor Runtime

A self-contained WebRTC client that manages its connection lifecycle
on a dedicated thread with its own asyncio event loop.

The WebRTCClient handles:
- SDP offer/answer exchange with ICE gathering
- Video track output (model -> client)
- Data channel messaging (bidirectional)
- Event emission for connection state changes and incoming data
- Cooperative shutdown via stop event for fast superseding
- Thread-safe frame/message sending from external threads
"""

import asyncio
import json
import logging
import threading
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from aiortc import (
    RTCConfiguration,
    RTCIceServer,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.rtcdatachannel import RTCDataChannel
from av import VideoFrame
from reactor_runtime.runtime_api import SessionInformation

logger = logging.getLogger(__name__)

# =============================================================================
# Video Track Implementation
# =============================================================================


class WebRTCSessionInformation(SessionInformation):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__(loop)
        self.webrtc_connected: bool = False

    def set_webrtc_connected(self, connected: bool) -> None:
        self.webrtc_connected = connected


def numpy_to_video_frame(frame: np.ndarray) -> VideoFrame:
    """
    Convert a NumPy array (H, W, 3) RGB to an av.VideoFrame.

    Args:
        frame: NumPy array in RGB format with shape (H, W, 3).

    Returns:
        av.VideoFrame in yuv420p format suitable for WebRTC.
    """
    video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
    video_frame = video_frame.reformat(format="yuv420p")
    return video_frame


def video_frame_to_numpy(frame: VideoFrame) -> np.ndarray:
    """
    Convert an av.VideoFrame to a NumPy array (H, W, 3) RGB.

    Args:
        frame: av.VideoFrame to convert.

    Returns:
        NumPy array in RGB format with shape (H, W, 3).
    """
    if frame.format.name != "rgb24":
        frame = frame.reformat(format="rgb24")
    return frame.to_ndarray()


class OutputVideoTrack(VideoStreamTrack):
    """
    A video track that outputs frames provided via push_frame().

    This track is designed to be fed frames from the model's output.
    Thread-safe for push_frame() calls from external threads.
    """

    kind = "video"

    def __init__(self, stop_event: threading.Event):
        super().__init__()
        self._frame: Optional[VideoFrame] = None
        self._frame_lock = threading.Lock()
        self._pts = 0
        self._time_base: Optional[Fraction] = None
        self._stop_event = stop_event

    def push_frame(self, frame: np.ndarray) -> bool:
        """
        Push a new frame to be sent on the next recv() call.
        Thread-safe - can be called from any thread.

        Args:
            frame: NumPy array in RGB format with shape (H, W, 3).

        Returns:
            True if frame was queued successfully, False if stopped or failed.
        """
        if self._stop_event.is_set():
            return False

        try:
            video_frame = numpy_to_video_frame(frame)
            with self._frame_lock:
                video_frame.pts = self._pts
                if self._time_base is not None:
                    video_frame.time_base = self._time_base
                self._frame = video_frame
                self._pts += 1
            return True
        except Exception as e:
            logger.warning(f"Failed to push frame: {e}")
            return False

    async def recv(self) -> VideoFrame:
        """
        Get the next frame to send.

        Returns:
            The current video frame, or a black frame if none available.
        """
        pts, time_base = await self.next_timestamp()

        with self._frame_lock:
            if self._frame is not None:
                frame = self._frame
                frame.pts = pts
                frame.time_base = time_base
                self._time_base = time_base
                return frame

        # Return a black frame if no frame is available
        black_frame = VideoFrame(width=1280, height=720)
        black_frame.pts = pts
        black_frame.time_base = time_base
        return black_frame


# =============================================================================
# Exceptions
# =============================================================================


class WebRTCSupersededError(Exception):
    """Raised when a WebRTC client is stopped/superseded during setup."""

    pass


# =============================================================================
# Event Types
# =============================================================================


@dataclass
class WebRTCEvent:
    """Base class for WebRTC events."""

    name: str


@dataclass
class ConnectedEvent(WebRTCEvent):
    """Emitted when WebRTC connection is established."""

    name: str = field(default="connected", init=False)


@dataclass
class DisconnectedEvent(WebRTCEvent):
    """Emitted when WebRTC connection is closed or failed."""

    name: str = field(default="disconnected", init=False)
    reason: str = "unknown"


@dataclass
class MessageEvent(WebRTCEvent):
    """Emitted when a data channel message is received."""

    name: str = field(default="message", init=False)
    data: str = ""


@dataclass
class VideoFrameEvent(WebRTCEvent):
    """Emitted when an incoming video frame is received."""

    name: str = field(default="video_frame", init=False)
    frame: np.ndarray = field(default_factory=lambda: np.array([]))


# Type alias for event handlers
EventHandler = Callable[[WebRTCEvent], None]


# =============================================================================
# WebRTC Client
# =============================================================================


class WebRTCClient:
    """
    Manages a single WebRTC connection lifecycle on its own thread/event loop.

    The client runs all WebRTC operations on a dedicated thread with its own
    asyncio event loop. This provides isolation and allows thread-safe
    interaction from the main application thread.

    Features cooperative shutdown via a stop event that allows fast superseding
    of connections - if stop() is called during setup, the setup will abort
    quickly and raise WebRTCSupersededError.

    Events:
        - 'connected': When WebRTC connection is established
        - 'disconnected': When WebRTC connection is closed/failed
        - 'message': When a data channel message is received
        - 'video_frame': When an incoming video frame is received

    Usage:
        # Create client with SDP offer
        client, answer = WebRTCClient.create_sync(sdp_offer, "offer")

        # Register event handlers
        client.on("message", handle_message)
        client.on("disconnected", handle_disconnect)

        # Send frames/messages (thread-safe)
        client.send_frame(numpy_frame)
        client.send_message({"type": "response", "data": ...})

        # Cooperative shutdown (fast, waits for thread to exit)
        client.stop()
    """

    def __init__(self):
        """
        Initialize the WebRTC client.
        Do not call directly - use create_sync() factory method.
        """
        # Stop event for cooperative/collaborative thread exiting.
        # When set, all long-running operations (ICE gathering, connection setup,
        # video processing, etc.) check this flag and exit quickly, allowing the
        # client to be superseded by a new connection without blocking.
        self._stop_event = threading.Event()

        # Thread and event loop
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._loop_ready = threading.Event()

        # WebRTC state (accessed only from _loop thread)
        self._pc: Optional[RTCPeerConnection] = None
        self._data_channel: Optional[RTCDataChannel] = None
        self._output_video_track: Optional[OutputVideoTrack] = None

        # Event system
        self._event_handlers: Dict[str, List[EventHandler]] = {}
        self._handlers_lock = threading.Lock()

        # Connection state
        self._connected = threading.Event()

        # Track if we were superseded (stopped during setup)
        self._was_superseded = False

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @staticmethod
    async def create(
        sdp_offer: str,
        sdp_type: str = "offer",
        ice_servers: Optional[List[str]] = None,
    ) -> Tuple["WebRTCClient", RTCSessionDescription]:
        """
        Create a WebRTCClient asynchronously.

        Starts the client thread, establishes the WebRTC connection,
        and returns the SDP answer. Yields to the event loop periodically
        during setup.

        Args:
            sdp_offer: The SDP offer string from the remote peer.
            sdp_type: The type of SDP. Must be either "offer" or "answer".
            ice_servers: Optional list of ICE server URLs.

        Returns:
            Tuple of (client instance, SDP answer).

        Raises:
            WebRTCSupersededError: If stop() was called during setup.
            RuntimeError: If connection setup fails for other reasons.
        """
        client = WebRTCClient()
        answer = await client._start_and_connect(sdp_offer, sdp_type, ice_servers)
        return client, answer

    async def _start_and_connect(
        self,
        sdp_offer: str,
        sdp_type: str,
        ice_servers: Optional[List[str]],
    ) -> RTCSessionDescription:
        """
        Start the client thread and establish the WebRTC connection.

        Args:
            sdp_offer: The SDP offer string.
            sdp_type: The type of SDP.
            ice_servers: Optional list of ICE server URLs.

        Returns:
            The SDP answer.

        Raises:
            WebRTCSupersededError: If stop() was called during setup.
        """
        # Start the dedicated thread
        self._thread = threading.Thread(
            target=self._run_event_loop,
            name="webrtc-client",
            daemon=False,
        )
        self._thread.start()

        # Wait for the event loop to be ready (with stop check)
        while not self._loop_ready.is_set():
            if self._stop_event.is_set():
                self._was_superseded = True
                self._join_thread()
                raise WebRTCSupersededError("Client stopped before loop ready")
            # Yield to caller's event loop while waiting
            await asyncio.sleep(0.05)

        # Schedule the connection setup on the WebRTC thread
        loop = self._loop
        assert loop is not None, "Loop should be set after _loop_ready"
        future = asyncio.run_coroutine_threadsafe(
            self._setup_connection(sdp_offer, sdp_type, ice_servers),
            loop,
        )

        # Wrap the concurrent.futures.Future in an asyncio.Future for async waiting
        async def wait_for_future():
            """Wait for the threadsafe future, yielding periodically."""
            while True:
                if self._stop_event.is_set():
                    future.cancel()
                    self._was_superseded = True
                    self._join_thread()
                    raise WebRTCSupersededError("Client stopped during setup")

                try:
                    # Check if done without blocking
                    if future.done():
                        return future.result()
                    # Yield to event loop
                    await asyncio.sleep(0.05)
                except asyncio.CancelledError:
                    future.cancel()
                    self._was_superseded = True
                    self._join_thread()
                    raise WebRTCSupersededError("Client setup cancelled")

        try:
            answer = await wait_for_future()
            return answer
        except WebRTCSupersededError:
            raise
        except Exception as e:
            logger.exception(f"Failed to setup WebRTC connection: {e}")
            self.stop()
            raise RuntimeError(f"WebRTC connection setup failed: {e}")

    def _run_event_loop(self) -> None:
        """
        Run the asyncio event loop on the dedicated thread.
        This method runs until stop is requested.
        """
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop_ready.set()

        try:
            self._loop.run_until_complete(self._wait_for_stop())
        except Exception as e:
            logger.warning(f"Event loop exited: {e}")
        finally:
            # Cleanup
            try:
                self._loop.run_until_complete(self._cleanup())
            except Exception as e:
                logger.warning(f"Cleanup error: {e}")

            # Cancel pending tasks
            pending = asyncio.all_tasks(self._loop)
            for task in pending:
                task.cancel()

            # Run loop until tasks are cancelled
            if pending:
                self._loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )

            self._loop.close()
            logger.debug("WebRTC client event loop closed")

    async def _wait_for_stop(self) -> None:
        """Wait for stop signal with short polling interval."""
        while not self._stop_event.is_set():
            await asyncio.sleep(0.05)

    async def _cleanup(self) -> None:
        """Clean up WebRTC resources."""
        if self._pc is not None:
            try:
                if self._pc.connectionState != "closed":
                    await self._pc.close()
            except Exception as e:
                logger.warning(f"Error closing peer connection: {e}")
            self._pc = None

        self._data_channel = None
        self._output_video_track = None
        logger.debug("WebRTC resources cleaned up")

    # =========================================================================
    # Connection Setup
    # =========================================================================

    def _check_stopped(self) -> None:
        """Check if stop was requested and raise if so."""
        if self._stop_event.is_set():
            raise WebRTCSupersededError("Client stopped")

    async def _check_stopped_async(self) -> None:
        """Async check if stop was requested."""
        if self._stop_event.is_set():
            raise WebRTCSupersededError("Client stopped")

    async def _setup_connection(
        self,
        sdp_offer: str,
        sdp_type: str,
        ice_servers: Optional[List[str]],
    ) -> RTCSessionDescription:
        """
        Setup the WebRTC peer connection.
        Checks stop event at each major step for fast abort.

        Args:
            sdp_offer: The SDP offer string.
            sdp_type: The type of SDP.
            ice_servers: Optional list of ICE server URLs.

        Returns:
            The SDP answer.

        Raises:
            WebRTCSupersededError: If stop() was called during setup.
        """
        await self._check_stopped_async()

        # Create RTCConfiguration
        if ice_servers is None:
            ice_servers = ["stun:stun.l.google.com:19302"]

        rtc_config = RTCConfiguration(iceServers=[RTCIceServer(urls=ice_servers)])

        # Create peer connection
        pc = RTCPeerConnection(configuration=rtc_config)
        self._pc = pc

        # Setup event handlers
        self._setup_pc_handlers(pc)

        await self._check_stopped_async()

        # Set remote description (the offer)
        offer = RTCSessionDescription(sdp=sdp_offer, type=sdp_type)
        await pc.setRemoteDescription(offer)

        await self._check_stopped_async()

        # Find video transceiver from the offer (only add video if offer includes it)
        video_transceiver = None
        for transceiver in pc.getTransceivers():
            if transceiver.kind == "video":
                video_transceiver = transceiver
                break

        # Only create output video track if the offer includes video
        if video_transceiver:
            output_track = OutputVideoTrack(self._stop_event)
            self._output_video_track = output_track
            video_transceiver.sender.replaceTrack(output_track)
            video_transceiver.direction = "sendrecv"

        await self._check_stopped_async()

        # Create and set the answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        await self._check_stopped_async()

        # Wait for ICE gathering to complete (with stop checks)
        await self._gather_ice_candidates(pc)

        await self._check_stopped_async()

        local_desc = pc.localDescription
        if local_desc is None:
            raise RuntimeError("Failed to create local SDP description")

        return local_desc

    async def _gather_ice_candidates(
        self, pc: RTCPeerConnection, timeout: float = 10.0
    ) -> None:
        """
        Wait for ICE gathering to complete with cooperative stop checks.

        Args:
            pc: The RTCPeerConnection.
            timeout: Maximum time to wait in seconds.
        """
        if pc.iceGatheringState == "complete":
            return

        gathering_complete = asyncio.Event()

        @pc.on("icegatheringstatechange")
        def on_ice_gathering_state_change():
            if pc.iceGatheringState == "complete":
                gathering_complete.set()

        # Wait with periodic stop checks
        elapsed = 0.0
        check_interval = 0.1
        while elapsed < timeout:
            await self._check_stopped_async()

            try:
                await asyncio.wait_for(
                    gathering_complete.wait(), timeout=check_interval
                )
                return  # Gathering complete
            except asyncio.TimeoutError:
                elapsed += check_interval
                continue

        logger.warning(
            f"ICE gathering timed out after {timeout}s, proceeding with current candidates"
        )

    def _setup_pc_handlers(self, pc: RTCPeerConnection) -> None:
        """Setup event handlers for the peer connection."""

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            state = pc.connectionState
            logger.info(f"WebRTC connection state: {state}")

            if state == "connected":
                self._connected.set()
                self._emit_event(ConnectedEvent())
            elif state in ("failed", "closed", "disconnected"):
                self._connected.clear()
                self._emit_event(DisconnectedEvent(reason=state))

        @pc.on("datachannel")
        def on_datachannel(channel: RTCDataChannel):
            logger.info(f"Data channel received: {channel.label}")
            self._data_channel = channel
            self._setup_data_channel_handlers(channel)

        @pc.on("track")
        def on_track(track):
            logger.info(f"Track received: {track.kind}")
            if track.kind == "video":
                asyncio.create_task(self._process_incoming_video(track))

    def _setup_data_channel_handlers(self, channel: RTCDataChannel) -> None:
        """Setup handlers for a data channel."""

        @channel.on("message")
        def on_message(message):
            if not self._stop_event.is_set():
                self._emit_event(MessageEvent(data=message))

        @channel.on("open")
        def on_open():
            logger.debug(f"Data channel opened: {channel.label}")

        @channel.on("close")
        def on_close():
            logger.debug(f"Data channel closed: {channel.label}")

    async def _process_incoming_video(self, track) -> None:
        """Process incoming video frames from a track with stop checks."""
        try:
            while not self._stop_event.is_set():
                try:
                    # Use wait_for with short timeout to allow stop checks
                    frame = await asyncio.wait_for(track.recv(), timeout=0.1)
                    numpy_frame = video_frame_to_numpy(frame)
                    self._emit_event(VideoFrameEvent(frame=numpy_frame))
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    if "MediaStreamError" in str(type(e).__name__):
                        logger.debug("Video track ended")
                        break
                    logger.warning(f"Error processing video frame: {e}")
                    break
        except Exception as e:
            logger.warning(f"Video processing stopped: {e}")

    # =========================================================================
    # Event System
    # =========================================================================

    def on(self, event: str, handler: EventHandler) -> None:
        """
        Register an event handler.

        Args:
            event: The event name ('connected', 'disconnected', 'message', 'video_frame').
            handler: Callback function that receives the event object.
        """
        with self._handlers_lock:
            if event not in self._event_handlers:
                self._event_handlers[event] = []
            self._event_handlers[event].append(handler)

    def off(self, event: str, handler: Optional[EventHandler] = None) -> None:
        """
        Unregister an event handler.

        Args:
            event: The event name.
            handler: The handler to remove. If None, removes all handlers for the event.
        """
        with self._handlers_lock:
            if event not in self._event_handlers:
                return
            if handler is None:
                self._event_handlers[event] = []
            elif handler in self._event_handlers[event]:
                self._event_handlers[event].remove(handler)

    def _emit_event(self, event: WebRTCEvent) -> None:
        """
        Emit an event to all registered handlers.
        Handlers are called synchronously in the caller's context.

        Args:
            event: The event to emit.
        """
        with self._handlers_lock:
            handlers = self._event_handlers.get(event.name, [])[:]

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.exception(f"Error in event handler for '{event.name}': {e}")

    # =========================================================================
    # Public API - Sending Data
    # =========================================================================

    def send_frame(self, frame: np.ndarray) -> bool:
        """
        Send a video frame to the remote peer.
        Thread-safe - can be called from any thread.

        Args:
            frame: NumPy array in RGB format with shape (H, W, 3).

        Returns:
            True if frame was queued, False if stopped or failed.
        """
        if self._stop_event.is_set() or self._output_video_track is None:
            return False

        return self._output_video_track.push_frame(frame)

    def send_message(self, data: Union[dict, str]) -> bool:
        """
        Send a message over the data channel.
        Thread-safe - can be called from any thread.

        Args:
            data: Dictionary to send as JSON, or string to send directly.

        Returns:
            True if message was scheduled, False if stopped or failed.
        """
        if self._stop_event.is_set():
            return False

        loop = self._loop
        if loop is None or loop.is_closed():
            return False

        try:
            asyncio.run_coroutine_threadsafe(
                self._send_message_async(data),
                loop,
            )
            return True
        except Exception as e:
            logger.warning(f"Failed to schedule message send: {e}")
            return False

    async def _send_message_async(self, data: Union[dict, str]) -> None:
        """Send a message on the data channel (runs on WebRTC thread)."""
        if self._stop_event.is_set():
            return

        if self._data_channel is None:
            return

        if self._data_channel.readyState != "open":
            return

        try:
            message = json.dumps(data) if isinstance(data, dict) else data
            self._data_channel.send(message)
        except Exception as e:
            logger.warning(f"Failed to send data channel message: {e}")

    # =========================================================================
    # Stop / Shutdown
    # =========================================================================

    def _join_thread(self, timeout: float = 5.0) -> None:
        """Join the client thread if it exists."""
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("WebRTC client thread did not exit cleanly")
        self._thread = None

    def stop(self, timeout: float = 5.0) -> None:
        """
        Stop the WebRTC client cooperatively.

        Sets the stop event which all long-running operations check,
        allowing them to exit quickly. Then waits for the thread to exit.

        Args:
            timeout: Maximum time to wait for thread exit in seconds.
        """
        if self._stop_event.is_set():
            # Already stopping/stopped, just wait for thread
            self._join_thread(timeout)
            return

        logger.debug("WebRTC client stop requested")
        self._stop_event.set()
        self._join_thread(timeout)
        logger.debug("WebRTC client stopped")

    @property
    def was_superseded(self) -> bool:
        """Check if this client was stopped during setup (superseded by another)."""
        return self._was_superseded

    @property
    def is_stopped(self) -> bool:
        """Check if stop has been requested."""
        return self._stop_event.is_set()

    def is_connected(self) -> bool:
        """
        Check if the WebRTC connection is currently established.

        Returns:
            True if connected and not stopped.
        """
        return self._connected.is_set() and not self._stop_event.is_set()

    def __del__(self):
        """Ensure cleanup on garbage collection."""
        if not self._stop_event.is_set():
            try:
                self.stop(timeout=1.0)
            except Exception:
                pass
