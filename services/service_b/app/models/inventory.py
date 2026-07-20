from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.warehouse import Warehouse


class Inventory(Base):
    """Product quantity available in a warehouse."""

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    warehouse_id: Mapped[int] = mapped_column(
        ForeignKey(
            "warehouses.id",
            name="fk_inventory_warehouse",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    product_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(default=0, server_default="0", nullable=False)

    warehouse: Mapped["Warehouse"] = relationship(back_populates="inventory_items")
