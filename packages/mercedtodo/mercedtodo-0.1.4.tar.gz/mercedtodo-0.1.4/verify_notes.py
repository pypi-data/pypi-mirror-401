
from mercedtodo.database import DatabaseManager
from mercedtodo.models import Note
from pathlib import Path
import os
import sqlite3

def verify_notes_functionality():
    db_path = Path("test_verify_notes.db")
    if db_path.exists():
        os.remove(db_path)
    
    print("Initializing DB...")
    db = DatabaseManager(db_path)
    
    # 1. Create a note
    print("Creating note...")
    note = db.add_note("My First Note", "This is content", "Personal")
    assert note.id is not None
    assert note.title == "My First Note"
    assert note.category == "Personal"
    print(f"Note created: {note}")

    # 2. Get notes
    print("Retrieving notes...")
    notes = db.get_notes()
    assert len(notes) == 1
    assert notes[0].title == "My First Note"
    print(f"Notes retrieved: {len(notes)}")
    
    # 3. Update note
    print("Updating note...")
    db.update_note(note.id, "Updated Title", "Updated Content", "Work")
    notes = db.get_notes()
    updated_note = notes[0]
    assert updated_note.title == "Updated Title"
    assert updated_note.content == "Updated Content"
    assert updated_note.category == "Work"
    print(f"Note updated: {updated_note}")

    # 4. Delete note
    print("Deleting note...")
    db.delete_note(note.id)
    notes = db.get_notes()
    assert len(notes) == 0
    print("Note deleted.")

    if db_path.exists():
        os.remove(db_path)
    print("Verification Successful!")

if __name__ == "__main__":
    verify_notes_functionality()
