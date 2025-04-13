from datetime import datetime

from pydantic import BaseModel


class InventoryBase(BaseModel):
    user_id: int
    product_id: int


class UserInventoryAddProduct(InventoryBase):
    quantity: int | None = 1


class ResponseUserInventoryAddProduct(InventoryBase):
    quantity: int
    created_at: datetime
    updated_at: datetime
