#!/usr/bin/env python3
import asyncio
import logging
from typing import Callable, List, Optional
import os
import sys

from omegaconf import DictConfig

logger = logging.getLogger(__name__)


def add_import_paths(paths: List[str]) -> None:
    """
    Prepend provided directories to sys.path if they exist.
    """
    for p in paths:
        if not p:
            continue
        ap = os.path.abspath(p)
        if os.path.isdir(ap) and ap not in sys.path:
            sys.path.insert(0, ap)
            logger.info(f"Added to sys.path: {ap}")


def configure_logging(level: str) -> None:
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
    # Reduce noise from aiortc/av unless debugging
    if level.upper() != "DEBUG":
        logging.getLogger("aiortc").setLevel(logging.WARNING)
        logging.getLogger("av").setLevel(logging.WARNING)
        logging.getLogger("aioice").setLevel(logging.WARNING)


async def run_reactor_runtime(
    runtime_serve_fn: Callable,
    model: str,
    model_name: str,
    model_root: Optional[str] = None,
    model_config: Optional[DictConfig] = None,
    log_level: str = "INFO",
    **runtime_kwargs,
) -> None:
    """
    Run the Reactor Runtime with the specified parameters.

    Args:
        runtime_serve_fn: The serve() function from the runtime module
        model: Python import path to the VideoModel class (module:Class)
        model_name: Name of the model
        model_root: Directory to add to sys.path for resolving the model module:Class
        model_config: DictConfig of kwargs to pass to the model constructor
        log_level: Logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
        **runtime_kwargs: Runtime-specific arguments passed to serve()
    """
    configure_logging(log_level)

    # Add user-provided module roots for model resolution
    if model_root is not None:
        add_import_paths([model_root])

    logging.info(f"Launching Reactor Runtime with model={model}")

    await runtime_serve_fn(
        model_spec=model,
        model_config=model_config,
        model_name=model_name,
        **runtime_kwargs,
    )


def run_reactor_runtime_sync(
    runtime_serve_fn: Callable,
    model: str,
    model_name: str,
    model_root: Optional[str] = None,
    model_config: Optional[DictConfig] = None,
    log_level: str = "INFO",
    **runtime_kwargs,
) -> None:
    """
    Synchronous wrapper for run_reactor_runtime.

    Args:
        runtime_serve_fn: The serve() function from the runtime module
        model: Python import path to the VideoModel class (module:Class)
        model_name: Name of the model
        model_root: Directory to add to sys.path for resolving the model module:Class
        model_config: DictConfig of kwargs to pass to the model constructor
        log_level: Logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
        **runtime_kwargs: Runtime-specific arguments passed to serve()
    """
    asyncio.run(
        run_reactor_runtime(
            runtime_serve_fn=runtime_serve_fn,
            model=model,
            model_root=model_root,
            model_config=model_config,
            model_name=model_name,
            log_level=log_level,
            **runtime_kwargs,
        )
    )
