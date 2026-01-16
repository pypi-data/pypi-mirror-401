from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Intent(str, Enum):
    """Classified user intent from natural language input."""

    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    DELETE = "delete"


class TodoItem(BaseModel):
    """Represents a single task in the todo list."""

    id: int = Field(..., gt=0, description="Unique identifier (auto-increment)")
    title: str = Field(
        ..., min_length=1, max_length=500, description="Task description"
    )
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp (UTC)",
    )

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or whitespace only")
        return stripped

    model_config = {"frozen": False}
