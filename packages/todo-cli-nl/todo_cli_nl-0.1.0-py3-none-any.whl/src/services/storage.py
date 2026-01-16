import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.models.todo import TodoItem


class TodoStore(BaseModel):
    """Represents the persisted state (JSON file structure)."""

    next_id: int = 1
    items: list[TodoItem] = []


class TodoStorage:
    """Handles JSON file persistence for todo items."""

    DEFAULT_PATH = Path.home() / ".todo" / "todos.json"

    def __init__(self, path: Optional[Path] = None):
        self.path = path or self.DEFAULT_PATH
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage directory and file if they don't exist."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._save(TodoStore())

    def _load(self) -> TodoStore:
        """Load the store from disk.

        Handles malformed JSON gracefully by returning an empty store.
        This ensures the app remains functional even if the storage file
        is corrupted.
        """
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return TodoStore.model_validate(data)
        except json.JSONDecodeError:
            # Malformed JSON - start fresh but preserve the corrupted file
            backup_path = self.path.with_suffix(".json.bak")
            if self.path.exists():
                self.path.rename(backup_path)
            return TodoStore()
        except FileNotFoundError:
            return TodoStore()
        except Exception:
            # Pydantic validation errors or other issues
            return TodoStore()

    def _save(self, store: TodoStore) -> None:
        """Save the store to disk."""
        self.path.write_text(
            store.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def add_todo(self, title: str) -> TodoItem:
        """Create a new todo item and persist it."""
        store = self._load()
        item = TodoItem(id=store.next_id, title=title)
        store.items.append(item)
        store.next_id += 1
        self._save(store)
        return item

    def get_open_todos(self) -> list[TodoItem]:
        """Return all incomplete todo items."""
        store = self._load()
        return [item for item in store.items if not item.completed]

    def get_all_todos(self) -> list[TodoItem]:
        """Return all todo items."""
        store = self._load()
        return store.items

    def find_todo(self, query: str) -> Optional[TodoItem]:
        """Find a todo by ID (#N) or fuzzy title match."""
        store = self._load()

        # Check for ID pattern (#N or just N)
        query_stripped = query.strip()
        if query_stripped.startswith("#"):
            query_stripped = query_stripped[1:]

        try:
            item_id = int(query_stripped)
            for item in store.items:
                if item.id == item_id:
                    return item
        except ValueError:
            pass

        # Fuzzy title match (case-insensitive contains)
        query_lower = query.lower().strip()
        for item in store.items:
            if query_lower in item.title.lower():
                return item

        return None

    def complete_todo(self, item_id: int) -> Optional[TodoItem]:
        """Mark a todo item as completed."""
        store = self._load()
        for item in store.items:
            if item.id == item_id:
                item.completed = True
                self._save(store)
                return item
        return None

    def delete_todo(self, item_id: int) -> Optional[TodoItem]:
        """Delete a todo item from the store."""
        store = self._load()
        for i, item in enumerate(store.items):
            if item.id == item_id:
                deleted = store.items.pop(i)
                self._save(store)
                return deleted
        return None
