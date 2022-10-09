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


auth_router = APIRouter()


@auth_router.post("/register", response_model=schemas.user.User, status_code=201)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(core.deps.get_db)):
    return crud.user.register_user(user, db)


@auth_router.post("/login")
async def login(user: schemas.user.UserLogin, db: Session = Depends(core.deps.get_db)):
    return crud.user.login_user(user, db)


@auth_router.get("/me", response_model=schemas.user.User)
async def read_users_me(current_user: models.user.User = Depends(core.deps.get_current_user)):
    user = current_user
    return user

