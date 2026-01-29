"""
Git-related utilities.

This module provides functions for interacting with git repositories,
including running git commands, cloning snippet repositories, and staging
modified files for commit.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from pre_commit_snippet.config import SnippetSource
from pre_commit_snippet.logging import logger


def run_cmd(args: list[str], cwd: Path | None = None, check: bool = True) -> str:
    """
    Run a shell command and return its stdout, stripped of whitespace.

    Args:
        args: Command and arguments as a list of strings.
        cwd: Working directory for the command. Defaults to current directory.
        check: If True, raise CalledProcessError on non-zero exit. Defaults to True.

    Returns:
        The command's stdout with leading/trailing whitespace removed.

    Raises:
        subprocess.CalledProcessError: If check is True and the command fails.
    """
    logger.debug("Running command: %s", " ".join(args))
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
        )
        if result.stdout.strip():
            logger.debug("stdout: %s", result.stdout.strip())
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error("Command failed: %s", " ".join(args))
        if e.stderr:
            logger.error("  %s", e.stderr.strip())
        raise


def get_repo_root() -> Path:
    """
    Get the root directory of the current git repository.

    Returns:
        Path to the repository root.

    Raises:
        subprocess.CalledProcessError: If not in a git repository.
    """
    return Path(run_cmd(["git", "rev-parse", "--show-toplevel"]))


def clone_snippet_repo(source: SnippetSource, dest: Path) -> Path:
    """
    Clone a snippet repository to a destination directory.

    Args:
        source: The snippet source configuration.
        dest: Destination directory for the clone.

    Returns:
        Path to the snippet root (dest / subdir).

    Raises:
        subprocess.CalledProcessError: If the clone fails.
        FileNotFoundError: If the snippet subdirectory doesn't exist.
    """
    if dest.exists():
        logger.debug("Removing existing temp directory: %s", dest)
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    clone_args = ["git", "clone", "--depth", "1"]
    if source.branch:
        clone_args.extend(["--branch", source.branch])
    clone_args.extend([source.repo, str(dest)])

    logger.debug("Cloning snippet repo: %s", source.repo)
    run_cmd(clone_args)

    snippet_root = dest / source.subdir
    if not snippet_root.is_dir():
        shutil.rmtree(dest, ignore_errors=True)
        raise FileNotFoundError(f"Snippet subdirectory not found: {source.subdir}")

    logger.debug("Snippet root: %s", snippet_root)
    return snippet_root


def cleanup_temp_dir(tmp_dir: Path) -> None:
    """
    Remove a temporary directory.

    Args:
        tmp_dir: The directory to remove.
    """
    logger.debug("Cleaning up temp directory: %s", tmp_dir)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def stage_files(files: list[str], repo_root: Path) -> None:
    """
    Stage files for commit.

    Args:
        files: List of file paths relative to repo root.
        repo_root: Root of the git repository.
    """
    logger.debug("Staging files: %s", ", ".join(files))
    run_cmd(["git", "add"] + files, cwd=repo_root)
