from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_products_api.database import get_session
from fastapi_products_api.models.users import User
from fastapi_products_api.schemas.auth import OAuth_scheme
from fastapi_products_api.settings import Settings

settings = Settings()

pwd_context = PasswordHash.recommended()

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_Token = Annotated[str, Depends(OAuth_scheme)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(session: T_Session, token: T_Token):
    credentials_exeception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials!',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_username = payload.get('sub')

        if not subject_username:
            raise credentials_exeception

    except DecodeError:
        raise credentials_exeception

    except ExpiredSignatureError:
        raise credentials_exeception

    db_user = await session.scalar(
        select(User).where(User.username == subject_username)
    )

    if not db_user:
        raise credentials_exeception

    return db_user
