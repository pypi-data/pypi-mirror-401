"""Add attachments table

Revision ID: 002
Revises: 001
Create Date: 2026-01-09

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add attachments table for file attachments."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY,
            task_uuid TEXT NOT NULL,
            filename TEXT NOT NULL,
            hash TEXT NOT NULL,
            size INTEGER NOT NULL,
            mime_type TEXT,
            entry TEXT NOT NULL,
            FOREIGN KEY (task_uuid) REFERENCES tasks(uuid) ON DELETE CASCADE
        )
    """)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_attachments_task ON attachments(task_uuid)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_attachments_hash ON attachments(hash)")


def downgrade() -> None:
    """Remove attachments table."""
    op.execute("DROP INDEX IF EXISTS idx_attachments_hash")
    op.execute("DROP INDEX IF EXISTS idx_attachments_task")
    op.execute("DROP TABLE IF EXISTS attachments")
