from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory


class InventoryRepository:
    """Database access methods for inventory records."""

    allowed_columns = {
        "id": Inventory.id,
        "warehouse_id": Inventory.warehouse_id,
        "product_name": Inventory.product_name,
        "quantity": Inventory.quantity,
    }

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an active database session."""
        self.db = db

    def get_by_column(self, column: str, value: str) -> Inventory | None:
        """Return one inventory row matching an allowed column and value."""
        model_column = self.allowed_columns.get(column)
        if model_column is None:
            return None

        query_value = int(value) if column in {"id", "warehouse_id", "quantity"} else value
        statement = select(Inventory).where(model_column == query_value)

        return self.db.execute(statement).scalar_one_or_none()

    def update_by_id(self, inventory_id: int, values: dict[str, object]) -> Inventory | None:
        """Update an inventory row by id and return the refreshed row."""
        inventory = self.db.get(Inventory, inventory_id)
        if inventory is None:
            return None

        for field, value in values.items():
            setattr(inventory, field, value)

        self.db.commit()
        self.db.refresh(inventory)

        return inventory
