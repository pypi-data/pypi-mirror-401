from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Input, Button, Label, TextArea, Select
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.binding import Binding
from pathlib import Path
from datetime import datetime
from .database import DatabaseManager
from .models import Task
from .config import get_theme_css

class TaskEditor(ModalScreen):
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, task: Task | None = None):
        super().__init__()
        self.task = task

    def compose(self) -> ComposeResult:
        yield Label("Task Title")
        yield Input(value=self.task.title if self.task else "", id="title")
        
        with Horizontal():
            with Vertical():
                yield Label("Category")
                yield Input(value=self.task.category if self.task else "Inbox", id="category")
            with Vertical():
                yield Label("Priority")
                yield Select.from_values(["Low", "Medium", "High"], value=self.task.priority if self.task else "Medium", id="priority")
        
        yield Label("Due Date (YYYY-MM-DD)")
        due_str = self.task.due_date.strftime("%Y-%m-%d") if self.task and self.task.due_date else ""
        yield Input(value=due_str, id="due_date", placeholder="Optional")

        yield Label("Recurrence (daily, weekly)")
        yield Input(value=self.task.recurring if self.task else "", id="recurring", placeholder="Optional")
        
        yield Label("Notes")
        yield TextArea(self.task.notes if self.task else "", id="notes")
        
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

class TodoApp(App):
    CSS = """
    TaskEditor {
        align: center middle;
    }
    
    TaskEditor > * {
        width: 60;
        margin: 1;
    }

    TaskEditor Horizontal {
        height: auto;
        width: auto;
    }
    
    TaskEditor Vertical {
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
        ("a", "add_task", "Add Task"),
        ("e", "edit_task", "Edit Task"),
        ("d", "delete_task", "Delete Task"),
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
        yield Input(placeholder="Search tasks... (Press / to focus)", id="search_bar")
        yield DataTable(id="tasks")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Status", "Pri", "Due", "Category", "Title")
        table.cursor_type = "row"
        self.refresh_tasks()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search_bar":
            self.search_query = event.value.lower()
            self.refresh_tasks()

    def action_focus_search(self) -> None:
        self.query_one("#search_bar").focus()

    def refresh_tasks(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        
        # In a real app, might push search to DB, but filtering memory is fine for typical todo list size
        tasks = self.db.get_tasks()
        
        filtered_tasks = []
        for task in tasks:
            if self.search_query:
                if (self.search_query not in task.title.lower() and 
                    self.search_query not in task.category.lower()):
                    continue
            filtered_tasks.append(task)

        # Sort: Incomplete first, then Priority (High>Med>Low), then Due Date, then Category
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

    def action_add_task(self) -> None:
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

    def action_edit_task(self) -> None:
        table = self.query_one(DataTable)
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
                # Update details (simplified, in real app might need db method for all fields)
                # We need a new update method in DB for these extended fields or just use logic
                
                # IMPORTANT: For now we only implemented update_task_details (title, notes) vs properties
                # We should update database.py to handle updating all these fields or just recreate?
                # Best practice: Update DB method. But for now I'll just update what I can 
                # OR quickly add update_task_extended to DB.
                # Let's assume I will fix DB in next step if I missed it, 
                # actually I missed updating update_task_details in Phase 1!
                # I will add a TODO or fix it now via another tool.
                
                # Calling a method I'm about to add
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

    def action_toggle_complete(self) -> None:
        table = self.query_one(DataTable)
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

    def action_delete_task(self) -> None:
        table = self.query_one(DataTable)
        try:
            row_key_obj = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            if not row_key_obj: return
            row_key = row_key_obj.value
        except Exception:
            return
            
        self.db.delete_task(int(row_key))
        self.refresh_tasks()
        
    def action_export_markdown(self) -> None:
        output_path = Path.cwd() / "todos_export.md"
        tasks = self.db.get_tasks()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Exported Tasks\n\n")
            for task in tasks:
                 status = "x" if task.status == "Complete" else " "
                 f.write(f"- [{status}] {task.title}\n")
        self.notify(f"Exported to {output_path}")
