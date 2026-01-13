# Architecture Documentation

## Overview
MercedTodo is a Python application primarily driven by `Textual` for the TUI and `Typer` for the CLI entry point. It uses `SQLite` for local data persistence.

## Core Components

### 1. Data Layer (`database.py`, `models.py`)
- **DatabaseManager**: Handles the SQLite connection and schema migration.
- **Task Model**: A unified dataclass representing a Todo item.
- **Schema**:
    - `tasks` table: `id`, `title`, `category`, `status`, `notes`, `created_at`.
    - **Extensions**: `priority`, `due_date`, `recurring`, `archived`.

### 2. Application Layer (`tui.py`, `logic.py`, `config.py`)
- **TodoApp**: Subclass of `textual.app.App`.
    - Manages the main event loop and screen stack.
    - **Search**: Real-time filtering in memory.
- **TaskBrowser**: The primary dashboard. Columns updated for Priority/Due Date.
- **TaskEditor**: Form for creating/updating details (Priority Select, Date Input).
- **Logic Modules**:
    - `RecurringManager`: Handles logic for next-task generation.
    - `ImportManager`: parsers for JSON/Todo.txt.
    - `Config`: Loads TOML preferences.


### 3. CLI Layer (`cli.py`, `__main__.py`)
- **Typer App**: Parses command line arguments.
- **Commands**:
    - `run`: Initializes `TodoApp`.
    - `export`: Direct call to `DatabaseManager` to format and write Markdown.

## Design Decisions
- **Separation of Concerns**: The `DatabaseManager` is agnostic of the TUI/CLI. It can be reused by other interfaces.
- **Zero Config**: Defaults to `~/.mercedtodo` but allows overrides via flags.
