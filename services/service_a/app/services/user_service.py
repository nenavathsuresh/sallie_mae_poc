from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate


class UserService:
    """Business operations for user lookup and updates."""

    allowed_columns = {"id", "name", "email", "phone"}

    def __init__(self, db: Session) -> None:
        """Initialize the service with a request-scoped database session."""
        self.repository = UserRepository(db)

    def get_user_by_column(self, column: str, value: str) -> User | None:
        """Fetch a user by a supported column name and string query value."""
        if column not in self.allowed_columns:
            raise ValueError(f"Unsupported user lookup column: {column}")

        if column == "id" and not value.isdigit():
            raise ValueError("User id must be a number")

        return self.repository.get_by_column(column, value)

    def get_customer_id_by_email(self, email: str) -> int | None:
        """Return the customer id for an email address, if the user exists."""
        user = self.repository.get_by_email(email)
        return user.id if user else None

    def update_user_by_email(self, email: str, payload: UserUpdate) -> User | None:
        """Update a user identified by email using only provided payload fields."""
        update_values = payload.model_dump(exclude_unset=True)
        if not update_values:
            raise ValueError("At least one field is required for update")

        return self.repository.update_by_email(email, update_values)
