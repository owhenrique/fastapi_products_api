from dataclasses import asdict
from decimal import Decimal

import pytest
from sqlalchemy import select

from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.product_user import ProductUser
from fastapi_products_api.models.products import Product
from fastapi_products_api.models.users import User


@pytest.mark.asyncio
async def test_create_product(session, mock_db_time):
    with mock_db_time(model=Product) as time:
        new_product = Product(
            name='kinder_joy',
            brand='kinder',
            price=13.99,
            type=ProductType.GROCERIES,
        )

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

    db_product = await session.scalar(
        select(Product).where(Product.id == new_product.id)
    )

    assert asdict(db_product) == {
        'id': 1,
        'name': 'kinder_joy',
        'brand': 'kinder',
        'price': Decimal('13.99'),
        'type': ProductType.GROCERIES,
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='admin0test',
            email='admin@test.com',
            password='secret',
            is_superuser=True,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

    db_user = await session.scalar(select(User).where(User.id == new_user.id))

    assert asdict(db_user) == {
        'id': 1,
        'username': 'admin0test',
        'email': 'admin@test.com',
        'password': 'secret',
        'is_superuser': True,
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_create_inventory(session, user, product, mock_db_time):
    with mock_db_time(model=ProductUser) as time:
        new_inventory = ProductUser(user_id=user.id, product_id=product.id)

        session.add(new_inventory)
        await session.commit()
        await session.refresh(new_inventory)

    db_inventory = await session.scalar(
        select(ProductUser).where(
            ProductUser.user_id == user.id,
            ProductUser.product_id == product.id,
        )
    )

    assert asdict(db_inventory) == {
        'user_id': user.id,
        'product_id': product.id,
        'quantity': 1,
        'created_at': time,
        'updated_at': time,
    }
