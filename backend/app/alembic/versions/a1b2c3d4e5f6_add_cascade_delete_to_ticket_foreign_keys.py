"""add cascade delete to ticket foreign keys

Revision ID: a1b2c3d4e5f6
Revises: 5cf962e1e0c7
Create Date: 2026-11-09 07:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '5cf962e1e0c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing foreign keys and re-add with ondelete='CASCADE'
    op.drop_constraint('ticket_activities_ticket_id_fkey', 'ticket_activities', type_='foreignkey')
    op.create_foreign_key(
        'ticket_activities_ticket_id_fkey',
        'ticket_activities',
        'tickets',
        ['ticket_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('ticket_replies_ticket_id_fkey', 'ticket_replies', type_='foreignkey')
    op.create_foreign_key(
        'ticket_replies_ticket_id_fkey',
        'ticket_replies',
        'tickets',
        ['ticket_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('ticket_replies_ticket_id_fkey', 'ticket_replies', type_='foreignkey')
    op.create_foreign_key(
        'ticket_replies_ticket_id_fkey',
        'ticket_replies',
        'tickets',
        ['ticket_id'],
        ['id'],
    )

    op.drop_constraint('ticket_activities_ticket_id_fkey', 'ticket_activities', type_='foreignkey')
    op.create_foreign_key(
        'ticket_activities_ticket_id_fkey',
        'ticket_activities',
        'tickets',
        ['ticket_id'],
        ['id'],
    )
