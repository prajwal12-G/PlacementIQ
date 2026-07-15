"""
Authentication dependencies.

FastAPI dependency callables for the auth flow. These are wiring-only
functions — they compose repositories and services for a single request
and stay free of business logic and side effects beyond construction.
"""

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_auth_service() -> AuthService:
    """Build an `AuthService` wired with a fresh `UserRepository`.

    The database session is *not* opened here; it is supplied per call by
    the service's methods. This keeps the dependency cheap to construct,
    easy to override in tests (`app.dependency_overrides[get_auth_service]`),
    and free of any session-lifecycle concerns.

    Returns:
        A ready-to-use `AuthService` instance.
    """
    user_repository = UserRepository()
    return AuthService(user_repository)


__all__ = ["get_auth_service"]
