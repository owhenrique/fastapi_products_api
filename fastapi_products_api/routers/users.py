from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_products_api.dependencies import T_CurrentUser, T_Session
from fastapi_products_api.models.users import User
from fastapi_products_api.schemas.users import (
    FilterUsers,
    ResponseUser,
    ResponseUserList,
    UserCreate,
    UserUpdate,
)
from fastapi_products_api.security import get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ResponseUser)
async def create_user(user: UserCreate, session: T_Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get('/{user_id}', response_model=ResponseUser)
async def read_user(user_id: int, session: T_Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@router.get('/', response_model=ResponseUserList)
async def read_users(
    filter_users: Annotated[FilterUsers, Query()], session: T_Session
):
    query = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )

    db_users = query.all()

    return {'users': db_users}


@router.patch('/{user_id}', response_model=ResponseUser)
async def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: T_CurrentUser,
    session: T_Session,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not enough permissions',
        )

    try:
        for key, value in user.model_dump(exclude_unset=True).items():
            if key == 'password':
                setattr(current_user, key, get_password_hash(value))
            else:
                setattr(current_user, key, value)

        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )

    return current_user


@router.delete('/{user_id}', response_model=ResponseUser)
async def delete_user(
    user_id: int, current_user: T_CurrentUser, session: T_Session
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not enough permissions',
        )

    deleted_user = current_user

    await session.delete(current_user)
    await session.commit()

    return deleted_user
