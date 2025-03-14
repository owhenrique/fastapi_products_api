from http import HTTPStatus


def test_read_index_should_return_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
