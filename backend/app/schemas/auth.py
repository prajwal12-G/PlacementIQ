"""
Authentication Schemas.

Pydantic v2 models used by the auth API layer to validate request payloads
and shape response bodies. This module is intentionally free of any
database, ORM, or JWT logic — it only describes data contracts.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------


class UserRegisterRequest(BaseModel):
    """Payload accepted by the user registration endpoint."""

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Full name of the registering user.",
        examples=["Prajwal Gupta"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address used for login and notifications.",
        examples=["prajwal@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Plain-text password; will be hashed server-side before storage.",
        examples=["S3cureP@ssword!"],
    )
    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Optional contact phone number.",
        examples=["+91-9876543210"],
    )
    college: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional college or institution name.",
        examples=["IIT Delhi"],
    )
    branch: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional academic branch / department.",
        examples=["Computer Science"],
    )
    graduation_year: Optional[int] = Field(
        default=None,
        ge=1950,
        le=2100,
        description="Optional expected graduation year.",
        examples=[2027],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class UserLoginRequest(BaseModel):
    """Payload accepted by the user login endpoint."""

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["prajwal@example.com"],
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=72,
        description="Plain-text password to verify against the stored hash.",
        examples=["S3cureP@ssword!"],
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class TokenResponse(BaseModel):
    """Response body returned after a successful login."""

    access_token: str = Field(
        ...,
        description="Opaque access token (typically a JWT) to be sent as `Authorization: Bearer <token>`.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="OAuth2 token type; always `bearer` for this API.",
        examples=["bearer"],
    )


class UserResponse(BaseModel):
    """Public-facing representation of a user account."""

    id: int = Field(
        ...,
        description="Server-assigned unique identifier for the user.",
        examples=[42],
    )
    full_name: str = Field(
        ...,
        description="Full name of the user.",
        examples=["Prajwal Gupta"],
    )
    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["prajwal@example.com"],
    )
    phone: Optional[str] = Field(
        default=None,
        description="Contact phone number, if provided.",
        examples=["+91-9876543210"],
    )
    college: Optional[str] = Field(
        default=None,
        description="College or institution, if provided.",
        examples=["IIT Delhi"],
    )
    branch: Optional[str] = Field(
        default=None,
        description="Academic branch, if provided.",
        examples=["Computer Science"],
    )
    graduation_year: Optional[int] = Field(
        default=None,
        description="Expected graduation year, if provided.",
        examples=[2027],
    )
    is_verified: bool = Field(
        ...,
        description="Whether the user has verified their email address.",
        examples=[False],
    )
    is_active: bool = Field(
        ...,
        description="Whether the user account is active and allowed to authenticate.",
        examples=[True],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp at which the user account was created (UTC).",
        examples=["2026-07-12T10:15:00Z"],
    )

    model_config = ConfigDict(
        from_attributes=True, 
        extra="ignore"
        )


__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "UserResponse",
]
