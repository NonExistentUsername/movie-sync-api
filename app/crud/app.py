from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas.command
import models.user
import models.command
import os
import datetime
import core.config
from starlette.responses import FileResponse


def get_last_app_update():
    time = os.path.getmtime(os.path.join(core.config.BASE_DIR, "media/app.zip"))

    return {
        "last_update": datetime.datetime.fromtimestamp(time)
    }


def download_app():
    return FileResponse(os.path.join(core.config.BASE_DIR, "media/app.zip"),
                        media_type='application/octet-stream',
                        filename="app.zip")
