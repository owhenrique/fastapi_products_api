from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from fastapi_products_api.dependencies import T_CurrentUser, T_Session
from fastapi_products_api.models.product_user import ProductUser
from fastapi_products_api.models.products import Product
from fastapi_products_api.schemas.inventory import (
    FilterUserInventory,
    ResponseUserInventoryAddProduct,
    ResponseUserInventoryReadList,
    ResponseUserInventoryReadProduct,
    UserInventoryAddProduct,
)

router = APIRouter(prefix='/inventory', tags=['inventory'])


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseUserInventoryAddProduct,
)
async def add_product_to_user_inventory(
    inventory: UserInventoryAddProduct,
    current_user: T_CurrentUser,
    session: T_Session,
):
    db_product = await session.scalar(
        select(Product).where(Product.id == inventory.product_id)
    )

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    new_inventory = ProductUser(
        user_id=current_user.id,
        product_id=inventory.product_id,
        quantity=inventory.quantity,
    )

    session.add(new_inventory)
    await session.commit()
    await session.refresh(new_inventory)

    return new_inventory


@router.get('/{product_id}', response_model=ResponseUserInventoryReadProduct)
async def read_product_inventory_by_product_id(
    product_id: int, current_user: T_CurrentUser, session: T_Session
):
    stmt = (
        select(
            ProductUser.quantity,
            ProductUser.product_id,
            Product.name,
            Product.brand,
            Product.price,
            Product.type,
        )
        .join_from(ProductUser, Product)
        .where(
            ProductUser.user_id == current_user.id,
            ProductUser.product_id == product_id,
        )
    )

    if inventory_data := (await session.execute(stmt)).mappings().first():
        return inventory_data

    raise HTTPException(status_code=404, detail='Product not found')


@router.get('/', response_model=ResponseUserInventoryReadList)
async def read_product_inventory_list(
    filter_products: Annotated[FilterUserInventory, Query()],
    current_user: T_CurrentUser,
    session: T_Session,
):
    stmt = (
        select(
            ProductUser.quantity,
            Product.id.label('product_id'),
            Product.name,
            Product.brand,
            Product.price,
            Product.type,
        )
        .join_from(ProductUser, Product)
        .where(ProductUser.user_id == current_user.id)
        .offset(filter_products.offset)
        .limit(filter_products.limit)
    )

    result = await session.execute(stmt)
    products_data = result.mappings().all()

    return {'products': products_data}
