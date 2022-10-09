from pydantic import BaseModel, Field
from typing import Optional, List
import datetime


class CommandBase(BaseModel):
    command: str = Field(max_length=64)
    param: Optional[str] = Field(max_length=256, default=None)


class CommandCreate(CommandBase):
    room_name: str


class CommandDelete(BaseModel):
    commands: List[int]


class CommandDeleted(BaseModel):
    deleted_commands: List[int]


class Command(CommandBase):
    id: int
    sender_id: int
    room_name: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True
