"""
Cache handling for snippet hashes.

This module provides functions for computing content hashes and managing
the cache file that tracks which snippets have been applied to which files.
The cache prevents unnecessary file rewrites when snippets haven't changed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def compute_hash(text: str) -> str:
    """
    Return a deterministic SHA-256 hex digest for a Unicode string.

    Args:
        text: The string to hash.

    Returns:
        A 64-character lowercase hexadecimal SHA-256 digest.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_cache(cache_file: Path) -> dict[str, str]:
    """
    Load the JSON cache from disk.

    Args:
        cache_file: Path to the cache file.

    Returns:
        A dictionary mapping cache keys to hash values.
        Returns an empty dict if the file does not exist or is corrupt.
    """
    if not cache_file.is_file():
        return {}
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return dict(data)
        return {}
    except Exception:
        return {}


def save_cache(cache_file: Path, cache: dict[str, str]) -> None:
    """
    Write the cache to disk atomically.

    Uses a temporary file and rename to avoid corruption on crash.

    Args:
        cache_file: Path to the cache file.
        cache: A dictionary mapping cache keys to hash values.
    """
    tmp = cache_file.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(cache_file)
