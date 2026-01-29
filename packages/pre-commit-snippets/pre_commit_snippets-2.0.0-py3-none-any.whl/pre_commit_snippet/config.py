"""
Configuration loading and validation.

This module handles loading the .pre-commit-snippets-config.yaml file and
validating its contents. It defines dataclasses for structured configuration
and provides a minimal YAML parser with no external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SnippetSource:
    """
    Configuration for a single snippet source repository.

    Attributes:
        repo: URL or path to the snippet repository.
        branch: Branch or tag to clone. Empty string for default branch.
        subdir: Subdirectory within the repo containing snippets.
        ext: File extension for snippet files (e.g., ".md").
    """

    repo: str
    branch: str = ""
    subdir: str = "."
    ext: str = ".md"


@dataclass
class Config:
    """
    Main configuration for the snippet hook.

    Attributes:
        sources: List of snippet source repositories.
        target_files: List of file paths (relative to repo root) to process.
    """

    sources: list[SnippetSource] = field(default_factory=list)
    target_files: list[str] = field(default_factory=list)

    @property
    def primary_source(self) -> SnippetSource | None:
        """
        Get the primary (first) snippet source.

        Returns:
            The first SnippetSource, or None if no sources are configured.
        """
        return self.sources[0] if self.sources else None


def load_yaml(path: Path) -> dict[str, str | list[str]]:
    """
    Parse the very simple flat YAML used for the config.

    Supports only flat key-value pairs and lists (using "- item" syntax).
    Does not handle nested structures, quoted strings with colons, or multiline values.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        A dictionary mapping keys to either string values or lists of strings.
    """
    data: dict[str, str | list[str]] = {}
    cur_key: str | None = None
    with path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line and not line.startswith("-"):
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "":
                    cur_key = key
                    data[cur_key] = []
                else:
                    data[key] = val
                    cur_key = None
            elif line.startswith("-") and cur_key is not None:
                cur_list = data[cur_key]
                if isinstance(cur_list, list):
                    cur_list.append(line.lstrip("-").strip())
    return data


def load_config(config_path: Path) -> Config:
    """
    Load and validate configuration from a YAML file.

    Args:
        config_path: Path to the configuration file.

    Returns:
        A validated Config object.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        ValueError: If required config keys are missing.
    """
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    cfg = load_yaml(config_path)

    # Build snippet sources
    sources: list[SnippetSource] = []

    # Primary source (legacy single-repo format)
    if "snippet_repo" in cfg:
        repo = cfg["snippet_repo"]
        if not isinstance(repo, str):
            raise ValueError("snippet_repo must be a string")

        branch = cfg.get("snippet_branch", "")
        if not isinstance(branch, str):
            branch = ""

        subdir = cfg.get("snippet_subdir", ".")
        if not isinstance(subdir, str):
            subdir = "."

        ext = cfg.get("snippet_ext", ".md")
        if not isinstance(ext, str):
            ext = ".md"

        sources.append(SnippetSource(repo=repo, branch=branch, subdir=subdir, ext=ext))

    if not sources:
        raise ValueError("Missing required config key: snippet_repo")

    # Target files
    target_files = cfg.get("target_files", [])
    if not isinstance(target_files, list):
        target_files = []

    return Config(sources=sources, target_files=target_files)
