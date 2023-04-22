import core.deps
import core.global_variables
import crud.app
import crud.auth
import crud.command
import models.user
import schemas.app
import schemas.user
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

auth_router = APIRouter()


@auth_router.post("/register", response_model=schemas.user.User, status_code=201)
async def create_user(user: schemas.user.UserCreate, db: Session = Depends(core.deps.get_db)):
    return crud.auth.register_user(user, db)


@auth_router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(core.deps.get_db)):
    return crud.auth.login_user(user, db)


@auth_router.get("/me", response_model=schemas.user.User)
async def read_users_me(
    current_user: models.user.User = Depends(core.deps.get_current_user),
):
    user = current_user
    return user
