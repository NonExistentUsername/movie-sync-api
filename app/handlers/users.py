from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.user
import schemas.app
import models.user
import crud.user
import crud.command
import crud.app
import core.deps
import core.global_variables

from fastapi_pagination import Page, paginate

users_router = APIRouter()


@users_router.get("/", response_model=Page[schemas.user.User])
async def get_users(db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return paginate(crud.user.get_users(db, current_user))


@users_router.get("/user", response_model=schemas.user.User)
async def get_user(username: str, db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.user.get_user(username, db, current_user)


@users_router.post("/update", response_model=schemas.user.User)
async def update_rights(user: schemas.user.UserUpdate, db: Session = Depends(core.deps.get_db), current_user: models.user.User = Depends(core.deps.get_current_user)):
    return crud.user.set_admin_rights_for_user(user, db, current_user)

