from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.warehouse import WarehouseResponse, WarehouseUpdate
from app.services.warehouse_service import WarehouseService

router = APIRouter()


@router.get("/by-column", response_model=WarehouseResponse)
def get_warehouse_by_column(
    column: Annotated[str, Query(pattern="^(id|name|city)$")],
    value: Annotated[str, Query(min_length=1)],
    db: Session = Depends(get_db),
) -> WarehouseResponse:
    """Fetch a single warehouse by one supported warehouse column."""
    try:
        warehouse = WarehouseService(db).get_warehouse_by_column(column, value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return WarehouseResponse.model_validate(warehouse)


@router.patch("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse_by_id(
    warehouse_id: int,
    payload: WarehouseUpdate,
    db: Session = Depends(get_db),
) -> WarehouseResponse:
    """Update a warehouse by id."""
    try:
        warehouse = WarehouseService(db).update_warehouse_by_id(warehouse_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return WarehouseResponse.model_validate(warehouse)
