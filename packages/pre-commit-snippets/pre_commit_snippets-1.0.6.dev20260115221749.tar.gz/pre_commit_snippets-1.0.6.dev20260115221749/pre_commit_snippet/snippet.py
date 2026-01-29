"""
Core snippet replacement logic.

This module contains the main logic for finding and replacing snippet blocks
in markdown files. It handles parsing SNIPPET-START/SNIPPET-END markers,
comparing hashes to detect changes, and updating file contents.
"""

from __future__ import annotations

import re
from pathlib import Path

from pre_commit_snippet.cache import compute_hash
from pre_commit_snippet.logging import logger

# Regexes for the block markers
START_RE = re.compile(r"<!--\s*SNIPPET-START:\s*(?P<name>[^>]+?)\s*-->")
END_RE = re.compile(r"<!--\s*SNIPPET-END\s*-->")


def replace_blocks(
    md_path: Path,
    repo_root: Path,
    snippet_root: Path,
    snippet_ext: str,
    cache: dict[str, str],
    dry_run: bool = False,
) -> bool:
    """
    Process a markdown file and replace snippet blocks with central repo content.

    Walks the file, finds each SNIPPET-START/SNIPPET-END pair, and rewrites the
    block only when the cached hash differs from the authoritative snippet hash.

    Args:
        md_path: Path to the markdown file to process.
        repo_root: Root of the git repository.
        snippet_root: Root directory of the cloned snippet repo.
        snippet_ext: File extension for snippet files.
        cache: Mutable cache dictionary to update.
        dry_run: If True, don't write changes to disk.

    Returns:
        True if the file was (or would be) modified, False otherwise.
    """
    logger.debug("Processing file: %s", md_path)
    original = md_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    out: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        start_match = START_RE.search(lines[i])
        if start_match:
            snippet_name = start_match.group("name").strip()
            logger.debug("Found snippet marker: %s at line %d", snippet_name, i + 1)

            # locate the matching END marker
            j = i + 1
            while j < len(lines) and not END_RE.search(lines[j]):
                j += 1
            if j >= len(lines):
                logger.warning("Missing SNIPPET-END after line %d in %s", i + 1, md_path)
                out.append(lines[i])
                i += 1
                continue

            # ----- Existing block hash (cached or compute) -----
            existing_block = "".join(lines[i + 1 : j]).rstrip("\n")
            cache_key = f"{md_path.relative_to(repo_root)}::{snippet_name}"
            cached_hash = cache.get(cache_key)

            if cached_hash is None:
                existing_hash = compute_hash(existing_block)
                cache[cache_key] = existing_hash
                cached_hash = existing_hash
                logger.debug("Computed hash for existing block: %s", cached_hash[:12])

            # ----- Authoritative snippet hash -----
            snippet_path = snippet_root / f"{snippet_name}{snippet_ext}"
            if not snippet_path.is_file():
                logger.warning("Snippet not found: %s%s", snippet_name, snippet_ext)
                out.extend(lines[i : j + 1])
                i = j + 1
                continue

            snippet_body = snippet_path.read_text(encoding="utf-8").rstrip("\n")
            snippet_hash = compute_hash(snippet_body)
            logger.debug("Snippet hash: %s", snippet_hash[:12])

            # ----- Decide whether to rewrite -----
            if cached_hash != snippet_hash:
                logger.info("Updating snippet '%s' in %s", snippet_name, md_path.name)
                logger.debug(
                    "Hash mismatch: cached=%s, snippet=%s",
                    cached_hash[:12],
                    snippet_hash[:12],
                )
                out.append(f"<!-- SNIPPET-START: {snippet_name} -->\n")
                out.append(snippet_body + "\n")
                out.append("<!-- SNIPPET-END -->\n")
                changed = True
                cache[cache_key] = snippet_hash
            else:
                logger.debug("Snippet '%s' is up to date", snippet_name)
                out.extend(lines[i : j + 1])

            i = j + 1
        else:
            out.append(lines[i])
            i += 1

    if changed and not dry_run:
        logger.debug("Writing updated file: %s", md_path)
        md_path.write_text("".join(out), encoding="utf-8")
    elif changed and dry_run:
        logger.info("Would update: %s", md_path.name)

    return changed
