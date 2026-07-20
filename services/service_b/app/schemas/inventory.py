from pydantic import BaseModel, ConfigDict, Field


class InventoryUpdate(BaseModel):
    """Fields allowed when updating an inventory row."""

    warehouse_id: int | None = Field(default=None, gt=0)
    product_name: str | None = Field(default=None, min_length=1, max_length=100)
    quantity: int | None = Field(default=None, ge=0)


class InventoryResponse(BaseModel):
    """Inventory payload returned by the API."""

    id: int
    warehouse_id: int
    product_name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)
