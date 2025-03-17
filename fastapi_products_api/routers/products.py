from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Query
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_products_api.database import get_session
from fastapi_products_api.models.products import Product
from fastapi_products_api.schemas.products import (
    FilterPage,
    ProductCreate,
    ProductResponse,
    ProductsResponse,
    ProductUpdate,
)

router = APIRouter(prefix='/products', tags=['products'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=ProductResponse
)
def create_product(product: ProductCreate, session: T_Session):
    db_product = session.scalar(
        select(Product).where(Product.name == product.name)
    )

    if db_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product name already exits',
        )

    new_product = Product(
        name=product.name,
        brand=product.brand,
        type=product.type,
        price=product.price,
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product


@router.get('/', response_model=ProductsResponse)
def read_products(
    filter_products: Annotated[FilterPage, Query()], session: T_Session
):
    products = session.scalars(
        select(Product)
        .offset(filter_products.offset)
        .limit(filter_products.limit)
    ).all()

    return {'products': products}


@router.get('/{product_id}', response_model=ProductResponse)
def read_product(product_id: int, session: T_Session):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    return db_product


@router.put('/{product_id}', response_model=ProductResponse)
def update_product(product_id, product: ProductUpdate, session: T_Session):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    try:
        db_product.name = product.name
        db_product.brand = product.brand
        db_product.price = product.price
        db_product.type = product.type

        session.add(db_product)
        session.commit()
        session.refresh(db_product)

        return db_product

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Product name already exists',
        )


@router.delete('/{product_id}', response_model=ProductResponse)
def delete_product(product_id: int, session: T_Session):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    deleted_product = db_product

    session.delete(db_product)
    session.commit()

    return deleted_product
