from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from fastapi_products_api.app import app
from fastapi_products_api.database import get_session
from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.products import Product, products_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    products_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    products_registry.metadata.drop_all(engine)


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


@pytest.fixture
def product(session):
    new_product = Product(
        name='test-product',
        brand='test-brand',
        price=299.99,
        type=ProductType.TOYS_AND_GAMES,
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product
