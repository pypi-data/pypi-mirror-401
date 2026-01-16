# Feature Specification: CLI Todo List App

**Feature Branch**: `001-cli-todo`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "I am building a todo list app which will be operated from the command line. It should provide for adding new todo list items, marking todo list items complete, deleting todo list items, and list the current set of open todo items. It should analyse each request to classify the intent of the instruction and proceed from there."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a Todo Item (Priority: P1)

A user wants to quickly add a new task to their todo list by typing a natural language instruction at the command line.

**Why this priority**: Adding items is the foundational action - without it, no other features are useful. This enables the core value proposition.

**Independent Test**: Can be fully tested by running the app with an "add" instruction and verifying the item appears in storage.

**Acceptance Scenarios**:

1. **Given** an empty todo list, **When** the user enters "add buy groceries", **Then** a new todo item "buy groceries" is created and confirmation is displayed
2. **Given** an existing todo list with 3 items, **When** the user enters "remember to call mom", **Then** a new todo item "call mom" is added and the list now contains 4 items
3. **Given** the app is running, **When** the user enters "I need to finish the report", **Then** the intent is classified as "add" and "finish the report" is added as a new item

---

### User Story 2 - List Open Todo Items (Priority: P1)

A user wants to see all their incomplete tasks so they can decide what to work on next.

**Why this priority**: Viewing tasks is essential for the app to provide value - users need to see what they've added.

**Independent Test**: Can be tested by pre-populating storage with items and verifying they display correctly.

**Acceptance Scenarios**:

1. **Given** a todo list with 3 incomplete items, **When** the user enters "show my todos", **Then** all 3 items are displayed with identifiers
2. **Given** a todo list with 2 complete and 2 incomplete items, **When** the user enters "list tasks", **Then** only the 2 incomplete items are displayed
3. **Given** an empty todo list, **When** the user enters "what do I need to do", **Then** a message indicates there are no open items

---

### User Story 3 - Mark Todo Item Complete (Priority: P2)

A user wants to mark a task as done when they finish it.

**Why this priority**: Completing items is core functionality but depends on items existing first (P1 stories).

**Independent Test**: Can be tested by creating an item, marking it complete, and verifying it no longer appears in open items.

**Acceptance Scenarios**:

1. **Given** a todo list with item "buy groceries", **When** the user enters "done buy groceries", **Then** the item is marked complete and confirmation is displayed
2. **Given** a todo list with item #2 "call mom", **When** the user enters "complete item 2", **Then** item #2 is marked complete
3. **Given** a todo list with no matching item, **When** the user enters "finish nonexistent task", **Then** an error message indicates the item was not found

---

### User Story 4 - Delete Todo Item (Priority: P3)

A user wants to remove a task entirely from their list (not just mark complete).

**Why this priority**: Deletion is useful but less common than adding/completing. Users may want to remove mistaken entries or irrelevant tasks.

**Independent Test**: Can be tested by creating an item, deleting it, and verifying it no longer exists in storage.

**Acceptance Scenarios**:

1. **Given** a todo list with item "buy groceries", **When** the user enters "delete buy groceries", **Then** the item is permanently removed and confirmation is displayed
2. **Given** a todo list with item #3, **When** the user enters "remove item 3", **Then** item #3 is permanently deleted
3. **Given** a todo list with no matching item, **When** the user enters "delete nonexistent", **Then** an error message indicates the item was not found

---

### Edge Cases

- What happens when the user enters an ambiguous command that could be multiple intents?
  - System uses keyword-priority matching (DELETE → COMPLETE → LIST → ADD) as defined in data-model.md. No interactive clarification prompt in v1.
- How does the system handle empty input?
  - Display a help message with available commands
- What happens when the user tries to complete an already-completed item?
  - Display a message indicating the item is already complete
- How does the system handle special characters in todo item text?
  - Accept and store them as-is

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept natural language input from the command line
- **FR-002**: System MUST classify user input into one of four intents: add, list, complete, delete
- **FR-003**: System MUST create new todo items with a title extracted from user input
- **FR-004**: System MUST assign a unique identifier to each todo item
- **FR-005**: System MUST persist todo items between sessions
- **FR-006**: System MUST display only incomplete items when listing todos
- **FR-007**: System MUST allow marking items complete by title match or identifier
- **FR-008**: System MUST allow deleting items by title match or identifier
- **FR-009**: System MUST display appropriate confirmation messages after each action
- **FR-010**: System MUST display helpful error messages when operations fail

### Key Entities

- **Todo Item**: Represents a single task. Contains: unique identifier, title (text description), completion status (complete/incomplete), creation timestamp
- **Intent**: The classified action the user wants to perform. One of: add, list, complete, delete

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new todo item in under 5 seconds
- **SC-002**: Users can view their open items in under 2 seconds
- **SC-003**: Intent classification correctly identifies user intent at least 90% of the time for common phrasings
- **SC-004**: All todo items persist correctly between application restarts
- **SC-005**: Users receive clear feedback (confirmation or error) for every action attempted

## Assumptions

- Users will interact with the app via a single command-line session at a time
- Local file storage is acceptable for persistence (no multi-device sync required)
- English language input only
- No user authentication required (single-user app)
- No due dates or priorities for items (can be added in future iterations)
