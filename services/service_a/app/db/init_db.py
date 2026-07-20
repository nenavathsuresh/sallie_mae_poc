from app.db.base import Base
from app.db.session import get_engine
from app.models import Order, OrderItem, Product, User

__all_models = (Order, OrderItem, Product, User)


def create_tables() -> None:
    Base.metadata.create_all(bind=get_engine())
