"""Test intent classification accuracy (SC-003: ≥90%)."""

import pytest

from src.models.todo import Intent
from src.services.classifier import IntentClassifier


class TestIntentClassifier:
    """Test intent classification with 10+ examples per intent."""

    @pytest.fixture
    def classifier(self) -> IntentClassifier:
        return IntentClassifier()

    # ADD intent tests (12 examples)
    @pytest.mark.parametrize(
        "input_text",
        [
            "add buy groceries",
            "add call mom",
            "create a new task",
            "new meeting at 3pm",
            "remember to water plants",
            "I need to finish the report",
            "todo pick up dry cleaning",
            "add schedule dentist appointment",
            "create reminder for bills",
            "new project kickoff",
            "remember meeting tomorrow",
            "I need to call the bank",
        ],
    )
    def test_add_intent(self, classifier: IntentClassifier, input_text: str) -> None:
        result = classifier.classify(input_text)
        assert result.intent == Intent.ADD, f"Expected ADD for: {input_text}"

    # LIST intent tests (12 examples)
    @pytest.mark.parametrize(
        "input_text",
        [
            "list",
            "list all",
            "show my todos",
            "show tasks",
            "display todos",
            "display my tasks",
            "what do I need to do",
            "what do I have to do",
            "what are my todos",
            "todos",
            "tasks",
            "what tasks do I have",
        ],
    )
    def test_list_intent(self, classifier: IntentClassifier, input_text: str) -> None:
        result = classifier.classify(input_text)
        assert result.intent == Intent.LIST, f"Expected LIST for: {input_text}"

    # COMPLETE intent tests (12 examples)
    @pytest.mark.parametrize(
        "input_text",
        [
            "done buy groceries",
            "done #1",
            "complete the report",
            "complete #2",
            "finish homework",
            "finished the project",
            "check off groceries",
            "done with call mom",
            "complete item 3",
            "finished calling bank",
            "check meeting task",
            "done meeting",
        ],
    )
    def test_complete_intent(
        self, classifier: IntentClassifier, input_text: str
    ) -> None:
        result = classifier.classify(input_text)
        assert result.intent == Intent.COMPLETE, f"Expected COMPLETE for: {input_text}"

    # DELETE intent tests (12 examples)
    @pytest.mark.parametrize(
        "input_text",
        [
            "delete buy groceries",
            "delete #1",
            "remove the task",
            "remove #2",
            "cancel meeting",
            "cancel appointment",
            "drop the project",
            "delete item 3",
            "remove old task",
            "cancel #5",
            "drop homework",
            "delete all completed",
        ],
    )
    def test_delete_intent(
        self, classifier: IntentClassifier, input_text: str
    ) -> None:
        result = classifier.classify(input_text)
        assert result.intent == Intent.DELETE, f"Expected DELETE for: {input_text}"

    def test_classification_accuracy(self, classifier: IntentClassifier) -> None:
        """Verify overall classification accuracy is ≥90%."""
        test_cases = [
            # ADD
            ("add buy groceries", Intent.ADD),
            ("add call mom", Intent.ADD),
            ("create a new task", Intent.ADD),
            ("new meeting at 3pm", Intent.ADD),
            ("remember to water plants", Intent.ADD),
            ("I need to finish the report", Intent.ADD),
            ("todo pick up dry cleaning", Intent.ADD),
            ("add schedule dentist appointment", Intent.ADD),
            ("create reminder for bills", Intent.ADD),
            ("new project kickoff", Intent.ADD),
            # LIST
            ("list", Intent.LIST),
            ("show my todos", Intent.LIST),
            ("display todos", Intent.LIST),
            ("what do I need to do", Intent.LIST),
            ("what are my todos", Intent.LIST),
            ("todos", Intent.LIST),
            ("tasks", Intent.LIST),
            ("show tasks", Intent.LIST),
            ("display my tasks", Intent.LIST),
            ("what tasks do I have", Intent.LIST),
            # COMPLETE
            ("done buy groceries", Intent.COMPLETE),
            ("done #1", Intent.COMPLETE),
            ("complete the report", Intent.COMPLETE),
            ("complete #2", Intent.COMPLETE),
            ("finish homework", Intent.COMPLETE),
            ("finished the project", Intent.COMPLETE),
            ("check off groceries", Intent.COMPLETE),
            ("done with call mom", Intent.COMPLETE),
            ("complete item 3", Intent.COMPLETE),
            ("finished calling bank", Intent.COMPLETE),
            # DELETE
            ("delete buy groceries", Intent.DELETE),
            ("delete #1", Intent.DELETE),
            ("remove the task", Intent.DELETE),
            ("remove #2", Intent.DELETE),
            ("cancel meeting", Intent.DELETE),
            ("cancel appointment", Intent.DELETE),
            ("drop the project", Intent.DELETE),
            ("delete item 3", Intent.DELETE),
            ("remove old task", Intent.DELETE),
            ("cancel #5", Intent.DELETE),
        ]

        correct = 0
        total = len(test_cases)

        for input_text, expected_intent in test_cases:
            result = classifier.classify(input_text)
            if result.intent == expected_intent:
                correct += 1

        accuracy = correct / total
        assert accuracy >= 0.90, f"Accuracy {accuracy:.1%} is below 90% target"
