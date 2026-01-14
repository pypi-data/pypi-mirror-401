"""Version parsing and compatibility utilities."""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """Parse a version string into a tuple of integers for comparison.

    Args:
        version_str: Version string in format "x.y.z" (e.g., "1.0.0", "4.0.1")

    Returns:
        Tuple of (major, minor, patch) as integers

    Raises:
        ValueError: If version string is not in the expected format
    """
    if not version_str or not isinstance(version_str, str):
        raise ValueError(f"Version must be a non-empty string, got: {version_str}")

    parts = version_str.split(".")
    if len(parts) != 3:
        raise ValueError(
            f"Version must have exactly 3 parts (x.y.z), got: {version_str}"
        )

    try:
        major, minor, patch = map(int, parts)
        return (major, minor, patch)
    except ValueError:
        raise ValueError(f"Version parts must be integers, got: {version_str}")


def is_version_compatible(manifest_version_spec: str, runtime_version: str) -> bool:
    """Check if the runtime version satisfies the manifest version requirement.

    The manifest_version_spec can include comparison operators:
    - ">=1.0.0" - runtime must be greater than or equal to 1.0.0
    - ">1.0.0" - runtime must be greater than 1.0.0
    - "<=1.0.0" - runtime must be less than or equal to 1.0.0
    - "<1.0.0" - runtime must be less than 1.0.0
    - "==1.0.0" - runtime must be exactly 1.0.0
    - "1.0.0" - no operator defaults to ">=" (greater than or equal)

    Both the manifest version spec and runtime version must use 3-part versioning (x.y.z).

    Args:
        manifest_version_spec: Version requirement from manifest.json (e.g., ">=1.0.0", "1.0.0")
        runtime_version: Installed runtime version (e.g., "1.2.3")

    Returns:
        bool: True if versions are compatible, False otherwise
    """
    try:
        # Parse operator and version from manifest spec
        manifest_version_spec = manifest_version_spec.strip()

        # Check for operators
        operator = ">="  # default operator
        version_str = manifest_version_spec

        if manifest_version_spec.startswith(">="):
            operator = ">="
            version_str = manifest_version_spec[2:].strip()
        elif manifest_version_spec.startswith("<="):
            operator = "<="
            version_str = manifest_version_spec[2:].strip()
        elif manifest_version_spec.startswith("=="):
            operator = "=="
            version_str = manifest_version_spec[2:].strip()
        elif manifest_version_spec.startswith(">"):
            operator = ">"
            version_str = manifest_version_spec[1:].strip()
        elif manifest_version_spec.startswith("<"):
            operator = "<"
            version_str = manifest_version_spec[1:].strip()

        # Parse both versions (this will validate they are 3-part versions)
        manifest_version = parse_version(version_str)
        runtime_version_tuple = parse_version(runtime_version)

        # Compare based on operator
        if operator == ">=":
            return runtime_version_tuple >= manifest_version
        elif operator == ">":
            return runtime_version_tuple > manifest_version
        elif operator == "<=":
            return runtime_version_tuple <= manifest_version
        elif operator == "<":
            return runtime_version_tuple < manifest_version
        elif operator == "==":
            return runtime_version_tuple == manifest_version

        return False

    except ValueError as e:
        # If version parsing fails, return False
        logger.error(f"Version compatibility check failed: {e}")
        return False
    except Exception as e:
        # Handle any unexpected errors
        logger.error(f"Unexpected error in version compatibility check: {e}")
        return False
