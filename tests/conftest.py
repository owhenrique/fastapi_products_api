from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_products_api.app import app
from fastapi_products_api.database import get_session
from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.product_user import ProductUser
from fastapi_products_api.models.products import Product
from fastapi_products_api.models.users import User
from fastapi_products_api.registry import table_registry
from fastapi_products_api.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2012, 12, 21)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def product(session):
    new_product = Product(
        name='test-product',
        brand='test-brand',
        price=299.99,
        type=ProductType.TOYS_AND_GAMES,
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


@pytest_asyncio.fixture
async def user(session):
    password = 'secret'

    new_user = User(
        username='test-user',
        email='test@mail.com',
        password=get_password_hash(password),
        is_superuser=True,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    new_user.plain_password = password

    return new_user


@pytest_asyncio.fixture
async def other_user(session):
    password = 'secret'

    new_user = User(
        username='other-test-user',
        email='other-test@mail.com',
        password=get_password_hash(password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    new_user.plain_password = password

    return new_user


@pytest_asyncio.fixture
async def inventory(session, user, product):
    new_inventory = ProductUser(
        user_id=user.id, product_id=product.id, quantity=2
    )

    session.add(new_inventory)
    await session.commit()
    await session.refresh(new_inventory)

    return new_inventory


@pytest_asyncio.fixture
async def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.plain_password},
    )

    return response.json()['access_token']
