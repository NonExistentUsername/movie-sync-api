from pydantic import BaseModel, Field, validator
from typing import Optional, List


class UserMinimal(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    name: str = Field(max_length=32, min_length=4)
    capacity: int = Field(default=10, ge=2, le=32)


class RoomJoin(BaseModel):
    name: str = Field(max_length=32, min_length=4)
    key: str = Field(max_length=8, min_length=8)


class Room(RoomBase):
    id: int
    key: str
    creator_id: int
    members_of_room: List[UserMinimal]

    class Config:
        orm_mode = True
