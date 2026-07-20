from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Database access methods for user records."""

    allowed_columns = {
        "id": User.id,
        "name": User.name,
        "email": User.email,
        "phone": User.phone,
    }

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an active database session."""
        self.db = db

    def get_by_column(self, column: str, value: str) -> User | None:
        """Return one user matching an allowed column and value."""
        model_column = self.allowed_columns.get(column)
        if model_column is None:
            return None

        query_value = int(value) if column == "id" else value
        statement = select(User).where(model_column == query_value)

        return self.db.execute(statement).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        """Return one user by email address."""
        statement = select(User).where(User.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def update_by_email(self, email: str, values: dict[str, object]) -> User | None:
        """Update one user found by email and return the refreshed row."""
        user = self.get_by_email(email)
        if user is None:
            return None

        for field, value in values.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user
