from pydantic import BaseModel, Field, validator

from typing import Optional
import re


def is_valid_username(username: str) -> bool:
    regex_name = re.compile(r'^(?=.{3,64}$)[a-zA-Z_]\w*$', re.IGNORECASE)
    result = regex_name.search(username)
    if result and result.string == username:
        return True
    return False


class UserBase(BaseModel):
    username: str = Field(max_length=64, min_length=3)

    @classmethod
    @validator("username")
    def validate_username(cls, v):
        if not is_valid_username(v):
            raise ValueError("Username can contain letters, numbers and underscore.")
        return v


class UserUpdate(UserBase):
    is_admin: Optional[bool] = Field(default=None)
    have_access: Optional[bool] = Field(default=None)


def is_valid_password(password: str) -> bool:
    regex_name = re.compile(r'^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$')
    result = regex_name.search(password)
    if result and result.string == password:
        return True
    return False


class UserCreate(UserBase):
    password: str = Field(max_length=32, min_length=6)

    @classmethod
    @validator("password")
    def validate_username(cls, v):
        if not is_valid_password(v):
            raise ValueError("Password must contain letter and number.")
        return v


class UserLogin(UserCreate):
    pass


class User(UserBase):
    id: int
    is_admin: bool
    have_access: bool

    class Config:
        orm_mode = True
