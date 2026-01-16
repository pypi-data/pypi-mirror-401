import re
from dataclasses import dataclass
from typing import Optional

from src.models.todo import Intent


@dataclass
class ClassificationResult:
    """Result of intent classification."""

    intent: Intent
    extracted_text: str  # The text after removing intent keywords


class IntentClassifier:
    """Classifies user input into intents using keyword matching.

    Classification Priority (for ambiguous input):
    1. DELETE (destructive - needs explicit keywords)
    2. COMPLETE (needs item reference)
    3. LIST (needs query keywords)
    4. ADD (default fallback)
    """

    # Keywords for each intent (order matters for priority)
    INTENT_KEYWORDS: dict[Intent, list[str]] = {
        Intent.DELETE: ["delete", "remove", "cancel", "drop"],
        Intent.COMPLETE: ["done", "complete", "finish", "finished", "check"],
        Intent.LIST: [
            "what do i need to do",
            "what do i have to do",
            "list",
            "show",
            "display",
            "what",
            "todos",
            "tasks",
        ],
        Intent.ADD: ["add", "create", "new", "remember", "need to", "todo"],
    }

    def classify(self, user_input: str) -> ClassificationResult:
        """Classify user input and extract the relevant text."""
        input_lower = user_input.lower().strip()

        # First pass: check multi-word keywords (higher specificity)
        for intent in [Intent.DELETE, Intent.COMPLETE, Intent.LIST, Intent.ADD]:
            keywords = self.INTENT_KEYWORDS[intent]
            for keyword in keywords:
                if " " in keyword and keyword in input_lower:
                    extracted = self._extract_text(user_input, keyword)
                    return ClassificationResult(intent=intent, extracted_text=extracted)

        # Second pass: check single-word keywords at start of input
        # This prevents "finish the report" from matching COMPLETE when user says
        # "I need to finish the report" (which should be ADD)
        words = input_lower.split()
        first_word = words[0] if words else ""

        for intent in [Intent.DELETE, Intent.COMPLETE, Intent.LIST, Intent.ADD]:
            keywords = self.INTENT_KEYWORDS[intent]
            for keyword in keywords:
                if " " not in keyword and first_word == keyword:
                    extracted = self._extract_text(user_input, keyword)
                    return ClassificationResult(intent=intent, extracted_text=extracted)

        # Third pass: check single-word keywords anywhere (fallback)
        for intent in [Intent.DELETE, Intent.COMPLETE, Intent.LIST, Intent.ADD]:
            keywords = self.INTENT_KEYWORDS[intent]
            for keyword in keywords:
                if " " not in keyword and keyword in input_lower:
                    extracted = self._extract_text(user_input, keyword)
                    return ClassificationResult(intent=intent, extracted_text=extracted)

        # Default to ADD if no keywords matched
        return ClassificationResult(
            intent=Intent.ADD, extracted_text=user_input.strip()
        )

    def _extract_text(self, user_input: str, keyword: str) -> str:
        """Remove the intent keyword from the input to get the task text."""
        # Case-insensitive removal of keyword
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        result = pattern.sub("", user_input, count=1).strip()

        # Clean up common filler words at the start
        fillers = ["to", "a", "the", "my", "i", "need", "want"]
        words = result.split()
        while words and words[0].lower() in fillers:
            words.pop(0)

        return " ".join(words).strip()

    def extract_item_reference(self, text: str) -> Optional[str]:
        """Extract item reference (#N or title) from text."""
        text = text.strip()
        if not text:
            return None

        # Check for #N pattern
        match = re.match(r"#?(\d+)", text)
        if match:
            return f"#{match.group(1)}"

        return text
