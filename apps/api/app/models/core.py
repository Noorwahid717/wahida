"""Core SQLAlchemy models describing the primary Wahida data schema."""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from typing import Any, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class UserRole(str, enum.Enum):
    """Roles supported by the platform."""

    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"


class ClassRoom(Base):
    """Represents a classroom grouping for users."""

    __tablename__ = "classes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[str] = mapped_column(String(16), nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="classroom")
    contents: Mapped[list["Content"]] = relationship(back_populates="classroom")


class User(Base):
    """Application users including students, teachers, and parents."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    class_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classes.id", ondelete="SET NULL"), nullable=True
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)

    classroom: Mapped[Optional[ClassRoom]] = relationship(back_populates="users")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="user")
    streak: Mapped[Optional["Streak"]] = relationship(back_populates="user", uselist=False)
    badges: Mapped[list["UserBadge"]] = relationship(back_populates="user")
    events: Mapped[list["AnalyticsEvent"]] = relationship(back_populates="user")


class Content(Base):
    """Learning content metadata."""

    __tablename__ = "contents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    class_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classes.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[str] = mapped_column(String(16), nullable=False)
    topic: Mapped[str] = mapped_column(String(128), nullable=False)
    level: Mapped[str] = mapped_column(String(32), nullable=False)
    md_url: Mapped[str] = mapped_column(String(512), nullable=False)
    tokens: Mapped[int] = mapped_column(Integer, nullable=False)

    classroom: Mapped[Optional[ClassRoom]] = relationship(back_populates="contents")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="content")


class Chunk(Base):
    """Chunked sections of learning content for retrieval."""

    __tablename__ = "chunks"
    __table_args__ = (
        UniqueConstraint("content_id", "ord", name="uq_chunk_content_ord"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contents.id", ondelete="CASCADE"), nullable=False
    )
    ord: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    content: Mapped[Content] = relationship(back_populates="chunks")
    embedding: Mapped[Optional["Embedding"]] = relationship(back_populates="chunk", uselist=False)


class Embedding(Base):
    """Vector representation for a chunk."""

    __tablename__ = "embeddings"

    chunk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chunks.id", ondelete="CASCADE"), primary_key=True
    )
    vec: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)

    chunk: Mapped[Chunk] = relationship(back_populates="embedding")


class ExerciseType(str, enum.Enum):
    """Exercise modalities supported by the system."""

    MCQ = "mcq"
    CODE = "code"
    SHORT = "short"


class Exercise(Base):
    """Practice items and assessments."""

    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type: Mapped[ExerciseType] = mapped_column(
        Enum(ExerciseType, name="exercise_type"), nullable=False
    )
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    answer_key: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    attempts: Mapped[list["Attempt"]] = relationship(back_populates="exercise")


class Attempt(Base):
    """Tracks how users interact with exercises."""

    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="attempts")
    exercise: Mapped[Exercise] = relationship(back_populates="attempts")


class Streak(Base):
    """Aggregated streak data for users."""

    __tablename__ = "streaks"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    current: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    longest: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_day_done: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    user: Mapped[User] = relationship(back_populates="streak")


class Badge(Base):
    """Achievement metadata."""

    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    rule: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    icon: Mapped[str] = mapped_column(String(255), nullable=False)

    awarded_users: Mapped[list["UserBadge"]] = relationship(back_populates="badge")


class UserBadge(Base):
    """Association table between users and badges."""

    __tablename__ = "user_badges"
    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badges_user_badge"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    badge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False
    )
    awarded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped[User] = relationship(back_populates="badges")
    badge: Mapped[Badge] = relationship(back_populates="awarded_users")


class AnalyticsEvent(Base):
    """Captures analytics events emitted by the product."""

    __tablename__ = "events_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    event_name: Mapped[str] = mapped_column(String(255), nullable=False)
    props: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped[Optional[User]] = relationship(back_populates="events")


__all__ = [
    "AnalyticsEvent",
    "Attempt",
    "Badge",
    "Chunk",
    "ClassRoom",
    "Content",
    "Embedding",
    "Exercise",
    "ExerciseType",
    "Streak",
    "User",
    "UserBadge",
    "UserRole",
]
