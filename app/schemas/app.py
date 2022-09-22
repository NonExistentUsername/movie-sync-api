from pydantic import BaseModel
import datetime


class AppLastUpdate(BaseModel):
    last_update: datetime.datetime
