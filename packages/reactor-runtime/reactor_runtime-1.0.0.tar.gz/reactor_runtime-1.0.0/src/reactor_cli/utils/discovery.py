"""
Model discovery module for Reactor CLI.

This module provides utilities to discover @model decorated VideoModel classes
in the current project directory without requiring a manifest.json file.
"""

import importlib.util
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from reactor_runtime.registry import (
    get_registered_model,
    clear_model_registry,
)

logger = logging.getLogger(__name__)


def import_project_modules(path: Path, recursive: bool = False) -> None:
    """
    Import all Python modules in a directory to trigger @model decorator registration.

    When a module containing a @model decorated class is imported, the decorator
    executes and registers the model in MODEL_REGISTRY. This function imports
    all eligible Python files to enable model discovery.

    Args:
        path: Directory path to search for Python modules
        recursive: If True, recursively import from subdirectories

    Note:
        - Files starting with '_' are skipped (private modules)
        - __pycache__ directories are skipped
        - Import errors are logged as warnings
    """
    if not path.exists():
        logger.warning(f"Path does not exist: {path}")
        return

    if not path.is_dir():
        logger.warning(f"Path is not a directory: {path}")
        return

    # Add path to sys.path for imports to work
    path_str = str(path.resolve())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
        logger.debug(f"Added to sys.path: {path_str}")

    # Choose glob pattern based on recursive flag
    pattern = "**/*.py" if recursive else "*.py"

    for file in path.glob(pattern):
        # Skip private modules and cache directories
        if file.name.startswith("_"):
            continue
        if "__pycache__" in file.parts:
            continue

        module_name = file.stem

        # For recursive imports, create a qualified module name
        if recursive and file.parent != path:
            relative_path = file.relative_to(path)
            # Convert path to module name (e.g., subdir/model.py -> subdir.model)
            parts = list(relative_path.parts[:-1]) + [file.stem]
            module_name = ".".join(parts)

        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            if spec is None or spec.loader is None:
                logger.debug(f"Could not create spec for {file}")
                continue

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            logger.debug(f"Imported module: {module_name} from {file}")

        except Exception as e:
            logger.warning(f"Failed to import {file.name}: {e}")


def discover_model(
    project_path: Optional[Path] = None, recursive: bool = False
) -> Dict[str, Any]:
    """
    Clear any registered model.
    Discover and return the registered model from the project directory.

    This function:
    1. Clears any previously registered models
    2. Imports all Python modules in the project directory
    3. This triggers @model decorators to register models
    4. Returns the single registered model's metadata

    Args:
        project_path: Path to the project directory (defaults to cwd)
        recursive: If True, search subdirectories for models

    Returns:
        Dict containing model metadata and class reference:
        {
            "class": <ModelClass>,
            "name": "model-name",
            "config": "config.yaml" or None,
            "weights": ["weight1", "weight2"],
            ...additional metadata...
        }

    Raises:
        RuntimeError: If no model or multiple models are found
    """
    # Clear any previously registered models (for testing/reloading)
    clear_model_registry()

    if project_path is None:
        project_path = Path.cwd()

    logger.info(f"Discovering models in: {project_path}")

    # Import project modules to trigger @model decorator registration
    import_project_modules(project_path, recursive=recursive)

    # Get the registered model (raises if none or multiple)
    return get_registered_model()


def get_model_spec(model_info: Dict[str, Any]) -> str:
    """
    Generate a model spec string (module:ClassName) from model info.

    Args:
        model_info: Dict from discover_model() containing "class" key

    Returns:
        String in format "module:ClassName" for use with model loader
    """
    cls = model_info["class"]
    return f"{cls.__module__}:{cls.__name__}"
