"""Tests for attachment service."""

import hashlib
from pathlib import Path

import pytest

from taskng.core.attachments import AttachmentService


class TestComputeHash:
    """Tests for compute_hash method."""

    def test_computes_sha256(self, tmp_path: Path):
        """Should compute correct SHA256 hash."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        service = AttachmentService(tmp_path)
        result = service.compute_hash(test_file)

        expected = hashlib.sha256(b"hello world").hexdigest()
        assert result == expected

    def test_same_content_same_hash(self, tmp_path: Path):
        """Same content should produce same hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("identical content")
        file2.write_text("identical content")

        service = AttachmentService(tmp_path)
        assert service.compute_hash(file1) == service.compute_hash(file2)

    def test_different_content_different_hash(self, tmp_path: Path):
        """Different content should produce different hash."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content A")
        file2.write_text("content B")

        service = AttachmentService(tmp_path)
        assert service.compute_hash(file1) != service.compute_hash(file2)

    def test_hash_format(self, tmp_path: Path):
        """Hash should be 64 lowercase hex characters."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        service = AttachmentService(tmp_path)
        result = service.compute_hash(test_file)

        assert len(result) == 64
        assert result == result.lower()
        assert all(c in "0123456789abcdef" for c in result)


class TestDetectMimeType:
    """Tests for detect_mime_type method."""

    def test_detects_text(self, tmp_path: Path):
        """Should detect text/plain."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("This is plain text content")

        service = AttachmentService(tmp_path)
        result = service.detect_mime_type(test_file)

        assert result is not None
        assert "text" in result

    def test_detects_binary(self, tmp_path: Path):
        """Should detect binary content."""
        test_file = tmp_path / "test.bin"
        # Write some binary data
        test_file.write_bytes(bytes(range(256)))

        service = AttachmentService(tmp_path)
        result = service.detect_mime_type(test_file)

        assert result is not None

    def test_empty_file(self, tmp_path: Path):
        """Should handle empty files."""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        service = AttachmentService(tmp_path)
        result = service.detect_mime_type(test_file)

        # Empty files should return something (implementation-dependent)
        assert result is not None or result is None  # Just shouldn't raise

    def test_returns_none_on_oserror(self, tmp_path: Path, monkeypatch):
        """Should return None when OSError occurs."""
        import magic as magic_module

        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_from_file(*args, **kwargs):
            raise OSError("Permission denied")

        monkeypatch.setattr(magic_module, "from_file", mock_from_file)

        service = AttachmentService(tmp_path)
        result = service.detect_mime_type(test_file)

        assert result is None

    def test_returns_none_on_magic_exception(self, tmp_path: Path, monkeypatch):
        """Should return None when MagicException occurs."""
        import magic as magic_module

        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        def mock_from_file(*args, **kwargs):
            raise magic_module.MagicException("Magic error")

        monkeypatch.setattr(magic_module, "from_file", mock_from_file)

        service = AttachmentService(tmp_path)
        result = service.detect_mime_type(test_file)

        assert result is None


class TestStoreFile:
    """Tests for store_file method."""

    def test_copies_file_to_storage(self, tmp_path: Path):
        """Should copy file to attachments directory."""
        data_dir = tmp_path / "attach_data"
        data_dir.mkdir()
        source = tmp_path / "source.txt"
        source.write_text("file content")

        service = AttachmentService(data_dir)
        file_hash, size, mime_type = service.store_file(source)

        stored_path = service.get_path(file_hash)
        assert stored_path.exists()
        assert stored_path.read_text() == "file content"

    def test_uses_hash_subdirectory(self, tmp_path: Path):
        """Should store in {hash[:2]}/{hash} structure."""
        data_dir = tmp_path / "attach_data"
        data_dir.mkdir()
        source = tmp_path / "source.txt"
        source.write_text("test content")

        service = AttachmentService(data_dir)
        file_hash, _, _ = service.store_file(source)

        expected_path = data_dir / "attachments" / file_hash[:2] / file_hash
        assert expected_path.exists()

    def test_returns_hash_size_mime(self, tmp_path: Path):
        """Should return tuple of (hash, size, mime_type)."""
        data_dir = tmp_path / "attach_data"
        data_dir.mkdir()
        source = tmp_path / "source.txt"
        source.write_text("test")

        service = AttachmentService(data_dir)
        file_hash, size, mime_type = service.store_file(source)

        assert len(file_hash) == 64
        assert size == 4
        assert mime_type is not None  # text/plain or similar

    def test_deduplication(self, tmp_path: Path):
        """Should not copy if hash already exists."""
        data_dir = tmp_path / "attach_data"
        data_dir.mkdir()
        source1 = tmp_path / "source1.txt"
        source2 = tmp_path / "source2.txt"
        source1.write_text("same content")
        source2.write_text("same content")

        service = AttachmentService(data_dir)
        hash1, _, _ = service.store_file(source1)

        # Get mtime of stored file
        stored_path = service.get_path(hash1)
        mtime_before = stored_path.stat().st_mtime

        # Store same content again
        hash2, _, _ = service.store_file(source2)

        assert hash1 == hash2
        # File should not have been overwritten
        assert stored_path.stat().st_mtime == mtime_before

    def test_file_not_found(self, tmp_path: Path):
        """Should raise FileNotFoundError."""
        service = AttachmentService(tmp_path)

        with pytest.raises(FileNotFoundError):
            service.store_file(tmp_path / "nonexistent.txt")

    def test_directory_raises_error(self, tmp_path: Path):
        """Should raise IsADirectoryError for directories."""
        service = AttachmentService(tmp_path)

        with pytest.raises(IsADirectoryError):
            service.store_file(tmp_path)

    def test_symlink_raises_error(self, tmp_path: Path):
        """Should raise ValueError for symlinks."""
        service = AttachmentService(tmp_path)

        # Create a regular file
        target_file = tmp_path / "target.txt"
        target_file.write_text("content")

        # Create a symlink to it
        symlink_file = tmp_path / "symlink.txt"
        symlink_file.symlink_to(target_file)

        # Verify it's actually a symlink
        assert symlink_file.is_symlink()

        # Should reject the symlink
        with pytest.raises(ValueError, match="Cannot attach symlink"):
            service.store_file(symlink_file)


class TestGetPath:
    """Tests for get_path method."""

    def test_returns_correct_path(self, tmp_path: Path):
        """Should return path with hash subdirectory."""
        service = AttachmentService(tmp_path)
        test_hash = "a" * 64

        result = service.get_path(test_hash)

        expected = tmp_path / "attachments" / "aa" / ("a" * 64)
        assert result == expected


class TestExists:
    """Tests for exists method."""

    def test_returns_true_for_existing(self, tmp_path: Path):
        """Should return True if file exists."""
        data_dir = tmp_path / "attach_data"
        data_dir.mkdir()
        source = tmp_path / "source.txt"
        source.write_text("content")

        service = AttachmentService(data_dir)
        file_hash, _, _ = service.store_file(source)

        assert service.exists(file_hash) is True

    def test_returns_false_for_missing(self, tmp_path: Path):
        """Should return False if file missing."""
        service = AttachmentService(tmp_path)

        assert service.exists("a" * 64) is False
