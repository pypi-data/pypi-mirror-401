from importlib.metadata import version, PackageNotFoundError

from reactor_runtime.model_api import VideoModel, command, model
from reactor_runtime.context_api import get_ctx

try:
    __version__ = version("reactor_runtime")
except PackageNotFoundError:
    __version__ = "0.0.0.dev"  # Development/test mode

__all__ = ["VideoModel", "command", "model", "get_ctx", "__version__"]
