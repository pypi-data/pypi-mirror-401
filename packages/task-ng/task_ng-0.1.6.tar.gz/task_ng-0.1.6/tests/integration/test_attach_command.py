"""Integration tests for attachment CLI commands."""

from pathlib import Path

from taskng.cli.main import app
from taskng.config.settings import get_data_dir
from taskng.storage.repository import TaskRepository


class TestAttachCommand:
    """Integration tests for attach command."""

    def test_attach_single_file(self, temp_db, cli_runner, tmp_path: Path):
        """Should attach single file to task."""
        # Create a task first
        cli_runner.invoke(app, ["add", "Test task"])

        # Create a file to attach
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        assert result.exit_code == 0
        assert "Attached" in result.output
        assert "test.txt" in result.output

        # Verify in database
        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        assert len(task.attachments) == 1
        assert task.attachments[0].filename == "test.txt"

    def test_attach_multiple_files(self, temp_db, cli_runner, tmp_path: Path):
        """Should attach multiple files at once."""
        cli_runner.invoke(app, ["add", "Test task"])

        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content 1")
        file2.write_text("content 2")

        result = cli_runner.invoke(
            app, ["attachment", "add", "1", str(file1), str(file2)]
        )

        assert result.exit_code == 0

        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        assert len(task.attachments) == 2

    def test_attach_nonexistent_task(self, temp_db, cli_runner, tmp_path: Path):
        """Should show error for nonexistent task."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        result = cli_runner.invoke(app, ["attachment", "add", "999", str(test_file)])

        assert result.exit_code == 1
        assert "not found" in result.output

    def test_attach_nonexistent_file(self, temp_db, cli_runner):
        """Should show error for nonexistent file."""
        cli_runner.invoke(app, ["add", "Test task"])

        result = cli_runner.invoke(
            app, ["attachment", "add", "1", "/nonexistent/file.txt"]
        )

        assert "not found" in result.output.lower()

    def test_attach_updates_modified(self, temp_db, cli_runner, tmp_path: Path):
        """Should update task's modified timestamp."""
        cli_runner.invoke(app, ["add", "Test task"])

        repo = TaskRepository(temp_db)
        task_before = repo.get_by_id(1)
        modified_before = task_before.modified

        # Wait a tiny bit to ensure timestamp differs
        import time

        time.sleep(0.01)

        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        task_after = repo.get_by_id(1)
        assert task_after.modified > modified_before

    def test_attach_symlink_rejected(self, temp_db, cli_runner, tmp_path: Path):
        """Should reject symlinks with clear error message."""
        cli_runner.invoke(app, ["add", "Test task"])

        # Create a target file
        target_file = tmp_path / "target.txt"
        target_file.write_text("sensitive content")

        # Create a symlink
        symlink_file = tmp_path / "link.txt"
        symlink_file.symlink_to(target_file)

        # Attempt to attach symlink
        result = cli_runner.invoke(app, ["attachment", "add", "1", str(symlink_file)])

        # Should fail with clear error message
        assert (
            "Cannot attach symlink" in result.output
            or "symlink" in result.output.lower()
        )

        # Verify no attachment was created
        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        assert len(task.attachments) == 0


class TestAttachmentsCommand:
    """Integration tests for attachments command."""

    def test_list_attachments(self, temp_db, cli_runner, tmp_path: Path):
        """Should list all attachments for task."""
        cli_runner.invoke(app, ["add", "Test task"])

        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        result = cli_runner.invoke(app, ["attachment", "list", "1"])

        assert result.exit_code == 0
        assert "test.txt" in result.output

    def test_empty_attachments(self, temp_db, cli_runner):
        """Should show message when no attachments."""
        cli_runner.invoke(app, ["add", "Test task"])

        result = cli_runner.invoke(app, ["attachment", "list", "1"])

        assert result.exit_code == 0
        assert "No attachments" in result.output

    def test_nonexistent_task(self, temp_db, cli_runner):
        """Should show error for nonexistent task."""
        result = cli_runner.invoke(app, ["attachment", "list", "999"])

        assert result.exit_code == 1
        assert "not found" in result.output


class TestDetachCommand:
    """Integration tests for detach command."""

    def test_detach_by_index(self, temp_db, cli_runner, tmp_path: Path):
        """Should remove attachment by index."""
        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        result = cli_runner.invoke(app, ["attachment", "remove", "1", "1"])

        assert result.exit_code == 0
        assert "Removed" in result.output

        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        assert len(task.attachments) == 0

    def test_detach_by_filename(self, temp_db, cli_runner, tmp_path: Path):
        """Should remove attachment by filename."""
        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "myfile.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        result = cli_runner.invoke(app, ["attachment", "remove", "1", "myfile.txt"])

        assert result.exit_code == 0
        assert "Removed" in result.output

    def test_detach_all(self, temp_db, cli_runner, tmp_path: Path):
        """Should remove all attachments with --all."""
        cli_runner.invoke(app, ["add", "Test task"])
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("1")
        file2.write_text("2")
        cli_runner.invoke(app, ["attachment", "add", "1", str(file1), str(file2)])

        result = cli_runner.invoke(app, ["attachment", "remove", "1", "--all"])

        assert result.exit_code == 0
        assert "2" in result.output  # "Removed 2 attachment(s)"

    def test_detach_invalid_index(self, temp_db, cli_runner, tmp_path: Path):
        """Should show error for invalid index."""
        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        result = cli_runner.invoke(app, ["attachment", "remove", "1", "99"])

        assert result.exit_code == 1
        assert "not found" in result.output

    def test_detach_file_not_removed_from_storage(
        self, temp_db, cli_runner, tmp_path: Path, isolate_test_data
    ):
        """Should NOT delete file from storage."""
        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        # Get the stored file path
        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        file_hash = task.attachments[0].hash
        stored_path = get_data_dir() / "attachments" / file_hash[:2] / file_hash

        assert stored_path.exists()

        # Detach
        cli_runner.invoke(app, ["attachment", "remove", "1", "1"])

        # File should still exist in storage
        assert stored_path.exists()


class TestShowWithAttachments:
    """Integration tests for show command with attachments."""

    def test_show_displays_attachments(self, temp_db, cli_runner, tmp_path: Path):
        """Should display attachments in show output."""
        cli_runner.invoke(app, ["add", "Test task"])

        test_file = tmp_path / "document.pdf"
        test_file.write_bytes(b"PDF content here")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        result = cli_runner.invoke(app, ["show", "1"])

        assert result.exit_code == 0
        assert "Attachments" in result.output
        assert "document.pdf" in result.output

    def test_show_no_attachments_section_when_empty(self, temp_db, cli_runner):
        """Should not show attachments section when no attachments."""
        cli_runner.invoke(app, ["add", "Test task"])

        result = cli_runner.invoke(app, ["show", "1"])

        assert result.exit_code == 0
        assert "Attachments" not in result.output


class TestExportAttachmentCommand:
    """Integration tests for export-attachment command."""

    def test_export_to_directory(self, temp_db, cli_runner, tmp_path: Path):
        """Should export to directory with original filename."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "original.txt"
        source.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        export_dir = tmp_path / "exports"
        export_dir.mkdir()

        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(export_dir)]
        )

        assert result.exit_code == 0
        exported = export_dir / "original.txt"
        assert exported.exists()
        assert exported.read_text() == "content"

    def test_export_with_new_name(self, temp_db, cli_runner, tmp_path: Path):
        """Should export with custom filename."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "original.txt"
        source.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        dest = tmp_path / "renamed.txt"

        result = cli_runner.invoke(app, ["attachment", "save", "1", "1", str(dest)])

        assert result.exit_code == 0
        assert dest.exists()
        assert dest.read_text() == "content"

    def test_export_invalid_attachment(self, temp_db, cli_runner, tmp_path: Path):
        """Should show error for invalid attachment."""
        cli_runner.invoke(app, ["add", "Test task"])

        result = cli_runner.invoke(app, ["attachment", "save", "1", "1", str(tmp_path)])

        assert result.exit_code == 1
        assert "not found" in result.output

    def test_export_prevents_path_traversal(self, temp_db, cli_runner, tmp_path: Path):
        """Should sanitize filename to prevent path traversal attacks."""
        # Create a task and attach a file
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "normal.txt"
        source.write_text("sensitive content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        # Manually modify the attachment filename in the database to include path traversal
        repo = TaskRepository(temp_db)
        task = repo.get_by_id(1)
        attachment = task.attachments[0]

        # Update the filename to include path traversal attempt
        with temp_db.connection() as conn:
            conn.execute(
                "UPDATE attachments SET filename = ? WHERE id = ?",
                ("../../../tmp/malicious.txt", attachment.id),
            )

        # Create export directory
        export_dir = tmp_path / "exports"
        export_dir.mkdir()

        # Attempt to export - should sanitize the filename
        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(export_dir)]
        )

        assert result.exit_code == 0

        # File should be exported with sanitized name (basename only)
        safe_export = export_dir / "malicious.txt"
        assert safe_export.exists()
        assert safe_export.read_text() == "sensitive content"

        # File should NOT exist at traversed path
        traversed_path = tmp_path / "tmp" / "malicious.txt"
        assert not traversed_path.exists()


class TestDuplicateFilenameWarning:
    """Test duplicate filename detection."""

    def test_warns_on_duplicate(self, temp_db, cli_runner, tmp_path):
        """Should warn when attaching duplicate filename."""
        cli_runner.invoke(app, ["add", "Test task"])

        file1 = tmp_path / "doc.txt"
        file2 = tmp_path / "other" / "doc.txt"
        file2.parent.mkdir()
        file1.write_text("content 1")
        file2.write_text("content 2")

        cli_runner.invoke(app, ["attachment", "add", "1", str(file1)])
        result = cli_runner.invoke(
            app, ["attachment", "add", "1", str(file2)], input="n\n"
        )

        assert result.exit_code == 0
        assert "Warning" in result.output or "warning" in result.output.lower()
        assert "already has attachment" in result.output.lower()


class TestFileSizeValidation:
    """Test file size validation."""

    def test_rejects_oversized_file(self, temp_db, cli_runner, tmp_path, monkeypatch):
        """Should reject file exceeding size limit."""
        # Set small limit for testing
        monkeypatch.setenv("TASKNG_ATTACHMENT__MAX_SIZE", "1024")

        cli_runner.invoke(app, ["add", "Test task"])
        big_file = tmp_path / "big.bin"
        big_file.write_bytes(b"x" * 2048)

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(big_file)])

        assert "too large" in result.output.lower()
        assert "limit" in result.output.lower()


class TestAttachErrorHandling:
    """Test exception handling in attach command."""

    def test_handles_permission_error(self, temp_db, cli_runner, tmp_path, monkeypatch):
        """Should handle PermissionError gracefully."""
        from taskng.core.attachments import AttachmentService

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_store_file(self, path):
            raise PermissionError("Permission denied")

        monkeypatch.setattr(AttachmentService, "store_file", mock_store_file)

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        assert result.exit_code == 0  # Continues processing other files
        assert "Failed to attach" in result.output
        assert "Permission denied" in result.output
        assert "Ensure the file is readable" in result.output

    def test_handles_oserror(self, temp_db, cli_runner, tmp_path, monkeypatch):
        """Should handle OSError gracefully."""
        from taskng.core.attachments import AttachmentService

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_store_file(self, path):
            raise OSError("Disk full")

        monkeypatch.setattr(AttachmentService, "store_file", mock_store_file)

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        assert result.exit_code == 0
        assert "Failed to attach" in result.output
        assert "Disk full" in result.output

    def test_handles_valueerror(self, temp_db, cli_runner, tmp_path, monkeypatch):
        """Should handle ValueError gracefully (e.g., symlink rejection)."""
        from taskng.core.attachments import AttachmentService

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_store_file(self, path):
            raise ValueError("Cannot attach symlink")

        monkeypatch.setattr(AttachmentService, "store_file", mock_store_file)

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        assert result.exit_code == 0
        assert "Failed to attach" in result.output
        assert "symlink" in result.output.lower()

    def test_reraises_unexpected_error(
        self, temp_db, cli_runner, tmp_path, monkeypatch
    ):
        """Should re-raise truly unexpected exceptions."""
        from taskng.core.attachments import AttachmentService

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_store_file(self, path):
            raise RuntimeError("Unexpected internal error")

        monkeypatch.setattr(AttachmentService, "store_file", mock_store_file)

        result = cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        # Unexpected errors should cause the command to fail
        assert result.exit_code != 0
        assert "Unexpected error" in result.output
        # The exception should be re-raised
        assert result.exception is not None
        assert isinstance(result.exception, RuntimeError)


class TestVirtualTagFiltering:
    """Test ATTACHED virtual tag filtering."""

    def test_filter_by_attached(self, temp_db, cli_runner, tmp_path):
        """Should filter tasks by +ATTACHED."""
        cli_runner.invoke(app, ["add", "Task 1"])
        cli_runner.invoke(app, ["add", "Task 2"])

        file1 = tmp_path / "file1.txt"
        file1.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(file1)])

        result = cli_runner.invoke(app, ["list", "+ATTACHED"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" not in result.output

    def test_exclude_attached(self, temp_db, cli_runner, tmp_path):
        """Should exclude tasks with -ATTACHED."""
        cli_runner.invoke(app, ["add", "Task 1"])
        cli_runner.invoke(app, ["add", "Task 2"])

        file1 = tmp_path / "file1.txt"
        file1.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(file1)])

        result = cli_runner.invoke(app, ["list", "--", "-ATTACHED"])

        assert result.exit_code == 0
        assert "Task 1" not in result.output
        assert "Task 2" in result.output


class TestOpenAttachmentErrorHandling:
    """Test error handling in attachment open command."""

    def test_open_reports_subprocess_failure(
        self, temp_db, cli_runner, tmp_path, monkeypatch
    ):
        """Should report error when subprocess fails."""
        import subprocess
        from unittest.mock import Mock

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        # Mock subprocess.run to return non-zero exit code
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Failed to open file"

        def mock_run(*args, **kwargs):
            return mock_result

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(app, ["attachment", "open", "1", "1"])

        assert result.exit_code == 0  # Command itself succeeds
        assert "Warning" in result.output or "Could not open" in result.output
        assert "exit code 1" in result.output

    def test_open_handles_missing_opener(
        self, temp_db, cli_runner, tmp_path, monkeypatch
    ):
        """Should handle FileNotFoundError when opener is missing."""
        import subprocess

        cli_runner.invoke(app, ["add", "Test task"])
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(test_file)])

        # Mock subprocess.run to raise FileNotFoundError
        def mock_run(*args, **kwargs):
            raise FileNotFoundError("xdg-open not found")

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = cli_runner.invoke(app, ["attachment", "open", "1", "1"])

        assert result.exit_code == 0  # Command itself succeeds
        assert "Error" in result.output or "not found" in result.output


class TestExportOverwriteProtection:
    """Test overwrite protection in attachment export."""

    def test_warns_on_existing_file(self, temp_db, cli_runner, tmp_path):
        """Should warn when destination file exists."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "doc.txt"
        source.write_text("new content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        # Create existing file at destination
        dest = tmp_path / "existing.txt"
        dest.write_text("old content")

        # Try to export without --force, decline overwrite
        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(dest)], input="n\n"
        )

        assert result.exit_code == 0
        assert "Warning" in result.output or "already exists" in result.output
        assert "Existing:" in result.output  # File size comparison
        assert "cancelled" in result.output.lower()
        # Original file should be unchanged
        assert dest.read_text() == "old content"

    def test_overwrites_with_confirmation(self, temp_db, cli_runner, tmp_path):
        """Should overwrite when user confirms."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "doc.txt"
        source.write_text("new content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        dest = tmp_path / "existing.txt"
        dest.write_text("old content")

        # Confirm overwrite
        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(dest)], input="y\n"
        )

        assert result.exit_code == 0
        assert "Exported" in result.output
        # File should be overwritten
        assert dest.read_text() == "new content"

    def test_force_flag_skips_confirmation(self, temp_db, cli_runner, tmp_path):
        """Should skip confirmation with --force flag."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "doc.txt"
        source.write_text("new content")
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        dest = tmp_path / "existing.txt"
        dest.write_text("old content")

        # Use --force flag
        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(dest), "--force"]
        )

        assert result.exit_code == 0
        assert "Exported" in result.output
        # Should not see warning or prompt
        assert "Warning" not in result.output
        assert "Overwrite?" not in result.output
        # File should be overwritten
        assert dest.read_text() == "new content"

    def test_shows_file_sizes_in_warning(self, temp_db, cli_runner, tmp_path):
        """Should show file sizes when prompting for overwrite."""
        cli_runner.invoke(app, ["add", "Test task"])
        source = tmp_path / "doc.txt"
        source.write_text("a" * 2048)  # 2 KB
        cli_runner.invoke(app, ["attachment", "add", "1", str(source)])

        dest = tmp_path / "existing.txt"
        dest.write_text("b" * 1024)  # 1 KB

        result = cli_runner.invoke(
            app, ["attachment", "save", "1", "1", str(dest)], input="n\n"
        )

        assert result.exit_code == 0
        # Should show both file sizes
        assert "Existing:" in result.output
        assert "New:" in result.output
        # Should include size units (KB, MB, etc)
        assert "KB" in result.output or "B" in result.output
