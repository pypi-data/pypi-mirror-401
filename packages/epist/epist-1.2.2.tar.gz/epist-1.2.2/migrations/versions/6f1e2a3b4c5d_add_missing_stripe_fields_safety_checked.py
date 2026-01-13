"""add missing stripe fields safety checked

Revision ID: 6f1e2a3b4c5d
Revises: ab16e3d4200d
Create Date: 2025-12-27 20:46:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6f1e2a3b4c5d'
down_revision: Union[str, None] = 'ab16e3d4200d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use inspector to check for column existence before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Organizations
    org_columns = [c['name'] for c in inspector.get_columns('organizations')]
    if 'tier' not in org_columns:
        op.add_column('organizations', sa.Column('tier', sa.String(), nullable=False, server_default='free'))
    if 'stripe_customer_id' not in org_columns:
        op.add_column('organizations', sa.Column('stripe_customer_id', sa.String(), nullable=True))
        op.create_index(op.f('ix_organizations_stripe_customer_id'), 'organizations', ['stripe_customer_id'], unique=False)
    if 'stripe_subscription_id' not in org_columns:
        op.add_column('organizations', sa.Column('stripe_subscription_id', sa.String(), nullable=True))
    if 'subscription_status' not in org_columns:
        op.add_column('organizations', sa.Column('subscription_status', sa.String(), nullable=True))
    if 'current_period_end' not in org_columns:
        op.add_column('organizations', sa.Column('current_period_end', sa.DateTime(), nullable=True))
    if 'last_webhook_id' not in org_columns:
        op.add_column('organizations', sa.Column('last_webhook_id', sa.String(), nullable=True))

    # 2. Audio Resources
    audio_columns = [c['name'] for c in inspector.get_columns('audio_resources')]
    if 'error' not in audio_columns:
        op.add_column('audio_resources', sa.Column('error', sa.Text(), nullable=True))
    if 'is_public' not in audio_columns:
        op.add_column('audio_resources', sa.Column('is_public', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    # 3. Users
    user_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'onboarding_completed' not in user_columns:
        op.add_column('users', sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default=sa.text('false')))


def downgrade() -> None:
    # Safely remove columns if they exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 1. Users
    user_columns = [c['name'] for c in inspector.get_columns('users')]
    if 'onboarding_completed' in user_columns:
        op.drop_column('users', 'onboarding_completed')

    # 2. Audio Resources
    audio_columns = [c['name'] for c in inspector.get_columns('audio_resources')]
    if 'is_public' in audio_columns:
        op.drop_column('audio_resources', 'is_public')
    if 'error' in audio_columns:
        op.drop_column('audio_resources', 'error')

    # 3. Organizations
    org_columns = [c['name'] for c in inspector.get_columns('organizations')]
    if 'last_webhook_id' in org_columns:
        op.drop_column('organizations', 'last_webhook_id')
    if 'current_period_end' in org_columns:
        op.drop_column('organizations', 'current_period_end')
    if 'subscription_status' in org_columns:
        op.drop_column('organizations', 'subscription_status')
    if 'stripe_subscription_id' in org_columns:
        op.drop_column('organizations', 'stripe_subscription_id')
    if 'stripe_customer_id' in org_columns:
        op.drop_index(op.f('ix_organizations_stripe_customer_id'), table_name='organizations')
        op.drop_column('organizations', 'stripe_customer_id')
    if 'tier' in org_columns:
        op.drop_column('organizations', 'tier')
