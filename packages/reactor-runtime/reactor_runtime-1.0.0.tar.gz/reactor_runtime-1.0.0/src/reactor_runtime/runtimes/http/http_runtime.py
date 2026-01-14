"""
HTTP Runtime for Reactor

An HTTP-based runtime that exposes REST endpoints for session management
and WebRTC for real-time video/audio/data streaming.

Endpoints:
    POST /start_session  - Start the model session
    POST /stop_session   - Stop the model session
    POST /sdp_params     - Exchange SDP offer/answer for WebRTC connection
"""

import argparse
import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Optional
import numpy as np
from fastapi import FastAPI, Request, HTTPException

from omegaconf import DictConfig
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from reactor_runtime.runtime_api import Runtime, RuntimeConfig, State
from reactor_runtime.utils.messages import ApplicationMessage
from reactor_runtime.utils.webrtc import (
    WebRTCClient,
    WebRTCSupersededError,
    MessageEvent,
    DisconnectedEvent,
    VideoFrameEvent,
)

logger = logging.getLogger(__name__)


# TODO(REA-162) Move these types to protobuf
class SDPRequest(BaseModel):
    """SDP offer request body."""

    sdp: str
    type: str = "offer"


class SDPResponse(BaseModel):
    """SDP answer response body."""

    sdp: str
    type: str


@dataclass
class HttpRuntimeConfig(RuntimeConfig):
    """
    Configuration for the HTTP Runtime.

    Extends RuntimeConfig with HTTP-specific settings.
    """

    host: str = "0.0.0.0"
    port: int = 8080
    orphan_timeout: float = (
        30.0  # Seconds to wait before stopping session when WebRTC disconnects
    )

    @staticmethod
    def parser() -> argparse.ArgumentParser:
        """
        Return an argument parser for HTTP runtime-specific arguments.

        Returns:
            argparse.ArgumentParser with HTTP-specific arguments
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--host",
            type=str,
            default="0.0.0.0",
            help="Host to bind the HTTP server to. Default: 0.0.0.0",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8080,
            help="Port to bind the HTTP server to. Default: 8080",
        )
        parser.add_argument(
            "--orphan-timeout",
            type=float,
            default=30.0,
            help="Seconds to wait before stopping session when WebRTC disconnects. Default: 30.0. Set to 0 to disable.",
        )
        return parser


class HttpRuntime(Runtime):
    """
    An HTTP runtime that exposes REST endpoints for session control
    and uses WebRTC for real-time media streaming.

    Endpoints:
        POST /start_session  - Start the model session
        POST /stop_session   - Stop the model session
        POST /sdp_params     - Exchange SDP offer/answer for WebRTC
    """

    config: HttpRuntimeConfig

    def __init__(self, config: HttpRuntimeConfig):
        """
        Initialize the HTTP runtime.

        Args:
            config: HttpRuntimeConfig containing model and runtime-specific settings.
        """
        # WebRTC client - single connection at a time
        # Protected by _client_lock for thread-safe access
        self._webrtc_client: Optional[WebRTCClient] = None
        self._client_lock = asyncio.Lock()

        # Orphan timeout task - stops session if no WebRTC connection for too long
        self._orphan_task: Optional[asyncio.Task] = None

        # FastAPI app
        self.app = FastAPI(title="Reactor HTTP Runtime")

        # Configure CORS to allow any origin
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self._setup_routes()

        # Call parent constructor (loads model)
        super().__init__(config)

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""

        @self.app.post("/start_session")
        async def start_session(request: Request):
            """Start the model session."""
            current_state = self.get_state()
            if current_state == State.RUNNING:
                logger.warning(
                    "Received start session request but session already running. Accepting."
                )
                return JSONResponse(
                    status_code=202, content={"state": current_state.value}
                )
            elif current_state in (State.IDLE, State.ERROR):
                self._start_http_session()
                return JSONResponse(content={"state": self.get_state().value})
            else:
                return JSONResponse(
                    status_code=409,
                    content={
                        "error": "Cannot start session",
                        "state": current_state.value,
                    },
                )

        @self.app.post("/stop_session")
        async def stop_session(request: Request):
            """Stop the model session."""
            current_state = self.get_state()
            if current_state != State.RUNNING:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Cannot stop session",
                        "state": current_state.value,
                    },
                )

            await self._stop_http_session()
            return JSONResponse(content={"state": self.get_state().value})

        @self.app.post("/sdp_params", response_model=SDPResponse)
        async def sdp_params(sdp_request: SDPRequest):
            """
            Handle SDP offer and return SDP answer.
            Sets up WebRTC connection with video track and data channel.

            If a previous connection exists, it is stopped cooperatively
            before creating the new one. If the new connection is superseded
            by another request during setup, returns 409 Conflict.
            """
            if not self.session_running:
                raise HTTPException(status_code=400, detail="No session running")
            try:
                answer = await self._handle_sdp_offer(sdp_request.sdp, sdp_request.type)
                return SDPResponse(sdp=answer.sdp, type=answer.type)
            except WebRTCSupersededError:
                raise HTTPException(
                    status_code=409, detail="Connection superseded by newer request"
                )
            except HTTPException:
                raise
            except Exception as e:
                logger.exception(f"Error handling SDP offer: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/health")
        async def health():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "model": self.config.model_name,
                "state": self.get_state().value,
            }

    # ===============================
    # WebRTC Connection Management
    # ===============================

    async def _handle_sdp_offer(self, sdp: str, sdp_type: str):
        """
        Handle an SDP offer and create an answer.

        Simple flow:
        1. If existing client exists, stop it cooperatively
        2. Create new client
        3. If client was superseded during creation, raise WebRTCSupersededError

        Args:
            sdp: The SDP offer string.
            sdp_type: The type of SDP (usually "offer").

        Returns:
            The SDP answer.

        Raises:
            WebRTCSupersededError: If this connection was superseded.
            RuntimeError: If connection setup fails.
        """
        # Stop existing client if any (cooperative, fast)
        async with self._client_lock:
            if self._webrtc_client is not None:
                logger.info("Stopping existing WebRTC client")
                # Stop is cooperative - signals the client to exit quickly
                self._webrtc_client.stop()
                self._webrtc_client = None

        # Create new WebRTC client
        # Uses async polling internally, yielding to event loop during setup
        logger.info("Creating new WebRTC connection")
        client, answer = await WebRTCClient.create(sdp, sdp_type)

        # Install the new client
        async with self._client_lock:
            # Check if another client was installed while we were creating
            if self._webrtc_client is not None:
                # Another request beat us, stop our client
                client.stop()
                raise WebRTCSupersededError(
                    "Connection superseded by concurrent request"
                )

            self._setup_webrtc_handlers(client)
            self._webrtc_client = client
            # Cancel any pending orphan timeout since we have a new connection
            self._cancel_orphan_timeout()
            logger.info("WebRTC connection established")

        return answer

    def _setup_webrtc_handlers(self, client: WebRTCClient) -> None:
        """Setup event handlers for a WebRTC client."""

        def on_message(event: MessageEvent):
            """Handle incoming data channel message."""
            if not self.loop.is_closed():
                self.loop.call_soon_threadsafe(
                    asyncio.create_task, self._on_data_channel_message(event.data)
                )

        def on_disconnect(event: DisconnectedEvent):
            """Handle WebRTC disconnection."""
            logger.info(f"WebRTC disconnected: {event.reason}")
            # Clear the client reference and start orphan timeout
            self._webrtc_client = None
            if self.session_running and not self.loop.is_closed():
                self.loop.call_soon_threadsafe(self._start_orphan_timeout)

        def on_video_frame(event: VideoFrameEvent):
            """Handle incoming video frame."""
            if not self.loop.is_closed():
                asyncio.run_coroutine_threadsafe(
                    self._on_incoming_video_frame(event.frame), self.loop
                )

        client.on("message", on_message)
        client.on("disconnected", on_disconnect)
        client.on("video_frame", on_video_frame)

    async def _stop_webrtc_client(self) -> None:
        """Stop and clear the current WebRTC client."""
        async with self._client_lock:
            if self._webrtc_client is not None:
                self._webrtc_client.stop()
                self._webrtc_client = None
                logger.info("WebRTC client stopped")

    # ===============================
    # Orphan Timeout Management
    # ===============================

    def _start_orphan_timeout(self) -> None:
        """
        Start the orphan timeout coroutine.

        If no WebRTC connection is established within the timeout period,
        the session will be stopped automatically.
        """
        # Don't start orphan timeout if no session is running
        # This handles the case where the disconnect handler fires after
        # the session was already stopped (e.g., via coordinator stop signal)
        if not self.session_running:
            logger.debug("Orphan timeout not started - no session running")
            return

        if self.config.orphan_timeout <= 0:
            logger.debug("Orphan timeout disabled (orphan_timeout <= 0)")
            return

        # Cancel any existing orphan task
        self._cancel_orphan_timeout()

        async def orphan_timeout_coro():
            try:
                logger.info(f"Orphan timeout started ({self.config.orphan_timeout}s)")
                await asyncio.sleep(self.config.orphan_timeout)

                # Double-check conditions before stopping
                if self.session_running and self._webrtc_client is None:
                    logger.info("Orphan timeout expired, stopping session")
                    await self._stop_http_session()
                else:
                    logger.info(
                        "Orphan timeout expired but conditions changed, not stopping"
                    )
            except asyncio.CancelledError:
                logger.info("Orphan timeout cancelled")

        self._orphan_task = asyncio.create_task(orphan_timeout_coro())

    def _cancel_orphan_timeout(self) -> None:
        """Cancel the orphan timeout if running."""
        if self._orphan_task is not None:
            self._orphan_task.cancel()
            self._orphan_task = None
            logger.debug("Orphan timeout cancelled")

    async def _on_data_channel_message(self, message: str) -> None:
        """
        Handle incoming data channel message.
        Routes the message to the model via command.

        Args:
            message: The message string (expected to be JSON).
        """
        if not self.session_running:
            logger.warning("Received data channel message but no session running")
            return

        try:
            data = json.loads(message)
            cmd_name = data.get("command", data.get("cmd", data.get("type")))
            cmd_args = data.get("args", data.get("data", {}))

            if cmd_name and self.model:
                try:
                    result = self.model.send(cmd_name, cmd_args)
                    if result is not None:
                        await self._send_data_channel_message(result)
                except ValueError as e:
                    logger.warning(f"Invalid command: {e}")
                except Exception as e:
                    logger.exception(f"Command execution failed: {e}")
        except json.JSONDecodeError:
            logger.warning(f"Received non-JSON data channel message: {message}")

    async def _on_incoming_video_frame(self, frame: np.ndarray) -> None:
        """
        Handle incoming video frame from WebRTC.
        Currently logs the frame dimensions - override for custom handling.

        Args:
            frame: NumPy array in RGB format with shape (H, W, 3).
        """
        if self.model:
            self.model.on_frame(frame)

    async def _send_data_channel_message(self, data: dict) -> None:
        """
        Send a message over the data channel.

        Args:
            data: Dictionary to send as JSON.
        """
        async with self._client_lock:
            if self._webrtc_client is not None:
                self._webrtc_client.send_message(data)

    # ===============================
    # Runtime API implementation - MODEL -> CLIENT (WebRTC)
    # ===============================

    async def send_out_app_message(self, data: ApplicationMessage) -> None:
        """
        Send an application message via the WebRTC data channel.
        """
        # Don't use lock here - send_message is thread-safe and we don't want to block
        client = self._webrtc_client
        if client is not None:
            if client.send_message(data):
                logger.debug("Sent app message via data channel")
            else:
                logger.debug("Data channel not available, message not sent")
        else:
            logger.debug("No WebRTC client, message not sent")

    async def send_out_app_frame(self, frame: np.ndarray) -> None:
        """
        Send an output frame via the WebRTC video track.
        This is called periodically by the frame buffer.

        Silently skips if no WebRTC connection is active - the model
        session continues and frames will be sent once a client connects.

        Args:
            frame: NumPy array in RGB format with shape (H, W, 3).
        """
        # Don't use lock here - send_frame is thread-safe and we don't want to block
        client = self._webrtc_client
        if client is not None:
            client.send_frame(frame)

    # ===============================
    # Runtime API implementation - Model Lifecycle Handlers
    # ===============================

    def on_model_exit(self, error: Optional[Exception]) -> None:
        """
        Called AFTER internal cleanup when the model thread exits.
        Closes the WebRTC connection if the model exited with an error.
        """
        if error:
            logger.warning(f"Model exited with error: {error}")
        else:
            logger.info("Model session ended")

        # Stop WebRTC client on exit
        client = self._webrtc_client
        if client is not None and not self.loop.is_closed():
            try:
                self.loop.call_soon_threadsafe(
                    asyncio.create_task, self._stop_webrtc_client()
                )
            except RuntimeError:
                # Event loop closed, stop synchronously
                client.stop()
                self._webrtc_client = None

    def _start_http_session(self) -> None:
        """
        Start the HTTP session and model in thread.
        """
        if self.session_running:
            logger.warning("Session already running")
            return

        if self.start_model_in_thread():
            logger.info("HTTP session started")
            # Start orphan timeout - will stop session if no client connects in time
            self._start_orphan_timeout()
        else:
            logger.error("Failed to start HTTP session")

    async def _stop_http_session(self) -> None:
        """
        Stop the HTTP session, close WebRTC connection, and cleanup.
        """
        # Cancel orphan timeout first
        self._cancel_orphan_timeout()

        # Stop the model session BEFORE stopping WebRTC client
        # This ensures session_running is False when the disconnect handler fires,
        # preventing it from starting a new orphan timeout
        self.stop_session()

        # Now stop WebRTC client - disconnect handler will see session_running=False
        await self._stop_webrtc_client()

        logger.info("HTTP session stopped")

    async def run(self) -> None:
        """
        Main entry point to run the HTTP runtime.
        Starts the FastAPI server with uvicorn.
        """
        logger.info(f"Starting HTTP runtime on {self.config.host}:{self.config.port}")

        uvicorn_config = uvicorn.Config(
            app=self.app, host=self.config.host, port=self.config.port, log_level="info"
        )
        server = uvicorn.Server(uvicorn_config)

        try:
            await server.serve()
        except KeyboardInterrupt:
            logger.info("HTTP runtime interrupted")
        finally:
            if self.session_running:
                await self._stop_http_session()
            else:
                await self._stop_webrtc_client()
            logger.info("HTTP runtime shutdown complete")


async def serve(
    model_spec: str, model_name: str, model_config: DictConfig, **kwargs
) -> None:
    """
    Entry point for running the HTTP runtime from a CLI.

    Args:
        model_spec: Python import path to the VideoModel class (module:Class)
        model_name: Name of the model
        model_config: DictConfig of kwargs to pass to the model constructor
        **kwargs: Runtime-specific arguments from HttpRuntimeConfig.parser()
            - host: Host to bind to (default: "0.0.0.0")
            - port: Port to bind to (default: 8080)
            - orphan_timeout: Seconds to wait before stopping orphaned session (default: 30.0)
    """
    host = kwargs.get("host", "0.0.0.0")
    port = kwargs.get("port", 8080)
    orphan_timeout = kwargs.get("orphan_timeout", 30.0)

    config = HttpRuntimeConfig(
        model_name=model_name,
        model_args=model_config,
        model_spec=model_spec,
        host=host,
        port=port,
        orphan_timeout=orphan_timeout,
    )

    runtime = HttpRuntime(config)
    await runtime.run()
