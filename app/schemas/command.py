from pydantic import BaseModel
from typing import Optional, List
import datetime


class CommandBase(BaseModel):
    command: str
    param: Optional[str]


class CommandCreate(CommandBase):
    receiver_id: Optional[int]


class CommandDelete(BaseModel):
    commands: List[int]


class CommandDeleted(BaseModel):
    deleted_commands: List[int]


class Command(CommandBase):
    id: int
    sender_id: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
