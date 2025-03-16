from pydantic import BaseModel, ConfigDict

from fastapi_products_api.models.enums import ProductType


class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    type: ProductType


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductsResponse(BaseModel):
    products: list[ProductResponse]


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100
