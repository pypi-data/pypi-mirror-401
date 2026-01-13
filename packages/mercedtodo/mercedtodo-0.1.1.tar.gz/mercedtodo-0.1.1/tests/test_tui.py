import pytest
from mercedtodo.tui import TodoApp
from mercedtodo.database import DatabaseManager

@pytest.mark.asyncio
async def test_app_startup(tmp_path):
    # Using tmp_path fixture from pytest
    db_path = tmp_path / "test_tui.db"
    db = DatabaseManager(db_path)
    app = TodoApp(db)
    async with app.run_test() as pilot:
        assert app.is_running
        # Check if table exists
        assert app.query("DataTable")
        await pilot.exit(None)
