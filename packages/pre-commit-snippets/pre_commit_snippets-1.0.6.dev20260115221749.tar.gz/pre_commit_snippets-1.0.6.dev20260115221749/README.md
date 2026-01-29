# pre-commit-snippet

[![CI](https://github.com/RemoteRabbit/pre-commit-snippets/actions/workflows/ci.yaml/badge.svg)](https://github.com/RemoteRabbit/pre-commit-snippets/actions/workflows/ci.yaml)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://remoterabbit.github.io/pre-commit-snippets/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pre-commit hook that automatically syncs markdown snippets from a central repository into your documentation files.

## Features

- **Marker-based replacement**: Uses `<!-- SNIPPET-START: name -->` / `<!-- SNIPPET-END -->` markers to identify replaceable blocks
- **SHA-256 caching**: Only rewrites blocks when the central snippet has actually changed, avoiding unnecessary file churn
- **Automatic staging**: Modified files are automatically staged for commit
- **Branch/tag support**: Pin snippets to a specific branch or tag
- **Dry-run mode**: Preview changes without modifying files
- **Debug logging**: Detailed logging for troubleshooting

## Installation

### Using pre-commit framework

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/RemoteRabbit/pre-commit-snippet
    rev: v1.0.4  # Use the latest tag
    hooks:
      - id: snippet-sync
```

### Manual installation

1. Clone this repository
2. Create a `pre-commit-snippet-config.yaml` configuration file (see below)
3. Run `python main.py` before committing

## Configuration

Create a `pre-commit-snippet-config.yaml` file in your repository root:

```yaml
# URL of the repository containing your snippets (required)
snippet_repo: https://github.com/your-org/snippets.git

# Branch or tag to use (optional, default: default branch)
snippet_branch: main

# Subdirectory within the snippet repo where snippets are stored (optional)
snippet_subdir: snippets

# File extension for snippet files (optional, default: .md)
snippet_ext: .md

# List of files to process (required)
target_files:
  - README.md
  - docs/CONTRIBUTING.md
  - docs/SECURITY.md
```

## Usage

In your markdown files, wrap the areas you want to sync with snippet markers:

```markdown
# My Project

<!-- SNIPPET-START: license-notice -->
This content will be replaced with the contents of `license-notice.md` from your snippet repo.
<!-- SNIPPET-END -->

## Other content...
```

When the hook runs, it will:

1. Clone the snippet repository (shallow clone)
2. Find all `SNIPPET-START` / `SNIPPET-END` marker pairs
3. Replace the content between markers with the corresponding snippet file
4. Cache hashes to avoid rewriting unchanged blocks
5. Stage any modified files

## Command Line Options

```bash
pre-commit-snippet [OPTIONS]
# or
python main.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without modifying files |
| `--verbose`, `-v` | Print info-level logs (files being processed, updates) |
| `--debug` | Print debug-level logs with timestamps (commands, hashes, paths) |

### Examples

```bash
# Normal run
pre-commit-snippet

# Preview what would change
pre-commit-snippet --dry-run

# See detailed processing info
pre-commit-snippet --verbose

# Debug issues with full detail
pre-commit-snippet --debug
```

## Cache File

The hook creates a `.snippet-hashes.json` file to track which snippets have been applied. You should commit this file to avoid unnecessary rewrites on other machines.

## Project Structure

```
pre-commit-snippet/
├── main.py                      # CLI entry point
├── pre_commit_snippet/
│   ├── __init__.py              # Package init
│   ├── cache.py                 # Hash computation and caching
│   ├── cli.py                   # Argument parsing and main logic
│   ├── config.py                # Configuration loading
│   ├── git.py                   # Git operations
│   ├── logging.py               # Logging configuration
│   └── snippet.py               # Snippet replacement logic
└── tests/
    └── test_main.py             # Test suite
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, conventional commits, and release process.

## License

MIT
