from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.inventory import Inventory


class Warehouse(Base):
    """Warehouse location that can hold inventory records."""

    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    inventory_items: Mapped[list["Inventory"]] = relationship(
        back_populates="warehouse",
        cascade="all, delete-orphan",
    )
