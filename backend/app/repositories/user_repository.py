"""
User Repository.

Owns all persistence operations for the `User` aggregate. The repository
is a thin SQLAlchemy adapter — it knows how to read and write `User`
rows, and nothing else. Password hashing, business validation, and
authentication policy live in higher layers.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Data-access object for the `User` table.

    A new instance is created per request via a dependency in
    `app/dependencies/`. The repository is stateless; the SQLAlchemy
    session is supplied per call so it can be scoped to a unit of work.
    """

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Fetch a user by their email address.

        Args:
            db: Active SQLAlchemy session.
            email: Email address to look up.

        Returns:
            The matching `User` or `None` if no row exists.
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Fetch a user by their primary key.

        Args:
            db: Active SQLAlchemy session.
            user_id: Numeric primary key of the user.

        Returns:
            The matching `User` or `None` if no row exists.
        """
        return db.query(User).filter(User.id == user_id).first()

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def create(
        self,
        db: Session,
        full_name: str,
        email: str,
        password: str,
        phone: Optional[str] = None,
        college: Optional[str] = None,
        branch: Optional[str] = None,
        graduation_year: Optional[int] = None,
    ) -> User:
        """Persist a new user and return the refreshed ORM instance.

        The caller is responsible for supplying a *hashed* password — this
        method does not touch the value, only stores it.

        Args:
            db: Active SQLAlchemy session.
            full_name: User's full name.
            email: Unique email address.
            password: Hashed password (bcrypt or compatible).
            phone: Optional contact phone number.
            college: Optional college or institution name.
            branch: Optional academic branch / department.
            graduation_year: Optional expected graduation year.

        Returns:
            The newly created `User`, refreshed from the database so
            server-default columns (e.g. `created_at`) are populated.
        """
        new_user = User(
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            college=college,
            branch=branch,
            graduation_year=graduation_year,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


__all__ = ["UserRepository"]
