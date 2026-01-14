"""Upload command implementation."""

import logging
import os
import sys
from pathlib import Path

from reactor_cli.utils.discovery import discover_model, get_model_spec
from supabase import create_client

logger = logging.getLogger(__name__)


class UploadCommand:
    @staticmethod
    def register_subcommand(subparsers):
        """Register upload command"""
        upload_parser = subparsers.add_parser("upload", help="Upload model to Supabase")
        upload_parser.add_argument(
            "--path",
            "-p",
            type=str,
            default=None,
            help="Path to model directory (default: current directory)",
        )
        upload_parser.set_defaults(func=UploadCommand)

    def __init__(self, args):
        """Initialize command with parsed arguments"""
        self.args = args

    def run(self):
        """Upload model information to Supabase"""
        model_path = Path(self.args.path).resolve() if self.args.path else Path.cwd()

        # Discover model via @model decorator
        try:
            model_info = discover_model(model_path)
        except RuntimeError as e:
            logger.error(f"Error: {e}")
            sys.exit(1)

        model_name = model_info["name"]
        model_class = model_info["class"]

        logger.info(f"Uploading model: {model_name}")

        # Get static command schema directly from the class (no instance needed)
        logger.info("Extracting model capabilities...")
        try:
            capabilities = model_class.commands()
        except Exception as e:
            logger.error(f"Error extracting capabilities: {e}")
            sys.exit(1)

        # Get Supabase credentials from environment
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

        if not supabase_url or not supabase_key:
            logger.error("Missing Supabase credentials in environment.")
            logger.error(
                "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables."
            )
            sys.exit(1)

        # Connect to Supabase
        logger.info("Connecting to Supabase...")
        supabase = create_client(supabase_url, supabase_key)

        # Prepare data for insertion
        data = {
            "model_id": model_name,
            "class": get_model_spec(model_info),
            "weights": model_info.get("weights", []),
            "config": model_info.get("config"),
            "capabilities": capabilities,
        }

        # Check if model with same name already exists
        logger.info("Checking for existing model...")
        try:
            existing = (
                supabase.table("models")
                .select("id")
                .eq("model_id", model_name)
                .execute()
            )

            if existing.data:
                # Model exists, update it
                existing_id = existing.data[0]["id"]
                logger.info(
                    f"Model '{model_name}' already exists (ID: {existing_id}). Updating..."
                )

                response = (
                    supabase.table("models")
                    .update(data)
                    .eq("id", existing_id)
                    .execute()
                )
                logger.info(f"✓ Successfully updated model '{model_name}' in Supabase!")
                logger.info(f"Record ID: {existing_id}")
            else:
                # Model doesn't exist, insert new
                logger.info(f"Creating new record for model '{model_name}'...")
                response = supabase.table("models").insert(data).execute()
                logger.info(
                    f"✓ Successfully uploaded model '{model_name}' to Supabase!"
                )
                logger.info(
                    f"Record ID: {response.data[0]['id'] if response.data else 'N/A'}"
                )

        except Exception as e:
            logger.error(f"Error uploading to Supabase: {e}")
            sys.exit(1)
