from mercedtodo.models import Task

from datetime import datetime

def test_add_task_extended(db_manager):
    now = datetime.now()
    task = db_manager.add_task(
        "Buy Milk", 
        "Personal", 
        "2%", 
        priority="High", 
        due_date=now,
        recurring="daily"
    )
    assert task.title == "Buy Milk"
    assert task.priority == "High"
    assert task.due_date is not None
    assert task.recurring == "daily"
    assert task.archived is False

def test_get_tasks(db_manager):
    db_manager.add_task("Task 1")
    db_manager.add_task("Task 2", category="Work")
    
    tasks = db_manager.get_tasks()
    assert len(tasks) == 2
    
    work_tasks = db_manager.get_tasks(category="Work")
    assert len(work_tasks) == 1
    assert work_tasks[0].title == "Task 2"

def test_archive_task(db_manager):
    task = db_manager.add_task("Task 1")
    db_manager.archive_task(task.id)
    
    # default get_tasks should not show archived
    tasks = db_manager.get_tasks()
    assert len(tasks) == 0
    
    # explicit include_archived
    all_tasks = db_manager.get_tasks(include_archived=True)
    assert len(all_tasks) == 1
    assert all_tasks[0].archived is True

def test_update_status(db_manager):
    task = db_manager.add_task("Task 1")
    db_manager.update_task_status(task.id, "Complete")
    
    tasks = db_manager.get_tasks()
    assert tasks[0].status == "Complete"

def test_delete_task(db_manager):
    task = db_manager.add_task("Task 1")
    db_manager.delete_task(task.id)
    assert len(db_manager.get_tasks()) == 0
