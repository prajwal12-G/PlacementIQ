"""
Resume Schemas.

Pydantic v2 models used by the resume API layer to validate request
payloads and shape response bodies. This module is intentionally
free of any database, ORM, or storage logic — it only describes
data contracts for resume metadata.

Resume *upload* itself is handled via multipart/form-data (UploadFile +
Form fields) and is therefore not represented here as a JSON request
schema. AI-derived fields (ATS score, parsed text, skills, embeddings,
match percentage, suggestions) intentionally do **not** live in this
module — they belong to dedicated downstream schemas.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Base schemas
# ---------------------------------------------------------------------------


class ResumeBase(BaseModel):
    """Shared resume fields reused across response schemas."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User-supplied title for this resume version.",
        examples=["Google SDE Intern Resume"],
    )


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class ResumeResponse(ResumeBase):
    """Public-facing representation of a resume's metadata."""

    id: int = Field(
        ...,
        description="Server-assigned unique identifier for the resume.",
        examples=[17],
    )
    user_id: int = Field(
        ...,
        description="Identifier of the owning user.",
        examples=[42],
    )
    original_filename: str = Field(
        ...,
        description="Filename as originally uploaded by the user.",
        examples=["prajwal_resume_v2.pdf"],
    )
    stored_filename: str = Field(
        ...,
        description="Server-generated unique filename used on disk.",
        examples=["7f3a1b2c-resume.pdf"],
    )
    file_path: str = Field(
        ...,
        description="Internal storage path of the uploaded resume.",
        examples=["/var/placementiq/resumes/7f3a1b2c-resume.pdf"],
    )
    file_type: str = Field(
        ...,
        description="MIME type or extension of the resume file.",
        examples=["application/pdf"],
    )
    file_size: int = Field(
        ...,
        ge=0,
        description="Size of the resume file in bytes.",
        examples=[184320],
    )
    version: int = Field(
        ...,
        ge=1,
        description="Monotonically increasing version number for this resume.",
        examples=[2],
    )
    is_active: bool = Field(
        ...,
        description="Whether this resume is the user's currently preferred version.",
        examples=[True],
    )
    uploaded_at: datetime = Field(
        ...,
        description="Timestamp at which the resume was first uploaded (UTC).",
        examples=["2026-07-12T10:15:00Z"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp at which the resume metadata was last updated (UTC).",
        examples=["2026-07-13T08:42:11Z"],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class ResumeListResponse(BaseModel):
    """Response body returned when listing a user's resumes."""

    resumes: list[ResumeResponse] = Field(
        ...,
        description="Collection of resume metadata records belonging to the user.",
    )


__all__ = [
    "ResumeBase",
    "ResumeResponse",
    "ResumeListResponse",
]
