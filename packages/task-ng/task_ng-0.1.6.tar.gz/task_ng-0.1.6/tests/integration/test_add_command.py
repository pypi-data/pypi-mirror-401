"""Integration tests for task add command."""

from pathlib import Path

from taskng.cli.main import app
from taskng.storage.database import Database
from taskng.storage.repository import TaskRepository


class TestAddCommand:
    """Integration tests for add command."""

    def test_add_simple_task(self, temp_db_path, cli_runner):
        """Should create a task with just a description."""
        result = cli_runner.invoke(app, ["add", "Buy groceries"])
        assert result.exit_code == 0
        assert "Created task 1" in result.output
        assert "Buy groceries" in result.output

        # Verify task was actually created in database
        db = Database(temp_db_path)
        repo = TaskRepository(db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].description == "Buy groceries"

    def test_add_with_tags(self, temp_db, cli_runner):
        """Should extract tags from description."""
        result = cli_runner.invoke(app, ["add", "Buy groceries +shopping +urgent"])
        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "+shopping" in result.output
        assert "+urgent" in result.output

        # Verify tags in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        assert "shopping" in tasks[0].tags
        assert "urgent" in tasks[0].tags
        assert tasks[0].description == "Buy groceries"

    def test_add_with_project(self, temp_db, cli_runner):
        """Should set project from option."""
        result = cli_runner.invoke(app, ["add", "Fix bug", "--project", "Work"])
        assert result.exit_code == 0
        assert "Project:" in result.output
        assert "Work" in result.output

        # Verify in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert tasks[0].project == "Work"

    def test_add_with_priority(self, temp_db, cli_runner):
        """Should set priority from option."""
        result = cli_runner.invoke(app, ["add", "Urgent task", "--priority", "H"])
        assert result.exit_code == 0
        assert "Priority:" in result.output

        # Verify in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert tasks[0].priority.value == "H"

    def test_add_priority_lowercase(self, temp_db, cli_runner):
        """Should accept lowercase priority."""
        result = cli_runner.invoke(app, ["add", "Task", "--priority", "m"])
        assert result.exit_code == 0

        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert tasks[0].priority.value == "M"

    def test_add_invalid_priority(self, temp_db_path, cli_runner):
        """Should reject invalid priority."""
        result = cli_runner.invoke(app, ["add", "Task", "--priority", "X"])
        assert result.exit_code == 1
        assert "Invalid priority" in result.output

    def test_add_with_short_options(self, temp_db, cli_runner):
        """Should accept short option flags."""
        result = cli_runner.invoke(app, ["add", "Task", "-p", "Home", "-P", "L"])
        assert result.exit_code == 0
        assert "Home" in result.output

        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert tasks[0].project == "Home"
        assert tasks[0].priority.value == "L"

    def test_add_empty_description_with_only_tags(self, temp_db_path, cli_runner):
        """Should reject description that becomes empty after tag extraction."""
        result = cli_runner.invoke(app, ["add", "+tag1 +tag2"])
        assert result.exit_code == 1
        assert "empty" in result.output.lower()

    def test_add_multiple_tasks(self, temp_db, cli_runner):
        """Should assign sequential IDs."""
        cli_runner.invoke(app, ["add", "First task"])
        cli_runner.invoke(app, ["add", "Second task"])
        result = cli_runner.invoke(app, ["add", "Third task"])

        assert result.exit_code == 0
        assert "Created task 3" in result.output

    def test_add_initializes_database(self, temp_db_path, cli_runner):
        """Should auto-initialize database on first run."""
        # Database doesn't exist yet
        assert not temp_db_path.exists()

        result = cli_runner.invoke(app, ["add", "First task"])
        assert result.exit_code == 0

        # Database should now exist
        assert temp_db_path.exists()


class TestAddWithAttachments:
    """Integration tests for add command with --attach option."""

    def test_add_with_single_attachment(self, temp_db, cli_runner, tmp_path: Path):
        """Should create task and attach file."""
        # Create a test file
        test_file = tmp_path / "document.txt"
        test_file.write_text("test content")

        result = cli_runner.invoke(
            app, ["add", "Task with attachment", "--attach", str(test_file)]
        )

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Attachments:" in result.output
        assert "document.txt" in result.output

        # Verify in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        task = tasks[0]
        assert len(task.attachments) == 1
        assert task.attachments[0].filename == "document.txt"

    def test_add_with_multiple_attachments(self, temp_db, cli_runner, tmp_path: Path):
        """Should attach multiple files at once."""
        # Create test files
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content 1")
        file2.write_text("content 2")

        result = cli_runner.invoke(
            app,
            [
                "add",
                "Task with multiple attachments",
                "--attach",
                str(file1),
                "--attach",
                str(file2),
            ],
        )

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Attachments:" in result.output
        assert "file1.txt" in result.output
        assert "file2.txt" in result.output

        # Verify in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        task = tasks[0]
        assert len(task.attachments) == 2
        filenames = {att.filename for att in task.attachments}
        assert filenames == {"file1.txt", "file2.txt"}

    def test_add_with_nonexistent_file(self, temp_db, cli_runner):
        """Should warn about nonexistent file but still create task."""
        result = cli_runner.invoke(
            app, ["add", "Task", "--attach", "/nonexistent/file.txt"]
        )

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Warning" in result.output or "not found" in result.output

        # Task should be created without attachment
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        assert len(tasks[0].attachments) == 0

    def test_add_with_directory(self, temp_db, cli_runner, tmp_path: Path):
        """Should warn about directory but still create task."""
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()

        result = cli_runner.invoke(app, ["add", "Task", "--attach", str(test_dir)])

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Warning" in result.output or "directory" in result.output.lower()

        # Task should be created without attachment
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        assert len(tasks[0].attachments) == 0

    def test_add_with_symlink(self, temp_db, cli_runner, tmp_path: Path):
        """Should warn about symlink but still create task."""
        # Create a target file
        target_file = tmp_path / "target.txt"
        target_file.write_text("content")

        # Create a symlink
        symlink_file = tmp_path / "link.txt"
        symlink_file.symlink_to(target_file)

        result = cli_runner.invoke(app, ["add", "Task", "--attach", str(symlink_file)])

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Warning" in result.output or "symlink" in result.output.lower()

        # Task should be created without attachment
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        assert len(tasks[0].attachments) == 0

    def test_add_with_mixed_valid_invalid_attachments(
        self, temp_db, cli_runner, tmp_path: Path
    ):
        """Should attach valid files and warn about invalid ones."""
        # Create valid file
        valid_file = tmp_path / "valid.txt"
        valid_file.write_text("content")

        result = cli_runner.invoke(
            app,
            [
                "add",
                "Task",
                "--attach",
                str(valid_file),
                "--attach",
                "/nonexistent.txt",
            ],
        )

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Warning" in result.output  # For nonexistent file

        # Task should be created with only valid attachment
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        task = tasks[0]
        assert len(task.attachments) == 1
        assert task.attachments[0].filename == "valid.txt"

    def test_add_with_attachment_and_other_options(
        self, temp_db, cli_runner, tmp_path: Path
    ):
        """Should combine attachments with other task options."""
        test_file = tmp_path / "doc.pdf"
        test_file.write_bytes(b"PDF content")

        result = cli_runner.invoke(
            app,
            [
                "add",
                "Important task +urgent",
                "--project",
                "Work",
                "--priority",
                "H",
                "--attach",
                str(test_file),
            ],
        )

        assert result.exit_code == 0
        assert "Created task" in result.output
        assert "Project: Work" in result.output
        assert "Priority:" in result.output
        assert "+urgent" in result.output
        assert "Attachments:" in result.output
        assert "doc.pdf" in result.output

        # Verify all properties in database
        repo = TaskRepository(temp_db)
        tasks = repo.list_pending()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.description == "Important task"
        assert task.project == "Work"
        assert task.priority.value == "H"
        assert "urgent" in task.tags
        assert len(task.attachments) == 1
        assert task.attachments[0].filename == "doc.pdf"
