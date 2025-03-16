from datetime import datetime

from pydantic import BaseModel, ConfigDict

from fastapi_products_api.models.enums import ProductType


class ProductBase(BaseModel):
    name: str
    brand: str
    type: ProductType


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
