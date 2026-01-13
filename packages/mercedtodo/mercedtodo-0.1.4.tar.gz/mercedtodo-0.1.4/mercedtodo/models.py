from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    category: str
    status: str
    notes: str
    created_at: datetime
    due_date: Optional[datetime] = None
    priority: str = "Medium"
    recurring: Optional[str] = None
    archived: bool = False

@dataclass
class Note:
    id: int
    title: str
    content: str
    category: str
    created_at: datetime

