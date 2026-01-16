"""Integration tests for the CLI todo application."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestCLIIntegration:
    """End-to-end tests for the CLI."""

    @pytest.fixture(autouse=True)
    def setup_storage(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Set up isolated storage for each test."""
        storage_dir = tmp_path / ".todo"
        storage_dir.mkdir()
        storage_file = storage_dir / "todos.json"

        # Patch the default storage path
        monkeypatch.setenv("HOME", str(tmp_path))

        self.storage_file = storage_file
        self.tmp_path = tmp_path
        return storage_file

    def run_todo(self, *args: str) -> subprocess.CompletedProcess:
        """Run the todo CLI with given arguments."""
        cmd = [sys.executable, "-m", "src.cli.main", *args]
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={"HOME": str(self.tmp_path), "PATH": ""},
        )

    # Help command tests
    def test_help_no_args(self) -> None:
        """Empty input shows help."""
        result = self.run_todo()
        assert result.returncode == 0
        assert "Usage: todo <command>" in result.stdout
        assert "add <task>" in result.stdout

    def test_help_explicit(self) -> None:
        """'help' command shows help."""
        result = self.run_todo("help")
        assert result.returncode == 0
        assert "Usage: todo <command>" in result.stdout

    def test_help_flag(self) -> None:
        """'--help' flag shows help."""
        result = self.run_todo("--help")
        assert result.returncode == 0
        assert "Usage: todo <command>" in result.stdout

    # Add todo tests
    def test_add_simple(self) -> None:
        """Add a simple todo."""
        result = self.run_todo("add", "buy groceries")
        assert result.returncode == 0
        assert '✓ Added: "buy groceries" (#1)' in result.stdout

    def test_add_natural_language_remember(self) -> None:
        """Add todo with 'remember' keyword."""
        result = self.run_todo("remember to call mom")
        assert result.returncode == 0
        assert "✓ Added:" in result.stdout
        assert "call mom" in result.stdout

    def test_add_natural_language_need_to(self) -> None:
        """Add todo with 'I need to' phrase."""
        result = self.run_todo("I need to finish the report")
        assert result.returncode == 0
        assert "✓ Added:" in result.stdout
        assert "finish the report" in result.stdout

    def test_add_empty_fails(self) -> None:
        """Adding empty todo fails."""
        result = self.run_todo("add")
        assert result.returncode == 1
        assert "✗ Error: Cannot add empty todo" in result.stdout

    def test_add_special_characters(self) -> None:
        """Special characters are preserved."""
        result = self.run_todo("add", "test @#$%^&*()!")
        assert result.returncode == 0
        assert "@#$%^&*()!" in result.stdout

    # List todos tests
    def test_list_empty(self) -> None:
        """List shows message when no todos."""
        result = self.run_todo("list")
        assert result.returncode == 0
        assert "No open todos" in result.stdout

    def test_list_with_items(self) -> None:
        """List shows added items."""
        self.run_todo("add", "task one")
        self.run_todo("add", "task two")

        result = self.run_todo("list")
        assert result.returncode == 0
        assert "Open todos:" in result.stdout
        assert "#1  task one" in result.stdout
        assert "#2  task two" in result.stdout

    def test_list_natural_language_show(self) -> None:
        """'show my todos' lists items."""
        self.run_todo("add", "test task")

        result = self.run_todo("show", "my", "todos")
        assert result.returncode == 0
        assert "Open todos:" in result.stdout
        assert "test task" in result.stdout

    def test_list_excludes_completed(self) -> None:
        """List only shows incomplete items."""
        self.run_todo("add", "task one")
        self.run_todo("add", "task two")
        self.run_todo("done", "#1")

        result = self.run_todo("list")
        assert result.returncode == 0
        assert "task one" not in result.stdout
        assert "task two" in result.stdout

    # Complete todo tests
    def test_complete_by_id(self) -> None:
        """Complete todo by ID."""
        self.run_todo("add", "test task")

        result = self.run_todo("complete", "#1")
        assert result.returncode == 0
        assert '✓ Completed: "test task" (#1)' in result.stdout

    def test_complete_by_title(self) -> None:
        """Complete todo by title match."""
        self.run_todo("add", "buy groceries")

        result = self.run_todo("done", "groceries")
        assert result.returncode == 0
        assert '✓ Completed: "buy groceries"' in result.stdout

    def test_complete_not_found(self) -> None:
        """Complete non-existent todo fails."""
        result = self.run_todo("done", "nonexistent")
        assert result.returncode == 1
        assert '✗ Error: No todo found matching "nonexistent"' in result.stdout

    def test_complete_already_done(self) -> None:
        """Completing already-complete todo shows info message."""
        self.run_todo("add", "test task")
        self.run_todo("done", "#1")

        result = self.run_todo("done", "#1")
        assert result.returncode == 0
        assert "is already complete" in result.stdout

    def test_complete_natural_language_finish(self) -> None:
        """'finish' keyword completes todo."""
        self.run_todo("add", "homework")

        result = self.run_todo("finish", "homework")
        assert result.returncode == 0
        assert "✓ Completed:" in result.stdout

    # Delete todo tests
    def test_delete_by_id(self) -> None:
        """Delete todo by ID."""
        self.run_todo("add", "test task")

        result = self.run_todo("delete", "#1")
        assert result.returncode == 0
        assert '✓ Deleted: "test task" (#1)' in result.stdout

    def test_delete_by_title(self) -> None:
        """Delete todo by title match."""
        self.run_todo("add", "buy groceries")

        result = self.run_todo("remove", "groceries")
        assert result.returncode == 0
        assert '✓ Deleted: "buy groceries"' in result.stdout

    def test_delete_not_found(self) -> None:
        """Delete non-existent todo fails."""
        result = self.run_todo("delete", "nonexistent")
        assert result.returncode == 1
        assert '✗ Error: No todo found matching "nonexistent"' in result.stdout

    def test_delete_removes_from_storage(self) -> None:
        """Deleted todo is removed from storage."""
        self.run_todo("add", "task one")
        self.run_todo("add", "task two")
        self.run_todo("delete", "#1")

        result = self.run_todo("list")
        assert "task one" not in result.stdout
        assert "task two" in result.stdout

    # End-to-end workflow tests
    def test_full_workflow(self) -> None:
        """Complete workflow: add, list, complete, delete."""
        # Add items
        self.run_todo("add", "buy groceries")
        self.run_todo("add", "call mom")
        self.run_todo("add", "finish report")

        # Verify list
        result = self.run_todo("list")
        assert "buy groceries" in result.stdout
        assert "call mom" in result.stdout
        assert "finish report" in result.stdout

        # Complete one
        result = self.run_todo("done", "groceries")
        assert result.returncode == 0

        # Verify it's not in list
        result = self.run_todo("list")
        assert "buy groceries" not in result.stdout
        assert "call mom" in result.stdout

        # Delete one
        result = self.run_todo("delete", "#2")
        assert result.returncode == 0

        # Verify only one remains
        result = self.run_todo("list")
        assert "call mom" not in result.stdout
        assert "finish report" in result.stdout

    def test_persistence_across_runs(self) -> None:
        """Data persists between CLI invocations."""
        # Add in one run
        self.run_todo("add", "persistent task")

        # Verify in another run
        result = self.run_todo("list")
        assert "persistent task" in result.stdout

        # Complete in another run
        self.run_todo("done", "#1")

        # Verify completed
        result = self.run_todo("list")
        assert "persistent task" not in result.stdout

    def test_storage_file_format(self) -> None:
        """Storage file has correct JSON format."""
        self.run_todo("add", "test task")

        # Read the storage file directly
        data = json.loads(self.storage_file.read_text())

        assert "next_id" in data
        assert data["next_id"] == 2
        assert "items" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["title"] == "test task"
        assert data["items"][0]["completed"] is False

    def test_id_increments_correctly(self) -> None:
        """IDs increment even after deletions."""
        self.run_todo("add", "task one")  # #1
        self.run_todo("add", "task two")  # #2
        self.run_todo("delete", "#1")
        self.run_todo("add", "task three")  # #3, not #1

        result = self.run_todo("list")
        assert "#2  task two" in result.stdout
        assert "#3  task three" in result.stdout
        assert "#1" not in result.stdout
