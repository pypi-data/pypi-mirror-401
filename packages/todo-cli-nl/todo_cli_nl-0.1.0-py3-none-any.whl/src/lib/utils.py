from pathlib import Path
from typing import Optional


def get_next_id(storage_path: Optional[Path] = None) -> int:
    """Get the next available ID from the store.

    Note: This is primarily handled by TodoStorage.add_todo() which
    manages the next_id counter. This utility is provided for cases
    where ID generation is needed outside the storage context.
    """
    from src.services.storage import TodoStorage

    storage = TodoStorage(path=storage_path)
    store = storage._load()
    return store.next_id
