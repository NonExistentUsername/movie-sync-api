import core.deps
import core.global_variables
import crud.app
import crud.command
import crud.user
import models.user
import schemas.app
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

app_router = APIRouter()


@app_router.get("/last_update", response_model=schemas.app.AppLastUpdate)
async def get_last_app_update():
    return crud.app.get_last_app_update()


@app_router.get("/download", response_class=FileResponse)
async def get_last_app_update():
    return crud.app.download_app()
