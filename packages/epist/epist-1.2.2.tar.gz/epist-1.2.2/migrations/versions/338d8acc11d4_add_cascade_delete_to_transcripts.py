"""add_cascade_delete_to_transcripts

Revision ID: 338d8acc11d4
Revises: 8d9e0f1a2b3c
Create Date: 2025-12-13 07:13:10.127705+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import pgvector


# revision identifiers, used by Alembic.
revision: str = '338d8acc11d4'
down_revision: Union[str, None] = '8d9e0f1a2b3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update Transcript -> AudioResource FK
    op.drop_constraint('transcripts_audio_resource_id_fkey', 'transcripts', type_='foreignkey')
    op.create_foreign_key(
        'transcripts_audio_resource_id_fkey', 'transcripts', 'audio_resources',
        ['audio_resource_id'], ['id'], ondelete='CASCADE'
    )

    # 2. Update TranscriptSegment -> Transcript FK
    op.drop_constraint('transcript_segments_transcript_id_fkey', 'transcript_segments', type_='foreignkey')
    op.create_foreign_key(
        'transcript_segments_transcript_id_fkey', 'transcript_segments', 'transcripts',
        ['transcript_id'], ['id'], ondelete='CASCADE'
    )


def downgrade() -> None:
    # Revert TranscriptSegment -> Transcript FK
    op.drop_constraint('transcript_segments_transcript_id_fkey', 'transcript_segments', type_='foreignkey')
    op.create_foreign_key(
        'transcript_segments_transcript_id_fkey', 'transcript_segments', 'transcripts',
        ['transcript_id'], ['id']
    )

    # Revert Transcript -> AudioResource FK
    op.drop_constraint('transcripts_audio_resource_id_fkey', 'transcripts', type_='foreignkey')
    op.create_foreign_key(
        'transcripts_audio_resource_id_fkey', 'transcripts', 'audio_resources',
        ['audio_resource_id'], ['id']
    )

