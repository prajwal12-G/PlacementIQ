from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    password = Column(String(255), nullable=False)

    phone = Column(String(15), nullable=True)

    college = Column(String(255), nullable=True)

    branch = Column(String(100), nullable=True)

    graduation_year = Column(Integer, nullable=True)

    is_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())