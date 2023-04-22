import datetime

from pydantic import BaseModel


class AppLastUpdate(BaseModel):
    last_update: datetime.datetime
