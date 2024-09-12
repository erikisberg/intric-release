"""completion model
Revision ID: 7b50df32c2f4
Revises: e3c6ceadc18f
Create Date: 2024-05-10 12:19:37.121278
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "7b50df32c2f4"
down_revision = "e3c6ceadc18f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "completion_models",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("token_limit", sa.Integer(), nullable=False),
        sa.Column("selectable", sa.Boolean(), nullable=False),
        sa.Column("nr_billion_parameters", sa.Integer(), nullable=True),
        sa.Column("hf_link", sa.String(), nullable=True),
        sa.Column(
            "family",
            sa.Enum("OPEN_AI", "MISTRAL", "VLLM", name="modelfamily"),
            nullable=False,
        ),
        sa.Column(
            "stability",
            sa.Enum("STABLE", "EXPERIMENTAL", name="modelstability"),
            nullable=False,
        ),
        sa.Column(
            "hosting", sa.Enum("USA", "EU", name="modelhostinglocation"), nullable=False
        ),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("completion_models")
    # ### end Alembic commands ###