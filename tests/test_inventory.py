from http import HTTPStatus

from fastapi_products_api.models.product_user import ProductUser


def test_add_product_to_user_inventory_should_return_created(
    client, product, token
):
    response = client.post(
        '/inventory',
        json={'product_id': product.id},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.CREATED


def test_add_product_to_user_inventory_should_return_ResponseSchema(
    client, user, product, token, mock_db_time
):
    with mock_db_time(model=ProductUser) as time:
        response = client.post(
            '/inventory',
            json={'product_id': product.id, 'quantity': 5},
            headers={'Authorization': f'Bearer {token}'}
        )

    assert response.json() == {
        'user_id': user.id,
        'product_id': product.id,
        'quantity': 5,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


def test_add_product_to_user_inventory_should_return_not_found(
    client, token
):
    response = client.post(
        '/inventory',
        json={'product_id': 999},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
