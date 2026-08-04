"""create rag_chunks table

Revision ID: b7c4e1f92a03
Revises:
Create Date: 2026-08-04

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b7c4e1f92a03"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "rag_chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chunk_id", sa.String(length=255), nullable=False),
        sa.Column("source_file", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column("embedding_model", sa.String(length=100), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("document_version", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rag_chunks_chunk_id"), "rag_chunks", ["chunk_id"], unique=True)
    op.create_index(op.f("ix_rag_chunks_source_file"), "rag_chunks", ["source_file"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_rag_chunks_source_file"), table_name="rag_chunks")
    op.drop_index(op.f("ix_rag_chunks_chunk_id"), table_name="rag_chunks")
    op.drop_table("rag_chunks")
