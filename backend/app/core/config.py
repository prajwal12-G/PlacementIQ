"""
Application configuration.

Centralizes all application settings used throughout PlacementIQ.

Configuration values are primarily loaded from environment variables via
`.env`. Values that are unlikely to change between environments (such as
resume upload limits) are defined here as application constants.

This module should remain free of business logic.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings:
    """Application settings."""

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # ------------------------------------------------------------------
    # JWT Authentication
    # ------------------------------------------------------------------

    SECRET_KEY: str | None = os.getenv("SECRET_KEY")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # ------------------------------------------------------------------
    # Resume Upload Configuration
    # ------------------------------------------------------------------

    UPLOAD_DIR: str = "uploads/resumes"

    MAX_RESUME_SIZE: int = 5 * 1024 * 1024  # 5 MB

    ALLOWED_RESUME_EXTENSIONS: set[str] = {
        "pdf",
        "docx",
    }


settings = Settings()


__all__ = ["settings", "Settings"]