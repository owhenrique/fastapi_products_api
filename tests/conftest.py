import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_products_api.app import app
from fastapi_products_api.models.products import products_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    products_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    products_registry.metadata.drop_all(engine)
