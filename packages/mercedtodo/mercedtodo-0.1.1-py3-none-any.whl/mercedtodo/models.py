from dataclasses import dataclass
from datetime import datetime

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

