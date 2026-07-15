"""
Resume Service.

Owns the business logic for resume uploads. The service orchestrates
the resume repository, filesystem utilities, and application settings
to enforce upload rules (extension whitelist, size limit, versioning,
active-resume replacement) without knowing anything about HTTP
requests, JSON serialization, or the underlying filesystem layout.
"""

from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.resume import Resume
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.utils.file_storage import (
    delete_uploaded_file,
    generate_unique_filename,
    get_file_extension,
    save_uploaded_file,
)


class ResumeService:
    """Service layer for resume upload and metadata management."""

    def __init__(self, resume_repository: ResumeRepository) -> None:
        """Initialize the service with its dependencies."""
        self._resume_repository = resume_repository
        self._upload_directory = Path(settings.UPLOAD_DIR)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upload_resume(
        self,
        db: Session,
        current_user: User,
        title: str,
        file: UploadFile,
    ) -> Resume:
        """
        Validate, persist, and register a new resume upload.

        Args:
            db: Active SQLAlchemy session.
            current_user: The authenticated user uploading the resume.
            title: User-supplied title for this resume version.
            file: The uploaded file (multipart/form-data).

        Returns:
            The newly created :class:`Resume` ORM instance.

        Raises:
            HTTPException:
                * ``400`` if the filename is empty.
                * ``400`` if the file extension is not allowed.
                * ``400`` if the file size exceeds the configured limit.
        """
        title = title.strip()

        original_filename = self._require_filename(file)

        file_extension = get_file_extension(original_filename)
        self._validate_extension(file_extension)

        file_size = self._measure_file_size(file)
        self._validate_file_size(file_size)

        stored_filename = generate_unique_filename(original_filename)

        stored_path = save_uploaded_file(
            file=file,
            directory=self._upload_directory,
            filename=stored_filename,
        )

        version = self._next_version(db, current_user.id)

        self._resume_repository.deactivate_all(db, current_user.id)

        try:
            new_resume = self._resume_repository.create(
                db=db,
                user_id=current_user.id,
                title=title,
                original_filename=original_filename,
                stored_filename=stored_filename,
                file_path=stored_path.as_posix(),
                file_type=file_extension,
                file_size=file_size,
                version=version,
                is_active=True,
            )

        except Exception:
            delete_uploaded_file(stored_path)
            raise

        return new_resume

    def get_user_resumes(
        self,
        db: Session,
        current_user: User,
    ) -> list[Resume]:
        """
        Return every resume owned by the authenticated user.

        Args:
            db: Active SQLAlchemy session.
            current_user: The authenticated user whose resumes are fetched.

        Returns:
            A list of :class:`Resume` ORM instances owned by the authenticated user,
            ordered from newest to oldest.
        """
        return self._resume_repository.get_all_by_user(
            db,
            current_user.id,
        )

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _require_filename(file: UploadFile) -> str:
        """
        Ensure the uploaded file carries a non-empty filename.

        Args:
            file: The uploaded file.

        Returns:
            The trimmed original filename.

        Raises:
            HTTPException: ``400`` if the filename is missing or empty.
        """
        filename = (file.filename or "").strip()

        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required.",
            )

        return filename

    @staticmethod
    def _validate_extension(file_extension: str) -> None:
        """
        Reject files whose extension is not in the allow-list.

        Args:
            file_extension: Lowercased file extension (no leading dot).

        Raises:
            HTTPException: ``400`` if the extension is not allowed.
        """
        if file_extension not in settings.ALLOWED_RESUME_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

    @staticmethod
    def _validate_file_size(file_size: int) -> None:
        """
        Reject files larger than the configured maximum.

        Args:
            file_size: Measured size of the upload in bytes.

        Raises:
            HTTPException: ``400`` if the upload exceeds the limit.
        """
        if file_size > settings.MAX_RESUME_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds the allowed limit.",
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _measure_file_size(file: UploadFile) -> int:
        """
        Determine the size of an uploaded file by reading the stream.

        The stream is rewound to position 0 before returning so the
        subsequent save is able to read the bytes again.

        Args:
            file: The uploaded file.

        Returns:
            Size of the upload in bytes.
        """
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        return size

    def _next_version(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Compute the version number for the next uploaded resume.

        Args:
            db: Active SQLAlchemy session.
            user_id: Identifier of the owning user.

        Returns:
            ``1`` when the user has no prior resumes, otherwise
            ``latest.version + 1``.
        """
        latest = self._resume_repository.get_latest_by_user(
            db,
            user_id,
        )

        if latest is None:
            return 1

        return latest.version + 1


__all__ = ["ResumeService"]