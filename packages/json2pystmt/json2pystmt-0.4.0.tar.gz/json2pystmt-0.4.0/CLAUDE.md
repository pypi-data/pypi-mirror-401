# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A utility and library that converts JSON into executable Python statements. Flattens nested JSON structures into line-by-line assignment statements.

Primary use cases:
- Grep searching JSON (searchable as flattened text)
- Diff checking between JSON objects
- Testing and debugging

## Development Commands

```bash
# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run single test
uv run pytest tests/test_json2pystmt.py::TestBuildJsonExprLines::test_simple_dict -v

# Lint
uv run ruff check .

# Format
uv run ruff format .

# Run CLI
uv run json2pystmt data.json
uv run json2pystmt -r myvar data.json
echo '{"key": "value"}' | uv run json2pystmt
```

## Requirements

- Python 3.10+ (uses structural pattern matching with `match`/`case`)

## Architecture

Package structure: `src/json2pystmt/`

### Core Components

1. **`_listref`** - Helper class representing list allocation expressions. Renders as `[]` for empty lists or `[None] * n` for lists with elements.

2. **`walk_container(parent, obj)`** - Recursive generator that traverses nested dicts/lists. Uses tuple-based path building and yields `(path_tuple, value)` pairs. Pattern matches on dict, list, or leaf values.

3. **`build_json_expr_lines(jsonobj, rootname="root")`** / **`json2pystmt()`** - Main API. Converts walk results into assignment statement strings using bracket notation.

4. **`main()`** - CLI entry point. Reads JSON from file or stdin, outputs flattened statements.
