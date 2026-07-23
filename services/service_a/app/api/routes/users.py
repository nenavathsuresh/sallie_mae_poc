from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.services.smrules import Smrules

router = APIRouter()


@router.get("/by-column", response_model=UserResponse)
def get_user_by_column(
    column: Annotated[str, Query(pattern="^(id|name|email|phone)$")],
    value: Annotated[str, Query(min_length=1)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Fetch a single user by one supported user column."""
    try:
        user = UserService(db).get_user_by_column(column, value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)


@router.patch("/by-email/{email}", response_model=UserResponse)
def update_user_by_email(
    email: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Find a user by email and update provided user fields."""
    try:
        user = UserService(db).update_user_by_email(email, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)

@router.get("showrules")
def show_rules():
    try:
        rules = Smrules().show_rules()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return rules
