# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tuible is a Python package for printing formatted CLI tables with ANSI colors. It provides both a Python API and a CLI interface for creating tables with customizable borders, colors, alignment, and multi-row cells.

## Development Commands

```bash
# Install dependencies
uv sync

# Run tests
PYTHONPATH=src uv run pytest

# Run a single test
PYTHONPATH=src uv run pytest tests/test_core.py::test_function_name -v

# Build package
uv run python -m build

# CLI usage (after uv sync)
uv run tuible --help
```

## Architecture

The codebase follows a simple three-layer design:

```
src/tuible/
├── cli.py      # Entry point: parses args → TuibleParams → TuibleTable.execute()
├── params.py   # TuibleParams dataclass: CLI parsing, env vars, mode/column storage
├── table.py    # TuibleTable: rendering logic for borders, headers, body rows
├── core.py     # Python API: print_line(), print_block(), print_table()
└── __init__.py # Public exports
```

**Data flow:**
1. CLI args/env vars → `TuibleParams.createFromArguments()` → populates `mode_stack` and `mode_columns`
2. `TuibleTable(params)` → calculates dynamic column widths if needed
3. `table.execute()` → iterates `mode_stack`, calls render methods once per mode

**Key concepts:**
- **Modes**: `top`, `head`, `body`, `bot`, `idx` - stacked in any order
- **Colon syntax**: `:value` continues in the same column (multi-row cells)
- **mode_columns**: Dict mapping mode names to column data `Dict[str, List[List[str]]]`
- **Index column**: When `idx` mode is used, it reserves the leftmost column for labels or auto-numbering

## Testing

Tests are in `tests/` directory. The test suite covers:
- `test_core.py`: Python API functions
- `test_cli.py`: CLI argument parsing and idx command functionality
