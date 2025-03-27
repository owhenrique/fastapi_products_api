from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fastapi_products_api.dependencies import T_OAuthForm, T_Session
from fastapi_products_api.models.users import User
from fastapi_products_api.schemas.auth import Token
from fastapi_products_api.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: T_OAuthForm, session: T_Session):
    db_user = await session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': db_user.username})

    return {'access_token': access_token}
