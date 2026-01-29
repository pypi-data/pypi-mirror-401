"""
Pre-commit hook that syncs markdown snippets from a central repository.

This package provides a pre-commit hook that automatically replaces content
between `<!-- SNIPPET-START: name -->` and `<!-- SNIPPET-END -->` markers
with content from a central snippet repository.

Modules:
    cache: Hash computation and cache file management.
    cli: Command-line interface and main entry point.
    config: Configuration loading and validation.
    git: Git operations (clone, stage, etc.).
    logging: Logging configuration.
    snippet: Core snippet replacement logic.

Example:
    Run as a pre-commit hook::

        pre-commit-snippets --verbose

    Or import and use programmatically::

        from pre_commit_snippet import main
        exit_code = main()
"""

from pre_commit_snippet.cli import main

__all__ = ["main"]
__version__ = "0.1.0"
