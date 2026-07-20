from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse


class WarehouseRepository:
    """Database access methods for warehouse records."""

    allowed_columns = {
        "id": Warehouse.id,
        "name": Warehouse.name,
        "city": Warehouse.city,
    }

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an active database session."""
        self.db = db

    def get_by_column(self, column: str, value: str) -> Warehouse | None:
        """Return one warehouse matching an allowed column and value."""
        model_column = self.allowed_columns.get(column)
        if model_column is None:
            return None

        query_value = int(value) if column == "id" else value
        statement = select(Warehouse).where(model_column == query_value)

        return self.db.execute(statement).scalar_one_or_none()

    def update_by_id(self, warehouse_id: int, values: dict[str, object]) -> Warehouse | None:
        """Update a warehouse by id and return the refreshed row."""
        warehouse = self.db.get(Warehouse, warehouse_id)
        if warehouse is None:
            return None

        for field, value in values.items():
            setattr(warehouse, field, value)

        self.db.commit()
        self.db.refresh(warehouse)

        return warehouse
