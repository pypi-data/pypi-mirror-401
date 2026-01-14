"""Run command implementation."""

from pathlib import Path
from omegaconf import DictConfig, OmegaConf
from reactor_cli.utils.config import load_model_config, print_model_config_help
from reactor_cli.utils.runtime import load_runtime
from reactor_cli.utils.discovery import discover_model, get_model_spec
from reactor_runtime.utils.launch import run_reactor_runtime_sync
import logging

logger = logging.getLogger(__name__)


class RunCommand:
    @staticmethod
    def register_subcommand(subparsers):
        """Register run command with basic args. Runtime-specific args are parsed later."""
        run_parser = subparsers.add_parser(
            "run",
            help="Run reactor runtime with @model decorated VideoModel",
            # Allow unknown args to be passed to runtime-specific parser
            add_help=False,
        )
        run_parser.add_argument(
            "--path",
            "-p",
            type=str,
            default=None,
            help="Path to model directory (default: current directory)",
        )
        run_parser.add_argument(
            "--runtime",
            type=str,
            default="headless",
            help="Runtime to use (e.g., 'headless'). Loads from reactor_runtime.runtimes.<name>.<name>_runtime. Default: headless",
        )
        run_parser.add_argument(
            "--config",
            "-c",
            type=str,
            default=None,
            help="Path to model config file to use.",
        )
        run_parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enable verbose (DEBUG) logging",
        )
        run_parser.add_argument(
            "-h",
            "--help",
            action="store_true",
            help="Show help message (includes runtime-specific options)",
        )
        run_parser.add_argument(
            "--config-help",
            action="store_true",
            help="Show available model config options (requires --model-config)",
        )
        run_parser.set_defaults(func=RunCommand)

    def __init__(self, args, remaining_args=None):
        """Initialize with parsed arguments"""
        self.args = args
        self.remaining_args = remaining_args or []

    def run(self):
        """Run the reactor runtime with the model discovered via @model decorator."""

        # Handle --model-help flag
        if self.args.config_help:
            if not self.args.config:
                print("Error: --config-help requires --config to be specified.")
                print("Usage: reactor run --config <config.yml> --config-help")
                return
            print_model_config_help(self.args.config)
            return

        runtime_name = self.args.runtime

        # =====================================================================
        # Dynamic Runtime Loading
        # =====================================================================
        # We dynamically load the runtime's config class and serve function based
        # on the --runtime flag (e.g., "headless", "http"). This allows:
        #
        # 1. Extensibility: New runtimes can be added without modifying this CLI code.
        #    Just create a new module at reactor_runtime.runtimes.<name>.<name>_runtime
        #    with a <Name>RuntimeConfig class and serve() function.
        #
        # 2. Lazy imports: Runtime dependencies (e.g., aiortc for HTTP runtime) are
        #    only imported when that specific runtime is selected, avoiding unnecessary
        #    dependency requirements for users who only need certain runtimes.
        #
        # 3. Runtime-specific CLI args: Each runtime's config class defines its own
        #    parser() method, so the CLI can dynamically show the correct --help
        #    options based on which runtime is selected.
        # =====================================================================
        try:
            config_class, serve_fn = load_runtime(runtime_name)
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error: {e}")
            return

        # Each runtime config class provides a parser() static method that returns
        # an ArgumentParser with runtime-specific options (e.g., --port for HTTP,
        # --output-root for headless). This enables runtime-specific help messages.
        runtime_parser = config_class.parser()

        # If help requested, show combined help
        if self.args.help:
            print(
                "Usage: reactor run [--path DIR] [--runtime NAME] [-v/--verbose] [runtime options]"
            )
            print("\nBase options:")
            print(
                "  --path, -p DIR     Path to model directory (default: current directory)"
            )
            print("  --runtime NAME     Runtime to use (default: headless)")
            print("  -v, --verbose      Enable verbose (DEBUG) logging")
            print(f"\nRuntime-specific options for '{runtime_name}':")
            runtime_parser.print_help()
            return

        # Parse runtime-specific arguments from remaining CLI args
        # Use parse_known_args to allow --model.* args to pass through
        runtime_args, extra_args = runtime_parser.parse_known_args(self.remaining_args)
        runtime_kwargs = vars(runtime_args)

        # =====================================================================
        # Model Discovery via @model Decorator
        # =====================================================================
        # Instead of reading manifest.json, we discover the model by importing
        # Python modules in the specified directory (or cwd). When a module
        # containing a @model decorated VideoModel class is imported, the
        # decorator registers it in MODEL_REGISTRY. This enables:
        #
        # 1. No manifest files: Model metadata is defined inline with the code
        # 2. Explicit opt-in: Only @model decorated classes are discovered
        # 3. Python-native: Familiar pattern used by pytest, FastAPI, etc.
        # =====================================================================
        model_path = Path(self.args.path).resolve() if self.args.path else Path.cwd()

        if not model_path.exists():
            print(f"Error: Model path does not exist: {model_path}")
            return
        if not model_path.is_dir():
            print(f"Error: Model path is not a directory: {model_path}")
            return

        try:
            model_info = discover_model(model_path)
        except RuntimeError as e:
            print(f"Error: {e}")
            return

        model_spec = get_model_spec(model_info)
        model_name = model_info["name"]
        model_config_path = model_info.get("config")

        # Extract model overrides from --model.* args
        model_overrides = []
        for arg in extra_args:
            if arg.startswith("--model."):
                model_overrides.append(arg.replace("--model.", ""))

        # Build config: CLI --config takes priority, then decorator config, then empty
        cfg: DictConfig = OmegaConf.create({})
        if self.args.config:
            # CLI --config takes highest priority for path from where to load the model.
            # CLI overrides are still applied on top of the config.
            cfg = load_model_config(self.args.config, model_overrides)
            logger.info(
                f"Loaded model config from CLI specified path: {self.args.config}"
            )
        elif model_config_path:
            # Resolve config path relative to model directory if not absolute
            if not Path(model_config_path).is_absolute():
                model_config_path = str(model_path / model_config_path)
            # Config from @model decorator is used if no CLI --config specified
            # CLI overrides are still applied on top of the config.
            cfg = load_model_config(model_config_path, model_overrides)
            logger.info(
                f"Loaded model config from @model decorator: {model_config_path}"
            )
        elif model_overrides:
            # No config file but have CLI overrides - create config from overrides only
            cfg = OmegaConf.from_dotlist(model_overrides)
            logger.info("Loaded model config from CLI only")

        print(f"Starting reactor runtime ({runtime_name})...")
        print(f"Model: {model_name} ({model_spec})")
        if cfg:
            print(f"Model config: {cfg}")

        # Convert verbose flag to log level
        log_level = "DEBUG" if self.args.verbose else "INFO"

        try:
            # The dynamically loaded serve_fn handles constructing the runtime config
            # and runtime instance internally. We pass it the model info from the
            # @model decorator plus any runtime-specific kwargs parsed from the CLI.
            run_reactor_runtime_sync(
                runtime_serve_fn=serve_fn,
                model=model_spec,
                model_config=cfg,
                model_root=str(model_path),
                log_level=log_level,
                model_name=model_name,
                **runtime_kwargs,
            )

        except KeyboardInterrupt:
            print("\nReactor runtime stopped by user.")
        except Exception as e:
            print(f"Error running reactor runtime: {e}")
            raise
