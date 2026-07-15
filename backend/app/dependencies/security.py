"""
Security dependencies.

Contains reusable authentication dependencies for protected routes.

Responsibilities:
- Extract JWT from the Authorization header.
- Verify the JWT signature and expiration.
- Load the authenticated user from the database.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import (
    verify_access_token,
    JWT_SUBJECT_CLAIM,
)
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

# ---------------------------------------------------------------------------
# OAuth2 Bearer Token
# ---------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
)

# ---------------------------------------------------------------------------
# Current User Dependency
# ---------------------------------------------------------------------------


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate the JWT and return the authenticated user.

    Args:
        token: JWT extracted from Authorization header.
        db: Active database session.

    Returns:
        Authenticated User instance.

    Raises:
        HTTPException:
            401 if the token is invalid, expired, or the user no longer exists.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = verify_access_token(token)

        email = payload.get(JWT_SUBJECT_CLAIM)

        if email is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    repository = UserRepository()

    user = repository.get_by_email(
        db,
        email,
    )

    if user is None:
        raise credentials_exception

    return user