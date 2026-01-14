"""
Headless Runtime for Reactor

A command-line runtime that reads commands from stdin and writes frames to disk.
Useful for testing models, batch processing, and non-interactive scenarios.
"""

import argparse
import asyncio
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import time
import cv2
import numpy as np

from omegaconf import DictConfig

from reactor_runtime.runtime_api import Runtime, RuntimeConfig, State
from reactor_runtime.utils.messages import ApplicationMessage


logger = logging.getLogger(__name__)


@dataclass
class HeadlessRuntimeConfig(RuntimeConfig):
    """
    Configuration for the Headless Runtime.

    Extends RuntimeConfig with headless-specific settings.
    """

    output_root: str = "./output"
    ignore_duplicates: bool = True

    @staticmethod
    def parser() -> argparse.ArgumentParser:
        """
        Return an argument parser for headless runtime-specific arguments.

        Returns:
            argparse.ArgumentParser with headless-specific arguments
        """
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "--output-root",
            type=str,
            default="./output",
            help="Root directory for output. Each session creates a subfolder with epoch timestamp. Default: ./output",
        )
        parser.add_argument(
            "--no-ignore-duplicates",
            action="store_true",
            dest="no_ignore_duplicates",
            help="Write all frames including duplicates (by default, duplicate frames are skipped)",
        )
        return parser


class HeadlessRuntime(Runtime):
    """
    A headless runtime that operates via stdin/stdout and saves output to files.

    Commands (via stdin):
        start           - Start the model session
        stop            - Stop the model session
        cmd <name> <json> - Send a command to the model
        help            - Show available commands
        quit            - Exit the runtime
    """

    config: HeadlessRuntimeConfig

    def __init__(self, config: HeadlessRuntimeConfig):
        """
        Initialize the headless runtime.

        Args:
            config: HeadlessRuntimeConfig containing model and runtime-specific settings.
        """
        self.file_path: Optional[Path] = None
        self._frame_count = 0
        self._duplicates_skipped = 0
        self._last_frame: Optional[np.ndarray] = None
        self._stdin_task: Optional[asyncio.Task] = None

        # Call parent constructor (loads model)
        super().__init__(config)

    # ===============================
    # Runtime API implementation - MODEL -> CLIENT (stdout)
    # ===============================

    async def send_out_app_message(self, data: ApplicationMessage) -> None:
        """
        Send an application message by printing to stdout.
        """
        output = json.dumps(data, indent=2)
        print(f"\n[MESSAGE] {output}", flush=True)

    async def send_out_app_frame(self, frame: np.ndarray) -> None:
        """
        Handle an output frame from the model.
        Writes each frame as a PNG file.
        """
        if self.file_path is None:
            logger.warning("Cannot save frame - no session running (file_path not set)")
            return

        # Check for duplicate frames
        if self.config.ignore_duplicates and self._last_frame is not None:
            if np.array_equal(frame, self._last_frame):
                self._duplicates_skipped += 1
                logger.debug(
                    f"Skipped duplicate frame (total skipped: {self._duplicates_skipped})"
                )
                return

        # Write frame to disk
        frame_path = self.file_path / f"frame_{self._frame_count:06d}.png"
        # Convert RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(frame_path), frame_bgr)
        logger.debug(f"Saved frame to {frame_path}")

        # Store reference to last frame for duplicate detection
        if self.config.ignore_duplicates:
            self._last_frame = frame.copy()

        self._frame_count += 1

    def _print_help(self) -> None:
        """Print available commands and model capabilities."""
        print("\n" + "=" * 60, flush=True)
        print("HEADLESS RUNTIME COMMANDS", flush=True)
        print("=" * 60, flush=True)
        print("  start              - Start the model session", flush=True)
        print("  stop               - Stop the model session", flush=True)
        print("  cmd <name> <json>  - Send a command to the model", flush=True)
        print("  help               - Show this help message", flush=True)
        print("  quit               - Exit the runtime", flush=True)
        print("=" * 60, flush=True)

        # Print model commands
        if self.model:
            commands_info = self.model.commands()
            if commands_info.get("commands"):
                print("\nMODEL COMMANDS:", flush=True)
                print("-" * 60, flush=True)
                for name, info in commands_info["commands"].items():
                    desc = info.get("description", "No description")
                    print(f"\n  {name}", flush=True)
                    print(f"    Description: {desc}", flush=True)
                    schema = info.get("schema", {})
                    if schema:
                        print(f"    Schema: {json.dumps(schema, indent=6)}", flush=True)
                print("-" * 60, flush=True)
            else:
                print("\nNo model commands available.", flush=True)

    # ===============================
    # Runtime API implementation - Model Lifecycle Handlers
    # ===============================

    def on_model_exit(self, error: Optional[Exception]) -> None:
        """
        Called AFTER internal cleanup when the model thread exits.
        """
        if error:
            print(f"\n[ERROR] Model exited with error: {error}", flush=True)
            logger.warning(f"Model exited with error: {error}")
        else:
            print("\n[INFO] Model session ended", flush=True)
            logger.info("Model session ended")

        # Print session summary
        summary = f"Total frames: {self._frame_count}"
        if self._duplicates_skipped > 0:
            summary += f", duplicates skipped: {self._duplicates_skipped}"
        print(f"\n[INFO] Session stopped. {summary}", flush=True)

    def start_headless_session(self) -> None:
        """
        Setup the headless session file paths, and then start the model in thread.
        """
        current_state = self.get_state()
        if current_state not in (State.IDLE, State.ERROR):
            print(
                f"\n[WARN] Cannot start session: state is {current_state.value}, expected idle or error",
                flush=True,
            )
            return

        # Reset implementation-specific state
        self._frame_count = 0
        self._duplicates_skipped = 0
        self._last_frame = None

        # Set output path to <output_root>/<current_epoch>
        self.file_path = Path(self.config.output_root) / str(int(time.time()))
        self.file_path.mkdir(parents=True, exist_ok=True)
        print(f"\n[INFO] Output directory: {self.file_path.absolute()}", flush=True)

        # Start model in thread (on_model_exit will be called when it exits)
        if self.start_model_in_thread():
            print("\n[INFO] Session started", flush=True)
        else:
            print("\n[ERROR] Failed to start session", flush=True)

    # ===============================
    # Runtime API implementation - Client Commands
    # ===============================

    def _send_command(self, cmd_line: str) -> None:
        """
        Parse and send a command to the model.

        Expected format: cmd <command_name> <json_args>
        """
        current_state = self.get_state()
        if current_state != State.RUNNING:
            print(
                f"\n[WARN] Cannot send command: state is {current_state.value}, expected running",
                flush=True,
            )
            return

        parts = cmd_line.split(maxsplit=2)
        if len(parts) < 2:
            print("\n[ERROR] Usage: cmd <command_name> [json_args]", flush=True)
            return

        cmd_name = parts[1]

        # Parse JSON args if provided
        args = {}
        if len(parts) >= 3:
            try:
                args = json.loads(parts[2])
            except json.JSONDecodeError as e:
                print(f"\n[ERROR] Invalid JSON: {e}", flush=True)
                return

        try:
            result = self.model.send(cmd_name, args)
            if result is not None:
                print(f"\n[RESULT] {json.dumps(result, indent=2)}", flush=True)
            else:
                print(f"\n[OK] Command '{cmd_name}' executed", flush=True)
        except ValueError as e:
            print(f"\n[ERROR] {e}", flush=True)
        except Exception as e:
            print(f"\n[ERROR] Command failed: {e}", flush=True)
            logger.exception("Command execution failed")

    async def _read_stdin_loop(self) -> None:
        """
        Main loop that reads commands from stdin.
        """
        print("\n" + "=" * 60, flush=True)
        print(f"Headless Runtime Ready - Model: {self.config.model_name}", flush=True)
        print("Type 'help' for available commands", flush=True)
        print("=" * 60, flush=True)

        loop = asyncio.get_event_loop()

        while True:
            try:
                # Print prompt
                status = f"[{self.get_state().value}]"
                print(f"\n{status}> ", end="", flush=True)

                # Read line from stdin asynchronously
                line = await loop.run_in_executor(None, sys.stdin.readline)

                if not line:
                    # EOF reached
                    break

                original_line = line.strip()
                line_lower = original_line.lower()

                if not original_line:
                    continue

                if line_lower == "start":
                    self.start_headless_session()
                elif line_lower == "stop":
                    current_state = self.get_state()
                    if current_state != State.RUNNING:
                        print(
                            f"\n[WARN] Cannot stop session: state is {current_state.value}, expected running",
                            flush=True,
                        )
                        continue
                    self.stop_session()
                elif line_lower.startswith("cmd "):
                    # Use original line to preserve case in command name and JSON args
                    self._send_command(original_line)
                elif line_lower == "help":
                    self._print_help()
                elif line_lower in ("quit", "exit"):
                    print("\n[INFO] Exiting...", flush=True)
                    break
                else:
                    print(
                        f"\n[ERROR] Unknown command: {original_line}. Type 'help' for available commands.",
                        flush=True,
                    )

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Error in stdin loop")
                print(f"\n[ERROR] {e}", flush=True)

        # Cleanup on exit
        if self.session_running:
            self.stop_session()

    async def run(self) -> None:
        """
        Main entry point to run the headless runtime.
        Starts the stdin reading loop and handles shutdown.
        """
        import os

        try:
            await self._read_stdin_loop()
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted", flush=True)
        finally:
            if self.session_running:
                print("\n[INFO] Stopping session...", flush=True)
                self.stop_session()
            print("\n[INFO] Runtime shutdown complete", flush=True)
            # Force exit to terminate the stdin executor thread that may still be blocking
            os._exit(0)


async def serve(
    model_spec: str, model_name: str, model_config: DictConfig, **kwargs
) -> None:
    """
    Entry point for running the headless runtime from a CLI. This has to be implemented specifically to allow compatibility with the CLI.

    Args:
        model_spec: Python import path to the VideoModel class (module:Class)
        model_name: Name of the model
        model_config: DictConfig of kwargs to pass to the model constructor
        **kwargs: Runtime-specific arguments from HeadlessRuntimeConfig.parser()
            - output_root: Root directory for output (default: "./output")
            - no_ignore_duplicates: If True, write all frames including duplicates (default: False)
    """
    # Extract runtime-specific args from kwargs
    output_root = kwargs.get("output_root", "./output")
    ignore_duplicates = not kwargs.get("no_ignore_duplicates", False)

    config = HeadlessRuntimeConfig(
        model_name=model_name,
        model_args=model_config,
        model_spec=model_spec,
        output_root=output_root,
        ignore_duplicates=ignore_duplicates,
    )

    runtime = HeadlessRuntime(config)
    await runtime.run()
