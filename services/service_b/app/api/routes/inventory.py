from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.inventory import InventoryResponse, InventoryUpdate
from app.services.inventory_service import InventoryService

router = APIRouter()


@router.get("/by-column", response_model=InventoryResponse)
def get_inventory_by_column(
    column: Annotated[str, Query(pattern="^(id|warehouse_id|product_name|quantity)$")],
    value: Annotated[str, Query(min_length=1)],
    db: Session = Depends(get_db),
) -> InventoryResponse:
    """Fetch a single inventory row by one supported inventory column."""
    try:
        inventory = InventoryService(db).get_inventory_by_column(column, value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return InventoryResponse.model_validate(inventory)


@router.patch("/{inventory_id}", response_model=InventoryResponse)
def update_inventory_by_id(
    inventory_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
) -> InventoryResponse:
    """Update an inventory row by id."""
    try:
        inventory = InventoryService(db).update_inventory_by_id(inventory_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")

    return InventoryResponse.model_validate(inventory)
