from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    nickname: str


class UserUpdate(UserBase):
    is_admin: Optional[bool] = None
    receives_commands: Optional[bool] = None


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class User(UserBase):
    id: int
    is_admin: bool
    receives_commands: bool

    class Config:
        orm_mode = True
