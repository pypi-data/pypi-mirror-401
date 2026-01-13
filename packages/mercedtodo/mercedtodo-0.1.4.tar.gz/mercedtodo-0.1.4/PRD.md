# Product Requirements Document: mercedtodo

## 1. Overview
`mercedtodo` is a Python-based CLI application that allows users to track todo items across different categories. It features a Terminal User Interface (TUI) for browsing tasks, adding notes, and marking tasks as complete.

## 2. User Stories
- As a user, I want to keep my todos organized by custom categories (e.g., Work, Personal, Project X).
- As a user, I want to launch a visual interface (TUI) to interactively browse my list.
- As a user, I want to add detailed notes to a specific todo item within the TUI.
- As a user, I want to easily toggle the completion status of a todo.
- As a user, I want to specific a custom directory for my data so I can manage different lists or sync them.
- As a user, I want to set due dates and priorities for my tasks.
- As a user, I want to have recurring tasks (e.g., daily standup) created automatically.
- As a user, I want to undo accidental changes.
- As a user, I want to customize the colors (themes).
- As a user, I want to sync my data to the cloud (Gist/S3).
- As a user, I want to archive old tasks without deleting them.

## 3. Functional Requirements

### 3.1 CLI Entry Point
- **Command Name**: `mercedtodo`
- **Arguments**:
    - `--path`, `-p`: Path to the data directory. Defaults to `~/.mercedtodo`.
    - `export`: Export all tasks and notes to a markdown file.
        - `--output`, `-o`: Output file path (default: `tasks_export.md`).
    - *Optional (Future)*: Quick-add arguments (e.g., `mercedtodo add "Buy milk"`).

### 3.2 Data Management
- **Storage**: JSON or SQLite database stored in the specified path.
- **Default Location**: `~/.mercedtodo/tasks.json` (or `.db`).
- **Data Model**:
    - `id`: Unique Identifier (UUID or Auto-inc).
    - `title`: String (Summary of task).
    - `category`: String (Default: "Inbox").
    - `status`: Enum (Pending, Complete, Archived).
    - `notes`: Text (Markup support optional).
    - `created_at`: Timestamp.
    - `due_date`: Timestamp (Optional).
    - `priority`: Enum (Low, Medium, High).
    - `recurring`: String (e.g., "daily", "weekly", or cron string) - Optional.

### 3.3 Terminal User Interface (TUI)
- **Library**: Recommended `Textual` (for modern, rich TUI) or `Rich` + `Prompt_toolkit`.
- **Views**:
    - **Dashboard/List View**:
        - List columns: Status (Checkmark/X), Priority (Color-coded), Due Date, Title, Category.
        - Navigation: Keyboard (Arrow keys, Vim bindings j/k).
        - Filtering: Filter by Category, Status, or Text Search (Ctrl+P/Context).
    - **Detail/Edit View**:
        - Opened by selecting a task.
        - Editable fields: Title, Notes (Multi-line text area), Priority, Due Date, Recurrence.
        - Actions: Save, Cancel, Delete, Toggle Complete, Export to Markdown, Archive.
- **Global Actions**:
    - `add`: Open a modal/form to create a new task.
    - `quit`: Exit the application.
    - `export`: Trigger export of current view/selection to Markdown.
    - `undo`: Indicated by hotkey (Ctrl+Z) to revert last action.
    - `sync`: Manually trigger cloud sync.

### 3.4 Configuration
- Support for config file (e.g., `~/.mercedtodo/config.toml`) to persist default paths, theme preferences (colors), and sync credentials.

### 3.5 Advanced Features
- **Import**: Support importing from `todo.txt` or JSON.
- **Cloud Sync**: Simple push/pull mechanism to a configured Endpoint (S3 Bucket or Gist).
- **Undo/Redo**: In-memory stack of actions (Add, Update, Delete) to allow reversion.

## 4. Non-Functional Requirements
- **Performance**: Startup time < 500ms.
- **Compatibility**: Cross-platform (Windows, macOS, Linux).
- **Usability**: Intuitive keyboard navigation.

## 5. Technical Stack Proposal
- **Language**: Python 3.10+
- **TUI Framework**: `Textual` (Robust, reactive, modern look).
- **Data Layer**: `tinydb` (Simple JSON store) or `sqlite3` (Built-in, robust).
- **CLI Framework**: `Typer` (Modern, easy API).

## 6. Milestones
1. **Core Setup**: Project structure, storage logic, Typer CLI shell.
2. **Basic TUI**: Read-only list view of tasks.
3. **Interactive TUI**: Add, Edit (Notes), Toggle Complete.
4. **Categories**: Filtering and grouping by category.
5. **Polish**: Persistence of user preferences (path), keybindings, styling.
