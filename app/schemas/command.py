from pydantic import BaseModel
from typing import Optional
import datetime


class CommandBase(BaseModel):
    command: str
    param: Optional[str]


class CommandCreate(CommandBase):
    receiver_id: Optional[int]


class CommandDelete(BaseModel):
    commands: list[int]


class CommandDeleted(BaseModel):
    deleted_commands: list[int]


class Command(CommandBase):
    id: int
    sender_id: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
