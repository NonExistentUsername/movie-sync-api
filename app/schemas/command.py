from pydantic import BaseModel
import datetime


class CommandBase(BaseModel):
    command: str
    param: str | None


class CommandCreate(CommandBase):
    receiver_id: int | None
    pass


class Command(CommandBase):
    id: int
    sender_id: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
