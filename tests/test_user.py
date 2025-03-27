from http import HTTPStatus

from fastapi_products_api.models.users import User
from fastapi_products_api.schemas.users import ResponseUser


def test_create_user_should_return_created(client):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_user_should_return_correct_user(client, mock_db_time):
    with mock_db_time(model=User) as time:
        response = client.post(
            '/users',
            json={
                'username': 'test',
                'email': 'test@test.com',
                'password': 'secret',
            },
        )

    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
        'is_superuser': False,
        'created_at': time.isoformat(),
        'updated_at': time.isoformat(),
    }


def test_create_user_should_return_conflict_user_email(client, other_user):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'other-test@mail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_should_return_conflict_user_username(client, other_user):
    response = client.post(
        '/users',
        json={
            'username': 'other-test-user',
            'email': 'test@mail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_read_user_should_return_ok(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK


def test_read_user_should_return_ResponseUser(client, user):
    user_schema = ResponseUser.model_validate(user).model_dump(mode='json')

    response = client.get(f'/users/{user.id}')

    assert response.json() == user_schema


def test_read_user_should_return_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_read_user_should_return_not_found_detail(client):
    response = client.get('/users/1')

    assert response.json() == {'detail': 'User not found'}


def test_read_users_should_return_ok(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK


def test_read_users_should_return_empty_users_list(client):
    response = client.get('/users')

    assert response.json() == {'users': []}


def test_read_users_should_return_ResponseUserList(client, user):
    user_schema = ResponseUser.model_validate(user).model_dump(mode='json')

    response = client.get('/users')

    assert response.json() == {'users': [user_schema]}


def test_update_user_should_return_ok(client, user, token):
    response = client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'johndoe',
            'email': 'jonh@doe.com',
            'password': 'my-secret-pwd',
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_should_return_ResponseUser(client, user, token):
    response = client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'johndoe',
            'email': 'jonh@doe.com',
            'password': 'my-secret-pwd',
        },
    )

    user_schema = ResponseUser.model_validate(response.json()).model_dump(
        mode='json'
    )

    assert response.json() == user_schema


def test_update_user_should_unauthorized(client, other_user, token):
    response = client.patch(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'johndoe',
            'email': 'jonh@doe.com',
            'password': 'my-secret-pwd',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_should_conflict_username(client, user, other_user, token):
    response = client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'other-test-user',
            'email': 'jonh@doe.com',
            'password': 'my-secret-pwd',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_update_user_should_conflict_email(client, user, other_user, token):
    response = client.patch(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'jonhdoe',
            'email': 'other-test@mail.com',
            'password': 'my-secret-pwd',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_user_should_return_ok(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK


def test_delete_user_should_return_unauthorized(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
