from jwt import decode

from fastapi_products_api.security import create_access_token, settings


def test_create_access_token_function():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
