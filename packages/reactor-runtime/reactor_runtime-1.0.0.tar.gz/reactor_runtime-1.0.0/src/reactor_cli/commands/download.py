"""Download command implementation."""

import os
import json
import logging
from typing import List, Optional
from pathlib import Path
from supabase import create_client
from reactor_cli.utils.weights import get_weights_parallel
from reactor_cli.utils.discovery import discover_model

# Set up logger
logger = logging.getLogger(__name__)


def parse_manifest(manifest_str: str) -> dict:
    """Parse a manifest string into a dictionary.

    Args:
        manifest_str: JSON string containing the manifest

    Returns:
        Parsed manifest dictionary
    """
    try:
        return json.loads(manifest_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse manifest JSON: {e}")
        raise ValueError(f"Invalid manifest JSON: {e}")


def get_weights_from_manifest(manifest: dict) -> List[str]:
    """Extract the weights list from a manifest dictionary.

    Args:
        manifest: Dictionary containing manifest data

    Returns:
        List of weight folder names
    """
    if "weights" not in manifest:
        logger.warning("Manifest does not contain a 'weights' field")
        return []

    weights = manifest["weights"]
    if not isinstance(weights, list):
        logger.error(f"'weights' field must be a list, got {type(weights)}")
        raise ValueError("'weights' field in manifest must be a list")

    return weights


def get_weights_from_local_model(model_path: Optional[Path] = None) -> List[str]:
    """Read weights from local @model decorator.

    Discovers the model via @model decorator and returns its weights list.

    Args:
        model_path: Path to model directory (default: current directory)

    Returns:
        List of weight folder names from @model decorator
    """
    if model_path is None:
        model_path = Path.cwd()

    try:
        model_info = discover_model(model_path)
    except RuntimeError as e:
        raise RuntimeError(f"Failed to discover model: {e}")

    weights = model_info.get("weights", [])
    if not isinstance(weights, list):
        logger.error(f"'weights' field must be a list, got {type(weights)}")
        raise ValueError("'weights' in @model decorator must be a list")

    return weights


def get_weights_from_model_id(model_id: str) -> List[str]:
    """Fetch model manifest from Supabase and extract weights.

    Args:
        model_id: Model identifier (e.g., "matrix-2")

    Returns:
        List of weight folder names from the model's manifest
    """
    model_name = model_id

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables must be set"
        )
    supabase = create_client(supabase_url, supabase_key)

    logger.info(f"Fetching manifest for model '{model_name}'...")

    result = (
        supabase.table("models").select("manifest").eq("model_id", model_name).execute()
    )

    if not result.data:
        raise ValueError(f"Model '{model_name}' not found in database")

    manifest = result.data[0]["manifest"]

    if not manifest:
        raise ValueError(f"Model '{model_name}' doesn't have a manifest in database.")

    return get_weights_from_manifest(manifest)


def get_weights_from_model_ids(model_ids: List[str]) -> List[str]:
    """Fetch manifests for multiple models and extract unique weights.

    Args:
        model_ids: List of model identifiers (e.g., ["matrix-2", "longlive", "mk64"])

    Returns:
        Deduplicated list of weight folder names from all models
    """
    all_weights = set()

    for model_id in model_ids:
        try:
            weights = get_weights_from_model_id(model_id)
            all_weights.update(weights)
            logger.info(f"Model '{model_id}' requires weights: {weights}")
        except Exception as e:
            logger.error(f"Failed to fetch weights for model '{model_id}': {e}")
            raise

    unique_weights = list(all_weights)
    logger.info(f"Total unique weights across all models: {unique_weights}")
    return unique_weights


class DownloadCommand:
    @staticmethod
    def register_subcommand(subparsers):
        """Register download command"""
        download_parser = subparsers.add_parser(
            "download", help="Download model weights"
        )
        download_parser.add_argument(
            "--path",
            "-p",
            type=str,
            default=None,
            help="Path to model directory (default: current directory)",
        )
        download_parser.add_argument(
            "--weights", nargs="+", help="List of weight folder names to download"
        )
        download_parser.add_argument(
            "--models",
            nargs="+",
            help="List of model identifiers to fetch weights from (e.g., matrix-2 longlive mk64)",
        )
        download_parser.add_argument(
            "--no-cache",
            action="store_true",
            help="Force re-download even if weights exist locally",
        )
        download_parser.set_defaults(func=DownloadCommand)

    def __init__(self, args):
        """Initialize command with parsed arguments"""
        self.args = args

    def run(self):
        """Download model weights from registry"""
        try:
            # Determine which route to take based on arguments
            weights_list: Optional[List[str]] = None

            if self.args.weights:
                # Route 1: Explicit weights list provided
                weights_list = self.args.weights
                logger.info(f"Downloading specified weights: {weights_list}")

            elif self.args.models:
                # Route 2: Fetch from model IDs in Supabase and deduplicate
                print(f"Fetching manifests for {len(self.args.models)} model(s)...")
                weights_list = get_weights_from_model_ids(self.args.models)
                print(f"Found {len(weights_list)} unique weight(s) across all models")
                logger.info(
                    f"Downloaded manifests for models {self.args.models}, unique weights: {weights_list}"
                )

            else:
                # Route 3: Default - read from local @model decorator
                model_path = (
                    Path(self.args.path).resolve() if self.args.path else Path.cwd()
                )
                logger.info(
                    "No arguments specified, discovering model via @model decorator..."
                )
                weights_list = get_weights_from_local_model(model_path)
                logger.info(f"Found weights in @model decorator: {weights_list}")

            if not weights_list:
                print("No weights to download.")
                return

            # Download weights in parallel
            if self.args.no_cache:
                print(
                    f"Force downloading {len(weights_list)} weight folder(s) (no-cache mode)..."
                )
            else:
                print(f"Downloading {len(weights_list)} weight folder(s)...")
            weight_paths = get_weights_parallel(
                weights_list, no_cache=self.args.no_cache
            )

            # Print results
            print("\nDownload complete! Weight paths:")
            for i, (weight_name, weight_path) in enumerate(
                zip(weights_list, weight_paths), 1
            ):
                if weight_path:
                    print(f"  {i}. {weight_name}: {weight_path}")
                else:
                    print(f"  {i}. {weight_name}: FAILED")

        except Exception as e:
            logger.error(f"Download command failed: {e}")
            print(f"Error: {e}")
            return
