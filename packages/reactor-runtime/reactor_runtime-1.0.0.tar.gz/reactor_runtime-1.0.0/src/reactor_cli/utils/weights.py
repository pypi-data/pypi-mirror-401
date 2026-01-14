"""S3 weight downloading utilities."""

import asyncio
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional

import boto3
from filelock import FileLock, Timeout
from tqdm import tqdm

logger = logging.getLogger(__name__)


def _download_single_file(args):
    """
    Helper function to download a single file (used for parallel execution).

    Uses OS-level file locking (via filelock) to prevent concurrent downloads.
    When a process crashes, the OS automatically releases the lock.
    Downloads to .tmp file first, then renames atomically to prevent partial files.
    """
    bucket_name, key, target_dir, idx, total, lock_timeout, no_cache = args

    s3 = boto3.client("s3")
    local_path = target_dir / key
    lock_path = local_path.with_suffix(local_path.suffix + ".lock")
    temp_path = local_path.with_suffix(local_path.suffix + ".tmp")
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip already existing file unless no_cache is True
    if local_path.exists() and not no_cache:
        logger.info(f"[{idx}/{total}] Skipping {key} (already exists)")
        return True

    # If no_cache, remove existing file
    if no_cache and local_path.exists():
        local_path.unlink()

    try:
        # Use OS-level file lock - automatically released if process crashes
        with FileLock(str(lock_path), timeout=lock_timeout):
            # Check again after acquiring lock (another process may have finished)
            if local_path.exists() and not no_cache:
                logger.info(
                    f"[{idx}/{total}] Skipping {key} (downloaded by another process)"
                )
                return True

            # Clean up any leftover temp files from previous failed downloads
            if temp_path.exists():
                temp_path.unlink()

            # Get file size for progress bar
            try:
                response = s3.head_object(Bucket=bucket_name, Key=key)
                file_size = response["ContentLength"]
            except Exception:
                file_size = None

            # Download to temp file first, then atomic rename (prevents partial files)
            try:
                if file_size:
                    with tqdm(
                        total=file_size,
                        desc=f"[{idx}/{total}] {key}",
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                        position=idx - 1,
                        leave=True,
                    ) as pbar:
                        s3.download_file(
                            bucket_name,
                            key,
                            str(temp_path),
                            Callback=lambda bytes_transferred: pbar.update(
                                bytes_transferred
                            ),
                        )
                else:
                    # Fallback without size information
                    logger.info(f"[{idx}/{total}] Downloading {key}...")
                    s3.download_file(bucket_name, key, str(temp_path))

                # Atomic rename: file only visible after complete download
                temp_path.rename(local_path)
                return True

            except Exception as e:
                logger.error(f"[{idx}/{total}] Failed to download {key}: {e}")
                # Clean up partial download
                if temp_path.exists():
                    temp_path.unlink()
                return False

    except Timeout:
        logger.warning(f"[{idx}/{total}] Skipping {key}: timed out waiting for lock")
        return False
    finally:
        # Clean up lock file (filelock leaves it behind)
        if lock_path.exists():
            try:
                lock_path.unlink()
            except Exception:
                pass


def download_weights(
    pattern: str,
    lock_timeout: float = 120.0,
    no_cache: bool = False,
    max_workers: Optional[int] = None,
):
    """
    Process-safe S3 downloader with parallel downloads.

    Downloads all S3 objects matching a regex pattern from a bucket into:
            ~/.cache/reactor_registry/

    Uses OS-level file locks (via filelock) to avoid concurrent downloads.
    Downloads to .tmp files first, then renames atomically to prevent partial files.

    Args:
            pattern: Regex pattern to match S3 keys
            lock_timeout: Maximum time to wait for lock acquisition (default 2 minutes)
            no_cache: If True, force re-download all files
            max_workers: Maximum number of parallel download threads (defaults to min(10, len(files)))
    """
    bucket_name = "reactor-models"

    regex = re.compile(pattern)
    s3 = boto3.client("s3")

    target_dir = Path.home() / ".cache" / "reactor_registry"
    target_dir.mkdir(parents=True, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name)

    matching_keys = []
    for page in page_iterator:
        if "Contents" in page:
            for obj in page["Contents"]:
                key = obj["Key"]
                if regex.search(key):
                    matching_keys.append(key)

    if not matching_keys:
        logger.info("No files matched the provided pattern.")
        return target_dir  # still return cache base for consistency

    logger.info(
        f"Found {len(matching_keys)} matching files. " "Starting parallel download..."
    )

    # Determine number of workers
    if max_workers is None:
        max_workers = min(10, len(matching_keys))

    # Prepare arguments for parallel execution
    download_args = [
        (bucket_name, key, target_dir, idx, len(matching_keys), lock_timeout, no_cache)
        for idx, key in enumerate(matching_keys, 1)
    ]

    # Download files in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_download_single_file, download_args))

    successful = sum(1 for r in results if r)
    logger.info(
        f"Download complete. {successful}/{len(matching_keys)} files "
        f"downloaded successfully. Files saved to: {target_dir}"
    )
    return target_dir


def get_weights(
    folder_name: str, no_cache: bool = False, max_workers: Optional[int] = None
) -> Path:
    """
    Fetches all weights for a given top-level folder.

    Example:
            get_weights("longlive")
    → Downloads all S3 objects matching "longlive/.*"
      and returns: ~/.cache/reactor_registry/longlive/

    If the folder already exists locally, returns it directly without downloading.

    Args:
            folder_name: Name of the top-level folder to download
            no_cache: If True, force re-download even if folder exists
            max_workers: Maximum number of parallel download threads
    """
    if not folder_name or not re.match(r"^[a-zA-Z0-9_\-]+$", folder_name):
        raise ValueError(
            "Folder name must be a single-level name (no slashes, only "
            "letters, numbers, underscores, or hyphens)."
        )

    # Check if folder already exists (skip check if no_cache)
    cache_dir = Path.home() / ".cache" / "reactor_registry"
    folder_path = cache_dir / folder_name

    if not no_cache and folder_path.exists() and folder_path.is_dir():
        logger.debug(
            f"Folder '{folder_name}' already exists at {folder_path}, "
            "skipping download."
        )
        return folder_path

    # Build regex for keys like: longlive/...
    pattern = rf"^{re.escape(folder_name)}/.*"

    if no_cache:
        logger.info(
            f"Force fetching weights for folder '{folder_name}' " "(no_cache=True)..."
        )
    else:
        logger.info(f"Fetching weights for folder '{folder_name}'...")

    cache_dir = download_weights(pattern, no_cache=no_cache, max_workers=max_workers)

    return cache_dir / folder_name


def get_weights_parallel(
    folder_names: List[str], max_workers: Optional[int] = None, no_cache: bool = False
) -> List[Optional[Path]]:
    """
    Fetches weights for multiple folders in parallel using threads.

    Args:
            folder_names: List of folder names to fetch weights for
            max_workers: Maximum number of worker threads (defaults to min(32, len(folder_names) + 4))
            no_cache: If True, force re-download all weights

    Returns:
            List of Path objects corresponding to each folder name, or None if the download failed
    """
    if not folder_names:
        return []

    if max_workers is None:
        max_workers = min(32, len(folder_names) + 4)

    results: List[Optional[Path]] = [None] * len(folder_names)

    # Create progress bars for each folder
    progress_bars = {}
    for i, folder_name in enumerate(folder_names):
        progress_bars[i] = tqdm(
            total=100,
            desc=f"[{i+1}/{len(folder_names)}] {folder_name}",
            position=i,
            leave=True,
            unit="%",
        )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {}
        for i, folder_name in enumerate(folder_names):
            future = executor.submit(get_weights, folder_name, no_cache)
            future_to_index[future] = i

        # Collect results as they complete
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                results[index] = result
                progress_bars[index].update(100 - progress_bars[index].n)
                progress_bars[index].set_description(
                    f"[{index+1}/{len(folder_names)}] {folder_names[index]} ✓"
                )
                logger.info(f"Successfully fetched weights for '{folder_names[index]}'")
            except Exception as e:
                progress_bars[index].set_description(
                    f"[{index+1}/{len(folder_names)}] {folder_names[index]} ✗"
                )
                progress_bars[index].update(100 - progress_bars[index].n)
                logger.error(
                    f"Failed to fetch weights for '{folder_names[index]}': {e}"
                )
                results[index] = None

    # Close all progress bars
    for pbar in progress_bars.values():
        pbar.close()

    return results


async def get_weights_parallel_async(
    folder_names: List[str], max_workers: Optional[int] = None, no_cache: bool = False
) -> List[Optional[Path]]:
    """
    Async wrapper for get_weights_parallel that runs on a separate thread to avoid blocking.

    Args:
            folder_names: List of folder names to fetch weights for
            max_workers: Maximum number of worker threads for the parallel downloads
            no_cache: If True, force re-download all weights

    Returns:
            List of Path objects corresponding to each folder name, or None if the download failed
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: get_weights_parallel(folder_names, max_workers, no_cache)
    )
