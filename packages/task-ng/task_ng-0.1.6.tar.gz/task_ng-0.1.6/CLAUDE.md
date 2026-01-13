# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Task-NG is a modern Python reimagining of Taskwarrior, a powerful CLI task management tool. Built with Python 3.11+, it uses:
- **Typer** for CLI commands
- **Pydantic** for data models
- **Rich** for terminal output
- **SQLite** with Alembic migrations for data storage
- **Ruff** for linting/formatting
- **Mypy** for type checking

## Development Commands

### Setup
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Generate version info (required before install or tests)
python scripts/generate_version.py
```

### Testing
```bash
# Run all tests with coverage
pytest -v --cov --cov-report=term

# Run specific test file
pytest tests/unit/test_filters.py -v

# Run specific test function
pytest tests/unit/test_filters.py::test_parse_filter -v

# Run integration tests only
pytest tests/integration/ -v
```

### Linting & Type Checking
```bash
# Check code style
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type check
mypy src/
```

### Database Migrations
```bash
# Create new migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Running the CLI
```bash
# After installation
task-ng <command>

# Or during development
python -m taskng.cli.main <command>
```

## Architecture

### Layered Architecture

```
CLI Layer (Typer commands)
    ↓
Core Domain Layer (Business logic, filters, urgency, recurrence)
    ↓
Storage Layer (SQLite + Repository pattern)
    ↓
Configuration Layer (TOML config)
```

### Key Directories

- **`src/taskng/cli/`** - Typer commands and CLI infrastructure
  - `main.py` - Entry point with Typer app definition
  - `commands/` - Individual command implementations
  - `output.py` - JSON vs Rich output modes
  - `display.py` - Styling and formatting functions
  - `error_handler.py` - Centralized error handling

- **`src/taskng/core/`** - Domain logic (pure Python, no I/O)
  - `models.py` - Pydantic models (Task, Priority, TaskStatus)
  - `filters.py` - Filter parsing and SQL generation
  - `urgency.py` - Urgency score calculation
  - `recurrence.py` - Recurring task logic
  - `virtual_tags.py` - Computed tags (OVERDUE, BLOCKED, etc.)
  - `dependencies.py` - Task dependency management
  - `reports.py` - Named report definitions
  - `boards.py` - Kanban board definitions

- **`src/taskng/storage/`** - Data persistence
  - `database.py` - SQLite connection management
  - `schema.py` - Table definitions
  - `repository.py` - Data access layer (Repository pattern)
  - `migrations/` - Alembic migration scripts

- **`src/taskng/config/`** - Configuration management
  - `settings.py` - Config loading (TOML + env vars)
  - `defaults.py` - Default configuration values

- **`src/taskng/sync/`** - Sync functionality (Git backend)
  - `engine.py` - Sync orchestration
  - `conflict.py` - Field-level conflict resolution
  - `backends/git.py` - Git-based sync backend

### Data Flow

1. **Command Input** → CLI parses command via Typer
2. **Filter Processing** → `FilterParser` converts to SQL WHERE clause
3. **Database Query** → `TaskRepository` executes parameterized queries
4. **Domain Logic** → Apply urgency calculation, virtual tags, etc.
5. **Storage Write** → Transaction committed, history recorded for undo
6. **Output** → Rich tables/JSON output depending on `--json` flag

### Filter Engine

The filter engine (`core/filters.py`) is central to the architecture:
- Parses Taskwarrior-compatible syntax: `project:Work +urgent priority:H`
- Compiles basic filters to SQL for database-level filtering
- Applies virtual tags (computed) in Python after query
- Supports in-memory filtering via `matches_task()` for multi-pass scenarios

### Virtual Tags

Virtual tags are computed attributes used in filtering:
- **Time-based**: `OVERDUE`, `TODAY`, `WEEK`, `MONTH`
- **Status**: `PENDING`, `COMPLETED`, `WAITING`
- **Priority**: `H`, `M`, `L`
- **Dependency**: `BLOCKED`, `READY`
- **Metadata**: `TAGGED`, `ANNOTATED`, `ATTACHED`, `PROJECT`, `RECURRING`, `ACTIVE`

See `core/virtual_tags.py` for implementation.

### Database Schema

Core tables (see `storage/schema.py`):
- **tasks** - Main task data with all fields
- **tags** - Normalized many-to-many tags
- **dependencies** - Task dependency relationships
- **annotations** - Timestamped notes
- **uda_values** - User-defined attributes
- **task_history** - Audit trail for undo support
- **attachments** - File attachment metadata (v0.1.4+)

All tables use `task_uuid` foreign keys with `ON DELETE CASCADE`.

## Important Implementation Details

### Version Management

Version is defined in `pyproject.toml` and should be the single source of truth. The `_version_info.py` file is **auto-generated** by `scripts/generate_version.py` during build/CI and contains git commit details. Never edit `_version_info.py` manually.

### Test Isolation

All tests use automatic fixtures from `tests/conftest.py`:
- `isolate_test_data` - Creates temp database per test
- `reset_json_mode` - Resets JSON output mode
- `reset_context` - Clears context state
- `cli_runner` - Typer CLI test runner
- `temp_db` - Initialized temporary database
- `task_repo` - Repository instance with temp db

Tests NEVER touch production data.

### Date Parsing

Natural language date parsing uses `dateparser` library via `core/dates.py`:
```python
parse_date("tomorrow")     # → datetime
parse_date("next friday")  # → datetime
parse_date("in 3 days")    # → datetime
```

### Urgency Calculation

Urgency is a weighted score calculated by `core/urgency.py`:
- Priority: H=6.0, M=3.9, L=1.8
- Due date: overdue=12.0, today=8.0, week=4.0
- Has project: +1.0
- Per tag: +0.5
- Age: +0.01/day (max 2.0)
- Blocked: ×0.5

All coefficients are configurable via `urgency.*` settings.

### Recurrence Engine

When completing a recurring task:
1. Task status → `completed`, `end` timestamp set
2. `core/recurrence.py` calculates next due date
3. New task created with `parent_uuid` pointing to template
4. Continues until `until` date (if specified)

### Error Handling

Use custom exceptions from `core/exceptions.py`:
- `TaskNotFoundError`
- `InvalidFilterError`
- `CircularDependencyError`
- `ConfigError`
- `SyncError`, `SyncNotInitializedError`

The `cli/error_handler.py` provides user-friendly messages.

### Output Modes

Commands support two output modes:
- **Rich mode** (default): Colored tables via Rich library
- **JSON mode** (`--json`): Serialized Pydantic models for scripting

Use `output.py` helpers: `output_task()`, `output_tasks()`, `output_success()`.

### Sync System

The sync system (`src/taskng/sync/`) provides:
- **Pluggable backends** (Git implemented, others possible)
- **Field-level conflict resolution** - merges field-by-field, not task-level
- **History tracking** - Uses `task_history` table to track changes
- **Content-addressed storage** - Attachments stored by SHA-256 hash

The Git backend stores tasks as individual JSON files, one per UUID.

### Attachment System (v0.1.4+)

File attachments use content-addressed storage:
- Files stored in `attachments/` directory by SHA-256 hash
- Database tracks metadata: filename, hash, size, MIME type
- Deduplication: identical files share storage
- Configurable file size limit (default 100MB) via `attachment.max_size`
- Visual indicator in list view (📎 emoji or `[A:count]`)
- Virtual tag `ATTACHED` for filtering tasks with attachments

Commands:
```bash
# Attach files to a task
task-ng attachment add <task-id> <file> [<file>...]

# List attachments for a task
task-ng attachment list <task-id>

# Remove attachment by index or filename
task-ng attachment remove <task-id> <index|filename>
task-ng attachment remove <task-id> --all

# Open attachment with default application
task-ng attachment open <task-id> <index|filename>

# Export attachment to filesystem
task-ng attachment save <task-id> <index|filename> [destination]

# Filter tasks by attachments
task-ng list +ATTACHED      # Tasks with attachments
task-ng list -ATTACHED       # Tasks without attachments
```

Features:
- Duplicate filename warnings with confirmation
- File size validation with helpful error messages
- Content-addressed storage prevents duplication
- Files retained in storage even when detached from tasks

See `core/attachments.py` and `cli/commands/attach.py` for implementation.

## Common Patterns

### Adding a New Command

1. Create `src/taskng/cli/commands/your_command.py`
2. Define Typer command with type hints
3. Import and register in `cli/main.py`
4. Use `cli_runner` fixture for testing
5. Add integration test in `tests/integration/`

### Adding a New Filter Attribute

1. Update `core/filters.py` to recognize the attribute
2. Update `FilterParser.to_sql()` to generate SQL
3. Add tests in `tests/unit/test_filters.py`

### Adding a Database Migration

1. Run `alembic revision -m "description"`
2. Edit the generated file in `storage/migrations/versions/`
3. Implement `upgrade()` and `downgrade()`
4. Test with `alembic upgrade head` and `alembic downgrade -1`

### Modifying Task Model

If adding fields to `core/models.py`:
1. Update Pydantic model
2. Create Alembic migration for schema
3. Update `storage/repository.py` CRUD methods
4. Update relevant commands
5. Add tests

## CI/CD

GitLab CI pipeline (`.gitlab-ci.yml`):
- **Lint stage**: ruff check, ruff format, mypy
- **Test stage**: pytest on Python 3.11, 3.12, 3.13
- **Security stage**: bandit, safety checks
- **Coverage stage**: >80% required
- **Deploy stage**: PyPI publishing on tags

## Documentation

Refer users to:
- `docs/USER_GUIDE.md` - End-user documentation
- `docs/ARCHITECTURE.md` - Detailed technical architecture (more comprehensive than this file)
- `README.md` - Quick start and screenshots

## Configuration Precedence

1. Defaults (`config/defaults.py`)
2. Config file (`~/.config/taskng/config.toml`)
3. Environment variables (`TASKNG_*`)
4. CLI flags (`--config`, `--data-dir`)

## Notes

- **Pydantic v2** is used - use `model_config = ConfigDict(from_attributes=True)` pattern
- **SQLite WAL mode** enabled for better concurrency
- All SQL queries use **parameterized queries** to prevent injection
- The repository uses **soft deletes** - tasks marked as `deleted`, not removed
- **History tracking** enables the `undo` command
