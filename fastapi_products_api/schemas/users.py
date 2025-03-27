from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class ResponseUser(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseUserList(BaseModel):
    users: list[ResponseUser]


class FilterUsers(BaseModel):
    offset: int = 0
    limit: int = 25
