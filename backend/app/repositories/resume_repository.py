"""
Resume Repository.

Owns all persistence operations for the `Resume` aggregate. The
repository is a thin SQLAlchemy adapter — it knows how to read and
write `Resume` rows, and nothing else. File validation, UUID filename
generation, physical file I/O, parsing, and ATS analysis live in higher
layers.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:
    """Data-access object for the `Resume` table.

    A new instance is created per request via a dependency in
    `app/dependencies/`. The repository is stateless; the SQLAlchemy
    session is supplied per call so it can be scoped to a unit of work.
    """

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_id(self, db: Session, resume_id: int) -> Optional[Resume]:
        """Fetch a resume by its primary key.

        Args:
            db: Active SQLAlchemy session.
            resume_id: Numeric primary key of the resume.

        Returns:
            The matching `Resume` or `None` if no row exists.
        """
        return db.query(Resume).filter(Resume.id == resume_id).first()

    def get_all_by_user(self, db: Session, user_id: int) -> list[Resume]:
        """Fetch every resume owned by a user, newest first.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.

        Returns:
            A list of `Resume` rows belonging to the user, sorted by
            `uploaded_at` descending. Returns an empty list when the
            user has no resumes.
        """
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
            .all()
        )

    def get_active_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> Optional[Resume]:
        """Fetch the user's currently active resume.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.

        Returns:
            The active `Resume` (where `is_active=True`) or `None` if
            the user has no active resume.
        """
        return (
            db.query(Resume)
            .filter(
                Resume.user_id == user_id,
                Resume.is_active.is_(True),
            )
            .first()
        )

    def get_latest_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> Optional[Resume]:
        """Fetch the user's most recent resume version.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.

        Returns:
            The resume with the highest version number, or ``None`` if
            the user has not uploaded any resumes.
        """
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.version.desc())
            .first()
        )

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
        self,
        db: Session,
        user_id: int,
        title: str,
        original_filename: str,
        stored_filename: str,
        file_path: str,
        file_type: str,
        file_size: int,
        version: int = 1,
        is_active: bool = True,
    ) -> Resume:
        """Persist a new resume and return the refreshed ORM instance.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.
            title: User-supplied resume title.
            original_filename: Filename as originally uploaded by the user.
            stored_filename: Server-generated unique filename used on disk.
            file_path: Storage path of the uploaded resume.
            file_type: MIME type or extension of the resume file.
            file_size: Size of the resume file in bytes.
            version: Monotonically increasing version number for this
                resume.
            is_active: Whether this resume is the user's preferred
                version.

        Returns:
            The newly created `Resume`, refreshed from the database so
            server-default columns (e.g. `uploaded_at`, `updated_at`)
            are populated.
        """
        new_resume = Resume(
            user_id=user_id,
            title=title,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            version=version,
            is_active=is_active,
        )

        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)

        return new_resume

    def deactivate_all(
        self,
        db: Session,
        user_id: int,
    ) -> None:
        """Mark every resume owned by the user as inactive.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.
        """
        (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .update(
                {Resume.is_active: False},
                synchronize_session=False,
            )
        )

        db.commit()

    def activate(
        self,
        db: Session,
        resume: Resume,
    ) -> Resume:
        """Mark a resume as the user's active resume.

        Args:
            db: Active SQLAlchemy session.
            resume: The `Resume` ORM instance to activate.

        Returns:
            The activated `Resume`, refreshed from the database so
            `updated_at` reflects the new value.
        """
        resume.is_active = True

        db.commit()
        db.refresh(resume)

        return resume

    def delete(
        self,
        db: Session,
        resume: Resume,
    ) -> None:
        """Delete a resume's metadata row.

        Args:
            db: Active SQLAlchemy session.
            resume: The `Resume` ORM instance to remove.

        Note:
            This removes only the database row. Any associated physical
            file must be handled by the calling service.
        """
        db.delete(resume)
        db.commit()


__all__ = ["ResumeRepository"]