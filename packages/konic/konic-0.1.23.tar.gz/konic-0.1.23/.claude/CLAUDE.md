# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Konic is an RL Agent Development Toolkit for training reinforcement learning agents with both traditional RL (via RLlib/Ray) and LLM finetuning (RLHF with PPO). Python 3.12+ required.

### !IMPORTANT!

Read `CODEBASE_STRUCTURE.md` file which is located at `./.claude` folder to deeply examine and understand the codebase module/folder structure before starting coding or answering.

Update codebase structure at `CODEBASE_STRUCTURE.md` file if any architectural changes occured in the development:

```bash
find src/konic -type f -name "*.py" | tree --fromfile > .claude/CODEBASE_STRUCTURE.md
```

## Development Commands

```bash
# Install dependencies (uses uv package manager)
uv sync

# Activate virtual env by running the command below on project root
source .venv/bin/activate

# Run all tests
uv run pytest

# Run single test file
uv run pytest tests/unit/sdk/test_konic_agent.py

# Run specific test by name
uv run pytest tests/unit/sdk/test_konic_agent.py -k "test_init_with_environment"

# Linting and formatting (auto-fixes)
uv run ruff check --fix && uv run ruff format

# Running the pre-commit linter hook (auto-fixes)
uv run pre-commit run --all-files

# Type checking
uv run mypy src/konic

# CLI entry point
uv run konic --help

```

## High-Level Architecture

### Two Training Paradigms

**1. Direct RL (Conventional/traditional RL processes) (`konic.agent` + `konic.engine`)**

- `KonicAgent` → configures environment, algorithm, module
- `KonicEngine` → orchestrates training via RLlib/Ray
- `KonicEnvironment` → gymnasium-compatible with reward/termination composers

**2. LLM Finetuning (`konic.finetuning`)**

- `KonicFinetuningAgent` → configures base model, LoRA, dataset
- `KonicFinetuningEngine` → PPO training loop for RLHF
- `KonicLLMRewardComposer` → compose multiple reward signals with `@llm_reward` decorator

### Core Patterns

**Composers**: Reward and termination logic use composer pattern with reducers (MeanReducer, WeightedSumReducer, etc.) to combine multiple signals.

**Spaces**: `KonicSpace` classes define action/observation spaces with `to_gym()` conversion. Use `KonicDiscrete`, `KonicBox`, etc.

**Runtime Registration**: `@register_agent` and `@register_data` decorators for CLI integration.

**Custom Errors**: Always use exceptions from `konic.common.errors` (e.g., `KonicConfigurationError`, `KonicRuntimeError`).

---

## Konic Development Guidelines

### Documentation Standards

| Rule              | Guideline                                                                                                                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Golden rule       | Make code self-documenting through naming/structure instead of comments                                                                                  |
| Module docstrings | 1-3 lines describing purpose                                                                                                                             |
| Class docstrings  | 1-2 lines, no attribute lists or examples                                                                                                                |
| Method docstrings | Public API only, 1-3 lines max                                                                                                                           |
| Inline comments   | Only for: non-obvious algorithms, workarounds, security/performance notes. Avoid unnecessary inline comments, write inline commands if its really needed |
| TODO/FIXME        | Must include context and ticket references                                                                                                               |

### Code Quality Standards

| Rule                  | Guideline                                       |
| --------------------- | ----------------------------------------------- |
| Method/Function       | ≤40 lines                                       |
| Class                 | ≤200 lines                                      |
| File                  | ≤400 lines                                      |
| Cyclomatic complexity | <10 per function                                |
| DRY                   | Extract on third occurrence                     |
| Function design       | Do one thing (no "and" in names)                |
| Error handling        | No bare `Exception`, include actionable context |

### Architecture Standards

| Rule          | Guideline                               |
| ------------- | --------------------------------------- |
| Import order  | stdlib → third-party → local            |
| TYPE_CHECKING | Single block per file                   |
| Inheritance   | Prefer composition; max 2-3 levels deep |
| ABCs          | Only if multiple implementations exist  |

### Naming Conventions

| Style                  | Usage                                  |
| ---------------------- | -------------------------------------- |
| `snake_case`           | functions, methods, variables, modules |
| `PascalCase`           | classes                                |
| `SCREAMING_SNAKE_CASE` | constants                              |
| `is_/has_/can_`        | booleans                               |
| `from_/create_`        | factories                              |
| `to_/as_`              | conversions                            |

**Avoid:** generic names (`data`, `info`, `temp`), redundant type info (`user_dict`), unclear abbreviations (`cfg`, `mgr`)

### Anti-Patterns

- Docstrings longer than the code they document
- Parameter descriptions repeating type hints
- God classes / deep inheritance
- Mutable default arguments
- `print()` instead of logging
- Circular imports
- Business logic in `__init__.py`
- ABCs with single implementation

### Decision Trees

**Docstring:**

```
Public API? → No → Skip (unless non-obvious)
           → Yes → Clear from name+signature? → Yes → 1 line
                                              → No → 2-3 lines
```

**Comment:**

```
Explains WHY? → No → Delete, improve code
             → Yes → Non-obvious to experts? → No → Delete
                                             → Yes → Keep
```
