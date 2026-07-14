"""
Authentication API routes.

Thin HTTP layer for registration and (in future) login. Endpoints here
delegate the actual work to `AuthService` — they exist only to:
  * accept a request payload,
  * hand a DB session and a service to the request,
  * shape the returned ORM object into the public response schema,
  * set the right HTTP status code.

No SQL, no password hashing, no business rules live in this file.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import get_auth_service
from app.dependencies.database import get_db
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService
from app.dependencies.security import get_current_user
from app.models.user import User



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Create a new user account with the provided profile details. "
        "Returns the public representation of the created user."
    ),
)
def register(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Register a new user account.

    Args:
        payload: Validated registration payload from the request body.
        db: Request-scoped SQLAlchemy session (provided by dependency).
        auth_service: Auth service wired with its repository (provided
            by dependency).

    Returns:
        A `UserResponse` describing the newly created user.
    """
    user = auth_service.register_user(db, payload)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate a user and return a JWT access token.",
)
def login(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Authenticate an existing user and return a JWT access token.
    """
    return auth_service.login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
    description="Return the currently authenticated user's profile.",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the currently authenticated user's profile.

    This endpoint requires a valid JWT Bearer token.
    """
    return UserResponse.model_validate(current_user)

@router.post(
    "/token",
    response_model=TokenResponse,
    summary="OAuth2 compatible login",
    description="OAuth2 compatible login endpoint used by Swagger UI.",
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    OAuth2-compatible login endpoint.

    Swagger UI submits credentials as form data using the
    fields 'username' and 'password'. Since our application
    authenticates users by email, the username field is treated
    as the user's email.
    """
    return auth_service.login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )


__all__ = ["router"]
