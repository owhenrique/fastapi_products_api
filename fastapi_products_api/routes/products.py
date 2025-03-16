from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_products_api.database import get_session
from fastapi_products_api.models.products import Product
from fastapi_products_api.schemas.products import (
    ProductCreate,
    ProductResponse,
)

router = APIRouter(prefix='/products', tags=['products'])

Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProductResponse
)
def create_product(product: ProductCreate, session: Session):
    db_product = session.scalar(
        select(Product).where(Product.name == product.name)
    )

    if db_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product name already exits',
        )

    new_product = Product(
        name=product.name, brand=product.brand, type=product.type
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product
