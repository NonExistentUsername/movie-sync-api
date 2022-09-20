from pydantic import BaseModel


class UserBase(BaseModel):
    nickname: str


class UserUpdate(UserBase):
    have_access: bool


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    pass


class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True
