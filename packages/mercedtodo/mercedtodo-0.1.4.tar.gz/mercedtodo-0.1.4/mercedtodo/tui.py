from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Input, Button, Label, TextArea, Select, TabbedContent, TabPane
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.binding import Binding
from pathlib import Path
from datetime import datetime
from .database import DatabaseManager
from .models import Task, Note
from .config import get_theme_css

class TaskEditor(ModalScreen):
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, task: Task | None = None):
        super().__init__()
        self.todo_task = task

    def compose(self) -> ComposeResult:
        yield Label("Task Title")
        yield Input(value=self.todo_task.title if self.todo_task else "", id="title")
        
        with Horizontal():
            with Vertical():
                yield Label("Category")
                yield Input(value=self.todo_task.category if self.todo_task else "Inbox", id="category")
            with Vertical():
                yield Label("Priority")
                yield Select.from_values(["Low", "Medium", "High"], value=self.todo_task.priority if self.todo_task else "Medium", id="priority")
        
        yield Label("Due Date (YYYY-MM-DD)")
        due_str = self.todo_task.due_date.strftime("%Y-%m-%d") if self.todo_task and self.todo_task.due_date else ""
        yield Input(value=due_str, id="due_date", placeholder="Optional")

        yield Label("Recurrence (daily, weekly)")
        yield Input(value=self.todo_task.recurring if self.todo_task else "", id="recurring", placeholder="Optional")
        
        yield Label("Notes")
        yield TextArea(self.todo_task.notes if self.todo_task else "", id="notes")
        
        with Horizontal():
            yield Button("Save", variant="primary", id="save")
            yield Button("Cancel", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "save":
            title = self.query_one("#title", Input).value
            category = self.query_one("#category", Input).value
            notes = self.query_one("#notes", TextArea).text
            priority = self.query_one("#priority", Select).value
            due_str = self.query_one("#due_date", Input).value
            recurring = self.query_one("#recurring", Input).value
            
            due_date = None
            if due_str:
                try:
                    due_date = datetime.strptime(due_str, "%Y-%m-%d")
                except ValueError:
                    pass # Ignore invalid date for now or show error

            self.dismiss({
                "title": title, 
                "category": category, 
                "notes": notes,
                "priority": priority,
                "due_date": due_date,
                "recurring": recurring or None
            })

class NoteEditor(ModalScreen):
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, note: Note | None = None):
        super().__init__()
        self.note = note

    def compose(self) -> ComposeResult:
        yield Label("Note Title")
        yield Input(value=self.note.title if self.note else "", id="note_title")
        
        yield Label("Category")
        yield Input(value=self.note.category if self.note else "General", id="note_category")
        
        yield Label("Content")
        yield TextArea(self.note.content if self.note else "", id="note_content")
        
        with Horizontal():
            yield Button("Save", variant="primary", id="save_note")
            yield Button("Cancel", variant="error", id="cancel_note")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel_note":
            self.dismiss(None)
        elif event.button.id == "save_note":
            title = self.query_one("#note_title", Input).value
            category = self.query_one("#note_category", Input).value
            content = self.query_one("#note_content", TextArea).text
            
            self.dismiss({
                "title": title,
                "category": category,
                "content": content
            })

class TodoApp(App):
    CSS = """
    TaskEditor, NoteEditor {
        align: center middle;
    }
    
    TaskEditor > *, NoteEditor > * {
        width: 60;
        margin: 1;
    }

    TaskEditor Horizontal, NoteEditor Horizontal {
        height: auto;
        width: auto;
    }
    
    TaskEditor Vertical, NoteEditor Vertical {
        height: auto;
    }

    #search_bar {
        dock: top;
        padding: 1;
        background: $panel;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add", "Add"),
        ("e", "edit", "Edit"),
        ("d", "delete", "Delete"),
        ("space", "toggle_complete", "Toggle Complete"),
        Binding("x", "export_markdown", "Export"),
        Binding("/", "focus_search", "Search"),
    ]

    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.search_query = ""
        # Inject user theme
        self.CSS += get_theme_css()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search... (Press / to focus)", id="search_bar")
        with TabbedContent():
            with TabPane("Tasks", id="tab_tasks"):
                yield DataTable(id="tasks_table")
            with TabPane("Notes", id="tab_notes"):
                yield DataTable(id="notes_table")
        yield Footer()

    def on_mount(self) -> None:
        tasks_table = self.query_one("#tasks_table", DataTable)
        tasks_table.add_columns("ID", "Status", "Pri", "Due", "Category", "Title")
        tasks_table.cursor_type = "row"

        notes_table = self.query_one("#notes_table", DataTable)
        notes_table.add_columns("ID", "Category", "Title", "Preview")
        notes_table.cursor_type = "row"
        
        self.refresh_data()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search_bar":
            self.search_query = event.value.lower()
            self.refresh_data()

    def action_focus_search(self) -> None:
        self.query_one("#search_bar").focus()

    def refresh_data(self) -> None:
        self.refresh_tasks()
        self.refresh_notes()

    def refresh_tasks(self) -> None:
        table = self.query_one("#tasks_table", DataTable)
        table.clear()
        
        tasks = self.db.get_tasks()
        
        filtered_tasks = []
        for task in tasks:
            if self.search_query:
                if (self.search_query not in task.title.lower() and 
                    self.search_query not in task.category.lower()):
                    continue
            filtered_tasks.append(task)

        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        
        filtered_tasks.sort(key=lambda t: (
            t.status == "Complete",
            priority_map.get(t.priority, 1),
            t.due_date or datetime.max, 
            t.category
        ))
        
        for task in filtered_tasks:
            status_icon = "✅" if task.status == "Complete" else "⭕"
            pri_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.priority, "⚪")
            due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
            
            table.add_row(
                str(task.id), 
                status_icon, 
                pri_icon, 
                due_str, 
                task.category, 
                task.title, 
                key=str(task.id)
            )

    def refresh_notes(self) -> None:
        table = self.query_one("#notes_table", DataTable)
        table.clear()
        
        notes = self.db.get_notes()
        
        filtered_notes = []
        for note in notes:
            if self.search_query:
                if (self.search_query not in note.title.lower() and 
                    self.search_query not in note.category.lower() and
                    self.search_query not in note.content.lower()):
                    continue
            filtered_notes.append(note)
            
        filtered_notes.sort(key=lambda n: (n.category, n.title))
        
        for note in filtered_notes:
            preview = (note.content[:50] + '...') if len(note.content) > 50 else note.content
            table.add_row(
                str(note.id),
                note.category,
                note.title,
                preview.replace('\n', ' '),
                key=str(note.id)
            )

    def action_add(self) -> None:
        tabs = self.query_one(TabbedContent)
        if tabs.active == "tab_tasks":
            self.add_task()
        else:
            self.add_note()

    def add_task(self) -> None:
        def handle_result(result):
            if result:
                self.db.add_task(
                    title=result["title"], 
                    category=result["category"], 
                    notes=result["notes"],
                    priority=result["priority"],
                    due_date=result["due_date"],
                    recurring=result["recurring"]
                )
                self.refresh_tasks()
        self.push_screen(TaskEditor(), handle_result)

    def add_note(self) -> None:
        def handle_result(result):
            if result:
                self.db.add_note(
                    title=result["title"],
                    content=result["content"],
                    category=result["category"]
                )
                self.refresh_notes()
        self.push_screen(NoteEditor(), handle_result)

    def action_edit(self) -> None:
        tabs = self.query_one(TabbedContent)
        if tabs.active == "tab_tasks":
            self.edit_task()
        else:
            self.edit_note()

    def edit_task(self) -> None:
        table = self.query_one("#tasks_table", DataTable)
        try:
            row_key_obj = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if not row_key_obj: return
            row_key = row_key_obj.value
        except Exception:
            return

        tasks = [t for t in self.db.get_tasks() if str(t.id) == row_key]
        if not tasks: return
        task = tasks[0]

        def handle_result(result):
            if result:
                self.db.update_task_full(
                    task.id, 
                    result["title"], 
                    result["category"], 
                    result["notes"],
                    result["priority"],
                    result["due_date"],
                    result["recurring"]
                )
                self.refresh_tasks()
        
        self.push_screen(TaskEditor(task), handle_result)

    def edit_note(self) -> None:
        table = self.query_one("#notes_table", DataTable)
        try:
            row_key_obj = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if not row_key_obj: return
            row_key = row_key_obj.value
        except Exception:
            return

        notes = [n for n in self.db.get_notes() if str(n.id) == row_key]
        if not notes: return
        note = notes[0]

        def handle_result(result):
            if result:
                self.db.update_note(
                    note.id,
                    result["title"],
                    result["content"],
                    result["category"]
                )
                self.refresh_notes()
        
        self.push_screen(NoteEditor(note), handle_result)

    def action_toggle_complete(self) -> None:
        tabs = self.query_one(TabbedContent)
        if tabs.active != "tab_tasks":
            return
            
        table = self.query_one("#tasks_table", DataTable)
        try:
            row_key_obj = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if not row_key_obj: return
            row_key = row_key_obj.value
        except Exception:
            return

        tasks = [t for t in self.db.get_tasks() if str(t.id) == row_key]
        if not tasks: return
        task = tasks[0]
        
        new_status = "Pending" if task.status == "Complete" else "Complete"
        self.db.update_task_status(task.id, new_status)
        self.refresh_tasks()

    def action_delete(self) -> None:
        tabs = self.query_one(TabbedContent)
        if tabs.active == "tab_tasks":
            self.delete_item(self.query_one("#tasks_table", DataTable), is_task=True)
        else:
            self.delete_item(self.query_one("#notes_table", DataTable), is_task=False)

    def delete_item(self, table: DataTable, is_task: bool) -> None:
        try:
            row_key_obj = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if not row_key_obj: return
            row_key = row_key_obj.value
        except Exception:
            return
            
        if is_task:
            self.db.delete_task(int(row_key))
            self.refresh_tasks()
        else:
            self.db.delete_note(int(row_key))
            self.refresh_notes()
        
    def action_export_markdown(self) -> None:
        output_path = Path.cwd() / "todos_export.md"
        tasks = self.db.get_tasks()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Exported Tasks\n\n")
            for task in tasks:
                 status = "x" if task.status == "Complete" else " "
                 f.write(f"- [{status}] {task.title}\n")
        self.notify(f"Exported to {output_path}")
