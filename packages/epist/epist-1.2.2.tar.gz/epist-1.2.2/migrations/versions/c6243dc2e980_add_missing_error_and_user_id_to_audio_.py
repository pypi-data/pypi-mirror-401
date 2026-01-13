"""add missing error and user_id to audio_resources

Revision ID: c6243dc2e980
Revises: 6f1e2a3b4c5d
Create Date: 2025-12-28 20:42:13.802327+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = 'c6243dc2e980'
down_revision: Union[str, None] = '6f1e2a3b4c5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use inspector to check for column existence before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Audio Resources
    audio_columns = [c['name'] for c in inspector.get_columns('audio_resources')]
    if 'error' not in audio_columns:
        op.add_column('audio_resources', sa.Column('error', sa.Text(), nullable=True))
    if 'user_id' not in audio_columns:
        # Note: postgres uses 'uuid' for UUID type in SQL. sa.UUID() maps correctly.
        op.add_column('audio_resources', sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=True))
        op.create_index(op.f('ix_audio_resources_user_id'), 'audio_resources', ['user_id'], unique=False)


def downgrade() -> None:
    # Safely remove columns if they exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    audio_columns = [c['name'] for c in inspector.get_columns('audio_resources')]
    if 'user_id' in audio_columns:
        op.drop_index(op.f('ix_audio_resources_user_id'), table_name='audio_resources')
        op.drop_column('audio_resources', 'user_id')
    if 'error' in audio_columns:
        op.drop_column('audio_resources', 'error')

