
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import Base


class UserMemory(Base):
    __tablename__ = "user_memories"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "memory_key",
            name="uq_user_memory_user_key",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)


    user_id: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    
    memory_key: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    memory_value: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
