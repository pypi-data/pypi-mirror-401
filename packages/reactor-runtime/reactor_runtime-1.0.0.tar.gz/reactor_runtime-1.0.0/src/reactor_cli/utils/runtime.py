"""Runtime loading utilities."""

import importlib
import re


def load_runtime(runtime_name: str):
    """
    Dynamically load a runtime module and extract its config class and serve function.

    This enables a plugin-like architecture where new runtimes can be added without
    modifying the CLI code. Each runtime must follow this convention:

    Module location:
        reactor_runtime.runtimes.<name>.<name>_runtime
        e.g., reactor_runtime.runtimes.headless.headless_runtime

    Required exports:
        - <Name>RuntimeConfig: A dataclass extending RuntimeConfig with a static
          parser() method that returns an ArgumentParser for runtime-specific CLI args.
        - serve(): An async function that constructs the config and runtime, then runs it.

    Benefits of dynamic loading:
        1. Lazy imports - runtime dependencies are only loaded when that runtime is used,
           so users don't need all dependencies installed (e.g., aiortc for HTTP runtime).
        2. Extensibility - new runtimes can be added by just creating a new module.
        3. Runtime-specific CLI - each runtime defines its own argument parser.

    Args:
        runtime_name: Name of the runtime (e.g., "headless", "http", "redis")

    Returns:
        Tuple of (config_class, serve_fn):
        - config_class: The RuntimeConfig subclass with parser() static method
        - serve_fn: The serve() async function from the module

    Raises:
        ModuleNotFoundError: If the runtime module doesn't exist
        AttributeError: If required class/function is missing
    """
    module_path = f"reactor_runtime.runtimes.{runtime_name}.{runtime_name}_runtime"
    # Convert runtime_name to PascalCase + "RuntimeConfig"
    # (e.g., "headless" -> "HeadlessRuntimeConfig")
    pascal_name = re.sub(r"[-_]", "", runtime_name.title())
    config_class_name = f"{pascal_name}RuntimeConfig"

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f"Runtime '{runtime_name}' not found. " f"Expected module at: {module_path}"
        )

    if not hasattr(module, config_class_name):
        raise AttributeError(
            f"Config class '{config_class_name}' not found in " f"module {module_path}."
        )

    config_class = getattr(module, config_class_name)

    if not hasattr(config_class, "parser"):
        raise AttributeError(
            f"Config class '{config_class_name}' does not have a "
            "parser() static method."
        )

    if not hasattr(module, "serve"):
        raise AttributeError(f"Module {module_path} does not have a serve() function.")

    return config_class, module.serve
