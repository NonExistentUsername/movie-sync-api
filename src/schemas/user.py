import re
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from schemas.validators import is_slug


class UserBase(BaseModel):
    username: str = Field(max_length=64, min_length=3)

    @classmethod
    @validator("username")
    def validate_username(cls, v):
        if not is_slug(v, 3, 64):
            raise ValueError("Username can contain letters, numbers and underscore.")
        return v


class UserUpdate(UserBase):
    is_admin: Optional[bool] = Field(default=None)
    have_access: Optional[bool] = Field(default=None)


def is_valid_password(password: str) -> bool:
    regex_name = re.compile(r"^(?=.*[a-zA-Z])(?=.*[0-9]).{6,}$")
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
    # member_of_rooms: List[int]

    class Config:
        orm_mode = True
