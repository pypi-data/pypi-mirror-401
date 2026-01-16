"""add_langgraph_checkpointer_tables

Revision ID: 209efbed60a4
Revises: eb0488e04b85
Create Date: 2026-01-07 14:48:17.056063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '209efbed60a4'
down_revision: Union[str, None] = 'eb0488e04b85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create checkpoints table for LangGraph state persistence
    op.execute("""
        CREATE TABLE IF NOT EXISTS checkpoints (
            thread_id TEXT NOT NULL,
            checkpoint_ns TEXT NOT NULL,
            checkpoint_id TEXT NOT NULL,
            parent_checkpoint_id TEXT,
            type TEXT,
            checkpoint JSONB NOT NULL,
            metadata JSONB NOT NULL,
            PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
        )
    """)

    # Create index on thread_id for faster lookups (idempotent)
    op.execute("""
        CREATE INDEX IF NOT EXISTS checkpoints_thread_id_idx ON checkpoints (thread_id)
    """)

    # Create checkpoint_writes table for incremental updates
    op.execute("""
        CREATE TABLE IF NOT EXISTS checkpoint_writes (
            thread_id TEXT NOT NULL,
            checkpoint_ns TEXT NOT NULL,
            checkpoint_id TEXT NOT NULL,
            task_id TEXT NOT NULL,
            idx INTEGER NOT NULL,
            channel TEXT NOT NULL,
            type TEXT,
            blob BYTEA NOT NULL,
            PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
        )
    """)

    # Create index on thread_id for faster lookups (idempotent)
    op.execute("""
        CREATE INDEX IF NOT EXISTS checkpoint_writes_thread_id_idx ON checkpoint_writes (thread_id)
    """)


def downgrade() -> None:
    # Drop checkpointer tables
    op.drop_table('checkpoint_writes')
    op.drop_table('checkpoints')
