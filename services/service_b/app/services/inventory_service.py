from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import InventoryUpdate


class InventoryService:
    """Business operations for inventory lookup and updates."""

    allowed_columns = {"id", "warehouse_id", "product_name", "quantity"}
    integer_columns = {"id", "warehouse_id", "quantity"}

    def __init__(self, db: Session) -> None:
        """Initialize the service with a request-scoped database session."""
        self.repository = InventoryRepository(db)

    def get_inventory_by_column(self, column: str, value: str) -> Inventory | None:
        """Fetch an inventory row by a supported column name and query value."""
        if column not in self.allowed_columns:
            raise ValueError(f"Unsupported inventory lookup column: {column}")

        if column in self.integer_columns and not value.isdigit():
            raise ValueError(f"Inventory {column} must be a number")

        return self.repository.get_by_column(column, value)

    def update_inventory_by_id(
        self,
        inventory_id: int,
        payload: InventoryUpdate,
    ) -> Inventory | None:
        """Update an inventory row identified by id using only provided fields."""
        update_values = payload.model_dump(exclude_unset=True)
        if not update_values:
            raise ValueError("At least one field is required for update")

        return self.repository.update_by_id(inventory_id, update_values)
