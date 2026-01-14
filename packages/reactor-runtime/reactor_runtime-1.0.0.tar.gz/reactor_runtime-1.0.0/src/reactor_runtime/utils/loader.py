import importlib
import inspect
import logging
import sys
from typing import Tuple

from omegaconf import DictConfig

from reactor_runtime.model_api import VideoModel

logger = logging.getLogger(__name__)


def parse_spec(spec: str) -> Tuple[str, str]:
    """
    Parse a 'module:ClassName' string into (module, class_name).
    """
    if not spec or ":" not in spec:
        raise ValueError(f"Invalid spec '{spec}'. Expected 'module:ClassName'.")
    module, class_name = spec.split(":", 1)
    module = module.strip()
    class_name = class_name.strip()
    if not module or not class_name:
        raise ValueError(f"Invalid spec '{spec}'. Expected 'module:ClassName'.")
    return module, class_name


def load_class(spec: str) -> type:
    """
    Dynamically import and return a class from 'module:ClassName'.

    Note: The caller is responsible for adding the model directory to sys.path
    before calling this function (typically done via launch.py's add_import_paths).
    """
    module_name, class_name = parse_spec(spec)

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Module '{module_name}' not found. "
            f"Ensure the model directory is in sys.path (current: {sys.path[:3]}...)"
        ) from e

    try:
        cls = getattr(module, class_name)
    except AttributeError:
        raise ImportError(f"Class '{class_name}' not found in module '{module_name}'")
    if not inspect.isclass(cls):
        raise TypeError(f"'{class_name}' in module '{module_name}' is not a class")
    return cls


def build_model(model_spec: str, config: DictConfig) -> VideoModel:
    """
    Instantiate a VideoModel from spec and config.

    Args:
        model_spec: Python import path to the VideoModel class (module:Class)
        config: DictConfig to pass to the model constructor
    """
    cls = load_class(model_spec)
    if not issubclass(cls, VideoModel):
        raise TypeError(
            f"Loaded class '{cls.__name__}' is not a subclass of VideoModel"
        )

    try:
        instance = cls(config=config)
    except TypeError as e:
        raise TypeError(
            f"Failed constructing model '{cls.__name__}' with config {config}: {e}"
        ) from e

    return instance
