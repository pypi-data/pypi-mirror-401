# Data Model: CLI Todo List App

**Date**: 2026-01-14
**Feature**: 001-cli-todo

## Entities

### TodoItem

Represents a single task in the todo list.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | Yes | Unique identifier (auto-increment) |
| title | str | Yes | Task description (1-500 chars) |
| completed | bool | Yes | Completion status (default: False) |
| created_at | datetime | Yes | Creation timestamp (UTC) |

**Validation Rules**:
- `title` must be non-empty and max 500 characters
- `id` must be positive integer
- `created_at` auto-set on creation

**State Transitions**:
```
[Created] --> completed=False
    |
    v (complete action)
[Completed] --> completed=True
```

### Intent

Represents the classified user intent from natural language input.

| Value | Description | Keywords |
|-------|-------------|----------|
| ADD | Create new todo item | add, create, new, remember, need to, todo |
| LIST | Display open items | list, show, display, what, todos, tasks |
| COMPLETE | Mark item done | done, complete, finish, finished, check |
| DELETE | Remove item | delete, remove, cancel, drop |

**Classification Priority** (for ambiguous input):
1. DELETE (destructive - needs explicit keywords)
2. COMPLETE (needs item reference)
3. LIST (needs query keywords)
4. ADD (default fallback)

### TodoStore

Represents the persisted state (JSON file structure).

```json
{
  "next_id": 4,
  "items": [
    {
      "id": 1,
      "title": "Buy groceries",
      "completed": false,
      "created_at": "2026-01-14T10:30:00Z"
    },
    {
      "id": 2,
      "title": "Call mom",
      "completed": true,
      "created_at": "2026-01-14T09:00:00Z"
    }
  ]
}
```

## Relationships

```
User Input (string)
    |
    v
Intent Classification
    |
    +--> ADD --> TodoItem created --> TodoStore updated
    |
    +--> LIST --> TodoStore queried --> Display incomplete items
    |
    +--> COMPLETE --> TodoItem.completed = True --> TodoStore updated
    |
    +--> DELETE --> TodoItem removed --> TodoStore updated
```

## Storage Location

- **Path**: `~/.todo/todos.json`
- **Format**: JSON (UTF-8)
- **Backup**: None (single-user, local)
- **Migration**: Not needed (v1)
