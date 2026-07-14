"""
Security utilities.

This module centralizes authentication-related functionality for the
PlacementIQ backend, including:

- Password hashing
- Password verification
- JWT access token creation
- JWT access token verification

All security configuration (secret key, algorithm, expiration time) is
loaded from application settings.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ---------------------------------------------------------------------------
# Password Hashing Configuration
# ---------------------------------------------------------------------------

# CryptContext is the Passlib-recommended way to manage password hashing.
# Using a context allows hashing algorithms to be upgraded later without
# changing application code.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ---------------------------------------------------------------------------
# JWT Configuration
# ---------------------------------------------------------------------------

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Standard JWT claim names
JWT_SUBJECT_CLAIM = "sub"
JWT_EXPIRATION_CLAIM = "exp"


# ---------------------------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------------------------

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password.

    Returns:
        Secure bcrypt hash suitable for database storage.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a stored hash.

    Args:
        plain_password: Password supplied during login.
        hashed_password: Password hash stored in the database.

    Returns:
        True if the password is valid, otherwise False.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ---------------------------------------------------------------------------
# JWT Utilities
# ---------------------------------------------------------------------------

def create_access_token(data: dict[str, Any]) -> str:
    """
    Create a signed JWT access token.

    The supplied payload is copied and automatically enriched with an
    expiration timestamp before being cryptographically signed.

    Args:
        data: Payload to encode into the JWT.
              Typically contains {"sub": user.email}.

    Returns:
        Encoded JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode[JWT_EXPIRATION_CLAIM] = expire

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    This function validates:

    - Token signature
    - Expiration time
    - Signing algorithm

    Args:
        token: JWT access token.

    Returns:
        Decoded JWT payload.

    Raises:
        JWTError:
            If the token is invalid, malformed, or expired.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        raise


__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "verify_access_token",
    "JWT_SUBJECT_CLAIM",
    "JWT_EXPIRATION_CLAIM",
]