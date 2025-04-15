from datetime import datetime

from pydantic import BaseModel

from fastapi_products_api.models.enums import ProductType


class InventoryBase(BaseModel):
    product_id: int


class UserInventoryAddProduct(InventoryBase):
    quantity: int | None = 1


class ResponseUserInventoryAddProduct(InventoryBase):
    user_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime


class ResponseUserInventoryReadProduct(InventoryBase):
    name: str
    brand: str
    price: float
    type: ProductType
    quantity: int