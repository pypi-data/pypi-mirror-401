from datetime import datetime, timedelta
from mercedtodo.logic import RecurringManager, UndoManager, Command
from mercedtodo.database import DatabaseManager

def test_recurring_daily(db_manager):
    now = datetime.now()
    task = db_manager.add_task("Daily Standup", "Work", recurring="daily", due_date=now)
    
    # Simulate completion
    db_manager.update_task_status(task.id, "Complete")
    next_task = RecurringManager.handle_completion(db_manager, task)
    
    assert next_task is not None
    assert next_task.title == "Daily Standup"
    assert next_task.status == "Pending"
    # Check if due date is roughly tomorrow (ignoring seconds diff)
    assert next_task.due_date.date() == (now + timedelta(days=1)).date()

def test_recurring_weekly(db_manager):
    now = datetime.now()
    task = db_manager.add_task("Weekly Report", "Work", recurring="weekly", due_date=now)
    
    next_task = RecurringManager.handle_completion(db_manager, task)
    assert next_task is not None
    assert next_task.due_date.date() == (now + timedelta(weeks=1)).date()

def test_undo_manager():
    # Mock command
    class AddCommand(Command):
        def __init__(self, val_list, val):
            self.val_list = val_list
            self.val = val
        def execute(self):
            self.val_list.append(self.val)
        def undo(self):
            self.val_list.remove(self.val)
            
    my_list = []
    manager = UndoManager()
    
    cmd = AddCommand(my_list, 1)
    manager.execute(cmd)
    assert my_list == [1]
    
    manager.undo()
    assert my_list == []

def test_import_json(db_manager, tmp_path):
    import json
    from mercedtodo.logic import ImportManager
    
    data = [
        {"title": "Imported Task 1", "category": "Work", "priority": "High"},
        {"title": "Imported Task 2"}
    ]
    json_file = tmp_path / "import.json"
    with open(json_file, 'w') as f:
        json.dump(data, f)
        
    count = ImportManager.import_from_json(db_manager, json_file)
    assert count == 2
    tasks = db_manager.get_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Imported Task 1"
    assert tasks[0].priority == "High"

def test_import_todotxt(db_manager, tmp_path):
    from mercedtodo.logic import ImportManager
    
    content = """
(A) High priority task +Work
Normal task +Personal
(C) Low task
    """
    txt_file = tmp_path / "todo.txt"
    with open(txt_file, 'w') as f:
        f.write(content.strip())
        
    count = ImportManager.import_from_todotxt(db_manager, txt_file)
    assert count == 3
    
    tasks = db_manager.get_tasks() # id 1, 2, 3
    # Check High priority
    t1 = next(t for t in tasks if "High" in t.title)
    assert t1.priority == "High"
    assert t1.category == "Work"
    # Check Low/default
    t3 = next(t for t in tasks if "Low" in t.title)
    assert t3.priority == "Low"

