from app.db.base import Base
from app.db.session import get_engine
from app.models import Inventory, Warehouse

__all_models = (Inventory, Warehouse)


def create_tables() -> None:
    """Create database tables for all service B ORM models."""
    Base.metadata.create_all(bind=get_engine())
