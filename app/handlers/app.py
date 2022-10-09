from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.app
import models.user
import crud.user
import crud.command
import crud.app
import core.deps
import core.global_variables
from starlette.responses import FileResponse

app_router = APIRouter()


@app_router.get("/last_update", response_model=schemas.app.AppLastUpdate)
async def get_last_app_update(
        current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.app.get_last_app_update(current_user)


@app_router.get("/test_long_poling_send")
async def app_test_long_poling_send(data: str, db: Session = Depends(core.deps.get_db)):
    return await crud.app.app_test_long_poling_send()


@app_router.get("/download", response_class=FileResponse)
async def get_last_app_update(current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.app.download_app(current_user)

