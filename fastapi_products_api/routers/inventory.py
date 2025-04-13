from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fastapi_products_api.dependencies import T_CurrentUser, T_Session
from fastapi_products_api.models.product_user import ProductUser
from fastapi_products_api.models.products import Product
from fastapi_products_api.schemas.inventory import (
    ResponseUserInventoryAddProduct,
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
