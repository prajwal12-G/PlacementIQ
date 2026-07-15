"""
Authentication Service.

Owns the business logic for user registration and authentication.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    UserRegisterRequest,
    TokenResponse,
)


class AuthService:
    """Service layer for registration and authentication."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_user(
        self,
        db: Session,
        user_data: UserRegisterRequest,
    ) -> User:

        existing_user = self._user_repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        hashed_password = hash_password(user_data.password)

        return self._user_repository.create(
            db=db,
            full_name=user_data.full_name,
            email=user_data.email,
            password=hashed_password,
            phone=user_data.phone,
            college=user_data.college,
            branch=user_data.branch,
            graduation_year=user_data.graduation_year,
        )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> Optional[User]:

        user = self._user_repository.get_by_email(db, email)

        if user is None:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    def login_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> TokenResponse:

        user = self.authenticate_user(
            db=db,
            email=email,
            password=password,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        access_token = create_access_token(
            data={"sub": user.email}
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )


__all__ = ["AuthService"]