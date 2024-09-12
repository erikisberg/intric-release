"""add embedding model
Revision ID: f86bab2a902c
Revises: e4857d967e73
Create Date: 2023-09-11 21:11:12.237174
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = 'f86bab2a902c'
down_revision = 'e4857d967e73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('info_blobs', sa.Column('embedding_model', sa.Text(), nullable=True))
    op.drop_column('info_blobs', 'path')
    op.add_column('settings', sa.Column('embedding_model', sa.Text(), nullable=True))

    op.execute("UPDATE info_blobs SET embedding_model = 'text-embedding-ada-002'")
    op.execute("UPDATE settings SET embedding_model = 'text-embedding-ada-002'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'embedding_model')
    op.add_column(
        'info_blobs', sa.Column('path', sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.drop_column('info_blobs', 'embedding_model')
    # ### end Alembic commands ###