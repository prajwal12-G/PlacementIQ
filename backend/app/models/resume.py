"""
Resume ORM model.

Stores resume file metadata for each user. Only metadata is persisted
on this model; file content, parsed text, ATS scores, embeddings, and
other AI-derived fields live in dedicated downstream models/services.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Resume(Base):
    """
    Resume metadata owned by a single user.

    A user may upload multiple resume versions over time.
    The ``is_active`` flag identifies the currently preferred resume.
    Deleting a user automatically deletes all associated resumes.
    """

    __tablename__ = "resumes"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="resumes",
    )

    # ------------------------------------------------------------------
    # Resume Information
    # ------------------------------------------------------------------

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Versioning
    # ------------------------------------------------------------------

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the resume."""
        return (
            f"<Resume(id={self.id}, "
            f"title='{self.title}', "
            f"user_id={self.user_id})>"
        )


__all__ = ["Resume"]