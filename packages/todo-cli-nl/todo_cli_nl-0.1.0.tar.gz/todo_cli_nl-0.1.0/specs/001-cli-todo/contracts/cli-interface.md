# CLI Interface Contract

**Date**: 2026-01-14
**Feature**: 001-cli-todo

## Usage

```bash
todo <natural language input>
```

## Input/Output Specification

### Add Item

**Input Examples**:
```bash
todo add buy groceries
todo remember to call mom
todo I need to finish the report
```

**Output**:
```
✓ Added: "buy groceries" (#1)
```

**Exit Code**: 0 (success), 1 (error)

---

### List Items

**Input Examples**:
```bash
todo list
todo show my todos
todo what do I need to do
```

**Output (items exist)**:
```
Open todos:
  #1  buy groceries
  #2  call mom
  #3  finish report
```

**Output (no items)**:
```
No open todos. Add one with: todo add <task>
```

**Exit Code**: 0

---

### Complete Item

**Input Examples**:
```bash
todo done buy groceries
todo complete #1
todo finished call mom
```

**Output (success)**:
```
✓ Completed: "buy groceries" (#1)
```

**Output (not found)**:
```
✗ Error: No todo found matching "nonexistent"
```

**Output (already complete)**:
```
ℹ "buy groceries" (#1) is already complete
```

**Exit Code**: 0 (success), 1 (not found)

---

### Delete Item

**Input Examples**:
```bash
todo delete buy groceries
todo remove #1
todo cancel call mom
```

**Output (success)**:
```
✓ Deleted: "buy groceries" (#1)
```

**Output (not found)**:
```
✗ Error: No todo found matching "nonexistent"
```

**Exit Code**: 0 (success), 1 (not found)

---

### Help

**Input**:
```bash
todo
todo help
todo --help
```

**Output**:
```
Usage: todo <command>

Commands (natural language):
  add <task>       Add a new todo item
  list             Show all open todos
  done <task>      Mark a todo as complete
  delete <task>    Remove a todo

Examples:
  todo add buy groceries
  todo show my todos
  todo done buy groceries
  todo delete #1
```

**Exit Code**: 0

---

## Error Handling

| Error | Message | Exit Code |
|-------|---------|-----------|
| Item not found | `✗ Error: No todo found matching "<query>"` | 1 |
| Empty input | Shows help | 0 |
| Storage error | `✗ Error: Could not save todos. Check ~/.todo/ permissions` | 1 |
