from http import HTTPStatus

from fastapi_products_api.models.product_user import ProductUser
from fastapi_products_api.schemas.inventory import (
    ResponseUserInventoryReadList,
    ResponseUserInventoryReadProduct,
    ResponseUserInventoryUpdateProductQuantity,
)


def test_add_product_to_user_inventory_should_return_created(
    client, product, token
):
    response = client.post(
        '/inventory',
        json={'product_id': product.id},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED


def test_add_product_to_user_inventory_should_return_ResponseSchema(
    client, user, product, token, mock_db_time
):
    with mock_db_time(model=ProductUser) as time:
        response = client.post(
            '/inventory',
            json={'product_id': product.id, 'quantity': 5},
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.json() == {
        'product_id': product.id,
        'quantity': 5,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


def test_add_product_to_user_inventory_should_return_not_found(client, token):
    response = client.post(
        '/inventory',
        json={'product_id': 999},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_product_inventory_by_product_id_should_return_ok(
    client, token, product, inventory
):
    response = client.get(
        f'/inventory/{product.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_read_product_inventory_by_product_id_should_return_inventory(
    client, token, product, inventory
):
    response = client.get(
        f'/inventory/{product.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    parsed_response = response.json()

    inventory_schema = ResponseUserInventoryReadProduct.model_validate(
        parsed_response
    ).model_dump()

    assert response.json() == inventory_schema


def test_read_product_inventory_by_product_id_should_return_not_found(
    client, token, inventory
):
    response = client.get(
        '/inventory/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_product_inventory_list_should_return_ok(
    client, token, product, inventory
):
    response = client.get(
        '/inventory',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_read_product_inventory_list_should_return_inventory_list(
    client, token, product, inventory
):
    response = client.get(
        '/inventory',
        headers={'Authorization': f'Bearer {token}'},
    )

    parsed_response = response.json()

    inventory_schema = ResponseUserInventoryReadList.model_validate(
        parsed_response
    ).model_dump()

    assert response.json() == inventory_schema


def test_update_product_inventory_quantity_should_return_ok(
    client, token, product, inventory
):
    response = client.patch(
        '/inventory',
        json={'product_id': product.id, 'quantity': 5},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_update_product_inventory_quantity_should_return_inventory(
    client, token, product, inventory
):
    response = client.patch(
        '/inventory',
        json={'product_id': product.id, 'quantity': 5},
        headers={'Authorization': f'Bearer {token}'},
    )

    parsed_response = response.json()

    inventory_schema = (
        ResponseUserInventoryUpdateProductQuantity.model_validate(
            parsed_response
        ).model_dump()
    )

    assert response.json() == inventory_schema
