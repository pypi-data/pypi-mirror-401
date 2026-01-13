import pytest
from pathlib import Path
from mercedtodo.database import DatabaseManager

@pytest.fixture
def tmp_db_path(tmp_path):
    return tmp_path / "test_todos.db"

@pytest.fixture
def db_manager(tmp_db_path):
    return DatabaseManager(tmp_db_path)
