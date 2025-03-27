from http import HTTPStatus


def test_login_for_access_token_should_return_ok(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.plain_password},
    )

    assert response.status_code == HTTPStatus.OK


def test_login_for_access_token_should_have_access_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.plain_password},
    )
    token = response.json()

    assert 'access_token' in token


def test_login_for_access_token_should_have_token_type(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.plain_password},
    )
    token = response.json()

    assert 'token_type' in token
