# Research: CLI Todo List App

**Date**: 2026-01-14
**Feature**: 001-cli-todo

## Research Areas

### 1. Intent Classification Approach

**Decision**: Keyword-based classification with pattern matching

**Rationale**:
- Simple and deterministic - no ML dependencies
- Fast execution (< 100ms)
- Easy to test and debug
- Meets 90% accuracy requirement for common phrasings
- Aligns with YAGNI principle

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| ML-based classifier (spaCy, transformers) | Overkill for 4 intents, adds heavy dependencies |
| LLM API calls | Adds latency, cost, network dependency |
| Regex only | Too brittle for natural language variations |

**Implementation**:
- Define keyword sets for each intent (add, list, complete, delete)
- Use fuzzy matching for item identification
- Fall back to "add" for ambiguous input (most common action)

### 2. Storage Format

**Decision**: JSON file in user's home directory (`~/.todo/todos.json`)

**Rationale**:
- Human-readable and debuggable
- Native Python support (no dependencies)
- Simple backup/restore (copy file)
- Sufficient for single-user, local storage

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| SQLite | Overkill for simple list, adds complexity |
| YAML | Requires dependency, no benefit over JSON |
| Plain text | Harder to parse structured data |

### 3. CLI Framework

**Decision**: No framework - use argparse from standard library

**Rationale**:
- Zero dependencies
- Sufficient for single-command input
- Aligns with simplicity principle

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Click | Adds dependency for minimal benefit |
| Typer | Adds dependency, designed for subcommand CLIs |
| Rich | Nice output but unnecessary complexity |

### 4. ID Generation

**Decision**: Auto-incrementing integer IDs

**Rationale**:
- Simple for users to reference ("complete item 2")
- Easy to implement and maintain
- Sufficient for single-user, local storage

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| UUID | Hard for users to type/remember |
| Timestamp-based | Unnecessarily complex |

## Unresolved Items

None - all technical decisions resolved.

## Dependencies Summary

| Dependency | Version | Purpose |
|------------|---------|---------|
| pydantic | >=2.0 | Data validation and models |
| pytest | >=7.0 | Testing (dev only) |
| ruff | latest | Linting (dev only) |
