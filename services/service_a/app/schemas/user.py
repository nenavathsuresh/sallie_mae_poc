from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserUpdate(BaseModel):
    """Fields allowed when updating a user."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=15)


class UserResponse(BaseModel):
    """User payload returned by the API."""

    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
