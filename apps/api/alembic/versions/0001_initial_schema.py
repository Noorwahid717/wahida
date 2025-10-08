"""Initial schema for Wahida core models."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


user_role_enum = sa.Enum("student", "teacher", "parent", name="user_role")
exercise_type_enum = sa.Enum("mcq", "code", "short", name="exercise_type")


def upgrade() -> None:
    user_role_enum.create(op.get_bind(), checkfirst=True)
    exercise_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "classes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("grade", sa.String(length=16), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="SET NULL"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "contents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("class_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("grade", sa.String(length=16), nullable=False),
        sa.Column("topic", sa.String(length=128), nullable=False),
        sa.Column("level", sa.String(length=32), nullable=False),
        sa.Column("md_url", sa.String(length=512), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("content_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ord", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("tokens", sa.Integer(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["content_id"], ["contents.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("content_id", "ord", name="uq_chunk_content_ord"),
    )

    op.create_table(
        "embeddings",
        sa.Column("chunk_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vec", Vector(dim=1536), nullable=False),
        sa.ForeignKeyConstraint(["chunk_id"], ["chunks.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "exercises",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", exercise_type_enum, nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("answer_key", sa.JSON(), nullable=False),
    )

    op.create_table(
        "attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("exercise_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "streaks",
        sa.Column("user_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("current", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("longest", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_day_done", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "badges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("rule", sa.JSON(), nullable=False),
        sa.Column("icon", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "user_badges",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("badge_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("awarded_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["badge_id"], ["badges.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "badge_id", name="uq_user_badges_user_badge"),
    )

    op.create_table(
        "events_analytics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_name", sa.String(length=255), nullable=False),
        sa.Column("props", sa.JSON(), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
    )


def downgrade() -> None:
    op.drop_table("events_analytics")
    op.drop_table("user_badges")
    op.drop_table("badges")
    op.drop_table("streaks")
    op.drop_table("attempts")
    op.drop_table("exercises")
    op.drop_table("embeddings")
    op.drop_table("chunks")
    op.drop_table("contents")
    op.drop_table("users")
    op.drop_table("classes")
    exercise_type_enum.drop(op.get_bind(), checkfirst=True)
    user_role_enum.drop(op.get_bind(), checkfirst=True)
