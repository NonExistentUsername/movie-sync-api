import time

from sqlalchemy.orm import Session
from fastapi import HTTPException
import schemas.command
import models.user
import models.command
import os
import datetime
import core.config
import core.global_variables
from starlette.responses import FileResponse


def get_last_app_update(current_user: models.user.User):
    if not current_user.is_admin and not current_user.receives_commands:
        raise HTTPException(status_code=403)

    time = os.path.getmtime(os.path.join(core.config.BASE_DIR, "media/app.py"))

    return {
        "last_update": datetime.datetime.fromtimestamp(time)
    }


def download_app(current_user: models.user.User):
    if not current_user.is_admin and not current_user.receives_commands:
        raise HTTPException(status_code=403)

    return FileResponse(os.path.join(core.config.BASE_DIR, "media/app.py"), media_type='application/octet-stream', filename="app.py")


async def app_test_long_poling_send():
    await core.global_variables.socket_manager.broadcast("Data")
    return {"status": "Done!"}
