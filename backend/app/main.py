"""
FastAPI application entry point.

This module acts as the composition root of the PlacementIQ backend.

Responsibilities:
    1. Configure application logging.
    2. Create the FastAPI application.
    3. Register application lifespan events.
    4. Mount API routers.

Layering Rule:
    This file must remain free of business logic, database queries,
    authentication logic, and application-specific policies.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.core.logger import setup_logging
from app.db.database import Base, engine

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

setup_logging()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """
    Handle application startup and shutdown events.

    This replaces the deprecated ``@app.on_event("startup")`` approach.

    During development, SQLAlchemy creates missing database tables
    automatically using ``Base.metadata.create_all()``.

    NOTE:
        This is a temporary solution for development. Once Alembic
        migrations are introduced, this call will be removed and all
        schema management will be handled through migration scripts.
    """

    # Temporary database initialization.
    Base.metadata.create_all(bind=engine)

    logger.info("Database connected successfully.")

    # Application runs while execution is paused here.
    yield

    logger.info("Application shutdown complete.")


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PlacementIQ API",
    version="1.0.0",
    description="AI-Powered Placement Readiness Platform",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# API Routers
# ---------------------------------------------------------------------------

app.include_router(auth_router)

# ---------------------------------------------------------------------------
# Health Endpoints
# ---------------------------------------------------------------------------


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    """
    API landing endpoint.
    """
    return {"message": "Welcome to PlacementIQ API 🚀"}


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    """
    Lightweight health-check endpoint.

    Used by monitoring systems and container orchestration tools
    to verify that the application is running.
    """
    return {"status": "healthy"}


__all__ = ["app"]