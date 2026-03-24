"""fixup_UUID

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-21 12:41:16.174375

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, Sequence[str], None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Используем batch_alter_table для sensor_data
    with op.batch_alter_table("sensor_data", schema=None) as batch_op:
        batch_op.alter_column(
            "sensor_sn",
            existing_type=sa.CHAR(length=32),
            type_=sa.UUID(),
            existing_nullable=False,
        )

    # Используем batch_alter_table для sensors
    with op.batch_alter_table("sensors", schema=None) as batch_op:
        batch_op.alter_column(
            "serial_number",
            existing_type=sa.CHAR(length=32),
            type_=sa.UUID(),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("sensors", schema=None) as batch_op:
        batch_op.alter_column(
            "serial_number",
            existing_type=sa.UUID(),
            type_=sa.CHAR(length=32),
            existing_nullable=False,
        )

    with op.batch_alter_table("sensor_data", schema=None) as batch_op:
        batch_op.alter_column(
            "sensor_sn",
            existing_type=sa.UUID(),
            type_=sa.CHAR(length=32),
            existing_nullable=False,
        )
