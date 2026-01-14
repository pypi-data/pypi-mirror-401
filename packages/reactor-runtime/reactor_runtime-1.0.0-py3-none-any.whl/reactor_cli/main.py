import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog="reactor")
    subparsers = parser.add_subparsers(dest="command")

    # Import and register commands
    from .commands import (
        RunCommand,
        InitCommand,
        DownloadCommand,
        UploadCommand,
        SetupCommand,
        CapabilitiesCommand,
    )

    RunCommand.register_subcommand(subparsers)
    InitCommand.register_subcommand(subparsers)
    DownloadCommand.register_subcommand(subparsers)
    UploadCommand.register_subcommand(subparsers)
    SetupCommand.register_subcommand(subparsers)
    CapabilitiesCommand.register_subcommand(subparsers)

    # Use parse_known_args to allow runtime-specific args to pass through
    args, remaining = parser.parse_known_args()
    if hasattr(args, "func"):
        # Pass remaining args to commands that support them (like RunCommand)
        if args.func == RunCommand:
            command = args.func(args, remaining_args=remaining)
        else:
            if remaining:
                parser.error(f"Unrecognized arguments: {' '.join(remaining)}")
            command = args.func(args)
        command.run()
    else:
        parser.print_help()
        sys.exit(1)
