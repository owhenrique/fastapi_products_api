from http import HTTPStatus

from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.products import Product


def test_create_product_should_return_created(client):
    response = client.post(
        '/products',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand-1',
            'type': ProductType.CLOTHING,
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_product_should_return_ProductResponse(client, mock_db_time):
    with mock_db_time(model=Product):
        response = client.post(
            '/products',
            json={
                'name': 'test-product-1',
                'brand': 'test-brand-1',
                'type': ProductType.CLOTHING,
            },
        )

    assert response.json() == {
        'id': 1,
        'name': 'test-product-1',
        'brand': 'test-brand-1',
        'type': 'clothing',
        'created_at': '2012-12-21T00:00:00',
        'updated_at': '2012-12-21T00:00:00',
    }


def test_create_product_should_return_conflit(client, product):
    response = client.post(
        '/products',
        json={
            'name': 'test-product',
            'brand': 'test-brand',
            'type': ProductType.CLOTHING,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
