import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from .models import Task

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'Inbox',
                status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Complete')),
                notes TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                priority TEXT DEFAULT 'Medium',
                recurring TEXT,
                archived INTEGER DEFAULT 0
            )
        """)
        # Migration logic for existing tables
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "due_date" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP")
        if "priority" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'")
        if "recurring" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN recurring TEXT")
        if "archived" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN archived INTEGER DEFAULT 0")

        conn.commit()
        conn.close()

    def _row_to_task(self, row) -> Task:
        # Handle potential missing columns if select * returns differently in older versions (though schema is updated)
        # We assume SELECT * returns columns in order of creation + added columns
        # id(0), title(1), category(2), status(3), notes(4), created(5), due(6), priority(7), recurring(8), archived(9)
        return Task(
            id=row[0],
            title=row[1],
            category=row[2],
            status=row[3],
            notes=row[4],
            created_at=row[5] if isinstance(row[5], datetime) else datetime.fromisoformat(str(row[5])),
            due_date=row[6] if row[6] else None,
            priority=row[7] if len(row) > 7 else "Medium",
            recurring=row[8] if len(row) > 8 else None,
            archived=bool(row[9]) if len(row) > 9 else False
        )

    def add_task(self, title: str, category: str = "Inbox", notes: str = "", 
                 priority: str = "Medium", due_date: Optional[datetime] = None, 
                 recurring: Optional[str] = None) -> Task:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, category, notes, priority, due_date, recurring) VALUES (?, ?, ?, ?, ?, ?)",
            (title, category, notes, priority, due_date, recurring)
        )
        task_id = cursor.lastrowid
        conn.commit()
        
        # Fetch the created task to get the correct timestamp
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        return self._row_to_task(row)

    def get_tasks(self, category: Optional[str] = None, status: Optional[str] = None, include_archived: bool = False) -> List[Task]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if not include_archived:
            query += " AND archived = 0"
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if status:
            query += " AND status = ?"
            params.append(status)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def archive_task(self, task_id: int):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET archived = 1 WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    def update_task_status(self, task_id: int, status: str):
        if status not in ("Pending", "Complete"):
            raise ValueError("Invalid status")
            
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        conn.close()
        
    def update_task_details(self, task_id: int, title: str, notes: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, notes = ? WHERE id = ?", (title, notes, task_id))
        conn.commit()
        conn.close()

    def update_task_full(self, task_id: int, title: str, category: str, notes: str, 
                        priority: str, due_date: Optional[datetime], recurring: Optional[str]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks 
            SET title = ?, category = ?, notes = ?, priority = ?, due_date = ?, recurring = ? 
            WHERE id = ?
        """, (title, category, notes, priority, due_date, recurring, task_id))
        conn.commit()
        conn.close()


    def delete_task(self, task_id: int):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
