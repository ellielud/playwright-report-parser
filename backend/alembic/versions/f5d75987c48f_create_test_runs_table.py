"""create test_runs table

Revision ID: f5d75987c48f
Revises: 
Create Date: 2025-06-12 20:29:10.269556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d75987c48f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE test_runs (
            id SERIAL PRIMARY KEY,
            test_name VARCHAR NOT NULL,
            status VARCHAR,
            error_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


def downgrade() -> None:
    pass
