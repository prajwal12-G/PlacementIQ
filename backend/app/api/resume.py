"""
Resume API routes.

Thin HTTP layer for resume operations. Endpoints here delegate the
actual work to `ResumeService` — they exist only to:

* accept a multipart/form-data upload,
* hand a DB session, an authenticated user, and a service to the
  request,
* shape the returned ORM object into the public response schema,
* set the right HTTP status code.

No SQL, no file I/O, no UUID generation, no extension or size
validation live in this file. Those concerns belong to the service
and repository layers.
"""

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.resume import get_resume_service
from app.dependencies.security import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeListResponse, ResumeResponse
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["Resume"],
)


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new resume",
    description=(
        "Upload a new resume file (multipart/form-data) for the "
        "authenticated user. The previous active resume, if any, is "
        "deactivated and the new upload becomes the active version. "
        "Returns the public representation of the newly created "
        "resume."
    ),
)
def upload_resume(
    title: str = Form(
        ...,
        min_length=1,
        max_length=100,
        description="User-supplied title for this resume version.",
    ),
    file: UploadFile = File(
        ...,
        description="Resume file to upload (PDF or DOCX).",
    ),
    db: Session = Depends(get_db),
    resume_service: ResumeService = Depends(get_resume_service),
    current_user: User = Depends(get_current_user),
) -> ResumeResponse:
    """Upload a new resume for the authenticated user.

    Args:
        title: Title for the new resume version (form field).
        file: Resume file supplied as multipart/form-data.
        db: Request-scoped SQLAlchemy session (provided by dependency).
        resume_service: Resume service wired with its repository
            (provided by dependency).
        current_user: The authenticated user uploading the resume
            (provided by dependency).

    Returns:
        A `ResumeResponse` describing the newly created resume.
    """
    resume = resume_service.upload_resume(
        db=db,
        current_user=current_user,
        title=title,
        file=file,
    )

    response = ResumeResponse.model_validate(resume)

    return response


@router.get(
    "",
    response_model=ResumeListResponse,
    status_code=status.HTTP_200_OK,
    summary="List the authenticated user's resumes",
    description=(
        "Return every resume uploaded by the authenticated user, "
        "ordered from newest to oldest. The list is empty when the "
        "user has not uploaded any resumes."
    ),
)
def list_user_resumes(
    db: Session = Depends(get_db),
    resume_service: ResumeService = Depends(get_resume_service),
    current_user: User = Depends(get_current_user),
) -> ResumeListResponse:
    """List every resume owned by the authenticated user.

    Args:
        db: Request-scoped SQLAlchemy session (provided by dependency).
        resume_service: Resume service wired with its repository
            (provided by dependency).
        current_user: The authenticated user whose resumes are fetched
            (provided by dependency).

    Returns:
        A `ResumeListResponse` containing the user's resume collection.
        The list is empty when the user has no resumes.
    """
    resumes = resume_service.get_user_resumes(
        db=db,
        current_user=current_user,
    )

    response = ResumeListResponse(
        resumes=[ResumeResponse.model_validate(resume) for resume in resumes],
    )

    return response


__all__ = ["router"]