"""SQLite database management for Task-NG."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from taskng.config.settings import get_data_dir

# Legacy constants for backward compatibility
DEFAULT_DATA_DIR = Path.home() / ".local" / "share" / "taskng"
DEFAULT_DB_PATH = DEFAULT_DATA_DIR / "task.db"


def get_db_path() -> Path:
    """Get the database path based on current data directory.

    Returns:
        Path to database file.
    """
    return get_data_dir() / "task.db"


class Database:
    """SQLite database manager."""

    def __init__(self, db_path: Path | None = None):
        """Initialize database with optional custom path.

        Args:
            db_path: Path to database file. Uses get_db_path() if not specified.
        """
        self.db_path = db_path or get_db_path()
        self._ensure_directory()
        self._schema_checked = False

    def _ensure_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a database connection with proper settings.

        Yields:
            SQLite connection with WAL mode and foreign keys enabled.
        """
        # Auto-migrate existing databases on first connection
        if not self._schema_checked and self.exists:
            self._apply_schema_if_needed()

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _apply_schema_if_needed(self) -> None:
        """Apply schema to existing database if needed.

        This ensures new tables are created in existing databases.
        Safe to call multiple times due to CREATE TABLE IF NOT EXISTS.
        """
        from taskng.storage.schema import SCHEMA

        conn = sqlite3.connect(self.db_path)
        try:
            conn.executescript(SCHEMA)
            conn.commit()
        finally:
            conn.close()
        self._schema_checked = True

    @contextmanager
    def cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Get a database cursor.

        Yields:
            SQLite cursor for executing queries.
        """
        with self.connection() as conn:
            cursor = conn.cursor()
            yield cursor

    def initialize(self) -> None:
        """Initialize database with schema."""
        from taskng.storage.schema import SCHEMA

        with self.connection() as conn:
            conn.executescript(SCHEMA)

    @property
    def exists(self) -> bool:
        """Check if database file exists."""
        return self.db_path.exists()

    def ensure_schema(self) -> None:
        """Ensure all tables exist in an existing database.

        This is safe to call on existing databases as the schema uses
        CREATE TABLE IF NOT EXISTS for all tables.
        """
        if self.exists:
            self.initialize()
