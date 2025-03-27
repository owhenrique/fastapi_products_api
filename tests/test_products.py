from http import HTTPStatus

from fastapi_products_api.models.enums import ProductType
from fastapi_products_api.models.products import Product
from fastapi_products_api.schemas.products import ProductResponse


def test_create_product_should_return_created(client):
    response = client.post(
        '/products',
        headers={},
        json={
            'name': 'test-product-1',
            'brand': 'test-brand-1',
            'price': 299.99,
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
                'price': 299.99,
                'type': ProductType.CLOTHING,
            },
        )

    parsed_response = response.json()

    product_schema = ProductResponse.model_validate(
        parsed_response
    ).model_dump()

    assert response.json() == product_schema


def test_create_product_should_return_conflit(client, product):
    response = client.post(
        '/products',
        json={
            'name': 'test-product',
            'brand': 'test-brand',
            'price': 299.99,
            'type': ProductType.CLOTHING,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_read_products_should_return_ok(client):
    response = client.get('/products')

    assert response.status_code == HTTPStatus.OK


def test_read_products_should_return_empty_product_list(client):
    response = client.get('/products')

    assert response.json() == {'products': []}


def test_read_products_should_return_product_list(client, product):
    product_schema = ProductResponse.model_validate(product).model_dump()
    response = client.get('/products')

    assert response.json() == {'products': [product_schema]}


def test_read_product_should_return_ok(client, product):
    response = client.get(f'/products/{product.id}')

    assert response.status_code == HTTPStatus.OK


def test_read_product_should_return_product(client, product):
    product_schema = ProductResponse.model_validate(product).model_dump()
    response = client.get(f'/products/{product.id}')

    assert response.json() == product_schema


def test_read_product_should_return_not_found(client):
    response = client.get('/products/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_product_should_return_ok(client, product):
    response = client.put(
        f'/products/{product.id}',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand-1',
            'price': 299.99,
            'type': ProductType.ELECTRONICS,
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_product_should_return_product(client, product):
    response = client.put(
        f'/products/{product.id}',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand-1',
            'price': 299.99,
            'type': ProductType.ELECTRONICS,
        },
    )
    product_schema = ProductResponse.model_validate(product).model_dump()

    assert response.json() == product_schema


def test_update_product_should_return_not_found(client):
    response = client.put(
        '/products/1',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand-1',
            'price': 299.99,
            'type': ProductType.ELECTRONICS,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_product_should_return_conflict(client, product):
    client.post(
        '/products',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand',
            'price': 299.99,
            'type': ProductType.CLOTHING,
        },
    )

    response = client.put(
        f'/products/{product.id}',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand',
            'price': 299.99,
            'type': ProductType.ELECTRONICS,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_update_product_should_return_integrity_error(client, product):
    client.post(
        '/products',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand',
            'price': 299.99,
            'type': ProductType.CLOTHING,
        },
    )

    response = client.put(
        f'/products/{product.id}',
        json={
            'name': 'test-product-1',
            'brand': 'test-brand',
            'price': 299.99,
            'type': ProductType.ELECTRONICS,
        },
    )

    assert response.json() == {'detail': 'Product name already exists'}


def test_delete_product_should_return_ok(client, product):
    response = client.delete(f'/products/{product.id}')

    assert response.status_code == HTTPStatus.OK


def test_delete_product_should_return_product(client, product):
    product_schema = ProductResponse.model_validate(product).model_dump()
    response = client.delete(f'/products/{product.id}')

    assert response.json() == product_schema


def test_delete_product_should_return_not_found(client):
    response = client.delete('/products/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
