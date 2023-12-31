"""Inital Database setup

Revision ID: 795f82aa698e
Revises: 
Create Date: 2023-12-15 05:58:17.219198

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from plutus.orchestration.models.links import Base

# revision identifiers, used by Alembic.
revision: str = "795f82aa698e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    Base.metadata.create_all(bind=op.get_bind())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
