"""add_stripe_fields

Revision ID: 8d9e0f1a2b3c
Revises: 1234567890ab
Create Date: 2025-12-12 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8d9e0f1a2b3c'
down_revision: Union[str, None] = '1234567890ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('organizations', sa.Column('stripe_customer_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('organizations', sa.Column('stripe_subscription_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('organizations', sa.Column('subscription_status', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('organizations', sa.Column('current_period_end', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_organizations_stripe_customer_id'), 'organizations', ['stripe_customer_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_organizations_stripe_customer_id'), table_name='organizations')
    op.drop_column('organizations', 'current_period_end')
    op.drop_column('organizations', 'subscription_status')
    op.drop_column('organizations', 'stripe_subscription_id')
    op.drop_column('organizations', 'stripe_customer_id')
