"""Model Registry for Reactor Runtime.

This module holds the global MODEL_REGISTRY and accessor functions.
It is intentionally kept dependency-free to avoid circular imports.

Attributes
----------
MODEL_REGISTRY : Dict[str, Dict[str, Any]]
    Global registry storing the single model class registered via the
    ``@model`` decorator. Only one model per execution is supported.
    If multiple models are decorated, an error will be raised during
    registration.
"""

from typing import Any, Dict

MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def get_registered_model() -> Dict[str, Any]:
    """
    Get the single registered model from the registry.

    Returns:
        Dict containing model metadata and class reference

    Raises:
        RuntimeError: If no model or multiple models are registered
    """
    if not MODEL_REGISTRY:
        raise RuntimeError(
            "No @model decorated class found in project. "
            "Ensure your VideoModel subclass has the @model decorator."
        )

    if len(MODEL_REGISTRY) > 1:
        raise RuntimeError(
            f"Multiple models found: {list(MODEL_REGISTRY.keys())}. "
            "Only one @model decorated class is allowed per project."
        )

    return next(iter(MODEL_REGISTRY.values()))


def clear_model_registry():
    """Clear the model registry. Useful for testing."""
    MODEL_REGISTRY.clear()
