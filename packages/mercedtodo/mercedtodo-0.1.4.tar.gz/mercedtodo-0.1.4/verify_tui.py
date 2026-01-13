
from mercedtodo.tui import TaskEditor
from mercedtodo.models import Task
import sys

print("Verifying TaskEditor instantiation...")
try:
    # Test 1: Instantiate without task
    editor = TaskEditor()
    print("SUCCESS: TaskEditor() instantiated.")

    # Test 2: Instantiate with task (mock object)
    # We can mock Task since it's a dataclass
    from datetime import datetime
    t = Task(id=1, title="Test", category="Inbox", status="Pending", notes="", created_at=datetime.now())
    editor_with_task = TaskEditor(task=t)
    print("SUCCESS: TaskEditor(task=t) instantiated.")
    
except AttributeError as e:
    print(f"FAILURE: AttributeError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"FAILURE: Unexpected Error: {e}")
    sys.exit(1)

print("All TUI Verification tests passed.")
