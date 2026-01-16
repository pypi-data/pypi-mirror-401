#!/usr/bin/env python3
"""CLI entry point for the todo application."""

import sys
from typing import NoReturn

from src.models.todo import Intent
from src.services.classifier import IntentClassifier
from src.services.storage import TodoStorage


def show_help() -> None:
    """Display help message."""
    print(
        """Usage: todo <command>

Commands (natural language):
  add <task>       Add a new todo item
  list             Show all open todos
  done <task>      Mark a todo as complete
  delete <task>    Remove a todo

Examples:
  todo add buy groceries
  todo show my todos
  todo done buy groceries
  todo delete #1"""
    )


def handle_add(storage: TodoStorage, title: str) -> int:
    """Handle ADD intent."""
    if not title.strip():
        print("✗ Error: Cannot add empty todo")
        return 1

    try:
        item = storage.add_todo(title)
        print(f'✓ Added: "{item.title}" (#{item.id})')
        return 0
    except ValueError as e:
        print(f"✗ Error: {e}")
        return 1
    except OSError:
        print("✗ Error: Could not save todos. Check ~/.todo/ permissions")
        return 1


def handle_list(storage: TodoStorage) -> int:
    """Handle LIST intent."""
    items = storage.get_open_todos()

    if not items:
        print("No open todos. Add one with: todo add <task>")
        return 0

    print("Open todos:")
    for item in items:
        print(f"  #{item.id}  {item.title}")
    return 0


def handle_complete(storage: TodoStorage, query: str) -> int:
    """Handle COMPLETE intent."""
    if not query.strip():
        print("✗ Error: Please specify which todo to complete")
        return 1

    item = storage.find_todo(query)
    if not item:
        print(f'✗ Error: No todo found matching "{query}"')
        return 1

    if item.completed:
        print(f'ℹ "{item.title}" (#{item.id}) is already complete')
        return 0

    storage.complete_todo(item.id)
    print(f'✓ Completed: "{item.title}" (#{item.id})')
    return 0


def handle_delete(storage: TodoStorage, query: str) -> int:
    """Handle DELETE intent."""
    if not query.strip():
        print("✗ Error: Please specify which todo to delete")
        return 1

    item = storage.find_todo(query)
    if not item:
        print(f'✗ Error: No todo found matching "{query}"')
        return 1

    storage.delete_todo(item.id)
    print(f'✓ Deleted: "{item.title}" (#{item.id})')
    return 0


def main() -> NoReturn:
    """Main entry point for the CLI."""
    # Get user input from command line arguments
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    user_input = " ".join(sys.argv[1:]).strip()

    # Handle empty input or help explicitly
    if not user_input or user_input.lower() in ("help", "--help", "-h"):
        show_help()
        sys.exit(0)

    # Classify intent and extract text
    classifier = IntentClassifier()
    result = classifier.classify(user_input)

    # Initialize storage
    storage = TodoStorage()

    # Route to appropriate handler
    if result.intent == Intent.ADD:
        exit_code = handle_add(storage, result.extracted_text)
    elif result.intent == Intent.LIST:
        exit_code = handle_list(storage)
    elif result.intent == Intent.COMPLETE:
        exit_code = handle_complete(storage, result.extracted_text)
    elif result.intent == Intent.DELETE:
        exit_code = handle_delete(storage, result.extracted_text)
    else:
        show_help()
        exit_code = 0

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
