import typer
from .database import DatabaseManager
from .models import Task
from .tui import TodoApp
from pathlib import Path
from typing import Optional

app = typer.Typer()

DEFAULT_DB_PATH = Path.home() / ".mercedtodo" / "tasks.db"

@app.command()
def run(path: Path = typer.Option(DEFAULT_DB_PATH, "--path", "-p")):
    """
    Launch the MercedTodo TUI.
    """
    # Ensure DB is ready
    db = DatabaseManager(path)
    tui = TodoApp(db)
    tui.run()

@app.command()
def export(
    output: Path = typer.Option(Path("tasks_export.md"), "--output", "-o"),
    path: Path = typer.Option(DEFAULT_DB_PATH, "--path", "-p")
):
    """
    Export all tasks to a Markdown file.
    """
    db = DatabaseManager(path)
    tasks = db.get_tasks()
    
    with open(output, "w", encoding="utf-8") as f:
        f.write("# Exported Tasks\n\n")
        if not tasks:
            f.write("_No tasks found._\n")
            
        current_category = None
        # Sort by category then id
        sorted_tasks = sorted(tasks, key=lambda t: (t.category, t.id))
        
        for task in sorted_tasks:
            if task.category != current_category:
                f.write(f"## {task.category}\n\n")
                current_category = task.category
                
            status = "x" if task.status == "Complete" else " "
            f.write(f"- [{status}] {task.title}\n")
            if task.notes:
                # Indent notes
                formatted_notes = task.notes.replace('\n', '\n  > ')
                f.write(f"  > {formatted_notes}\n")
            f.write("\n")
            
    typer.echo(f"Exported {len(tasks)} tasks to {output}")

@app.command("import")
def import_tasks(
    file: Path = typer.Argument(..., help="Path to JSON or todo.txt file"),
    path: Path = typer.Option(DEFAULT_DB_PATH, "--path", "-p")
):
    """
    Import tasks from a JSON or todo.txt file.
    """
    from .logic import ImportManager
    
    db = DatabaseManager(path)
    count = 0
    if file.suffix == ".json":
        count = ImportManager.import_from_json(db, file)
    elif file.suffix == ".txt":
        count = ImportManager.import_from_todotxt(db, file)
    else:
        typer.echo(f"Unsupported file format: {file.suffix}")
        raise typer.Exit(code=1)
        
    typer.echo(f"Imported {count} tasks.")

@app.command()
def sync(
    target: str = typer.Option(..., "--target", "-t", help="Sync target (local location or 's3' placeholder)"),
    path: Path = typer.Option(DEFAULT_DB_PATH, "--path", "-p")
):
    """
    Simulate syncing tasks to a target location.
    """
    # Placeholder for real sync logic
    import shutil
    
    if target == "s3":
        typer.echo("S3 sync not implemented yet (requires boto3 config)")
        return

    # Treat target as local folder
    target_path = Path(target)
    target_path.mkdir(parents=True, exist_ok=True)
    
    db_file = path
    if db_file.exists():
        shutil.copy2(db_file, target_path / db_file.name)
        typer.echo(f"Synced DB to {target_path}")
    else:
        typer.echo("Database not found.")

if __name__ == "__main__":
    app()
