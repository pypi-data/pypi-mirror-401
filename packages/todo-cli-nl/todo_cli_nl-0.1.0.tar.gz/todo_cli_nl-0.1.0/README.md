# Todo CLI

A command-line todo list application that accepts natural language input.

## Features

- **Natural language input** - No need to remember exact commands
- **Intent classification** - Automatically understands what you want to do
- **Local persistence** - Todos saved to `~/.todo/todos.json`
- **Simple and fast** - Operations complete in under 0.5 seconds

## Installation

### From PyPI

```bash
pip install todo-cli-nl
```

### From Source

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://gitlab.com/roscom/todo.git
cd todo
uv sync
```

## Usage

```bash
# If installed via pip
todo <command>

# If running from source
uv run todo <command>
```

### Add a Todo

```bash
uv run todo add buy groceries
uv run todo "remember to call mom"
uv run todo "I need to finish the report"
```

### List Open Todos

```bash
uv run todo list
uv run todo "show my todos"
uv run todo "what do I need to do"
```

Output:
```
Open todos:
  #1  buy groceries
  #2  call mom
  #3  finish the report
```

### Complete a Todo

By ID:
```bash
uv run todo "done #1"
uv run todo "complete #2"
```

By title:
```bash
uv run todo "done buy groceries"
uv run todo "finish the report"
```

### Delete a Todo

```bash
uv run todo "delete #1"
uv run todo "remove call mom"
```

### Help

```bash
uv run todo
uv run todo help
uv run todo --help
```

## Supported Commands

| Intent | Keywords |
|--------|----------|
| Add | `add`, `create`, `new`, `remember`, `need to`, `todo` |
| List | `list`, `show`, `display`, `what`, `todos`, `tasks` |
| Complete | `done`, `complete`, `finish`, `finished`, `check` |
| Delete | `delete`, `remove`, `cancel`, `drop` |

## Data Storage

Todos are stored in JSON format at `~/.todo/todos.json`.

To reset all todos:
```bash
rm -rf ~/.todo
```

## Development

### Run Tests

```bash
# All tests
uv run pytest

# Unit tests only
uv run pytest tests/unit -v

# Integration tests only
uv run pytest tests/integration -v

# With coverage
uv run pytest --cov=src
```

### Lint

```bash
uvx ruff check src/ tests/
```

## Project Structure

```
src/
├── models/todo.py       # TodoItem model + Intent enum
├── services/
│   ├── storage.py       # JSON file persistence
│   └── classifier.py    # Intent classification
├── cli/main.py          # CLI entry point
└── lib/utils.py         # Utilities

tests/
├── unit/                # Unit tests
└── integration/         # CLI integration tests
```

## License

MIT
