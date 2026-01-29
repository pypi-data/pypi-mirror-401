#!/usr/bin/env python3
"""Tests for pre-commit-snippet hook."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def git_cmd(args: list[str], cwd: Path) -> None:
    """Run a git command with GPG signing disabled."""
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def git_init(repo: Path) -> None:
    """Initialize a git repo with test config and GPG signing disabled."""
    git_cmd(["git", "init"], repo)
    git_cmd(["git", "config", "user.email", "test@test.com"], repo)
    git_cmd(["git", "config", "user.name", "Test"], repo)
    git_cmd(["git", "config", "commit.gpgsign", "false"], repo)


@pytest.fixture
def snippet_repo(tmp_path: Path) -> Path:
    """Create a temporary snippet repository."""
    repo = tmp_path / "snippets"
    repo.mkdir()

    git_init(repo)

    (repo / "greeting.md").write_text("Hello from snippet repo!\n")
    (repo / "footer.md").write_text("---\nThis is the footer.\n")

    git_cmd(["git", "add", "."], repo)
    git_cmd(["git", "commit", "-m", "Add snippets"], repo)

    return repo


@pytest.fixture
def target_repo(tmp_path: Path, snippet_repo: Path) -> Path:
    """Create a temporary target repository with config."""
    repo = tmp_path / "target"
    repo.mkdir()

    git_init(repo)

    config = f"""snippet_repo: {snippet_repo}
target_files:
  - README.md
  - docs/guide.md
"""
    (repo / "pre-commit-snippet-config.yaml").write_text(config)

    readme = """# Project

<!-- SNIPPET-START: greeting -->
old content here
<!-- SNIPPET-END -->

Some other text.
"""
    (repo / "README.md").write_text(readme)

    docs = repo / "docs"
    docs.mkdir()
    guide = """# Guide

<!-- SNIPPET-START: footer -->
placeholder
<!-- SNIPPET-END -->
"""
    (docs / "guide.md").write_text(guide)

    git_cmd(["git", "add", "."], repo)
    git_cmd(["git", "commit", "-m", "Initial commit"], repo)

    return repo


def get_main_script() -> Path:
    """Get the path to main.py."""
    return Path(__file__).parent.parent / "main.py"


def test_replaces_snippet_content(target_repo: Path) -> None:
    """Test that snippets are replaced with content from snippet repo."""
    result = subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Hook failed: {result.stderr}"

    readme = (target_repo / "README.md").read_text()
    assert "Hello from snippet repo!" in readme
    assert "old content here" not in readme


def test_replaces_multiple_files(target_repo: Path) -> None:
    """Test that multiple target files are processed."""
    subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        check=True,
        capture_output=True,
    )

    guide = (target_repo / "docs" / "guide.md").read_text()
    assert "This is the footer." in guide
    assert "placeholder" not in guide


def test_creates_cache_file(target_repo: Path) -> None:
    """Test that the cache file is created."""
    subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        check=True,
        capture_output=True,
    )

    cache_file = target_repo / ".snippet-hashes.json"
    assert cache_file.exists()


def test_no_rewrite_when_unchanged(target_repo: Path) -> None:
    """Test that files are not rewritten when snippets haven't changed."""
    subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        check=True,
        capture_output=True,
    )

    readme = target_repo / "README.md"
    mtime1 = readme.stat().st_mtime

    subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        check=True,
        capture_output=True,
    )

    mtime2 = readme.stat().st_mtime
    assert mtime1 == mtime2, "File was rewritten when it shouldn't have been"


def test_missing_snippet_warning(target_repo: Path) -> None:
    """Test that missing snippets produce a warning but don't fail."""
    readme = target_repo / "README.md"
    readme.write_text("""# Test

<!-- SNIPPET-START: nonexistent -->
content
<!-- SNIPPET-END -->
""")

    result = subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "nonexistent" in result.stderr


def test_missing_end_marker_warning(target_repo: Path) -> None:
    """Test that missing SNIPPET-END marker produces a warning."""
    readme = target_repo / "README.md"
    readme.write_text("""# Test

<!-- SNIPPET-START: greeting -->
content without end marker
""")

    result = subprocess.run(
        ["python", str(get_main_script())],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Missing SNIPPET-END" in result.stderr


def test_missing_config_fails(tmp_path: Path) -> None:
    """Test that missing config file causes exit with error."""
    repo = tmp_path / "no-config"
    repo.mkdir()
    git_init(repo)

    result = subprocess.run(
        ["python", str(get_main_script())],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Config file not found" in result.stderr


def test_empty_target_files_exits_cleanly(tmp_path: Path, snippet_repo: Path) -> None:
    """Test that empty target_files list exits with code 0."""
    repo = tmp_path / "empty-targets"
    repo.mkdir()
    git_init(repo)

    config = f"""snippet_repo: {snippet_repo}
target_files:
"""
    (repo / "pre-commit-snippet-config.yaml").write_text(config)

    result = subprocess.run(
        ["python", str(get_main_script())],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "No target_files" in result.stderr


def test_dry_run_does_not_modify_files(target_repo: Path) -> None:
    """Test that --dry-run doesn't modify files."""
    readme = target_repo / "README.md"
    original_content = readme.read_text()

    result = subprocess.run(
        ["python", str(get_main_script()), "--dry-run"],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Dry run" in result.stderr or "Would update" in result.stderr

    # File should not be modified
    assert readme.read_text() == original_content


def test_verbose_output(target_repo: Path) -> None:
    """Test that --verbose produces detailed output."""
    result = subprocess.run(
        ["python", str(get_main_script()), "--verbose"],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Processing" in result.stderr or "Snippet repo" in result.stderr


def test_debug_output(target_repo: Path) -> None:
    """Test that --debug produces debug-level output."""
    result = subprocess.run(
        ["python", str(get_main_script()), "--debug"],
        cwd=target_repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    # Debug output should include timestamps and DEBUG level
    assert "DEBUG" in result.stderr or "Repository root" in result.stderr


def test_branch_config(tmp_path: Path) -> None:
    """Test that snippet_branch config is recognized."""
    repo = tmp_path / "branch-test"
    repo.mkdir()
    git_init(repo)

    # Create a snippet repo with a branch
    snippet_repo = tmp_path / "snippets"
    snippet_repo.mkdir()
    git_init(snippet_repo)
    (snippet_repo / "test.md").write_text("Test content\n")
    git_cmd(["git", "add", "."], snippet_repo)
    git_cmd(["git", "commit", "-m", "Add snippet"], snippet_repo)
    git_cmd(["git", "branch", "test-branch"], snippet_repo)

    config = f"""snippet_repo: {snippet_repo}
snippet_branch: test-branch
target_files:
  - README.md
"""
    (repo / "pre-commit-snippet-config.yaml").write_text(config)
    (repo / "README.md").write_text("""# Test
<!-- SNIPPET-START: test -->
placeholder
<!-- SNIPPET-END -->
""")
    git_cmd(["git", "add", "."], repo)
    git_cmd(["git", "commit", "-m", "Initial"], repo)

    result = subprocess.run(
        ["python", str(get_main_script()), "--verbose"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Test content" in (repo / "README.md").read_text()
