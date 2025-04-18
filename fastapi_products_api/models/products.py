from datetime import datetime

from sqlalchemy import Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.registry import table_registry


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=None)
    brand: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Numeric(scale=2), nullable=False)
    type: Mapped[ProductType] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
