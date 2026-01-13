"""add missing context and trace columns

Revision ID: 263aa63a981b
Revises: c6243dc2e980
Create Date: 2025-12-29 04:34:11.566241+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '263aa63a981b'
down_revision: Union[str, None] = 'c6243dc2e980'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get inspector to check for columns before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    # 0. Ensure pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # 1. Ensure transcript_segments table exists
    if 'transcript_segments' not in tables:
        op.create_table(
            'transcript_segments',
            sa.Column('id', sa.Uuid(), nullable=False),
            sa.Column('transcript_id', sa.Uuid(), nullable=False),
            sa.Column('start', sa.Float(), nullable=False),
            sa.Column('end', sa.Float(), nullable=False),
            sa.Column('text', sa.String(), nullable=False),
            sa.Column('speaker', sa.String(), nullable=True),
            sa.Column('confidence', sa.Float(), nullable=True),
            sa.Column('overlap_context_before', sa.String(length=500), nullable=True),
            sa.Column('overlap_context_after', sa.String(length=500), nullable=True),
            sa.Column('words', sa.JSON(), nullable=True),
            sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True),
            sa.Column('content_vector', sa.dialects.postgresql.TSVECTOR(), nullable=True),
            sa.ForeignKeyConstraint(['transcript_id'], ['transcripts.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        # Create index for vector search if needed
        # op.create_index('ix_transcript_segments_embedding', 'transcript_segments', ['embedding'], postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'})

    else:
        # Existing update logic
        ts_columns = [col['name'] for col in inspector.get_columns('transcript_segments')]
        if 'overlap_context_before' not in ts_columns:
            op.add_column('transcript_segments', sa.Column('overlap_context_before', sa.String(length=500), nullable=True))
        if 'overlap_context_after' not in ts_columns:
            op.add_column('transcript_segments', sa.Column('overlap_context_after', sa.String(length=500), nullable=True))
        
    # 2. Update trace_events
    trace_columns = [col['name'] for col in inspector.get_columns('trace_events')]
    if 'user_id' not in trace_columns:
        op.add_column('trace_events', sa.Column('user_id', sa.Uuid(), sa.ForeignKey('users.id'), nullable=True))


def downgrade() -> None:
    # Get inspector to check for columns before dropping
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Update transcript_segments
    ts_columns = [col['name'] for col in inspector.get_columns('transcript_segments')]
    if 'overlap_context_before' in ts_columns:
        op.drop_column('transcript_segments', 'overlap_context_before')
    if 'overlap_context_after' in ts_columns:
        op.drop_column('transcript_segments', 'overlap_context_after')
        
    # 2. Update trace_events
    trace_columns = [col['name'] for col in inspector.get_columns('trace_events')]
    if 'user_id' in trace_columns:
        op.drop_column('trace_events', 'user_id')

