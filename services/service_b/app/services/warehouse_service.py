from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse
from app.repositories.warehouse_repository import WarehouseRepository
from app.schemas.warehouse import WarehouseUpdate


class WarehouseService:
    """Business operations for warehouse lookup and updates."""

    allowed_columns = {"id", "name", "city"}

    def __init__(self, db: Session) -> None:
        """Initialize the service with a request-scoped database session."""
        self.repository = WarehouseRepository(db)

    def get_warehouse_by_column(self, column: str, value: str) -> Warehouse | None:
        """Fetch a warehouse by a supported column name and string query value."""
        if column not in self.allowed_columns:
            raise ValueError(f"Unsupported warehouse lookup column: {column}")

        if column == "id" and not value.isdigit():
            raise ValueError("Warehouse id must be a number")

        return self.repository.get_by_column(column, value)

    def update_warehouse_by_id(
        self,
        warehouse_id: int,
        payload: WarehouseUpdate,
    ) -> Warehouse | None:
        """Update a warehouse identified by id using only provided fields."""
        update_values = payload.model_dump(exclude_unset=True)
        if not update_values:
            raise ValueError("At least one field is required for update")

        return self.repository.update_by_id(warehouse_id, update_values)
