# Quickstart: CLI Todo List App

**Date**: 2026-01-14
**Feature**: 001-cli-todo

## Prerequisites

- Python 3.10+
- uv (for dependency management)

## Setup

```bash
# Clone and enter directory
cd todo

# Install dependencies
uv sync

# Run the app
uv run todo "add buy groceries"
```

## Usage Examples

```bash
# Add items
uv run todo "add buy groceries"
uv run todo "remember to call mom"
uv run todo "I need to finish the report"

# List open items
uv run todo "list"
uv run todo "show my todos"

# Complete items
uv run todo "done buy groceries"
uv run todo "complete #1"

# Delete items
uv run todo "delete #2"
uv run todo "remove call mom"
```

## Development

```bash
# Run tests
uv run pytest

# Run linter
uvx ruff check src/

# Run single test file
uv run pytest tests/unit/test_classifier.py -v
```

## Project Structure

```
src/
├── models/todo.py       # TodoItem Pydantic model
├── services/
│   ├── storage.py       # JSON file persistence
│   └── classifier.py    # Intent classification
├── cli/main.py          # CLI entry point
└── lib/utils.py         # Utilities

tests/
├── unit/                # Unit tests
└── integration/         # CLI integration tests
```

## Data Storage

Todos are stored in `~/.todo/todos.json`. To reset:

```bash
rm -rf ~/.todo
```
