from typer.testing import CliRunner
from mercedtodo.cli import app
from mercedtodo.database import DatabaseManager

runner = CliRunner()

def test_export_command(tmp_path):
    db_file = tmp_path / "test.db"
    db = DatabaseManager(db_file)
    db.add_task("Buy Milk", "Personal", "Need 2%")
    
    output_file = tmp_path / "export.md"
    
    result = runner.invoke(app, ["export", "--path", str(db_file), "--output", str(output_file)])
    assert result.exit_code == 0
    assert "Exported 1 tasks" in result.stdout
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Buy Milk" in content
    assert "Need 2%" in content
    assert "Personal" in content

def test_export_empty(tmp_path):
    db_file = tmp_path / "empty.db"
    output_file = tmp_path / "empty_export.md"
    
    result = runner.invoke(app, ["export", "--path", str(db_file), "--output", str(output_file)])
    assert result.exit_code == 0
    content = output_file.read_text(encoding="utf-8")
    assert "No tasks found" in content
