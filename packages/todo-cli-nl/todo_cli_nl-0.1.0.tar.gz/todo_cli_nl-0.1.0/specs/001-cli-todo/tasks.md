---

description: "Task list for CLI Todo List App feature implementation"
---

# Tasks: CLI Todo List App

**Input**: Design documents from `/specs/001-cli-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No test tasks included (not explicitly requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/{models,services,cli,lib}/ and tests/{unit,integration}/
- [x] T002 Initialize Python project with uv: run `uv init` and `uv add pydantic>=2.0`
- [x] T003 [P] Configure ruff for linting with pyproject.toml or ruff.toml
- [x] T004 [P] Create .gitignore for Python project (__pycache__, .pytest_cache, .venv)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create TodoItem Pydantic model in src/models/todo.py (id, title, completed, created_at)
- [x] T006 Create Intent enum in src/models/todo.py (ADD, LIST, COMPLETE, DELETE)
- [x] T007 Create TodoStore structure for JSON persistence in src/services/storage.py
- [x] T008 Implement storage initialization (~/.todo/todos.json creation) in src/services/storage.py
- [x] T009 Implement ID generation utility in src/lib/utils.py (auto-increment from store)
- [x] T010 Create intent classifier with keyword matching in src/services/classifier.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a Todo Item (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks to their todo list using natural language input

**Independent Test**: Run app with "add buy groceries" and verify item appears in ~/.todo/todos.json

### Implementation for User Story 1

- [x] T011 [US1] Implement add_todo() function in src/services/storage.py (create TodoItem, assign ID, persist to JSON)
- [x] T012 [US1] Add title extraction logic to classifier in src/services/classifier.py (remove intent keywords from input)
- [x] T013 [US1] Create CLI entry point in src/cli/main.py with argparse for natural language input
- [x] T014 [US1] Implement ADD intent handler in src/cli/main.py (classify → extract title → add_todo → display confirmation)
- [x] T015 [US1] Add validation for empty titles and 500-char limit in src/models/todo.py
- [x] T016 [US1] Add error handling for storage failures (permissions, disk space) in src/cli/main.py
- [x] T017 [US1] Format success output per contract: "✓ Added: '{title}' (#{id})" in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List Open Todo Items (Priority: P1)

**Goal**: Users can view all incomplete tasks to decide what to work on next

**Independent Test**: Pre-populate ~/.todo/todos.json with items, run "list", verify only incomplete items display

### Implementation for User Story 2

- [x] T018 [US2] Implement get_open_todos() function in src/services/storage.py (filter completed=False)
- [x] T019 [US2] Implement LIST intent handler in src/cli/main.py (classify → get_open_todos → display formatted list)
- [x] T020 [US2] Format list output per contract: "Open todos:\n  #1  title\n  #2  title" in src/cli/main.py
- [x] T021 [US2] Handle empty list case with message: "No open todos. Add one with: todo add <task>" in src/cli/main.py
- [x] T022 [US2] Verify LIST intent keywords (list, show, display, what, todos, tasks) in src/services/classifier.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo Item Complete (Priority: P2)

**Goal**: Users can mark tasks as done when they finish them

**Independent Test**: Create item via US1, mark it complete, verify it no longer appears in list (US2)

### Implementation for User Story 3

- [x] T023 [US3] Implement find_todo() function in src/services/storage.py (match by ID or fuzzy title match)
- [x] T024 [US3] Implement complete_todo(item_id) function in src/services/storage.py (set completed=True, persist)
- [x] T025 [US3] Implement COMPLETE intent handler in src/cli/main.py (classify → find_todo → complete_todo → display confirmation)
- [x] T026 [US3] Add item extraction logic to classifier in src/services/classifier.py (extract #N or title from input)
- [x] T027 [US3] Format success output per contract: "✓ Completed: '{title}' (#{id})" in src/cli/main.py
- [x] T028 [US3] Handle not-found case: "✗ Error: No todo found matching '{query}'" with exit code 1 in src/cli/main.py
- [x] T029 [US3] Handle already-complete case: "ℹ '{title}' (#{id}) is already complete" in src/cli/main.py

**Checkpoint**: User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todo Item (Priority: P3)

**Goal**: Users can permanently remove tasks from their list

**Independent Test**: Create item via US1, delete it, verify it's gone from storage entirely

### Implementation for User Story 4

- [x] T030 [US4] Implement delete_todo(item_id) function in src/services/storage.py (remove from items list, persist)
- [x] T031 [US4] Implement DELETE intent handler in src/cli/main.py (classify → find_todo → delete_todo → display confirmation)
- [x] T032 [US4] Format success output per contract: "✓ Deleted: '{title}' (#{id})" in src/cli/main.py
- [x] T033 [US4] Handle not-found case: "✗ Error: No todo found matching '{query}'" with exit code 1 in src/cli/main.py
- [x] T034 [US4] Verify DELETE intent keywords (delete, remove, cancel, drop) in src/services/classifier.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T035 [P] Implement help command handler (empty input, "help", "--help") in src/cli/main.py
- [x] T036 [P] Format help output per contract (usage, commands, examples) in src/cli/main.py
- [x] T037 Add comprehensive error handling for malformed JSON in src/services/storage.py
- [x] T038 Add logging for debug purposes (optional - can use print statements) across all modules
- [x] T039 Validate all edge cases from spec.md: empty input, special characters, ambiguous commands
- [x] T040 Run quickstart.md validation (verify all usage examples work correctly)
- [x] T041 Run ruff check on all source files and fix any issues
- [x] T042 Performance validation: add operations < 5s, list operations < 2s
- [x] T043 Validate intent classification accuracy: create test suite with 10+ examples per intent (ADD, LIST, COMPLETE, DELETE) and verify ≥90% correct classification per SC-003

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1 (can run in parallel)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses find_todo which is new, but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Reuses find_todo from US3 if available, but can implement independently

### Within Each User Story

- Models created in Foundational phase
- Services use models
- CLI uses services
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- Once Foundational phase completes, User Stories 1 and 2 can start in parallel (different handlers, no conflicts)
- User Stories 3 and 4 can run in parallel if find_todo is duplicated or built into each
- All Polish tasks marked [P] can run in parallel (T035, T036)

---

## Parallel Example: User Story 1 & 2

```bash
# After Foundational phase, launch both P1 stories together:
# Developer A implements US1 (add functionality)
# Developer B implements US2 (list functionality)
# Both work on different functions in storage.py and different handlers in main.py
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add items)
4. Complete Phase 4: User Story 2 (List items)
5. **STOP and VALIDATE**: Test add and list together - this is minimal viable product
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 + 2 → Test together → Deploy/Demo (MVP - can add and view!)
3. Add User Story 3 → Test independently → Deploy/Demo (can now complete items)
4. Add User Story 4 → Test independently → Deploy/Demo (can now delete items)
5. Add Polish → Final validation → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add)
   - Developer B: User Story 2 (List)
   - Merge both for MVP
3. Developer C: User Story 3 (Complete)
4. Developer D: User Story 4 (Delete)
5. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Storage location: ~/.todo/todos.json (specified in data-model.md)
- Performance targets: add < 5s, list < 2s (from plan.md)
- All natural language input goes through classifier first
- Intent classification priority: DELETE → COMPLETE → LIST → ADD (from data-model.md)
