# Todo App Constitution

## Core Principles

### I. Simplicity
A todo item has a title and completion status. Start minimal, add features only when needed.

### II. Type Safety
Use Pydantic models for data validation.

### III. Testable
Core functionality must be testable in isolation.

### IV. Single Responsibility
Each module does one thing well.

### V. YAGNI
Don't build features until they're needed.

## Technology Stack

- Python 3.10+
- Pydantic for data models
- uv for dependency management

## Development Workflow

- Run code with `uv run`
- Install dependencies with `uv sync`
- Lint with `ruff check`

## Governance

Keep it simple. Extend only when necessary.

**Version**: 1.0.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14
