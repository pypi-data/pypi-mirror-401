from datetime import datetime, timedelta
from typing import Optional, List, Any, Callable
from .database import DatabaseManager
from .models import Task

class RecurringManager:
    """Handles logic for creating the next instance of a recurring task."""
    
    @staticmethod
    def handle_completion(db: DatabaseManager, task: Task) -> Optional[Task]:
        if not task.recurring or not task.due_date:
            return None
            
        # Simple recurrence logic: daily, weekly
        # For more complex cron-like logic, a library like 'croniter' would be needed,
        # but for now we stick to simple keywords as per requirements "daily, weekly"
        
        new_due_date = None
        recurring_lower = task.recurring.lower()
        
        if recurring_lower == "daily":
            new_due_date = task.due_date + timedelta(days=1)
        elif recurring_lower == "weekly":
            new_due_date = task.due_date + timedelta(weeks=1)
        else:
            # Fallback or unknown format
            return None
            
        # Create next task
        return db.add_task(
            title=task.title,
            category=task.category,
            notes=task.notes,
            priority=task.priority,
            due_date=new_due_date,
            recurring=task.recurring
        )

class Command:
    """Abstract command for Undo/Redo."""
    def execute(self):
        pass
    def undo(self):
        pass

class UndoManager:
    def __init__(self):
        self._history: List[Command] = []
        
    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
        
    def undo(self):
        if not self._history:
            return
        command = self._history.pop()
        command.undo()

import json
from pathlib import Path

class ImportManager:
    @staticmethod
    def import_from_json(db: DatabaseManager, file_path: Path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Expect list of dicts
            count = 0
            for item in data:
                # Basic validation
                if "title" in item:
                    db.add_task(
                        title=item.get("title"),
                        category=item.get("category", "Inbox"),
                        notes=item.get("notes", ""),
                        priority=item.get("priority", "Medium"),
                        # Date parsing omitted for brevity in this simple import
                        recurring=item.get("recurring"),
                    )
                    count += 1
            return count

    @staticmethod
    def import_from_todotxt(db: DatabaseManager, file_path: Path):
        # Very basic todo.txt parser: (A) Task +Project @Context
        count = 0
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                priority = "Medium"
                if line.startswith("(") and line[2] == ")":
                    p_char = line[1]
                    if p_char == "A": priority = "High"
                    elif p_char == "B": priority = "Medium"
                    else: priority = "Low"
                    line = line[4:] # Remove priority marker
                
                # Extract project as category (take first +Project)
                category = "Inbox"
                words = line.split()
                clean_words = []
                for word in words:
                    if word.startswith("+"):
                        if category == "Inbox": category = word[1:]
                        # Keep word in title? standard todo.txt says yes
                    clean_words.append(word)
                
                title = " ".join(clean_words)
                db.add_task(title=title, category=category, priority=priority)
                count += 1
        return count

