"""slug

Revision ID: 928708d5eec9
Revises: 922a0977e602
Create Date: 2025-05-20 22:46:43.139612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '928708d5eec9'
down_revision: Union[str, None] = '922a0977e602'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('slug', sa.String(), nullable=False))
    op.create_index(op.f('ix_bookings_slug'), 'bookings', ['slug'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bookings_slug'), table_name='bookings')
    op.drop_column('bookings', 'slug')
    # ### end Alembic commands ###
