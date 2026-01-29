"""
Command-line interface for pre-commit-snippet.

This module provides the main entry point and argument parsing for the
pre-commit hook. It orchestrates the overall flow: loading configuration,
cloning the snippet repository, processing target files, and staging changes.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from pre_commit_snippet.cache import load_cache, save_cache
from pre_commit_snippet.config import load_config
from pre_commit_snippet.git import (
    cleanup_temp_dir,
    clone_snippet_repo,
    get_repo_root,
    stage_files,
)
from pre_commit_snippet.logging import logger, setup_logging
from pre_commit_snippet.snippet import replace_blocks


def main() -> int:
    """
    Main entry point for the pre-commit hook.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = argparse.ArgumentParser(description="Sync markdown snippets from a central repository.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed information about processing.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information (implies --verbose).",
    )
    args = parser.parse_args()

    # Setup logging based on flags
    setup_logging(verbose=args.verbose, debug=args.debug)

    logger.debug("Starting pre-commit-snippet")
    logger.debug("Arguments: dry_run=%s, verbose=%s, debug=%s", args.dry_run, args.verbose, args.debug)

    # Get repo root
    try:
        repo_root = get_repo_root()
        logger.debug("Repository root: %s", repo_root)
    except subprocess.CalledProcessError:
        logger.error("Not in a git repository")
        return 1

    # Load configuration
    config_path = repo_root / "pre-commit-snippet-config.yaml"
    try:
        config = load_config(config_path)
        logger.debug("Loaded config from %s", config_path)
    except FileNotFoundError as e:
        logger.error("%s", e)
        return 1
    except ValueError as e:
        logger.error("%s", e)
        return 1

    if not config.target_files:
        logger.warning("No target_files specified in config; nothing to do.")
        return 0

    source = config.primary_source
    if source is None:
        logger.error("No snippet source configured")
        return 1

    logger.info("Snippet repo: %s", source.repo)
    if source.branch:
        logger.info("Branch/tag: %s", source.branch)
    logger.debug("Snippet subdir: %s", source.subdir)
    logger.debug("Snippet ext: %s", source.ext)
    logger.info("Target files: %s", ", ".join(config.target_files))

    # Clone the snippet repo
    tmp_dir = repo_root / ".git" / "hooks" / "tmp-snippets"
    try:
        snippet_root = clone_snippet_repo(source, tmp_dir)
    except subprocess.CalledProcessError:
        logger.error("Failed to clone snippet repository: %s", source.repo)
        cleanup_temp_dir(tmp_dir)
        return 1
    except FileNotFoundError as e:
        logger.error("%s", e)
        return 1

    # Load cache
    cache_file = repo_root / ".snippet-hashes.json"
    cache = load_cache(cache_file)
    logger.debug("Loaded cache with %d entries", len(cache))

    # Process each target file
    any_modified = False
    for rel in config.target_files:
        md_path = repo_root / rel
        if not md_path.is_file():
            logger.warning("Target file not found: %s", rel)
            continue
        logger.info("Processing %s", rel)
        if replace_blocks(
            md_path,
            repo_root,
            snippet_root,
            source.ext,
            cache,
            dry_run=args.dry_run,
        ):
            any_modified = True

    # Persist the cache
    if not args.dry_run:
        save_cache(cache_file, cache)
        logger.debug("Saved cache with %d entries", len(cache))

    # Cleanup temporary clone & stage modified files
    cleanup_temp_dir(tmp_dir)

    if any_modified and not args.dry_run:
        stage_files(config.target_files, repo_root)
        logger.info("Staged modified files")

    if args.dry_run and any_modified:
        logger.warning("Dry run complete. No files were modified.")
    elif not any_modified:
        logger.info("All snippets are up to date")

    logger.debug("Finished pre-commit-snippet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
