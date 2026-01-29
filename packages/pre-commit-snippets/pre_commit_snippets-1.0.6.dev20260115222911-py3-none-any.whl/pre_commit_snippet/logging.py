"""
Logging configuration for pre-commit-snippets.

This module provides a centralized logger and configuration function for
the package. It supports three verbosity levels: WARNING (default),
INFO (--verbose), and DEBUG (--debug).
"""

from __future__ import annotations

import logging
import sys

# Create a dedicated logger for the package
logger = logging.getLogger("pre_commit_snippet")


def setup_logging(verbose: bool = False, debug: bool = False) -> None:
    """
    Configure logging for the application.

    Args:
        verbose: If True, set level to INFO.
        debug: If True, set level to DEBUG (overrides verbose).
    """
    if debug:
        level = logging.DEBUG
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    elif verbose:
        level = logging.INFO
        fmt = "%(message)s"
    else:
        level = logging.WARNING
        fmt = "%(message)s"

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt))

    logger.setLevel(level)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
