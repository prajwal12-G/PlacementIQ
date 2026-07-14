"""
Resume dependencies.

FastAPI dependency callables for the resume module. These are
wiring-only functions — they compose repositories and services for a
single request and stay free of business logic, file operations, and
direct database access.
"""

from app.repositories.resume_repository import ResumeRepository
from app.services.resume_service import ResumeService


def get_resume_service() -> ResumeService:
    """Build a ``ResumeService`` wired with a fresh ``ResumeRepository``.

    The database session is *not* opened here; it is supplied per call
    by the service's methods. This keeps the dependency cheap to
    construct, easy to override in tests
    (``app.dependency_overrides[get_resume_service]``), and free of any
    session-lifecycle concerns.

    Returns:
        A ready-to-use ``ResumeService`` instance.
    """
    resume_repository = ResumeRepository()
    resume_service = ResumeService(resume_repository)

    return resume_service


__all__ = ["get_resume_service"]