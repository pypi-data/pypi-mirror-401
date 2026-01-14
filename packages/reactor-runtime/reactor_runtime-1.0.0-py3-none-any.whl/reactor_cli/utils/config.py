"""Model configuration utilities."""

from omegaconf import OmegaConf


def load_model_config(path, overrides):
    """Load a model config file and apply CLI overrides.

    Args:
        path: Path to the YAML config file
        overrides: List of dotlist override strings (e.g., ["key=value"])

    Returns:
        Merged OmegaConf DictConfig
    """
    cfg = OmegaConf.load(path)
    cli_cfg = OmegaConf.from_dotlist(overrides)
    return OmegaConf.merge(cfg, cli_cfg)


def print_model_config_help(config_path: str) -> None:
    """Print available model configuration options from a config file.

    Shows all keys in the config with their default values and how to override them.

    Args:
        config_path: Path to the model config file (YAML)
    """
    try:
        cfg = OmegaConf.load(config_path)
    except Exception as e:
        print(f"Error loading config file '{config_path}': {e}")
        return

    print(f"\nModel configuration options from: {config_path}")
    print("=" * 60)
    print("\nAvailable parameters (override with --model.<key>=<value>):\n")

    def _print_config(config, prefix=""):
        """Recursively print config keys with their values."""
        for key, value in config.items():
            full_key = f"{prefix}{key}" if prefix else key
            if OmegaConf.is_config(value):
                # Nested config - recurse
                _print_config(value, prefix=f"{full_key}.")
            else:
                value_type = type(value).__name__
                print(f"  --model.{full_key}={value}")
                print(f"      Type: {value_type}, Default: {value}\n")

    _print_config(cfg)
    print("=" * 60)
