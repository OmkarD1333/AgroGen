
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    String,
    Boolean,
    CheckConstraint,
    Index,
    Identity,
    text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "preferred_language IN ('mr', 'en')",
            name="check_users_preferred_language",
        ),
        CheckConstraint(
            "role IN ('farmer', 'admin')",
            name="check_users_role",
        ),
        Index("idx_users_role", "role"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="farmer",
        server_default=text("'farmer'"),
    )

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

