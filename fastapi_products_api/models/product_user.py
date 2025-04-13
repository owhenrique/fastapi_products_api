from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_products_api.registry import table_registry


@table_registry.mapped_as_dataclass
class ProductUser:
    __tablename__ = 'products_users'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id'), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
