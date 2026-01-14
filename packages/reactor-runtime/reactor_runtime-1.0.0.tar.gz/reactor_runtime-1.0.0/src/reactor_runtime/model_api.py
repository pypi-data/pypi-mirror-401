from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints
from pydantic import BaseModel, create_model
import inspect
from reactor_runtime.utils.schema import simplify_schema
from reactor_runtime.registry import (
    MODEL_REGISTRY,
)
from reactor_cli.utils.weights import get_weights
import numpy as np

logger = logging.getLogger(__name__)


def model(
    name: str,
    config: Optional[str] = None,
    weights: Optional[List[str]] = None,
    **metadata,
):
    """
    Decorator for registering a VideoModel class with the Reactor runtime.

    This decorator registers the model in a global registry (MODEL_REGISTRY) for CLI discovery.

    Args:
        name: Unique name for the model (required)
        config: Path to the model config file (optional, e.g., "config.yaml")
        weights: List of weight folder names to download from S3 (optional)
        **metadata: Additional metadata to store with the model

    Usage:
        from reactor_runtime import VideoModel, model

        @model(name="my-model", config="config.yaml", weights=["my-weights"])
        class MyModel(VideoModel):
            def start_session(self):
                ...

    The decorator:
    1. Validates that the decorated class is a VideoModel subclass
    2. Registers the class in MODEL_REGISTRY for CLI discovery
    """

    def decorator(cls: Type) -> Type:
        if not (isinstance(cls, type) and issubclass(cls, VideoModel)):
            raise TypeError(
                f"@model can only decorate VideoModel subclasses, got {cls}"
            )

        if name in MODEL_REGISTRY:
            existing = MODEL_REGISTRY[name]["class"]
            raise ValueError(
                f"Duplicate model name '{name}' registered. "
                f"Already registered by {existing.__module__}.{existing.__name__}"
            )

        # Register in global registry for CLI discovery
        MODEL_REGISTRY[name] = {
            "class": cls,
            "name": name,
            "config": config,
            "weights": weights or [],
            **metadata,
        }

        logger.debug(f"Registered model '{name}' from {cls.__module__}.{cls.__name__}")
        return cls

    return decorator


# =============================================================================
# Command Registry
# =============================================================================
# This section is used for declaration and storage of annotated commands.
# Annotated commands are registered to this registry, which stores each
# command and their declared capabilities.

command_registry: Dict[str, Dict] = {}


def _create_pydantic_model_from_signature(
    func: Callable, command_name: str
) -> Type[BaseModel]:
    """Create a Pydantic model from a function signature with type annotations."""
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    fields: Dict[str, Any] = {}
    for param_name, param in sig.parameters.items():
        # Skip 'self' parameter
        if param_name == "self":
            continue

        param_type = type_hints.get(param_name, Any)

        # Handle default values - check if it's a Pydantic Field
        if param.default != inspect.Parameter.empty:
            if (
                hasattr(param.default, "__class__")
                and param.default.__class__.__name__ == "FieldInfo"
            ):
                # This is a Pydantic Field() - use it directly
                fields[param_name] = (param_type, param.default)
            else:
                # Regular default value
                fields[param_name] = (param_type, param.default)
        else:
            # Required parameter
            fields[param_name] = (param_type, ...)

    # Create dynamic Pydantic model
    model_name = f"{command_name.title()}CommandModel"
    return create_model(model_name, **fields)


def command(name: str, description: str = ""):
    """Decorator for defining commands on VideoModel methods with automatic schema generation."""

    def decorator(func: Callable):
        if not (inspect.isfunction(func) or inspect.ismethod(func)):
            raise ValueError(f"@command can only decorate methods, got {type(func)}")

        pydantic_model = _create_pydantic_model_from_signature(func, name)
        command_registry[name] = {
            "model": pydantic_model,
            "description": description,
            "handler": func,
        }
        return func

    return decorator


class VideoModel(ABC):
    """
    A model that PRODUCES video frames and accepts command messages.

    Runtime contract:
      - The runtime will call `start(ctx, emit_frame)` in a background task.
      - The model should repeatedly call: `await emit_frame(frame)` to push frames.
      - The model should return from `start` only when stopped or on error.
      - The runtime may call `send(command, data)` at any time to control the model.
      - The runtime will call `stop()` on session teardown.

    Notes:
      - `frame` should be a NumPy ndarray (H, W, 3) in RGB.

    Registration:
      - Use the @model decorator to register your VideoModel subclass:

        @model(name="my-model", weights=["my-weights"])
        class MyModel(VideoModel):
            ...
    """

    name: str = "video-model"

    @abstractmethod
    def start_session(self) -> None:
        """
        Start producing frames and invoke `await emit_frame(frame)` for each frame.
        This method should return when the model is stopped.
        This method should NOT load from memory the model, but instead should take the already
        existing model reference (loaded in __init__) and run it.
        """
        raise NotImplementedError

    def on_frame(self, frame: np.ndarray):
        """
        Called for each frame arriving to the model from the client stream.
        """
        pass

    def send(self, cmd_name: str, args: Optional[dict] = None):
        """Dispatch a command to the model using the decorator-based command system."""
        # Handle built-in requestCapabilities command
        if cmd_name == "requestCapabilities":
            return self.commands()

        if cmd_name not in command_registry:
            raise ValueError(f"Unknown command: {cmd_name}")

        cmd = command_registry[cmd_name]
        model_cls = cmd["model"]
        handler = cmd["handler"]

        # Validate arguments using the Pydantic model
        if args is None:
            args = {}
        validated_obj = model_cls(**args)

        # Extract validated values as kwargs
        validated_kwargs = {
            k: getattr(validated_obj, k) for k in validated_obj.model_fields.keys()
        }

        # Call the method with validated arguments
        result = handler(self, **validated_kwargs)

        return result

    @classmethod
    def commands(cls) -> dict:
        """
        Returns the static command schema for this model.

        This method returns a dictionary describing all @command decorated methods
        and their parameter schemas. It reads from the global command_registry which
        is populated at import time by @command decorators.

        Note:
            This is a classmethod that accesses static metadata only. It does not
            depend on instance state and should not be overridden. The command
            schema is determined at class definition time by @command decorators.

        Returns:
            dict: Schema with format {"commands": {name: {"description": ..., "schema": ...}}}
        """
        return {
            "commands": {
                name: {
                    "description": meta["description"],
                    "schema": simplify_schema(meta["model"]),
                }
                for name, meta in command_registry.items()
            }
        }

    @staticmethod
    def weights(weight: str) -> Path:
        """
        Returns the path to the weights for the model.

        The weights list is defined in the @model decorator:

            @model(name="my-model", weights=["weight-folder-1", "weight-folder-2"])
            class MyModel(VideoModel):
                ...

        This method can be called on VideoModel directly or on any subclass:
            VideoModel.weights("my-weights")  # Works - looks up from MODEL_REGISTRY
            MyModel.weights("my-weights")     # Works - uses decorator metadata

        Args:
            weight: Name of the weight folder to retrieve

        Returns:
            Path to the downloaded weight folder

        Raises:
            ValueError: If the weight is not in the model's weights list
            RuntimeError: If no model is registered
        """
        # Look up weights from the registered model in MODEL_REGISTRY
        # This allows calling VideoModel.weights() without needing the subclass
        if not MODEL_REGISTRY:
            raise RuntimeError(
                "No @model decorated class found. "
                "Ensure your VideoModel subclass has the @model decorator."
            )

        # Get the single registered model's metadata
        model_info = next(iter(MODEL_REGISTRY.values()))
        weights_list = model_info.get("weights", [])

        if weight not in weights_list:
            if weights_list:
                weights_list_str = "\n- " + "\n- ".join(weights_list)
                logger.info(f"Available weights:{weights_list_str}")
            raise ValueError(
                f"Weight '{weight}' not found in @model decorator. "
                "Please ensure all weights used by the model are listed in the @model decorator's weights parameter."
            )

        result = get_weights(weight)
        logger.debug(f"Weight {weight} found at {result}")
        return result
