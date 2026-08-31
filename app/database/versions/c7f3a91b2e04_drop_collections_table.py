"""Drop collections table

Revision ID: c7f3a91b2e04
Revises: b019d2d86da0
Create Date: 2026-08-31 00:00:00.000000

"""

from typing import Sequence, Union

import sqlmodel.sql.sqltypes
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c7f3a91b2e04"
down_revision: Union[str, Sequence[str], None] = "b019d2d86da0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(
        "collections_index_0", table_name="collections", schema="arcana_vault"
    )
    op.drop_table("collections", schema="arcana_vault")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "collections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        schema="arcana_vault",
    )
    op.create_index(
        "collections_index_0",
        "collections",
        ["user_id"],
        unique=False,
        schema="arcana_vault",
    )
