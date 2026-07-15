"""
Database dependencies.

FastAPI dependency callables that own the SQLAlchemy session lifecycle
for a single request. The yielded session is automatically closed even
if the route handler raises.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session scoped to a single request.

    The session is closed in a `finally` block so it is released even if
    the downstream route handler raises an exception. Callers commit or
    roll back explicitly; this dependency intentionally does neither.

    Yields:
        A SQLAlchemy `Session` bound to the application's engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["get_db"]
