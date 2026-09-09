# app/models/inventory.py

from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "store_id",
            name="uq_inventory_product_store",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
    )

    quantity_on_hand: Mapped[int] = mapped_column(
        nullable=False,
    )

    reorder_threshold: Mapped[int] = mapped_column(
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Inventory(id={self.id}, "
            f"product_id={self.product_id}, "
            f"store_id={self.store_id}, "
            f"quantity_on_hand={self.quantity_on_hand})"
        )