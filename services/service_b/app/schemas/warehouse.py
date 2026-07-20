from pydantic import BaseModel, ConfigDict, Field


class WarehouseUpdate(BaseModel):
    """Fields allowed when updating a warehouse."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    city: str | None = Field(default=None, min_length=1, max_length=100)


class WarehouseResponse(BaseModel):
    """Warehouse payload returned by the API."""

    id: int
    name: str
    city: str

    model_config = ConfigDict(from_attributes=True)
