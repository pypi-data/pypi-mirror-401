"""Attachment service for file storage operations."""

import hashlib
import shutil
from pathlib import Path

import magic


class AttachmentService:
    """Manages file attachment storage and retrieval."""

    def __init__(self, data_dir: Path):
        """Initialize service with data directory.

        Args:
            data_dir: Base data directory (e.g., ~/.local/share/taskng)
        """
        self.attachments_dir = data_dir / "attachments"

    def store_file(self, source: Path) -> tuple[str, int, str | None]:
        """Copy file to content-addressed storage.

        Args:
            source: Path to source file.

        Returns:
            Tuple of (hash, size, mime_type).

        Raises:
            FileNotFoundError: If source doesn't exist.
            IsADirectoryError: If source is a directory.
            ValueError: If source is a symlink.
        """
        if not source.exists():
            raise FileNotFoundError(f"File not found: {source}")
        if source.is_dir():
            raise IsADirectoryError(f"Cannot attach directory: {source}")
        if source.is_symlink():
            raise ValueError(f"Cannot attach symlink: {source}")

        # Compute hash and get file info
        file_hash = self.compute_hash(source)
        file_size = source.stat().st_size
        mime_type = self.detect_mime_type(source)

        # Check if file already exists (deduplication)
        if not self.exists(file_hash):
            dest_path = self.get_path(file_hash)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest_path)

        return file_hash, file_size, mime_type

    def get_path(self, file_hash: str) -> Path:
        """Get filesystem path for stored file.

        Args:
            file_hash: SHA256 hash of file.

        Returns:
            Path to stored file.
        """
        return self.attachments_dir / file_hash[:2] / file_hash

    def exists(self, file_hash: str) -> bool:
        """Check if file exists in storage.

        Args:
            file_hash: SHA256 hash of file.

        Returns:
            True if file exists.
        """
        return self.get_path(file_hash).exists()

    def compute_hash(self, path: Path) -> str:
        """Compute SHA256 hash of file.

        Args:
            path: Path to file.

        Returns:
            Lowercase hex SHA256 hash (64 characters).
        """
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def detect_mime_type(self, path: Path) -> str | None:
        """Detect MIME type using python-magic.

        Args:
            path: Path to file.

        Returns:
            MIME type string or None if detection fails.
        """
        try:
            return magic.from_file(str(path), mime=True)
        except (OSError, magic.MagicException):
            # OSError: file access issues (permissions, etc.)
            # MagicException: magic library specific errors
            return None
