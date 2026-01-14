"""Capabilities command implementation."""

import json
from pathlib import Path
from reactor_cli.utils.discovery import discover_model


class CapabilitiesCommand:
    @staticmethod
    def register_subcommand(subparsers):
        """Register capabilities command"""
        run_parser = subparsers.add_parser(
            "capabilities", help="Print the capabilities of a reactor VideoModel."
        )
        run_parser.add_argument(
            "--path",
            "-p",
            type=str,
            default=None,
            help="Path to model directory (default: current directory)",
        )
        run_parser.set_defaults(func=CapabilitiesCommand)

    def __init__(self, args):
        """Initialize with parsed arguments"""
        self.args = args

    def run(self):
        """Print the capabilities of a reactor VideoModel."""
        model_path = Path(self.args.path).resolve() if self.args.path else Path.cwd()

        # Discover model via @model decorator
        try:
            model_info = discover_model(model_path)
        except RuntimeError as e:
            print(f"Error: {e}")
            return

        model_name = model_info["name"]
        model_class = model_info["class"]

        # Get static command schema directly from the class (no instance needed)
        try:
            capabilities = model_class.commands()
        except Exception as e:
            print(f"Error extracting capabilities: {e}")
            return

        print(f"Model: {model_name}")
        print(json.dumps(capabilities, indent=4))
